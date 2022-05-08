import random
import Fast_Sort
import numpy as np
from Population import *
import Choose_Util

from Initial import *
from Load_Process_Map import *
def Determina_Worse_Best(Pop):
    Nodominate = Pop.Nodominate_Ship    
    Di_Best = Fast_Sort.Modified_Crowding_Distance(Nodominate[0],Pop.Population_Member) # 拥挤度距离
    Di_Worse = Fast_Sort.Modified_Crowding_Distance(Nodominate[len(Nodominate)-1],Pop.Population_Member) 
    Best_Idv_Index = Choose_Util.Get_Max_Index(Di_Best)
    Worse_Idv_Index = Choose_Util.Get_Min_Index(Di_Worse)
    Best_Idv = Pop.Population_Member[Nodominate[0][Best_Idv_Index]]
    Worse_Idv = Pop.Population_Member[Nodominate[len(Nodominate)-1][Worse_Idv_Index]]
    return Best_Idv,Worse_Idv

def Update_Pop_DJaya(Pop,Map):
    New_Pop = Population()     
    New_Pop.Update_Pop(Pop.Population_Member)    
    Best_Idv,Worse_Idv = Determina_Worse_Best(Pop)
    for i in range(New_Pop.Pop_Size):
        if New_Pop.Population_Member[i] != Best_Idv and New_Pop.Population_Member[i] != Worse_Idv:
            New_Job_Chromosome ,New_Machine_Chromosome = Cross_Dyaja(New_Pop.Population_Member[i],Best_Idv,Worse_Idv)
            New_Pop.Population_Member[i].Update_Chromosome(New_Job_Chromosome,New_Machine_Chromosome,Map)           
    New_Pop.Determine_Nodominate_Ship() 
    return New_Pop


def Cross_Dyaja(P_Idv,B_Idv,W_Idv):
    Chromosome_Length = len(P_Idv.Job_Chromosome)           
    Sign_Variable = []                                     
    Job_Operator = [1] * max(P_Idv.Job_Chromosome)          
    Unchanged_Operator = []                                 
    New_Job_Chromosome = [0] * Chromosome_Length           
    New_Machine_Chromosome = [0] * Chromosome_Length       
    Changed_Machine_Index = []                              


    for i in range(Chromosome_Length):
        if P_Idv.Job_Chromosome[i] == W_Idv.Job_Chromosome[i]:
            Sign_Variable.append(i)                         # 需要变动的基因位置
        else:
            New_Job_Chromosome[i] = P_Idv.Job_Chromosome[i]
            Temp = []
            Temp.append(P_Idv.Job_Chromosome[i])
            Temp.append(Job_Operator[P_Idv.Job_Chromosome[i]-1])
            Job_Operator[P_Idv.Job_Chromosome[i]-1] += 1
            Unchanged_Operator.append(Temp)     # [[2,1],...,]

        if P_Idv.Machine_Chromosome[i] == W_Idv.Machine_Chromosome[i]:
            Changed_Machine_Index.append(i)
        else:
            New_Machine_Chromosome[i] = P_Idv.Machine_Chromosome[i]

    Job_Operator = [1] * max(P_Idv.Job_Chromosome)          
    Index = 0                                               

    for i in range(Chromosome_Length):
        Temp = []
        Temp.append(B_Idv.Job_Chromosome[i])
        Temp.append(Job_Operator[B_Idv.Job_Chromosome[i]-1])
        Job_Operator[B_Idv.Job_Chromosome[i]-1] += 1
        if Temp not in Unchanged_Operator:                  
            New_Job_Chromosome[Sign_Variable[Index]] = B_Idv.Job_Chromosome[i]
            Index += 1

    for i in Changed_Machine_Index:    
        New_Machine_Chromosome[i] = B_Idv.Machine_Chromosome[i]
    return New_Job_Chromosome ,New_Machine_Chromosome


def Get_Machine_Process(Idv,Map):
    Machine_Workload = [0] * Map.Machine_Num                       
    Machine_Assignment = [[] for _ in range(Map.Machine_Num)]       
    Machine_Assignment_Time = [[] for _ in range(Map.Machine_Num)]  

    Index = 0                                                       
    for i in range(Map.Job_Num):                                    
        for j in range(Map.Operation_Num[i]):                       # 此工件的每个工序
            Machine_Index = Map.Operation_Accessible_Machine_Index[i][j].index(Idv.Machine_Chromosome[Index] - 1)   # 加工机器下标
            Machine_Workload[Idv.Machine_Chromosome[Index] - 1] += Map.Operation_Accessible_Machine_Time[i][j][Machine_Index]         # 加工时间
            Temp = []         
            Temp.append(i)    
            Temp.append(j)    
            Machine_Assignment[Idv.Machine_Chromosome[Index] - 1].append(Temp)
            Machine_Assignment_Time[Idv.Machine_Chromosome[Index] - 1].append(Map.Operation_Accessible_Machine_Time[i][j][Machine_Index])
            Index += 1
    return Machine_Workload,Machine_Assignment,Machine_Assignment_Time


