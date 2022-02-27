import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt 
from sklearn import datasets

data = datasets.load_iris()                                 #ujicoba dataset : load_iris()
#create a DataFrame 
df = pd.DataFrame(data.data, columns=data.feature_names) 
df['Target'] = pd.DataFrame(data.target) 

#visualisasi hasil ConvexHull
import matplotlib.pyplot as plt
#Implementasi myConvexHull
import myConvexHull as ch

plt.figure(figsize = (10, 6))
colors = ['b','r','g']
plt.title('Petal Width vs Petal Length')                    #ujicoba dataset Iris : petal width vs petal length

# Atribut x
x_plot = 2

# Atribut y
y_plot = 3

plt.xlabel(data.feature_names[x_plot])
plt.ylabel(data.feature_names[y_plot])
for i in range(len(data.target_names)):
    bucket = df[df['Target'] == i]
    bucket = bucket.iloc[:,[x_plot , y_plot]].values
    hulls = ch.convexHull(bucket)
    p1 = hulls[0]
    p2 = hulls[len(hulls)-1]
    plt.scatter(bucket[:, 0], bucket[:, 1], label=data.target_names[i])

    upperP = p1 ; belowP = p1
    for idx in range(1,len(hulls)):
        p3 = hulls[idx]
        if(p3 == p2):
            #UPPER PART
            x_edge1 , y_edge1 = upperP[0] , upperP[1]
            x_edge2 , y_edge2 = p3[0] , p3[1]
            x = np.array([x_edge1] + [x_edge2])
            y = np.array([y_edge1] + [y_edge2])
            plt.plot(x, y, colors[i])
            #BELOW PART
            x_edge1 , y_edge1 = belowP[0] , belowP[1]
            x_edge2 , y_edge2 = p3[0] , p3[1]
        else:
            if(ch.whichArea(p1,p2,p3) == 1):
                x_edge1 , y_edge1 = upperP[0] , upperP[1]
                x_edge2 , y_edge2 = p3[0] , p3[1]
                upperP = p3
            elif(ch.whichArea(p1,p2,p3) == -1):
                x_edge1 , y_edge1 = belowP[0] , belowP[1]
                x_edge2 , y_edge2 = p3[0] , p3[1]
                belowP = p3

        x = np.array([x_edge1] + [x_edge2])
        y = np.array([y_edge1] + [y_edge2])
        plt.plot(x, y, colors[i])
plt.legend()