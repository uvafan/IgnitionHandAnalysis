def main():
	fin = open("Histories/1.txt")
	lines = fin.readlines()
	stats = findHandStats(lines)
	print("In this session, you won $" + str(round(stats[1], 2)) + " in " + str(stats[0]) + " hands.")
	print("Net profits from each position:")
	for i in range(0, 6):
		print(numToPos(i) + ": $" + str(round(stats[2][i],2)))

def findHandStats(lines):
	hands = 0
	inFor = 0
	outFor = 0
	positionProfits = [0] * 6
	curPosNum = -1
	for ln in lines:
		if ln[:8] == "Ignition":
			hands += 1
		for i in range(6, len(ln)):
			if ln[i:i + 3] == "ME]":
				if ln[i + 4: i + 6] == "($": #Dollar amounts at start of each hand
					curPosNum = posToNum(ln.split(' ')[2])
					if inFor == 0: #start of session
						inFor = findDollarAmount(ln, i + 6)
						outFor = inFor
					else: #check for bugs
						realOutFor = findDollarAmount(ln, i + 6)
						if round(outFor, 2) != realOutFor:
							print("outFor = " + str(round(outFor, 2)) + " at line: " + ln)
							exit(0)
				elif ln[i + 4:i + 19] == ": Table deposit": #User making a table deposit
					inFor += findDollarAmount(ln, i + 21)
					outFor += findDollarAmount(ln, i + 21)
				elif ln[i + 4:i + 10] == ": Bets": #User bets
					amt = findDollarAmount(ln, i + 12)
					positionProfits[curPosNum] -= amt
					outFor -= amt
				elif ln[i + 4:i + 11] == ": Calls": #User calls
					amt = findDollarAmount(ln, i + 13)
					positionProfits[curPosNum] -= amt
					outFor -= amt
				elif ln[i + 4:i + 12] == ": Raises": #User raises
					amt = findDollarAmount(ln, i + 14)
					positionProfits[curPosNum] -= amt
					outFor -= amt
				elif ln[i + 4:i + 19] == ": All-in(raise)": #User raises all in
					amt = findDollarAmount(ln, i + 21)
					positionProfits[curPosNum] -= amt
					outFor -= amt
				elif ln[i + 4:i + 12] == ": All-in": #User calls all in
					amt = findDollarAmount(ln, i + 14)
					positionProfits[curPosNum] -= amt
					outFor -= amt
				elif ln[i + 4:i + 17] == ": Hand result": #User wins pot
					amt = findDollarAmount(ln, i + 19)
					positionProfits[curPosNum] += amt
					outFor += amt
				elif ln[i + 4:i + 36] == ": Return uncalled portion of bet": #uncalled bet/raise returns
					amt = findDollarAmount(ln, i + 38)
					positionProfits[curPosNum] += amt
					outFor += amt
				elif ln[i + 4:i + 17] == ": Small Blind": #User's small blind
					amt = findDollarAmount(ln, i + 19)
					positionProfits[curPosNum] -= amt
					outFor -= amt
				elif ln[i + 4:i + 15] == ": Big blind": #User's big blind
					amt = findDollarAmount(ln, i + 17)
					positionProfits[curPosNum] -= amt
					outFor -= amt
	return [hands, outFor - inFor, positionProfits]

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