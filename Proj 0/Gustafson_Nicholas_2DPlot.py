#!/usr/bin/env python3
"""
Nicholas Gustafson
ngustaf@clemson.edu
C80372648
"""
import matplotlib.pyplot as plt

file = open("IrisData.txt", "r")

array1x = []
array2x = []
array3x = []
array1y = []
array2y = []
array3y = []

for line in file:
    lineData = line.split("\t")
    
    if (lineData[4] == 'setosa\n'):
        array1x.append(float(lineData[0]))
        array1y.append(float(lineData[2]))
    elif (lineData[4] == 'versicolor\n'):
        array2x.append(float(lineData[0]))
        array2y.append(float(lineData[2]))
    else:
        array3x.append(float(lineData[0]))
        array3y.append(float(lineData[2]))

plt.scatter(array1x, array1y, color = "green", label = "Setosa")
plt.scatter(array2x, array2y, color = "red", label = "Versicolor")
plt.scatter(array3x, array3y, color = "blue", label = "Virginica")

file.close()

plt.xlabel("Sepal Length")
plt.ylabel("Petal Length")
plt.title("Sepal VS Petal Length")

plt.savefig("Gustafson_Nicholas_MyPlot.png", bbox_inches="tight")
plt.show()
