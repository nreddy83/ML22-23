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
        if float(val) < float(v1): instances[j][i] = "low"
        elif float(val) < float(v2): instances[j][i] = "medium"
        else: instances[j][i] = "high"
    i += 1

print()

# split into testing and training using 67:33 ratio
random.shuffle(instances)
val = int(len(instances)*2/3)
training_instances = instances[:val]
testing_instances = instances[val:]

# classification
highScore = [0, 0] # attribute, #correct
rule = []
for i, attribute in enumerate(attributes):
    totSc = 0
    lst = []
    for j, cat in enumerate(dct[attribute]):
        sc = [0, 0]
        for k, c in enumerate(classes): 
            sc1 = 0
            for h, instance in enumerate(training_instances):
                if instance[i] != cat: continue
                if instance[-1] == c: sc1 += 1
            if sc1 > sc[0]: sc = [sc1, c]
        totSc += sc[0]
        lst.append([attribute, cat, sc[1]])
    if totSc > highScore[1]: 
        highScore = [i, totSc]
        rule = lst

# training results
print("Rules:")
for r in rule:
    print("If " + r[0] + " = " + r[1] + ", then class = " + r[2])
acc = round((100*totSc/len(training_instances)), 3)
print("Training Accuracy = " + str(acc) + "%")
print()

# testing
totSc = 0
for instance in testing_instances:
    b = False
    for r in rule:
        if instance[highScore[0]] != r[1]: continue
        if r[2] == instance[-1]: 
            totSc += 1

acc = round((100*totSc/len(testing_instances)), 3)
print("Testing Accuracy = " + str(acc) + "%")
print()

print("Training/Testing Split = " + str(len(training_instances)) + ":" + str(len(testing_instances)))