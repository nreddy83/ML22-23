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

# split into testing and training using 67:33 ratio in the code directly
random.shuffle(instances)
training_instances = instances[:int(len(instances)*2/3)]
testing_instances = instances[int(len(instances)*2/3):]

training_sets = []
for i in range(100): # different sample sets
    lst = []
    for i in range(20): # samples in each set
        r = random.randint(0, len(training_instances) - 1)
        lst.append(training_instances[r])
    training_sets.append(lst)

# function to calculate info gain/entropy
def calcEntropy(lst, tot):
    err = 0
    for val in lst:
        if val == 0: continue
        if val == tot: continue
        err += -(val/tot)*math.log2(val/tot)
    return err

def completed(decisionTree):
    return False

def sameclass(lst):
    v = lst[0][-1]
    for ins in lst:
        if ins[-1] != v: return False, v
    return True, v

decisionTree = {}
decisionTrees = []
tree = []

def makeTree(decisionTree, lst_instances, tree, head, dctToAdd):
    # adding recurred dct to tree
    for val in dctToAdd:
        decisionTree[val] = dctToAdd[val]

    # checking if tree is complete
    if completed(decisionTree): return decisionTree

    b, c = sameclass(lst_instances)
    if b:
        decisionTree[head] = "res" + str(classes.index(c))
    else:
    # determining best attribute to split this specific branch into
        bestE = 1
        bestAbt = -1
        bestLst = []
        for i, abt in enumerate(attributes):
            e = 0
            if (i, abt) in tree: continue
            currlst = []
            for val in dct[abt]:
                newlst = []
                for instance in lst_instances:
                    if instance[i] != val: continue
                    else: newlst.append(instance)
                currlst.append(newlst)
            for l in currlst:
                lst = [0 for i in range(len(classes))]
                ct = 0
                for val in l:
                    lst[classes.index(val[-1])] += 1
                    ct += 1
                e += ((ct)/len(lst_instances))*calcEntropy(lst, ct)
            if e < bestE:
                bestE = e
                bestAbt = i
                bestLst = currlst
        if bestAbt == -1: return decisionTree
        # building the branch
        tree.insert(0, (bestAbt, attributes[bestAbt]))
        lst = []
        newdct = {}
        newdct[head] = []
        for i, val in enumerate(dct[attributes[bestAbt]]):
            newdct[head].append(attributes[bestAbt] + val)
        for i, val in enumerate(dct[attributes[bestAbt]]):
            s = attributes[bestAbt] + val
            if len(bestLst) == 0: 
                newdct[head].remove(attributes[bestAbt] + val)
                continue
            elif len(bestLst[i]) == 0:
                newdct[head].remove(attributes[bestAbt] + val)
                continue
            else: decisionTree = makeTree(decisionTree, bestLst[i], tree, s, newdct)
        if bestE == 0:
            for i, ins in enumerate(bestLst):
                for inst in ins:
                    c = inst[-1]
                    h = attributes[bestAbt] + dct[attributes[bestAbt]][i]
                    decisionTree[h] = "res" + str(classes.index(c))
    return decisionTree

for training_set in training_sets:
    tree = []
    n = math.sqrt(len(attributes))
    n = int(math.floor(n))
    for i in range(n):
        r = random.randint(0, len(attributes) - 1)
        if (r, attributes[r]) not in tree: tree.append((r, attributes[r]))
        else:
            while (r, attributes[r]) in tree:
                r = random.randint(0, len(attributes) - 1)
            tree.append((r, attributes[r]))
    newt = []
    for i, abt in enumerate(attributes):
        if (i, abt) not in tree: newt.append((i, abt))
    dT = makeTree(decisionTree, training_set, tree, "root", {})
    decisionTrees.append((newt, dT))

# training accuracy
totSc = 0
for instance in training_instances:
    results = [0 for i in range(len(classes))]
    for tree, dT in decisionTrees:
        b = False
        ctr = 0
        v = instance[tree[ctr][0]]
        val = str(tree[ctr][1]) + str(v)
        if val not in dT and ctr >= len(val): continue
        else: 
            ctr += 1
            v = instance[tree[ctr][0]]
            val = str(tree[ctr][1]) + str(v)
            tree = [tree[1], tree[0]]
            ctr = 0
        if val not in dT: continue
        while b == False and "res" not in dT[val]:
            ctr += 1
            if ctr == len(tree): 
                b = True
                continue
            v = instance[tree[ctr][0]]
            val = str(tree[ctr][1]) + str(v)
            if val not in dT: b = True
        if b == True: continue
        r = dT[val]
        res = int(r[-1])
        results[res] += 1
    c = results.index(max(results))
    if classes[c] == instance[-1]: totSc += 1

acc = round((100*totSc/len(training_instances)), 3)
print("Training Accuracy = " + str(acc) + "%")
print()

# testing accuracy
totSc = 0
rlst = []
for instance in testing_instances:
    results = [0 for i in range(len(classes))]
    for tree, dT in decisionTrees:
        b = False
        ctr = 0
        v = instance[tree[ctr][0]]
        val = str(tree[ctr][1]) + str(v)
        if val not in dT  and ctr >= len(val): continue
        else: 
            ctr += 1
            v = instance[tree[ctr][0]]
            val = str(tree[ctr][1]) + str(v)
            tree = [tree[1], tree[0]]
            ctr = 0
        if val not in dT: continue
        while b == False and "res" not in dT[val]:
            ctr += 1
            if ctr == len(tree): 
                b = True
                continue
            v = instance[tree[ctr][0]]
            val = str(tree[ctr][1]) + str(v)
            if val not in dT: b = True
        if b == True: continue
        r = dT[val]
        res = int(r[-1])
        results[res] += 1
    c = results.index(max(results))
    if classes[c] == instance[-1]: totSc += 1
    rlst.append(classes[c])

cm = []
for c in classes:
    lst = [0 for i in range(len(classes))]
    for i, val in enumerate(rlst):
        if testing_instances[i][-1] != c: continue
        for j in range(len(lst)):
            if val == classes[j]: lst[j] += 1
    cm.append(lst)

acc = round((100*totSc/len(testing_instances)), 3)
print("Testing Accuracy = " + str(acc) + "%")
print("Confusion Matrix:")
for lst in cm:
    print(lst)
print()