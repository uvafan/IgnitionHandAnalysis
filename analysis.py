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
		for i in range(6, len(ln) - 17):
			if ln[i:i + 3] == "ME]":
				if ln[i + 4: i + 6] == "($": #Dollar amounts at start of each hand
					outFor = findDollarAmount(ln, i + 6)
					if inFor == 0:
						inFor = outFor
				elif  ln[i+4:i + 19] == ": Table deposit": #User making a table deposit
					inFor += findDollarAmount(ln, i + 21)
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