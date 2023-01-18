import math, random
# open file
import csv
with open("iris.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    attributes = [] #done
    classes = []
    instances = [] #done
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
                if val not in classes: classes.append(val)
            else:
                olddct[attributes[i]].append(val)

# discretize the data
print("Discretizing Data:")
dct = {}
i = 0
for key in olddct:
    lst = olddct[key] 
    lst.sort()
    mid = int(math.floor(len(instances)/3))
    v1 = lst[mid]
    v2 = lst[mid*2]
    print("For " + key + ", low = " + str(lst[0]) + " to " + str(v1) + ", medium = " + str(v1) + " to " + str(v2) + ", and high = " + str(v2) + " to " + str(lst[-1]))
    dct[key] = ["low", "medium", "high"]
    for j in range(len(instances)):
        val = instances[j][i]
        if float(val) < float(v1): instances[j][i] = 0
        elif float(val) < float(v2): instances[j][i] = 1
        else: instances[j][i] = 2
    i += 1

print()

# split into testing and training using 67:33 ratio
training_x = []
training_y = []
testing_x = []
testing_y = []
ct1 = 0
ct2 = 0
for i in range(len(instances)):
    r = random.random()
    if ct1 > len(instances)/3: 
        training_x.append(tuple(instances[i][:-1]))
        training_y.append(instances[i][-1])
    elif ct2 > 2*len(instances)/3: 
        testing_x.append(tuple(instances[i][:-1]))
        testing_y.append(instances[i][-1])
    elif r < 0.33: 
        testing_x.append(tuple(instances[i][:-1]))
        testing_y.append(instances[i][-1])
        ct1 += 1
    else:
        training_x.append(tuple(instances[i][:-1]))
        training_y.append(instances[i][-1])
        ct2 += 1

# classification
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(training_x, training_y)
print()

# training results
totSc = 0
res = model.predict(training_x)
for i, val in enumerate(res):
    if val == training_y[i]: totSc += 1

acc = round((100*totSc/len(training_x)), 3)
print("Training Accuracy = " + str(acc) + "%")
print()

# testing
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

acc = round((100*totSc/len(testing_x)), 3)
print("Testing Accuracy = " + str(acc) + "%")
print("Confusion Matrix:")
for lst in cm:
    print(lst)
print()