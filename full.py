
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

import datetime
from pandas_datareader import data

import matplotlib.pyplot as plt

fig= plt.figure()
ax=fig.add_subplot(111, projection='3d')

df3D = pd.read_csv('full.csv',index_col = 'date_time', parse_dates=True)
xTemp = df3D['Temperature']
yTurb = df3D['Turbitity']
zRain = df3D['Rain']
color = df3D['Contamination']


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.set_xlabel('Temperature C')
ax.set_ylabel('Turbitity')
ax.set_zlabel('Rain fall')

ax.scatter(xTemp, yTurb, zRain, c=color)


plt.show()
