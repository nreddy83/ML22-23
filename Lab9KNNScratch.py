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
training_instances = instances[:int(len(instances)*2/3)]
testing_instances = instances[int(len(instances)*2/3):]

def distance(ins_1, ins_2):
    d = 0
    if len(ins_1) != len(ins_2): return -1
    for i, val in enumerate(ins_1):
        if i == len(ins_1) - 1: continue
        calcd = abs(float(val)*float(val) - float(ins_2[i])*float(ins_2[i]))
        d += calcd
    return math.sqrt(d)

# training results
training_classes = []
totSc = 0
for i, instance in enumerate(training_instances):
    lstDistances = []
    for j, comp_instance in enumerate(training_instances):
        if i == j: continue
        d = distance(instance, comp_instance)
        lstDistances.append((d, comp_instance))
    lstDistances.sort()
    c = [0 for i in range(len(classes))]
    for j in range(k):
        cl = lstDistances[j][1][-1]
        c[classes.index(cl)] += 1
    clfy = classes[c.index(max(c))]
    training_classes.append(clfy)
    if clfy == instance[-1]: totSc += 1

cm = []
for c in classes:
    lst = [0 for i in range(len(classes))]
    for i, val in enumerate(training_classes):
        if training_instances[i][-1] != c: continue
        for j in range(len(lst)):
            if val == classes[j]: lst[j] += 1
    cm.append(lst)

acc = round((100*totSc/len(training_instances)), 3)
print("Training Accuracy = " + str(acc) + "%")
print("Training Confusion Matrix:")
for lst in cm:
    print(lst)
print()

# testing results
testing_classes = []
totSc = 0
for i, instance in enumerate(testing_instances):
    lstDistances = []
    for j, comp_instance in enumerate(testing_instances):
        if i == j: continue
        d = distance(instance, comp_instance)
        lstDistances.append((d, comp_instance))
    lstDistances.sort()
    c = [0 for i in range(len(classes))]
    for j in range(k):
        cl = lstDistances[j][1][-1]
        c[classes.index(cl)] += 1
    clfy = classes[c.index(max(c))]
    testing_classes.append(clfy)
    if clfy == instance[-1]: totSc += 1

cm = []
for c in classes:
    lst = [0 for i in range(len(classes))]
    for i, val in enumerate(testing_classes):
        if testing_instances[i][-1] != c: continue
        for j in range(len(lst)):
            if val == classes[j]: lst[j] += 1
    cm.append(lst)

acc = round((100*totSc/len(testing_instances)), 3)
print("Testing Accuracy = " + str(acc) + "%")
print("Testing Confusion Matrix:")
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
    if num == 0: totAvg += 0
    else: totAvg += (num/tot)
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
    newcm[1][1] = len(testing_instances) - tot
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