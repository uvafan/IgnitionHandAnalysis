def main():
	fin = open("Histories/1.txt")
	lines = fin.readlines()
	stats = findHandStats(lines)
	print("In this session, you won $" + str(round(stats[1], 2)) + " in " + str(stats[0]) + " hands.") 

def findHandStats(lines):
	hands = 0
	inFor = 0
	outFor = 0
	for ln in lines:
		if ln[:8] == "Ignition":
			hands += 1
		for i in range(6, len(ln)):
			if ln[i:i + 3] == "ME]":
				if ln[i + 4: i + 6] == "($": #Dollar amounts at start of each hand
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
					outFor -= findDollarAmount(ln, i + 12)
				elif ln[i + 4:i + 11] == ": Calls": #User calls
					outFor -= findDollarAmount(ln, i + 13)
				elif ln[i + 4:i + 12] == ": Raises": #User raises
					outFor -= findDollarAmount(ln, i + 14)
				elif ln[i + 4:i + 19] == ": All-in(raise)": #User raises all in
					outFor -= findDollarAmount(ln, i + 21)
				elif ln[i + 4:i + 12] == ": All-in": #User calls all in
					outFor -= findDollarAmount(ln, i + 14)
				elif ln[i + 4:i + 17] == ": Hand result": #User wins pot
					outFor += findDollarAmount(ln, i + 19)
				elif ln[i + 4:i + 36] == ": Return uncalled portion of bet": #uncalled raise returns
					outFor += findDollarAmount(ln, i + 38)
				elif ln[i + 4:i + 17] == ": Small Blind": #User's small blind
					outFor -= findDollarAmount(ln, i + 19)
				elif ln[i + 4:i + 15] == ": Big blind": #User's big blind
					outFor -= findDollarAmount(ln, i + 17)
	return [hands, outFor - inFor]

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

main()