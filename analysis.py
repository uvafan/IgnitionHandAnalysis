def main():
	sessions = []
	inp = input("Enter either a dash-separated range of sessions (e.g. 1-5) or a comma-separated list of sessions (e.g. 1,3,5)\n")
	if len(inp.split('-')) > 1:
		sessions = range(int(inp.split('-')[0]), int(inp.split('-')[1]) + 1)
	else:
		for s in inp.split(","):
			sessions.append(s)
	stats = findHandStats(sessions)
	print("In these sessions, you won $" + str(round(stats[1],2)) + " in " + str(stats[0]) + " hands.")
	print("Net profits/stats from each position:")
	for i in range(0, 6):
		print(numToPos(i) + ": $" + str(round(stats[2][i], 2)) + " VPIP: " + str(round(stats[3][i] * 100 / stats[5][i], 1)) + " PFR: " + str(round(stats[4][i] * 100 / stats[5][i], 1)))
	print("VPIP = " + str(round(sum(stats[3]) * 100 / stats[0], 1)))
	print("PFR = " + str(round(sum(stats[4]) * 100 / stats[0], 1)))

def findHandStats(sessions):
	totHands = 0
	totProfits = 0
	posProfits = [0] * 6
	totVPIP = [0] * 6
	totPFR = [0] * 6
	totPosHands = [0] * 6
	for n in sessions:
		fin = open("Histories/" + str(n) + ".txt")
		lines = fin.readlines()
		stats = findStatsWithinSession(lines, n)
		print("Session " + str(n) + ": Net $" + str(stats[1]) + " over " + str(stats[0]) + " hands.")
		totHands += stats[0]
		totProfits += stats[1]
		for i in range(0, 6):
			posProfits[i] += stats[2][i]
			totVPIP[i] += stats[3][i]
			totPFR[i] += stats[4][i]
			totPosHands[i] += stats[5][i]
	return [totHands, totProfits, posProfits, totVPIP, totPFR, totPosHands]

def findStatsWithinSession(lines, session):
	hands = 0
	inFor = 0
	outFor = 0
	curStreet = 0 #0 = pre, 1 = flop, 2 = turn, 3 = river
	posProfits = [0] * 6
	vpip = [0] * 6
	pfr = [0] * 6
	totPosHands = [0] * 6
	vpipAccountedFor = [0] * 100000
	curPosNum = -1
	for ln in lines:
		if ln[:12] == "*** FLOP ***" or ln[:12] == "*** TURN ***" or ln[:13] == "*** RIVER ***":
			curStreet += 1
		if ln[:8] == "Ignition":
			hands += 1
		for i in range(6, len(ln)):
			if ln[i:i + 3] == "ME]":
				if ln[i + 4: i + 6] == "($": #Dollar amounts at start of each hand
					curPosNum = posToNum(ln.split(' ')[2])
					curStreet = 0
					totPosHands[curPosNum] += 1
					realOutFor = findDollarAmount(ln, i + 6)
					if round(outFor, 2) != realOutFor:
						inFor += realOutFor - round(outFor, 2)
						outFor = realOutFor
				elif ln[i + 4:i + 19] == ": Table deposit": #User making a table deposit
					inFor += findDollarAmount(ln, i + 21)
					outFor += findDollarAmount(ln, i + 21)
				elif ln[i + 4:i + 10] == ": Bets": #User bets
					amt = findDollarAmount(ln, i + 12)
					posProfits[curPosNum] -= amt
					outFor -= amt
					vpip, vpipAccountedFor = incVPIP(vpip, vpipAccountedFor, hands, curPosNum) 
				elif ln[i + 4:i + 11] == ": Calls": #User calls
					amt = findDollarAmount(ln, i + 13)
					posProfits[curPosNum] -= amt
					outFor -= amt
					vpip, vpipAccountedFor = incVPIP(vpip, vpipAccountedFor, hands, curPosNum) 
				elif ln[i + 4:i + 12] == ": Raises": #User raises
					amt = findDollarAmount(ln, i + 14)
					posProfits[curPosNum] -= amt
					outFor -= amt
					if curStreet == 0 and not vpipAccountedFor[hands]:
						pfr[curPosNum] += 1
					vpip, vpipAccountedFor = incVPIP(vpip, vpipAccountedFor, hands, curPosNum) 
				elif ln[i + 4:i + 19] == ": All-in(raise)": #User raises all in
					amt = findDollarAmount(ln, i + 21)
					posProfits[curPosNum] -= amt
					outFor -= amt
					if curStreet == 0 and not vpipAccountedFor[hands]:
						pfr[curPosNum] += 1
					vpip, vpipAccountedFor = incVPIP(vpip, vpipAccountedFor, hands, curPosNum) 
				elif ln[i + 4:i + 12] == ": All-in": #User calls all in
					amt = findDollarAmount(ln, i + 14)
					posProfits[curPosNum] -= amt
					outFor -= amt
					if curStreet == 0 and not vpipAccountedFor[hands]:
						pfr[curPosNum] += 1
					vpip, vpipAccountedFor = incVPIP(vpip, vpipAccountedFor, hands, curPosNum) 
				elif ln[i + 4:i + 26] == ": Hand result-Side pot":
					amt = findDollarAmount(ln, i + 28)
					posProfits[curPosNum] += amt
					outFor += amt
				elif ln[i + 4:i + 17] == ": Hand result": #User wins pot
					amt = findDollarAmount(ln, i + 19)
					posProfits[curPosNum] += amt
					outFor += amt
				elif ln[i + 4:i + 36] == ": Return uncalled portion of bet": #uncalled bet/raise returns
					amt = findDollarAmount(ln, i + 38)
					posProfits[curPosNum] += amt
					outFor += amt
				elif ln[i + 4:i + 17] == ": Small Blind": #User's small blind
					amt = findDollarAmount(ln, i + 19)
					posProfits[curPosNum] -= amt
					outFor -= amt
				elif ln[i + 4:i + 15] == ": Big blind": #User's big blind
					amt = findDollarAmount(ln, i + 17)
					posProfits[curPosNum] -= amt
					outFor -= amt
	return [hands, round(outFor - inFor, 2), posProfits, vpip, pfr, totPosHands]

def incVPIP(vpip, vpipAccountedFor, hands, curPosNum):
	if vpipAccountedFor[hands]:
		return vpip, vpipAccountedFor
	vpipAccountedFor[hands] = 1
	vpip[curPosNum] += 1
	return vpip, vpipAccountedFor

def findDollarAmount(ln, startChar):
	ret = 0
	endChar = startChar + 1
	while endChar < len(ln) - 1 and ln[endChar] != ' ':
		endChar += 1
	convertToFloat = True
	if ln[endChar - 3] != '.':
		convertToFloat = False
	if convertToFloat:
		ret = float(ln[startChar:endChar])
	else:
		ret = int(ln[startChar:endChar])
	return ret

def posToNum(pos):
	return {
		"Small": 0,
		"Big": 1,
		"UTG": 2,
		"UTG+1": 3,
		"UTG+2": 4,
		"Dealer": 5	
	}[pos]

def numToPos(num):
	return {
		0: "Small",
		1: "Big",
		2: "UTG",
		3: "UTG+1",
		4: "UTG+2",
		5: "Dealer"	
	}[num]

main()