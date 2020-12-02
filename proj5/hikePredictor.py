import numpy as np
import matplotlib.pyplot as plt
import math

def timeToNumber(time):
  (h, m, s) = time.split(':')
  return int(h) * 3600 + int(m) * 60 + int(s)

def numberToTime(seconds):
  seconds = seconds % (24 * 3600) 
  hour = seconds // 3600
  seconds %= 3600
  minutes = seconds // 60
  seconds %= 60

  return "%d:%02d:%02d" % (hour, minutes, seconds)

def getData(file):
  firstLine = file.readline()

  lineData = firstLine.split("\t")
  numberOfLines = int(lineData[0])
  numberOfElements = int(lineData[1])

  data = np.zeros((numberOfLines, numberOfElements))
  resultData = np.zeros((numberOfLines, 1))

  for i, line in enumerate(file):
    lineData = line.split("\t")
    if lineData[-1] == '\n':
      lineData.pop(-1)

    resultData[i][0] = timeToNumber(lineData[-1])
    lineData.pop(-1)

    lineData = list(map(float, lineData))
    data[i] = [1] + lineData
  
  return (data, resultData, numberOfLines, numberOfElements)

def squaredErrorCost(hypothesis, data, resultData, numberOfLines):
  error = 0.0
  for i, element in enumerate(data):
    error += (hypothesis(element) - resultData[i])**2

  error = error / (2 * numberOfLines)
  return error[0]

def getHypothesis(data, resultData):
  w = np.dot(np.linalg.pinv(np.dot(data.T, data)), np.dot(data.T, resultData))
  weights = w.flatten()

  def hypothesis(values):
    guess = 0
    for i, value in enumerate(values):
      guess += value * weights[i]
    return guess
  
  return (hypothesis, weights)

def rSquared(resultData, squaredError, numberOfLines):
  bottom = 0
  mean = np.mean(resultData)

  for result in resultData:
    bottom += (result - mean)**2

  bottom = bottom / (2 * numberOfLines)

  return (1 - (squaredError / bottom))[0]

def changeData(data, power, numberOfLines):
  numberOfElements = power**2 + power*2 + 1
  newData = np.zeros((numberOfLines, numberOfElements))
  for k, dataline in enumerate(data):
    newLine = []
    for i in range(power + 1):
      for j in range(power + 1):
        temp = (dataline[1]**i)*(dataline[2]**j)
        if temp != 1:
          newLine.append(temp)
    newData[k] = [1] + newLine
  return (newData, numberOfElements)

def main():
  print("-- Hiking Time Predictor -- \n")

  trainFilename = input("Training file: ")
  trainFile = open(trainFilename, "r")
  (data, resultData, numberOfLines, numberOfElements) = getData(trainFile)
  trainFile.close()

  validFilename = input("Validation file: ")
  validFile = open(validFilename, "r")
  (validData, validResultData, validNumberOfLines, _) = getData(validFile)
  validFile.close()

  testFilename = input("Test file: ")
  testFile = open(testFilename, "r")
  (testData, testResultData, testNumberOfLines, _) = getData(testFile)
  testFile.close()

  (hypo, _) = getHypothesis(data, resultData)
  sqError = squaredErrorCost(hypo, data, resultData, numberOfLines)
  rSq = rSquared(resultData, sqError, numberOfLines)

  validSqError = squaredErrorCost(hypo, validData, validResultData, validNumberOfLines)
  validRSq = rSquared(validResultData, validSqError, validNumberOfLines)

  print("\n0: Train Adjusted R^2:       {}".format(rSq))
  print("0: Validation Adjusted R^2:  {}\n".format(validRSq))
  
  maxRSq = validRSq
  maxRSqIndex = 0
  hypos = [hypo]
  for i in range(1, 5):
    (data2, _) = changeData(data, i, numberOfLines)
    (hypo, _) = getHypothesis(data2, resultData)
    hypos.append(hypo)

    sqError = squaredErrorCost(hypo, data2, resultData, numberOfLines)
    rSq = rSquared(resultData, sqError, numberOfLines)

    (validData2, _) = changeData(validData, i, validNumberOfLines)
    validSqError = squaredErrorCost(hypo, validData2, validResultData, validNumberOfLines)
    validRSq = rSquared(validResultData, validSqError, validNumberOfLines)

    print("{}: Train Adjusted R^2:       {}".format(i, rSq))
    print("{}: Validation Adjusted R^2:  {}\n".format(i, validRSq))

    if maxRSq < validRSq:
      maxRSq = validRSq
      maxRSqIndex = i

  # Testing

  if maxRSqIndex != 0:
    (testData, _) = changeData(testData, maxRSqIndex, testNumberOfLines)
  
  sqError = squaredErrorCost(hypos[maxRSqIndex], testData, testResultData, testNumberOfLines)
  rSq = rSquared(testResultData, sqError, testNumberOfLines)
  print("\nTest error: {}\n\n".format(rSq))

  print("Figure out how long the next hike will take you!")
  hypo = hypos[maxRSqIndex]
  while True:
    milage = float(input("Milage: "))
    elevation = float(input("Elevation: "))
    data = np.array([[1, milage, elevation]])
    if maxRSqIndex != 0:
      (data, _) = changeData(data, maxRSqIndex, 1)
    guess = hypo(data[0])
    perMilePace = numberToTime(guess / milage)
    guess = numberToTime(guess)
    print("Guess: {}\nPer Mile Pace: {}\n".format(guess, perMilePace))

if __name__ == "__main__":
  main()
