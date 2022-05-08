import math
import random
import numpy as np

T1_Range = 0.8    
T2_Range = 0.6

def Get_Population_Adaptability(Population_Member):
    Adaptability = []   
    for i in range(len(Population_Member)):
        Temp = []
        Temp.append(Population_Member[i].Adaptability[0])
        Adaptability.append(Temp)
    return Adaptability

def Normal_Object_Space(Population_Member):
    Adaptability = Get_Population_Adaptability(Population_Member)  
    Normal_Population_Objection = []    
    Object_Dim = []     
    Object_Dim_Min = [] 
    Object_Dim_Max = [] 
    for i in range(len(Adaptability[0])):
        Object_Dim.append([item[i] for item in Adaptability])
        if min(Object_Dim[i]) != max(Object_Dim[i]):
            Object_Dim_Min.append(min(Object_Dim[i]))   
            Object_Dim_Max.append(max(Object_Dim[i]))
        else:
            Object_Dim_Min.append(min(Object_Dim[i]))   
            Object_Dim_Max.append(-1)            
               
    for i in range(len(Adaptability)):
        Normal_Population_Objection.append(
            ((np.array(Adaptability[i]) - np.array(Object_Dim_Min)) / 
            (np.array(Object_Dim_Max) - np.array(Object_Dim_Min))).tolist()
            )
   
    return Normal_Population_Objection

def Get_MaxDim_Dot(Dot_Ally):
    MaxDim_Dot = []         
    for i in range(len(Dot_Ally[0])):
        Devide_Value = np.array([math.exp(-6)]*len(Dot_Ally[0]))   
        Devide_Value[i] = math.exp(0)
        
        Temp_Devide = []    
        for j in range(len(Dot_Ally)):
            Temp = np.array(Dot_Ally[j])
            Temp = Temp / Devide_Value
            Temp_Devide.append(max(Temp))

        MaxDim_Dot.append(Temp_Devide.index(min(Temp_Devide)))
    return MaxDim_Dot

def Get_MaxDim_Dot_Normalize(Population_Member):
    Adaptability = Normal_Object_Space(Population_Member)
    return Get_MaxDim_Dot(Adaptability)


def Get_MaxDim_Dot_Nunormalize(Population_Member):
    Adaptability = Get_Population_Adaptability(Population_Member)
    return Get_MaxDim_Dot(Adaptability)


def Get_Equation_ThreeDim(Point1,Point2,Point3):   # [,,],[,,],[,,]
    # 计算方程中的未知数
    a = ((Point2[1]-Point1[1])*(Point3[2]-Point1[2])-(Point2[2]-Point1[2])*(Point3[1]-Point1[1]))
    b = ((Point2[2]-Point1[2])*(Point3[0]-Point1[0])-(Point2[0]-Point1[0])*(Point3[2]-Point1[2]))
    c = ((Point2[0]-Point1[0])*(Point3[1]-Point1[1])-(Point2[1]-Point1[1])*(Point3[0]-Point1[0]))
    d = (0-(a*Point1[0]+b*Point1[1]+c*Point1[2]))
    # 计算每维截距
    Intercept = []
    Intercept.append(-(d/a))
    Intercept.append(-(d/b))
    Intercept.append(-(d/c))
    return Intercept


def Dist(member1,member2):
    Euclidean_Distance = 0  
    for i in range(len(member1)):
        Euclidean_Distance += math.pow((member1[i] - member2[i]), 2)
    Euclidean_Distance = math.sqrt(Euclidean_Distance)
    return Euclidean_Distance


def Set_YU_Value(Population_Member):
    Adaptability = Normal_Object_Space(Population_Member)  
    Sum = 0  
    Member_Num = len(Population_Member) 
    for i in range(Member_Num):      
        if i != Member_Num - 1:
            for j in range(i+1,Member_Num):
                Sum += Dist(Adaptability[i],Adaptability[j])
    Sum = Sum / ((Member_Num * (Member_Num - 1))/2)
    T1 = Sum * T1_Range
    T2 = Sum * T2_Range
    return T1,T2


