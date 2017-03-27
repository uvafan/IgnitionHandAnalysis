def main():
	fin = open("HistFiles/3-25_3.txt")
	lines = fin.readlines()
	hands = findNumHands(lines)
	winnings = findWinnings(lines)
	print(winnings)

def findNumHands(lines):
	for ln in lines:
		if ln[:8] == "Ignition":
			hands += 1

def findWinnings(lines):
	start = 0
	end = 0
	for ln in lines:
		for i in range(12, len(ln) - 17):
			if ln[i:i + 7] == "[ME] ($":
				startChar = i+7
				endChar = startNumChar + 1
				while ln[endChar] != ' ':
					endChar += 1
				convertToFloat = true
				if ln[endChar - 3] != '.':
					convertToFloat = false
				if convertToFloat:
					end = float(ln[startChar:endChar])
				else:
					end = int(ln[startChar:endChar])
				if start == 0:
					start = end
	end = 

main()