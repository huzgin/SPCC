inputfile = open('F:\Sem6\AI\Exp4\data.csv', "r")
input = inputfile.read()
input = input.replace(' ','')
inputnew = input.split('\n')
for tok in inputnew:
    print("symps("+tok+").")
