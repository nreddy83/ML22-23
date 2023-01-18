import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sys; args = sys.argv[1:]
 
data = pd.read_csv("Iris.csv")

print (data.head(10))
lst1 = []
lst2 = []

myLines1 = open(args[0],'r').read().splitlines()
for line in myLines1:
    lst1.append(line)

myLines2 = open(args[1], 'r').read().splitlines()
for line in myLines2:
    lst2.append(line)

plt.xlabel("sepal length")
plt.ylabel("sepal width")
plt.scatter(lst1, lst2)
plt.show()