def Mutation_Pop_DJaya(Pop,Map,Prop):
    Same_Idv_Index = []   
    Same_Obj_Index = []    

    Sign_Idv = [0] * Pop.Pop_Size  
    Sign_Obj = [0] * Pop.Pop_Size  
    while 0 in Sign_Idv:                
        for i in range(Pop.Pop_Size):
            if Sign_Idv[i] == 0:        
                Temp = []
                Temp.append(i)          
                Sign_Idv[i] = 1        
                for j in range(Pop.Pop_Size):
                    if Sign_Idv[j] == 0:
                        if (Pop.Population_Member[i].Job_Chromosome.tolist() == Pop.Population_Member[j].Job_Chromosome.tolist() 
                        and Pop.Population_Member[i].Machine_Chromosome.tolist() == Pop.Population_Member[j].Machine_Chromosome.tolist()):
                            Temp.append(j)
                            Sign_Idv[j] = 1     
                if len(Temp) >= 2:
                    Same_Idv_Index.append(Temp)      

    while 0 in Sign_Obj:                   
        for i in range(Pop.Pop_Size):
            if Sign_Obj[i] == 0:        
                Temp = []
                Temp.append(i)          
                Sign_Obj[i] = 1         
                for j in range(Pop.Pop_Size):
                    if Sign_Obj[j] == 0:
                        if Pop.Population_Member[i].Adaptability == Pop.Population_Member[j].Adaptability:
                            Temp.append(j)
                            Sign_Obj[j] = 1     
                if len(Temp) >= 2:
                    Same_Obj_Index.append(Temp)   

    if len(Same_Idv_Index) != 0:            
        for i in range(len(Same_Idv_Index)):
            for j in range(1,len(Same_Idv_Index[i])):    
                R_Random = random.uniform(0,1)
                if R_Random <= Prop:
                    M_Idv = Maximum_Workload_Reduction(Pop.Population_Member[Same_Idv_Index[i][j]],Map)
                    J_Idv = Reverse_Operation_Mutation(M_Idv,Map)
                    Pop.Population_Member[Same_Idv_Index[i][j]] = J_Idv

    if len(Same_Obj_Index) != 0:           
        for i in range(len(Same_Obj_Index)):
            for j in range(1,len(Same_Obj_Index[i])):    
                R_Random = random.uniform(0,1)
                if R_Random <= Prop:
                    M_Idv = Maximum_Workload_Reduction(Pop.Population_Member[Same_Obj_Index[i][j]],Map)
                    J_Idv = Reverse_Operation_Mutation(M_Idv,Map)
                    Pop.Population_Member[Same_Obj_Index[i][j]] = J_Idv


def Maximum_Workload_Reduction(Idv,Map):
    Machine_Workload,Machine_Assignment,Machine_Assignment_Time = Get_Machine_Process(Idv,Map)
    Max_Workload_Machine_Index = Choose_Util.Get_Max_Index(Machine_Workload)    
    Processed_Operator = Machine_Assignment[Max_Workload_Machine_Index]         
    Processed_Operator_Num = len(Processed_Operator)                            
    Ratio = [0] * Processed_Operator_Num                                        
    for i in range(Processed_Operator_Num):                                     
        Ratio[i] = Machine_Assignment_Time[Max_Workload_Machine_Index][i] / (Processed_Operator[i][1] + 1)    
    Choose_Operator = Processed_Operator[Choose_Util.Get_Max_Index(Ratio)]      
    Choose_Operator_Map_Index = Map.Operation_Accessible_Machine_Index[Choose_Operator[0]][Choose_Operator[1]]
    Min_Workload_Machine = []
    Min_Workload_Machine_Index = []

    for i in range(len(Choose_Operator_Map_Index)):
        Min_Workload_Machine.append(Machine_Workload[Choose_Operator_Map_Index[i]])
        Min_Workload_Machine_Index.append(Choose_Operator_Map_Index[i])
    _,_,Choose_Index = Choose_Util.Get_Min_Info_With(Min_Workload_Machine,Min_Workload_Machine_Index)
    Temp_Machine_Index = 0         
    for i in range(Choose_Operator[0]):         
        Temp_Machine_Index += Map.Operation_Num[i]
    Temp_Machine_Index += Choose_Operator[1]    # 此工件
    Idv.Machine_Chromosome[Temp_Machine_Index] = Choose_Index + 1
    New_Idv = Individual()
    New_Idv.Update_Chromosome(Idv.Job_Chromosome,Idv.Machine_Chromosome,Map)
    return New_Idv

   
def Reverse_Operation_Mutation(Idv,Map):
    Random_Index1 = np.random.randint(0, Map.Chromosome_Length) 
    Random_Index2 = np.random.randint(0, Map.Chromosome_Length)  
    while Random_Index1 == Random_Index2:
        Random_Index2 = np.random.randint(0, Map.Chromosome_Length)  
    Left_Pos = Random_Index1 if Random_Index1 < Random_Index2 else Random_Index2
    Right_Pos = Random_Index1 if Random_Index1 > Random_Index2 else Random_Index2
    Temp_List = []      
    for i in range(Left_Pos,Right_Pos+1):
        Temp_List.append(Idv.Job_Chromosome[i])
    Temp_List.reverse()     # 反转
    for i in range(len(Temp_List)):   
        Idv.Job_Chromosome[Left_Pos] = Temp_List[i] 
        Left_Pos += 1
    New_Idv = Individual()
    New_Idv.Update_Chromosome(Idv.Job_Chromosome,Idv.Machine_Chromosome,Map)
    return New_Idv


def Get_Mutation_Prob(Iteration,Max_Iteration):
    R_Max = 0.8
    R_Min = 0.2
    return R_Max - (((R_Max - R_Min) / Max_Iteration) * Iteration)


if __name__ == "__main__":

    aaa = Individual()
    print(aaa == None)
