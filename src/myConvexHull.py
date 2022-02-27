import numpy as np
from sympy import false

def ndarray_to_list(l):
    newL = l.tolist()
    newL.sort()
    return newL

def det(p1,p2,p3):
    return (p1[0]*p2[1]) + (p3[0]*p1[1]) + (p2[0]*p3[1]) - (p1[0]*p3[1]) - (p2[0]*p1[1]) - (p3[0]*p2[1])

def whichArea(p1,p2,p3):
#memvalidasi daerah dari koordinat titik p3 terhadap garis p1p2
    determinan = det(p1,p2,p3)
    if(determinan == 0):
        return 0
    elif (determinan > 0):
        return 1
    elif (determinan < 0):
        return -1

def divideArea(p1,arr,p2):
#mengembalikan daerah s1 dan s2 terhadap garis p1p2
    s1 = [] ; s2 = []
    dontcare = 0
    for idx in range(len(arr)):
        area = whichArea(p1,p2,arr[idx])
        if(area == 1):
            s1.append(arr[idx])            
        if(area == 0):
            dontcare += 1
        if(area == -1):
            s2.append(arr[idx])

    return s1,s2

def eliminateInsideTriangle(p1,p2,p3,points,area):
    newPoint = []
    for point in points:
        a1 = whichArea(p1,p3,point)
        a2 = whichArea(p2,p3,point)
        if(area == 1):
            if(a1 == 1 or a2 == -1):
                newPoint.append(point)
        elif(area == 2):
            if(a1 == -1 or a2 == 1):
                newPoint.append(point)

    return newPoint

def farthestPoint(p1,arr,p2):
    farthest = [0,0]
    d = 0
    for idx in range(len(arr)):
        point1   = np.array(p1)
        point2   = np.array(p2)
        point    = np.array(arr[idx])
        distance = np.linalg.norm(np.cross(point2-point1, point1-point))/np.linalg.norm(point2-point1)
        
        if(d < distance):
            d = distance
            farthest = point.tolist()

    return farthest

def findConvex(p1,arr,p2,area):
    if(len(arr) == 0):
        return []
    if(len(arr) == 1):      #bersisa titik terluar atau tidak memiliki titik di luar hull
        return arr
    else:
        points = []
        if(area == 0):
            s1 , s2 = divideArea(p1 , arr , p2)

            #DAERAH S1
            newP1 = farthestPoint(p1,s1,p2)     #titik terjauh daerah S1
            points.append(newP1)
            newS1 = eliminateInsideTriangle(p1,p2,newP1,s1,1)

            s1_fromS1_left , ignorePart = divideArea(p1,newS1,newP1)       #daerah kiri-atas antara p1-newP1 (s1_fromS1_left)
            s1_fromS1_right , ignorePart = divideArea(newP1,newS1,p2)      #daerah kanan-atas antara newP1-p2 (s1_fromS1_right)
            newPoint1 = findConvex(p1 , s1_fromS1_left , newP1 , 1)
            newPoint2 = findConvex(newP1 , s1_fromS1_right , p2 , 1)

            #DAERAH S2
            newP2 = farthestPoint(p1,s2,p2)     #titik terjauh daerah S2
            points.append(newP2)
            newS2 = eliminateInsideTriangle(p1,p2,newP2,s2,2)

            ignorePart , s2_fromS2_left = divideArea(p1,newS2,newP2)       #daerah kiri-bawah antara p1-newP2 (s2_fromS2_left)
            ignorePart , s2_fromS2_right = divideArea(newP2,newS2,p2)      #daerah kanan-bawah antara newP2-p2 (s2_fromS2_right)
            newPoint3 = findConvex(p1 , s2_fromS2_left , newP2 , 2)
            newPoint4 = findConvex(newP2 , s2_fromS2_right , p2 , 2)

            return points + newPoint1 + newPoint2 + newPoint3 + newPoint4

        elif (area == 1):
            newP = farthestPoint(p1,arr,p2)
            points.append(newP)
            newS1 = eliminateInsideTriangle(p1,p2,newP,arr,1)

            s1_left , ignorePart = divideArea(p1,newS1,newP)
            s1_right , ignorePart = divideArea(newP,newS1,p2)
            newPoint1 = findConvex(p1, s1_left , newP , 1)
            newPoint2 = findConvex(newP, s1_right , p2 , 1)

            return points + newPoint1 + newPoint2

        elif (area == 2):
            newP = farthestPoint(p1,arr,p2)
            points.append(newP)
            newS2 = eliminateInsideTriangle(p1,p2,newP,arr,2)
            
            ignorePart , s2_left = divideArea(p1,newS2,newP)
            ignorePart , s2_right = divideArea(newP,newS2,p2)
            newPoint1 = findConvex(p1, s2_left , newP , 2)
            newPoint2 = findConvex(newP, s2_right , p2 , 2)
            
            return points + newPoint1 + newPoint2

def convexHull(bucket):
    newBucket = ndarray_to_list(bucket)
    p1 = newBucket[0]
    p2 = newBucket[len(newBucket)-1]
    Points = findConvex(p1 , newBucket , p2 , 0)
    Points.sort()
    return [p1] + Points + [p2]
