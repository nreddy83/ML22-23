import math, random
# open file
import csv
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
        if float(val) < float(v1): instances[j][i] = "low"
        elif float(val) < float(v2): instances[j][i] = "medium"
        else: instances[j][i] = "high"
    i += 1

print()

# split into testing and training using 67:33 ratio
random.shuffle(instances)
training_instances = []
testing_instances = []
ct1 = 0
ct2 = 0
for i in range(len(instances)):
    r = random.random()
    if ct1 > len(instances)/3: training_instances.append(instances[i])
    elif ct2 > 2*len(instances)/3: testing_instances.append(instances[i])
    elif r < 0.33: 
        testing_instances.append(instances[i])
        ct1 += 1
    else:
        training_instances.append(instances[i])
        ct2 += 1

# make a dctclass to make probability calculations easier
dcttrainclass = {}
dcttestclass = {}
for instance in training_instances:
    if instance[-1] not in dcttrainclass: dcttrainclass[instance[-1]] = [instance]
    else: dcttrainclass[instance[-1]].append(instance)
for instance in testing_instances:
    if instance[-1] not in dcttestclass: dcttestclass[instance[-1]] = [instance]
    else: dcttestclass[instance[-1]].append(instance)

# classification
probs = []
for c in classes:
    lst = []
    ctr = 0
    for i, a in enumerate(attributes):
        for cat in dct[a]:
            v = 0
            for instance in dcttrainclass[c]:
                if instance[-1] != c: continue
                if instance[i] == cat: v += 1
            lst.append(v/len(dcttrainclass[c]))
    probs.append(lst)

# print probability table
st = ""
for a in attributes:
    st += a + " "
print(st)

st = ""
for a in attributes:
    for cat in dct[a]:
        st += cat + " "
print(st)

for lst in probs:
    print(lst)

print()

# training results
totSc = 0
for instance in training_instances:
    bestVal = 0
    bestClass = ""
    for i, c in enumerate(classes):
        v = len(dcttrainclass[c])/len(training_instances)
        lstUsed = probs[i]
        for j, val in enumerate(instance):
            if j == len(instance) - 1: continue
            if val == "low": idx = 0
            if val == "medium": idx = 1
            if val == "high": idx = 2
            v *= lstUsed[j*len(dct[attributes[j]]) + idx]
        if v > bestVal: 
            bestVal = v
            bestClass = c
    if bestClass == instance[-1]: totSc += 1

acc = round((100*totSc/len(training_instances)), 3)
print("Training Accuracy = " + str(acc) + "%")
print()

# testing
totSc = 0
for instance in testing_instances:
    bestVal = 0
    bestClass = ""
    for i, c in enumerate(classes):
        v = len(dcttestclass[c])/len(testing_instances)
        lstUsed = probs[i]
        for j, val in enumerate(instance):
            if j == len(instance) - 1: continue
            if val == "low": idx = 0
            if val == "medium": idx = 1
            if val == "high": idx = 2
            v *= lstUsed[j*len(dct[attributes[j]]) + idx]
        if v > bestVal: 
            bestVal = v
            bestClass = c
    if bestClass == instance[-1]: totSc += 1

acc = round((100*totSc/len(testing_instances)), 3)
print("Testing Accuracy = " + str(acc) + "%")
print()