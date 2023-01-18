import csv
import random

def get_class_labels(data):
    lst = []
    seen = set()
    for instance in data:
        if instance[-1] not in seen:
            seen.add(instance[-1])
            lst.append(instance[-1])
    return lst

def kmeans_pp(data, centroids):
    weights = []
    for insIdx in range(len(data)):
        minDist = 1000000
        for centroid in centroids:
            dist = distance(centroid, data[insIdx]) #(distance squared)
            if dist<minDist: minDist = dist
        weights.append(minDist)
    return data[random.choices([insIdx for insIdx in range(len(data))],weights,k=1)[0]]

def distance(instance1, instance2):
    dist = 0
    for idx in range(len(instance1)-1):
        dist+=(float(instance1[idx])-float(instance2[idx]))*(float(instance1[idx])-float(instance2[idx]))
    return dist

# read in file with data
file = open('Iris.csv')
csvreader = csv.reader(file)
header = []
header = next(csvreader)
data = []
for row in csvreader:
    data.append(row)

classLabels = get_class_labels(data)
k = len(classLabels)

# kmeans++
centroids = []
# choose first centroid randomly
centroids.append(data[random.choices([insIdx for insIdx in range(len(data))],k=1)[0]])
for idx in range(1, k):
    next_centroid = kmeans_pp(data, centroids)
    centroids.append(next_centroid)

print(centroids)

