import numpy as np
import matplotlib.pyplot as plt
import math

def getData(file):
  firstLine = file.readline()

  lineData = firstLine.split("\t")
  numberOfLines = int(lineData[0])
  numberOfElements = int(lineData[1])

  data = np.zeros((numberOfLines, numberOfElements + 1))
  resultData = np.zeros((numberOfLines, 1))

  for i, line in enumerate(file):
    lineData = line.split("\t")
    if lineData[-1] == '\n':
      lineData.pop(-1)
    lineData = list(map(float, lineData))

    resultData[i][0] = lineData[-1]
    lineData.pop(-1)
    data[i] = [1] + lineData
  
  return (data, resultData, numberOfLines, numberOfElements)

def getJ(hypo, data, resultData):
  value = 0
  for i, dataPoints in enumerate(data):
    if resultData[i][0] == 0:
      value += np.log(1 - hypo(dataPoints))
    else:
      value += np.log(hypo(dataPoints))

  return -1 * value / len(data)

def getHypo(data, resultData, numberOfLines, numberOfElements):
  alpha = 3
  currentJ = -1
  pastJ = 0
  jIteration = 0
  weights = np.zeros((numberOfElements + 1, 1))

  def hypo(dataPoints):
    result = 0
    for i, weight in enumerate(weights):
      result += weight[0] * dataPoints[i]

    result = math.e**(-1 * result)

    return 1 / (1 + result)

  while pastJ - currentJ > 0.001 and pastJ - currentJ > 0 or jIteration < 100:
    for i, weight in enumerate(weights):
      summation = 0
      for j, dataPoints in enumerate(data):
        summation += (hypo(dataPoints) - resultData[j][0]) * dataPoints[i]
      weight[0] = weight[0] - ((alpha / numberOfLines) * summation)
    jIteration += 1
    pastJ = currentJ
    currentJ = getJ(hypo, data, resultData)
    plt.scatter(jIteration, currentJ)
    print(weights)
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    for i, dataPoints in enumerate(data):
      if resultData[i][0] == 1:
        if hypo(dataPoints) >= 0.5:
          tp += 1
        else:
          fp += 1
      else:
        if hypo(dataPoints) < 0.5:
          tn += 1
        else:
          fn += 1
    print(f"Final J: {currentJ}")
    print(f"FP: {fp}\nFN: {fn}\nTP: {tp}\nTN: {tn}")
    accuracy = (tp + tn) / (tp + tn + fp + fn)
    print(f"Accuracy: {accuracy}")
    precision = tp / (tp + fp)
    print(f"Precision: {precision}")
    recall = tp / (tp + fn)
    print(f"Recall: {recall}")
    f1 = 2 * 1 / (1/precision + 1/recall)
    print(f"F1: {f1}")

  return hypo

def main():
  dataFilename = input("Training file: ")
  dataFile = open(dataFilename, "r")

  (data, resultData, numberOfLines, numberOfElements) = getData(dataFile)
  hypo = getHypo(data, resultData, numberOfLines, numberOfElements)
  dataFile.close()
  plt.xlabel("Iterations")
  plt.ylabel("J Value")
  plt.title("Iterations vs. J")
  plt.savefig("Gustafson_Nicholas_Iterations_vs_J.png", bbox_inches="tight")
  plt.show()
  
  dataFilename = input("Test file: ")
  testFile = open(dataFilename, "r")

  (data, resultData, numberOfLines, numberOfElements) = getData(testFile)
  tp = 0
  tn = 0
  fp = 0
  fn = 0
  for i, dataPoints in enumerate(data):
    if resultData[i][0] == 1:
      if hypo(dataPoints) >= 0.5:
        tp += 1
      else:
        fp += 1
    else:
      if hypo(dataPoints) < 0.5:
        tn += 1
      else:
        fn += 1
  finalJ = getJ(hypo, data, resultData)
  print(f"Final J: {finalJ}")
  print(f"FP: {fp}\nFN: {fn}\nTP: {tp}\nTN: {tn}")
  accuracy = (tp + tn) / (tp + tn + fp + fn)
  print(f"Accuracy: {accuracy}")
  precision = tp / (tp + fp)
  print(f"Precision: {precision}")
  recall = tp / (tp + fn)
  print(f"Recall: {recall}")
  f1 = 2 * 1 / (1/precision + 1/recall)
  print(f"F1: {f1}")


if __name__ == "__main__":
  main()