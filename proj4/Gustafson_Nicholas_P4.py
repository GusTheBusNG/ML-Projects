import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math

def getData(file):
  firstLine = file.readline()

  lineData = firstLine.split("\t")
  numberOfLines = int(lineData[0])
  numberOfElements = int(lineData[1]) if len(lineData) > 1 else 2

  data = np.zeros((numberOfLines, numberOfElements))

  for i, line in enumerate(file):
    lineData = line.split("\t")
    if lineData[-1] == '\n':
      lineData.pop(-1)
    lineData = list(map(float, lineData))
    data[i] = [] + lineData
  
  return (data, numberOfLines, numberOfElements)

def printInitalPlot(data, centroids):
  for point in data:    
    plt.scatter(point[0], point[1], color="green", label="Data Point")
  
  colors = cm.rainbow(np.linspace(0, 1, len(centroids)))
  for centroid, color in zip(centroids, colors):
      plt.scatter(centroid[0], centroid[1], color=color, label="Centroid", marker="v")    

  plt.xlabel("X1 Axis")
  plt.ylabel("X2 Axis")
  plt.title("Initial Data Points")
  plt.savefig("Gustafson_Nicholas_Initial", bbox_inches="tight")
  plt.show()

def kmeans(data, centroids, numberOfCentroids):
  colors = cm.rainbow(np.linspace(0, 1, len(centroids)))
  firstCentroidPoints = []
  secondCentroidPoints = []
  check = []
  oldCheck = [0]
  while check != oldCheck:
    oldCheck = check
    firstCentroidPoints = []
    secondCentroidPoints = []
    check = []
    plt.clf()
    currentCentroidSumX = np.zeros(numberOfCentroids)
    currentCentroidSumY = np.zeros(numberOfCentroids)
    centroidAssignments = np.zeros(numberOfCentroids)
    for point in data:
      minDistance = 100
      assignedCentroid = 100
      for i, centroid in enumerate(centroids):
        dist = math.dist(point, centroid)
        if dist < minDistance:
          minDistance = dist
          assignedCentroid = i
      centroidAssignments[assignedCentroid] = centroidAssignments[assignedCentroid] + 1
      currentCentroidSumX[assignedCentroid] = currentCentroidSumX[assignedCentroid] + point[0]
      currentCentroidSumY[assignedCentroid] = currentCentroidSumY[assignedCentroid] + point[1]
      check.append(assignedCentroid)
      if assignedCentroid == 0:
        firstCentroidPoints.append(point)
      else:
        secondCentroidPoints.append(point)

      plt.scatter(point[0], point[1], color=colors[assignedCentroid], label="Point")
    
    for i, (total, x, y) in enumerate(zip(centroidAssignments, currentCentroidSumX, currentCentroidSumY)):
      x = x / total
      y = y / total
      centroids[i] = [x, y]
      plt.scatter(x, y, color=colors[i], label="Centroid", marker="v")

  plt.xlabel("X1 Axis")
  plt.ylabel("X2 Axis")
  plt.title("Clustered Data Points")
  plt.savefig("Gustafson_Nicholas_Clustered", bbox_inches="tight")
  plt.show()

  return (centroids, firstCentroidPoints, secondCentroidPoints)

def jValue(centroids, firstCentroidPoints, secondCentroidPoints):
  value = 0
  for point in firstCentroidPoints:
    value = value + (math.dist(centroids[0], point) ** 2)
  for point in secondCentroidPoints:
    value = value + (math.dist(centroids[1], point) ** 2)
  return value / (len(firstCentroidPoints) + len(secondCentroidPoints))

def main():
  dataFilename = input("Data file: ")
  dataFile = open(dataFilename, "r")

  (data, dataNumberOfLines, dataNumberOfElements) = getData(dataFile)

  centroidFilename = input("Centroid file: ")
  centroidFile = open(centroidFilename, "r")

  (centroids, centroidNumberOfLines, centroidNumberOfElements) = getData(centroidFile)

  print("- Initial Centroids -")
  print(centroids)
  printInitalPlot(data, centroids)

  (centroids, firstCentroidPoints, secondCentroidPoints) = kmeans(data, centroids, centroidNumberOfLines)

  print(" - Updated Centroids - ")
  print(centroids)

  jval = jValue(centroids, firstCentroidPoints, secondCentroidPoints)
  print(" - J Value - ")
  print(jval)

if __name__ == "__main__":
  main()