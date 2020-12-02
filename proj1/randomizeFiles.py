import numpy as np

#Randomize the data
def dataShuffle(data, m, n):
  shuffledData = np.zeros((m, n + 1))
  A = np.arange(0, m)
  np.random.shuffle(A)
  for k in range(m):
    for j in range(n + 1):
      shuffledData[A[k], j] = data[k][j]
  return shuffledData

def getData():
  filename = input("Data file: ")
  file = open(filename, "r")

  firstLine = file.readline()

  lineData = firstLine.split("\t")
  numberOfLines = int(lineData[0])
  numberOfElements = int(lineData[1])

  data = []

  for line in file:
    lineData = line.split("\t")
    lineData = list(map(float, lineData))
    data.append(lineData)

  return (data, numberOfLines, numberOfElements)

def main():
  (data, numberOfLines, numberOfElements) = getData()
  shuffledData = dataShuffle(data, numberOfLines, numberOfElements)

  trainingSetFilename = "Gustafson_Nicholas_Train.txt"
  validationSetFilename = "Gustafson_Nicholas_Valid.txt"
  testSetFilename = "Gustafson_Nicholas_Test.txt"

  trainingSetFile = open(trainingSetFilename, "w")
  validationSetFile = open(validationSetFilename, "w")
  testSetFile = open(testSetFilename, "w")

  i = 0
  trainingSetFile.write(f'{round(numberOfLines * 0.6)}\t{numberOfElements}\n')
  while i < round(numberOfLines * 0.6):
    line = ""
    for value in shuffledData[i]:
      line += f'{value}\t'
    trainingSetFile.write(f'{line[:len(line) - 2]}\n')
    i += 1
  
  passedLines = i
  validationSetFile.write(f'{round(numberOfLines * 0.2)}\t{numberOfElements}\n')
  while i < passedLines + round(numberOfLines * 0.2):
    line = ""
    for value in shuffledData[i]:
      line += f'{value}\t'
    validationSetFile.write(f'{line[:len(line) - 2]}\n')
    i += 1
  
  testSetFile.write(f'{numberOfLines - i}\t{numberOfElements}\n')
  while i < numberOfLines:
    line = ""
    for value in shuffledData[i]:
      line += f'{value}\t'
    testSetFile.write(f'{line[:len(line) - 2]}\n')
    i += 1

if __name__ == "__main__":
  main()