import math
# open file
import csv
k = 5 #establishing k value, values of 4 and 5 give much higher accuracies
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

iv = int(len(instances)/k)

def average(instances):
    avgIns = [0 for i in range(len(instances[0]))]
    for instance in instances:
        for i, val in enumerate(instance):
            if i == len(instance) - 1: continue
            avgIns[i] += float(val)
    for i, val in enumerate(avgIns):
        avgIns[i] = val/len(instances)
    return avgIns

def distance(a, b):
    d = 0
    for i in range(4):
        d += (float(a[i]) - float(b[i]))*(float(a[i]) - float(b[i]))
    return math.sqrt(d)

avgIns = average(instances)
newInstances = []
for instance in instances:
    inst = instance[:-1]
    d = distance(inst, avgIns)
    newInstances.append((d, instance))
newInstances.sort()

#kmeans
kmeans = []
buckets = {i: [] for i in range(k)}
places = {}

instances = [] # will change to account for tuple in code later -- just testing accuracy for now
for d, ins in newInstances:
    instances.append(ins)

s = int(math.floor(iv/2))
for i in range(k):
    idx = s + iv*i
    ctd = instances[idx]
    kmeans.append(ctd)

print(kmeans)

def mindist(a, kmeans):
    mindist = 99999999999999999999
    minidx = 0
    for i in range(k):
        d = distance(a, kmeans[i])
        if d < mindist: 
            mindist = d
            minidx = i
    return minidx

def updatemeans(kmeans, buckets):
    for bucket in buckets:
        tot = 0
        tot1 = 0
        tot2 = 0
        tot3 = 0
        tot4 = 0
        for val in buckets[bucket]:
            v = instances[val][:-1]
            v1, v2, v3, v4 = v
            tot1 += float(v1)
            tot2 += float(v2)
            tot3 += float(v3)
            tot4 += float(v4)
            tot += 1
        if tot != 0: kmeans[bucket] = (tot1/tot, tot2/tot, tot3/tot, tot4/tot)
        else: kmeans[bucket] = (tot1, tot2, tot3, tot4)
    return kmeans

b = True
ctr = 0
while(b):
    hopct = 0
    for i, p in enumerate(instances):
        if i < k and ctr == 0: bucket = i
        else: bucket = mindist(p, kmeans)
        buckets[bucket].append(i)
        if i not in places: hopct = 10
        elif places[i] != bucket: hopct += 1
        places[i] = bucket
    kmeans = updatemeans(kmeans, buckets)
    if hopct == 0: b = False
    else:
        for c in buckets:
            buckets[c] = []
    ctr += 1

print("Final means:")
for i in range(k):
    s = str(i+1) + ": " + str(kmeans[i]) + " => " + str(len(buckets[i]))
    print(s)

fin = [0 for i in range(len(buckets))]
for i, bucket in enumerate(buckets):
    majvot = [0 for i in range(len(classes))]
    for ins in buckets[bucket]:
        ins = instances[ins]
        majvot[classes.index(ins[-1])] += 1
    fin[i] = majvot.index(max(majvot))

rlst = [0 for i in range(len(instances))]
totSc = 0
for i, bucket in enumerate(buckets):
    for ins in buckets[bucket]:
        insc = instances[ins][-1]
        rlst[ins] = classes[fin[i]]
        if classes.index(insc) == fin[i]: totSc += 1

cm = []
for p, c in enumerate(classes):
    lst = [0 for i in range(len(classes))]
    for i, val in enumerate(rlst):
        if instances[i][-1] != c: continue
        for j in range(len(lst)):
            if val == classes[j]: 
                lst[j] += 1
    cm.append(lst)
    
acc = round((100*totSc/len(instances)), 3)
print("Accuracy = " + str(acc) + "%")

for lst in cm:
    print(lst)