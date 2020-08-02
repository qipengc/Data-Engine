# coding:utf8

import pandas as pd
import numpy as np
from pandas import DataFrame,Series
from sklearn.cluster import KMeans,Birch,k_means
from sklearn.manifold import TSNE
from sklearn.metrics import silhouette_score
from matplotlib import pyplot as plt

np.set_printoptions(suppress=True)

data=pd.read_csv('CarPrice_Assignment.csv',index_col=0)
lst_cols=['CarName','fueltype', 'aspiration','carbody', 'drivewheel', 'enginelocation','enginetype','fuelsystem',
          'doornumber','cylindernumber']
new_data=data[[col for col in data.columns if col not in lst_cols]]

for col in lst_cols:
    dummies_Model = pd.DataFrame(pd.factorize(data[col])[0])  # 将变量转化为虚拟变量
    dummies_Model.columns=[col]
    new_data = pd.concat([new_data, dummies_Model], axis=1)  # 加入原本数据框

d=new_data.dropna(how='any',axis=0)

# 聚类
mod = KMeans(n_clusters=5, n_jobs=4, max_iter=500)  # 聚成3类数据,并发数为4，最大循环次数为500
mod.fit_predict(d)  # y_pred表示聚类的结果

# 聚成3类数据，统计每个聚类下的数据量，并且求出他们的中心
r1 = pd.Series(mod.labels_).value_counts()
r2 = pd.DataFrame(mod.cluster_centers_)
r = pd.concat([r2, r1], axis=1)
r.columns = list(d.columns) + [u'类别数目']
# 给每一条数据标注上被分为哪一类
r = pd.concat([d, pd.Series(mod.labels_, index=d.index)], axis=1)
r.columns = list(d.columns) + [u'聚类类别']

# 可视化过程

ts = TSNE()
ts.fit_transform(r)
ts = pd.DataFrame(ts.embedding_, index=r.index)

lst_color=['orange', 'green', 'purple', 'black', 'blue']
for i in range(0,5):
    a = ts[r[u'聚类类别'] == i]
    plt.plot(a[0], a[1], lst_color[i],marker="*")
plt.show()
