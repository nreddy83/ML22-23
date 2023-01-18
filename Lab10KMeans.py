from sklearn.datasets import make_circles, make_moons
from matplotlib import pyplot
from pandas import DataFrame
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
# generate 2d classification dataset
X, y = make_moons(n_samples=200, noise=.1)

plt.grid(True)
plt.scatter(X[:,0], X[:,1])
plt.show()

clf = KMeans(n_clusters = 5, random_state = 0)
clf.fit(X)
print(clf.cluster_centers_)
print(clf.labels_)

plt.scatter(X[:,0], X[:,1], c = clf.labels_)
plt.show()