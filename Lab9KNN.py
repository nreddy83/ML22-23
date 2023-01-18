import math, random
# open file
import csv
k = 5 #establishing k value
with open("iris.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    attributes = []
    classes = []
    instances = []
    olddct = {}
    for row in reader:
        if len(attributes) == 0: 
            attributes = row[:-1]
            for a in attributes:
                olddct[a] = []
            continue
        instances.append(row)
        for i, val in enumerate(row):
            if i == len(row) - 1:
                if val not in classes: 
                    classes.append(val)
            else:
                olddct[attributes[i]].append(val)

# split into testing and training using 67:33 ratio in the code directly
random.shuffle(instances)
training_x = []
training_y = []
for i in range(int(len(instances)*2/3)):
    lst = []
    for j in range(len(instances[i])):
        if j == len(instances[i]) - 1: training_y.append(instances[i][j])
        else: lst.append(float(instances[i][j]))
    training_x.append(lst)

testing_x = []
testing_y = []
for i in range(int(len(instances)*2/3), len(instances)):
    lst = []
    for j in range(len(instances[i])):
        if j == len(instances[i]) - 1: testing_y.append(instances[i][j])
        else: lst.append(float(instances[i][j]))
    testing_x.append(lst)

from sklearn.neighbors import KNeighborsClassifier
model = KNeighborsClassifier(n_neighbors = 5)
model.fit(training_x, training_y)

# training results
totSc = 0
cm = []
res = model.predict(training_x)
for c in classes:
    lst = [0 for i in range(len(classes))]
    for i, val in enumerate(res):
        if training_y[i] != c: continue
        if val == training_y[i]: totSc += 1
        for j in range(len(lst)):
            if val == classes[j]: lst[j] += 1
    cm.append(lst)

acc = round((100*totSc/len(training_x)), 3)
print("Training Accuracy = " + str(acc) + "%")
print("Training Confusion Matrix:")
for lst in cm:
    print(lst)
print()

# training results
totSc = 0
cm = []
res = model.predict(testing_x)
for c in classes:
    lst = [0 for i in range(len(classes))]
    for i, val in enumerate(res):
        if testing_y[i] != c: continue
        if val == testing_y[i]: totSc += 1
        for j in range(len(lst)):
            if val == classes[j]: lst[j] += 1
    cm.append(lst)

acc = round((100*totSc/len(testing_y)), 3)
print("Testing Accuracy = " + str(acc) + "%")
print("Confusion Matrix:")
for lst in cm:
    print(lst)
print()


# macro averaging
totAvg = 0
for i in range(len(classes)):
    num = cm[i][i]
    tot = 0
    for j in range(len(classes)):
        tot += cm[j][i]
    totAvg += (num/tot)
totAvg = round((100*totAvg/len(classes)), 1)
print("Macroaverging Precision = " + str(totAvg) + "%")
print()

# micro averaging
newCms = []
for i in range(len(classes)):
    tot = 0
    newcm = [[0, 0], [0, 0]]
    newcm[0][0] = cm[i][i]
    tot += cm[i][i]
    for j in range(len(classes)):
        if j == i: continue
        newcm[0][1] += cm[i][j]
        newcm[1][0] += cm[j][i]
        tot += cm[i][j] + cm[j][i]
    newcm[1][1] = len(testing_y) - tot
    newCms.append(newcm)

finCm = [[0, 0], [0, 0]]
for cm in newCms:
    for i in range(2):
        for j in range(2):
            finCm[i][j] += cm[i][j]
print("Microaveraging Matrix:")
for i in range(len(finCm)):
    print(finCm[i])
totAvg = round((100*finCm[0][0]/(finCm[0][0] + finCm[0][1])), 1)
print("Microaveraging Precision = " + str(totAvg) + "%")