def Set_Cluster_Center(Clusters,Adaptability):
    Cluster_Center = []  
    for i in range(len(Clusters)):
        Temp_Center = np.array([0.0]*len(Adaptability[0]))    
        Cluster_Content = Clusters[i]
        for j in Cluster_Content:
            Temp_Center += np.array(Adaptability[j])
        # 取得均值--质心点
        Temp_Center = np.divide(Temp_Center, len(Cluster_Content))
        Cluster_Center.append(Temp_Center.tolist())
    return Cluster_Center

def Set_Member_Cluster(Cluster_Center,Adaptability,Population_Member):
    for i in range(len(Adaptability)):
        Temp_Dist = []          
        for j in range(len(Cluster_Center)):
            Temp_Dist.append(Dist(Cluster_Center[j], Adaptability[i]))
        Population_Member[i].Cluster_Index = Temp_Dist.index(min(Temp_Dist)) + 1


def K_Means(Cluster_Num,Adaptability,Population_Member):
    for i in range(Cluster_Num):
        Member_Cluster = [[] for m in range(Cluster_Num)]
        for j in range(len(Adaptability)):
            Member_Cluster[Population_Member[j].Cluster_Index - 1].append(j)

        Cluster_Center = Set_Cluster_Center(Member_Cluster,Adaptability)
        Set_Member_Cluster(Cluster_Center,Adaptability,Population_Member)

def Set_Population_Cluster(Population_Member):
    Adaptability = Normal_Object_Space(Population_Member)  
    T1,T2 = Set_YU_Value(Population_Member)  
    Cluster_Num = 0        
    Cluster_Center = []    
    Cluster = []        

    Sign = np.array([1]*len(Adaptability))     
    while 1 in Sign:       
        Temp_Save = []       
        Cluster_Num = Cluster_Num + 1       

        Temp_Sign = []      
        for i in range(len(Adaptability)):
            if Sign[i] == 1:
                Temp_Sign.append(i)
        Random_Index = random.sample(Temp_Sign, 1)
        Random_Choose = Adaptability[Random_Index[0]]    

        for i in range(len(Adaptability)):
            if Sign[i] != 0:
                if Dist(Adaptability[i], Random_Choose) <= T1:
                    Temp_Save.append(i)
                    if Dist(Adaptability[i], Random_Choose) <= T2:
                        Sign[i] = 0
        
        Cluster.append(Temp_Save)
    Cluster_Center = Set_Cluster_Center(Cluster,Adaptability)
    Set_Member_Cluster(Cluster_Center,Adaptability,Population_Member)
    K_Means(Cluster_Num,Adaptability,Population_Member)
    Adjust_Cluster_Balance(Population_Member)

def Adjust_Cluster_Balance(Population_Member):
    Temp_Cluster = []  
    for i in range(len(Population_Member)):
        Temp_Cluster.append(Population_Member[i].Cluster_Index)
    Cluster_Num = max(Temp_Cluster)
    Cluster_Member = [[] for m in range(Cluster_Num)]
    for i in range(len(Temp_Cluster)):
        Cluster_Member[Temp_Cluster[i] - 1].append(i)    
    
    Cluster_With_Member = []     
    for i in range(len(Cluster_Member)):
        if len(Cluster_Member[i]) > 2:
            Cluster_With_Member.append(i)  
    for i in range(len(Cluster_Member)):
        if len(Cluster_Member[i]) == 1 or len(Cluster_Member[i]) == 2: 
            for j in Cluster_Member[i]:
                Index = random.choice(Cluster_With_Member)
                Cluster_Member[Index].append(j)
    Index = 0
    while Index <= len(Cluster_Member) - 1:
        if len(Cluster_Member[Index]) <= 2:
            Cluster_Member.remove(Cluster_Member[Index])
            Index -= 1
        Index += 1
    for i in range(len(Cluster_Member)):
        Temp_Cluster = Cluster_Member[i]
        for j in Temp_Cluster:
            Population_Member[j].Cluster_Index = i + 1





