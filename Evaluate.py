import numpy as np
import math
def Is_Dominate(Obj1, Obj2):
    Objective_Dim = len(Obj1)
    Flag = [9999] * Objective_Dim
    for i in range(Objective_Dim):
        if Obj1[i] < Obj2[i]:
            Flag[i] = -1   
        elif Obj1[i] == Obj2[i]:
            Flag[i] = 0    
    return True if sum(Flag) < 0  else False

def Normal_Objective(Obj):
    Obj_Num = len(Obj)   
    if Obj_Num <= 1:     
        return Obj
    Normal_Population_Objection = []  
    Object_Dim = []     
    Object_Dim_Min = [] 
    Object_Dim_Max = [] 

    for i in range(len(Obj[0])):
        Object_Dim.append([item[i] for item in Obj])    
        if min(Object_Dim[i]) != max(Object_Dim[i]):
            Object_Dim_Min.append(min(Object_Dim[i]))  
            Object_Dim_Max.append(max(Object_Dim[i]))
        else:                                           
            Object_Dim_Min.append(0)                   
            Object_Dim_Max.append(1)            
    for i in range(Obj_Num):
        Normal_Population_Objection.append(
            ((np.array(Obj[i]) - np.array(Object_Dim_Min)) / 
            (np.array(Object_Dim_Max) - np.array(Object_Dim_Min))).tolist())    
    return Normal_Population_Objection


def Dist(member1,member2):
    Euclidean_Distance = 0  # 欧式距离
    for i in range(len(member1)):
        Euclidean_Distance += math.pow((member1[i] - member2[i]), 2)
    Euclidean_Distance = math.sqrt(Euclidean_Distance)
    return Euclidean_Distance

def Pareto_Num(Population_Member,Pareto):
    Temp_Pub = []
    for i in range(len(Pareto)):
        Temp = []
        Temp.append(Population_Member[Pareto[i]].Job_Chromosome.tolist())
        Temp.append(Population_Member[Pareto[i]].Machine_Chromosome.tolist())
        if Temp not in Temp_Pub:
            Temp_Pub.append(Temp)
    return len(Temp_Pub)


def Set_Coverage(Pareto_A,Pareto_B):
    Nodominate_Num = 0     # A 中支配 B的数目
    for i in range(len(Pareto_A)): 
        for j in range(len(Pareto_B)):
            if Is_Dominate(Pareto_A[i],Pareto_B[j]):
                Nodominate_Num += 1
                break
    return Nodominate_Num / len(Pareto_B)

def Inverse_Generational_Distance(Pareto_A,Pareto_B):
    N_Pareto_A_Size = len(Pareto_A)
    N_Pareto_B_Size = len(Pareto_B)
    Exclude_A = [] 
    Exclude_B = []  
    for i in range(N_Pareto_A_Size):
        for j in range(N_Pareto_B_Size):
            if Is_Dominate(Pareto_A[i],Pareto_B[j]): 
                if j not in Exclude_B:
                    Exclude_B.append(j)
            elif Is_Dominate(Pareto_B[j],Pareto_A[i]): 
                if i not in Exclude_A:
                    Exclude_A.append(i)
                break
    Combine_Normal = []
    Combine_Normal.extend(Pareto_A)
    Combine_Normal.extend(Pareto_B)
    Combine_Normal = Normal_Objective(Combine_Normal)
    N_Pareto_A = Combine_Normal[0:N_Pareto_A_Size]
    N_Pareto_B = Combine_Normal[N_Pareto_A_Size:N_Pareto_A_Size+N_Pareto_B_Size]
    # 合并Pareto
    True_Pareto = []
    for i in range(N_Pareto_A_Size):
        if i not in Exclude_A:
            True_Pareto.append(N_Pareto_A[i])

    for i in range(N_Pareto_B_Size):
        if i not in Exclude_B:
            True_Pareto.append(N_Pareto_B[i])

    IGD_A = 0
    IGD_B = 0
    for i in range(len(Exclude_A)):
        Temp_Value = []
        for j in range(len(True_Pareto)):
            Temp_Value.append(Dist(N_Pareto_A[Exclude_A[i]],True_Pareto[j]))
        IGD_A += min(Temp_Value)
    IGD_A /= N_Pareto_A_Size
    for i in range(len(Exclude_B)):
        Temp_Value = []
        for j in range(len(True_Pareto)):
            Temp_Value.append(Dist(N_Pareto_B[Exclude_B[i]],True_Pareto[j]))
        IGD_B += min(Temp_Value)
    IGD_B /= N_Pareto_B_Size
    return IGD_A,IGD_B

def Hypervolume(Pareto_A,Pareto_B):
    pass



