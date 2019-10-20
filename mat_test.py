## Example 4 with iris
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import datasets
from sklearn.decomposition import PCA
# import iris
iris = datasets.load_iris()
X = iris.data[:, 0]  # all rows and tcol 1
y = iris.data[:,1]
name1=iris.target_names[0]
name2=iris.target_names[1]

plt.figure(1, figsize=(8, 6))
plt.scatter(X, y)
plt.xlabel(name1)
plt.ylabel(name2)
plt.show()
### 3D plot number 2
fig = plt.figure(2, figsize=(8, 6))
ax = Axes3D(fig, elev=-120, azim=120)
## PCA reduce to 3D
X_PCA_3D = PCA(n_components=3).fit_transform(iris.data)
ax.scatter(X_PCA_3D[:, 0], X_PCA_3D[:, 1], X_PCA_3D[:, 2],
           c=y,
           cmap=plt.cm.Set1,
           edgecolor='k',
           s=40)
ax.set_title("Iris in 3D")
ax.set_xlabel("Eigenvector1")
ax.set_ylabel("Eigenvector2")
ax.set_zlabel("Eigenvector3")
plt.show()
