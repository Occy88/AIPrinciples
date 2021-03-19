f = open('sudoku_log')
lines = f.readlines()
lines.pop(0)
for l in range(1,len(lines)+1):
    print(lines[l-1][16], end=' ')
    if l % 3==0:
        print(" ", end='|')
    if l % 9==0:
        print("")
    if l%(9*3)==0:
        print("----------------------")
