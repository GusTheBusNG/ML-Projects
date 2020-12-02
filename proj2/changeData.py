import numpy as np

def main():
  newFileName = 'test.txt'
  fout = open(newFileName, 'w')

  dataFilename = input("file: ")
  dataFile = open(dataFilename, "r")

  firstLine = dataFile.readline()

  lineData = firstLine.split("\t")
  numberOfLines = int(lineData[0])
  numberOfElements = int(lineData[1])

  thePower = 8
  fout.write(f'{round(numberOfLines)}\t{thePower**2 + thePower*2}\n')

  for i, line in enumerate(dataFile):
    lineData = line.split("\t")
    if lineData[-1] == '\n':
      lineData.pop(-1)
    lineData = list(map(float, lineData))

    for j in range(thePower + 1):
      for i in range(thePower + 1):
        temp = (lineData[0]**i)*(lineData[1]**j)
        if temp != 1:
          fout.write(str(temp) + "\t")
    fout.write(str(lineData[-1])+"\n")

if __name__ == "__main__":
  main()
