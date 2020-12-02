# Nicholas Gustafson
# ngustaf@g.clemson.edu
# C80372648

import numpy as np

def getData(file, method):
  firstLine = file.readline()

  lineData = firstLine.split("\t")
  numberOfLines = int(lineData[0])
  numberOfElements = int(lineData[1])

  data = np.zeros((numberOfLines, numberOfElements + 1))
  resultData = np.zeros((numberOfLines, 1))

  for i, line in enumerate(file):
    lineData = line.split("\t")
    lineData = list(map(float, lineData))
    resultData[i][0] = lineData[-1]
    lineData.pop(-1)
    data[i] = [1] + list(map(method, lineData))

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

def main():
  dataFilename = input("Data file: ")
  dataFile = open(dataFilename, "r")

  (data, resultData, numberOfLines, _) = getData(dataFile, lambda x: x)
  (hypo, weights) = getHypothesis(data, resultData)
  sqError = squaredErrorCost(hypo, data, resultData, numberOfLines)
  rSq = rSquared(resultData, sqError, numberOfLines)
  print("Original Data:")
  for i, weight in enumerate(weights):
    print("W{}: {}".format(i, weight))
  print("J: {}".format(sqError))
  print("Adjusted R^2: {}\n".format(rSq))

  dataFile.seek(0)

  (sqData, _, _, _) = getData(dataFile, lambda x: x**2)
  (sqHypo, sqWeights) = getHypothesis(sqData, resultData)
  sqErrorSqData = squaredErrorCost(sqHypo, sqData, resultData, numberOfLines)
  rSqSqData = rSquared(resultData, sqErrorSqData, numberOfLines)
  print("Squared Data:")
  for i, weight in enumerate(sqWeights):
    print("W{}: {}".format(i, weight))
  print("J: {}".format(sqErrorSqData))
  print("Adjusted R^2: {} \n".format(rSqSqData))

  dataFile.seek(0)

  (sqOrData, _, _, _) = getData(dataFile, lambda x: x + x**2)
  (sqOrHypo, sqOrWeights) = getHypothesis(sqOrData, resultData)
  sqErrorSqOrData = squaredErrorCost(sqOrHypo, sqOrData, resultData, numberOfLines)
  rSqOr = rSquared(resultData, sqErrorSqOrData, numberOfLines)
  print("Original + Squared Data:")
  for i, weight in enumerate(sqOrWeights):
    print("W{}: {}".format(i, weight))
  print("J: {}".format(sqErrorSqOrData))
  print("Adjusted R^2: {}\n\n".format(rSqOr))

  validationFilename = input("Validatation file: ")
  validationFile = open(validationFilename, "r")

  (data, resultData, numberOfLines, _) = getData(validationFile, lambda x: x)
  sqError = squaredErrorCost(hypo, data, resultData, numberOfLines)
  rSq = rSquared(resultData, sqError, numberOfLines)
  print("Original Data Validation:")
  print("J: {}".format(sqError))
  print("Adjusted R^2: {}\n".format(rSq))

  validationFile.seek(0)

  (sqData, _, _, _) = getData(validationFile, lambda x: x**2)
  sqErrorSqData = squaredErrorCost(sqHypo, sqData, resultData, numberOfLines)
  rSqSqData = rSquared(resultData, sqErrorSqData, numberOfLines)
  print("Squared Data Validation:")
  print("J: {}".format(sqErrorSqData))
  print("Adjusted R^2: {}\n".format(rSqSqData))

  validationFile.seek(0)

  (sqOrData, _, _, _) = getData(validationFile, lambda x: x + x**2)
  sqErrorSqOrData = squaredErrorCost(sqOrHypo, sqOrData, resultData, numberOfLines)
  rSqOr = rSquared(resultData, sqErrorSqOrData, numberOfLines)
  print("Original + Squared Data Validation:")
  print("J: {}".format(sqErrorSqOrData))
  print("Adjusted R^2: {}".format(rSqOr))

if __name__ == "__main__":
  main()
