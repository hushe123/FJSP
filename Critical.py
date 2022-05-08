
import numpy as np
import SetAdp
from Individual import * 
from Load_Process_Map import *
import random

def Get_Operation_Order(Job_Chromosome,index):
    Num = 1                                                  
    for i in range(index):                                    
            if Job_Chromosome[i] == Job_Chromosome[index]:   
                    Num += 1                                  
    return Num


def Get_Machine_Index(Job_Chromosome,index):
    Job_Order_Num = np.zeros(len(Job_Chromosome),dtype=int)   
    for i in range(len(Job_Chromosome)):
        Job_Order_Num[Job_Chromosome[i] - 1] += 1
    Temp = 0                                                  
    for j in range(index):
        if(Job_Chromosome[j] == Job_Chromosome[index]):
            Temp += 1   
    Pre_sum = 0                                               
    for m in range(Job_Chromosome[index] - 1):
        Pre_sum += Job_Order_Num[m]    
    return Pre_sum + Temp


def Get_Pre_Operation_Post_Index(Job_Chromosome,Job_Index,Job_Operator_Num):
    Pre_Index = Index = Post_Index = -1                   
    Num = 0
    for i in range(len(Job_Chromosome)):
            if Job_Chromosome[i] == Job_Index:            
                    Num += 1
                    if Num == Job_Operator_Num - 1:      
                            Pre_Index = i
                            continue
                    if Num == Job_Operator_Num :          
                            Index = i
                            continue
                    if Num == Job_Operator_Num + 1:      
                            Post_Index = i
                            continue        
    return  Pre_Index, Index,Post_Index                   

   
def Get_Critiacl_Operation(Idv,Map):
    Start_Time,End_Time,_,_ = SetAdp.Decoder(Idv,Map)
    Reverse_Map = []    
    for i in range(Map.Job_Num):
        Temp = np.array(Map.Machine_Process_Map[i])
        Temp = Temp.tolist()
        Temp.reverse()
        Reverse_Map.append(Temp)

    Reverse_Job = np.array(Idv.Job_Chromosome)
    Reverse_Job = Reverse_Job.tolist()
    Reverse_Job.reverse()                             

    Reverse_Machine = []                              
    Order_Num = np.zeros(Map.Job_Num,dtype=int)       
    for i in Idv.Job_Chromosome:
        Order_Num[i - 1] += 1

    j = 0                                             
    for i in range(Map.Job_Num):
        Temp = []                                 
        Num = Order_Num[i]                        
        while(Num != 0):
            Temp.append(Idv.Machine_Chromosome[j])
            j = j + 1
            Num -= 1 
        Temp.reverse()
        for m in Temp:
            Reverse_Machine.append(m)
    
    Temp_idv = Individual()
    Temp_Reverse_Map = Load_Process_Map()       
    Temp_Reverse_Map.Update_Map(Reverse_Map)
    Temp_idv.Update_Chromosome(Reverse_Job,Reverse_Machine,Temp_Reverse_Map)        
    Reverse_Start_Time,Reverse_End_Time,_,_ = SetAdp.Decoder(Temp_idv,Temp_Reverse_Map)
    for i in range(len(Start_Time)):
        Temp1 = Reverse_Start_Time[i]
        Temp2 = Reverse_End_Time[i]
        for j in range(len(Temp1)):                
            if Temp1[j] != 0:
                Temp1[j] = Idv.Adaptability[0] - Temp1[j]
        for m in range(len(Temp2)):
            if Temp2[m] != 0:
                Temp2[m] = Idv.Adaptability[0] - Temp2[m]
        Temp1 = Temp1.tolist()                     
        Temp1.reverse()
        Temp1 = np.array(Temp1)
        Temp2 = Temp2.tolist()
        Temp2.reverse()
        Temp2 = np.array(Temp2)
        Reverse_Start_Time[i] = Temp1              
        Reverse_End_Time[i] = Temp2

    Temp = Reverse_Start_Time                          
    Reverse_Start_Time = Reverse_End_Time
    Reverse_End_Time = Temp

    Critical_Flag = np.zeros(Map.Chromosome_Length,dtype = int)  
    for i in range(len(Start_Time)):        
        Temp1 = Start_Time[i]
        Temp2 = End_Time[i]
        Temp3 = Reverse_Start_Time[i]
        Temp4 = Reverse_End_Time[i]
        for j in range(len(Temp1)):                          # 判断第j个工序是否为关键工序          
            if (Temp1[j]==Temp3[j] and Temp2[j]==Temp4[j] and Temp2[j]!=0) or (Temp1[j]==Temp3[j] and Temp2[j] == Idv.Adaptability[0]):
                Critical_Flag[j] = 1
    return Critical_Flag,Start_Time,End_Time,Reverse_Start_Time,Reverse_End_Time


def Change_Critical_Order(Idv,Map):
    Critical_Flag,_,_,_,_ = Get_Critiacl_Operation(Idv,Map)
    Temp = []                                               # 关键工序
    Temp_Index = []                                         
    for i in range(Map.Chromosome_Length):
        if Critical_Flag[i] != 0:
            Temp.append(Idv.Job_Chromosome[i])
            Temp_Index.append(i)
    
    Index1 = Index2 = Index3 = -1                          
    Index1 = random.choice(Temp_Index)
    Index2 = random.choice(Temp_Index)
    Index3 = random.choice(Temp_Index)
    while (Temp[Temp_Index.index(Index1)] == Temp[Temp_Index.index(Index2)] or
            Temp[Temp_Index.index(Index1)] == Temp[Temp_Index.index(Index3)] or
            Temp[Temp_Index.index(Index2)] == Temp[Temp_Index.index(Index3)]):
        Index1 = random.choice(Temp_Index)
        Index2 = random.choice(Temp_Index)
        Index3 = random.choice(Temp_Index)
    
    Sign = [Index1,Index2,Index3]                           
    random.shuffle(Sign)                                    
    while Sign == [Index1,Index2,Index3]:                   
        random.shuffle(Sign)
    Value1 = Temp[Temp_Index.index(Sign[0])]               
    Value2 = Temp[Temp_Index.index(Sign[1])]
    Value3 = Temp[Temp_Index.index(Sign[2])]
    Temp[Temp_Index.index(Index2)] = Value2  
    Temp[Temp_Index.index(Index3)] = Value3           

    for i in range(len(Temp)):                              
        Idv.Job_Chromosome[Temp_Index[i]] = Temp[i] 
    New_Idv = Individual()                                  
    New_Idv.Update_Chromosome(Idv.Job_Chromosome, Idv.Machine_Chromosome,Map)   
    return New_Idv


def Change_Critical_Machine(Idv,Map,Num):   
    Critical_Flag,_,_,_,_ = Get_Critiacl_Operation(Idv,Map)     
    Sign = [0] * Map.Chromosome_Length                       
    Sign_Num = 0
    while Sign_Num <= Num:                                    
        for i in range(Map.Chromosome_Length):
            if Critical_Flag != 0:                
                R = random.uniform(0,1)                       
                if Sign[i] == 0 and R < 0.2:
                    Sign[i] = 1
                    Sign_Num += 1

    for i in range(Map.Chromosome_Length):
        if Critical_Flag != 0 and Sign[i] == 1:             
            Machine_Set = Map.Operation_Accessible_Machine_Index[Idv.Job_Chromosome[i] - 1][Get_Operation_Order(Idv.Job_Chromosome,i) - 1]
            Idv.Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,i)] = random.choice(Machine_Set)

    New_Idv = Individual()                                    
    New_Idv.Update_Chromosome(Idv.Job_Chromosome, Idv.Machine_Chromosome,Map)  
    return New_Idv


def Get_Critical_Block(Idv,Map):       
    Critical_Flag,Start_Time,End_Time,Reverse_Start_Time,_ = Get_Critiacl_Operation(Idv,Map)
    Critical_Operation_Machine = [0] * Map.Chromosome_Length  
    for i in range(Map.Chromosome_Length):      
        if Critical_Flag[i] != 0:                              
            Critical_Operation_Machine[i] = Idv.Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,i)]

    Critical_Block = []                                      
    for i in range(Map.Chromosome_Length):
        if Critical_Flag[i] != 0:                             
            for j in range(i+1,Map.Chromosome_Length):
                if Critical_Flag[j] != 0:
                    if Critical_Operation_Machine[i] == Critical_Operation_Machine[j]:
                        Time1 = End_Time[Critical_Operation_Machine[i]-1][i]    
                        Time2 = Start_Time[Critical_Operation_Machine[j]-1][j]  
                        if Time1 == Time2:                                                         
                            Temp = []                         
                            Temp1 = []                        
                            Temp1.append(Start_Time[Critical_Operation_Machine[i]-1][i])
                            Temp1.append(End_Time[Critical_Operation_Machine[i]-1][i])
                            Temp1.append(Idv.Job_Chromosome[i])
                            Temp1.append(Get_Operation_Order(Idv.Job_Chromosome,i))
                            Temp1.append(Critical_Operation_Machine[i])

                            Temp2 = []     
                            Temp2.append(Start_Time[Critical_Operation_Machine[j]-1][j])
                            Temp2.append(End_Time[Critical_Operation_Machine[j]-1][j])
                            Temp2.append(Idv.Job_Chromosome[j])
                            Temp2.append(Get_Operation_Order(Idv.Job_Chromosome,j))
                            Temp2.append(Critical_Operation_Machine[j])      

                            Temp.append(Temp1)    
                            Temp.append(Temp2)     
                            Critical_Block.append(Temp)                           
    Critical_Block_Copy = []                  
    Sign = [0] * len(Critical_Block)      
    while 0 in Sign:
        Index = 0
        Temp = []
        while Index <= (len(Critical_Block)-1):
            if Sign[Index] != 0:   
                Index += 1
                continue
            if len(Temp) == 0:
                Temp.append(Critical_Block[Index][0])
                Temp.append(Critical_Block[Index][1])
                Sign[Index] = 1
            else:
                if Temp[len(Temp)-1] == Critical_Block[Index][0]:
                    Temp.append(Critical_Block[Index][1])
                    Sign[Index] = 1   
            Index += 1
        Critical_Block_Copy.append(Temp)
    return  Critical_Block_Copy,Critical_Flag,Start_Time,End_Time,Reverse_Start_Time     

                 
def GanTeGraph_To_Operation(Idv,Map,End_Time,Temp_Block_Operation,Index,Insert):
    Machine_Use_List = [-1] * len(Idv.Job_Chromosome)
    for i in range(len(End_Time)):
        Temp_End = End_Time[i]
        for j in range(len(Temp_End)):
            if Temp_End[j] == 0:
                    continue
            Machine_Use_List[j] = i
    Machine_Operation_List = [[] for _ in range(Map.Machine_Num)]
    Job_Operation_Num = [1] * Map.Job_Num
    for i in range(Map.Chromosome_Length):
        Temp = []
        Temp.append(Idv.Job_Chromosome[i])
        Temp.append(Job_Operation_Num[Idv.Job_Chromosome[i] - 1])
        Job_Operation_Num[Idv.Job_Chromosome[i] - 1] += 1
        Machine_Operation_List[Machine_Use_List[i]].append(Temp)
    Temp_Machine_Operation_List = []
    Temp_Machine_Operation_List.append(Temp_Block_Operation[2])
    Temp_Machine_Operation_List.append(Temp_Block_Operation[3])
    Machine_Operation_List[Temp_Block_Operation[4] - 1].remove(Temp_Machine_Operation_List)
    Machine_Operation_List[Insert[0]-1].insert(Insert[1],Temp_Machine_Operation_List)
    List = []
    for i in range(len(Machine_Operation_List[Insert[0]-1])):
        Temp = Machine_Operation_List[Insert[0]-1][i]
        if Temp[0] == Temp_Block_Operation[2]:
            List.append(Temp[1])  
    List_Copy = np.array(List)
    List_Copy = List_Copy.tolist()
    List_Copy = np.sort(List_Copy)
    if List != List_Copy.tolist():
        return [],[]
    Change_Job_Chromosome = [0] * len(Idv.Job_Chromosome)
    Sign = 0        # 标记新的工序排序染色体的每个位置
    Job_Operation_Num = [1] * Map.Job_Num
    Sign_Array = [i for i in range(Map.Machine_Num)]

    Machine_Sign = []
    while Sign <= Map.Chromosome_Length-1:            
        Machine_Choose = random.choice(Sign_Array)
        Machine_Sign.append(Machine_Choose)

        if len(Machine_Operation_List[Machine_Choose]) != 0:
            if Job_Operation_Num[Machine_Operation_List[Machine_Choose][0][0]-1] == Machine_Operation_List[Machine_Choose][0][1]:
                Change_Job_Chromosome[Sign] = Machine_Operation_List[Machine_Choose][0][0]
                Job_Operation_Num[Machine_Operation_List[Machine_Choose][0][0]-1] += 1  
                Machine_Operation_List[Machine_Choose].remove(Machine_Operation_List[Machine_Choose][0])                
                Sign += 1
                Machine_Sign = []

        New_Machine_Sign = list(set(Machine_Sign))
        if len(New_Machine_Sign) == len(Sign_Array):
            return [],[]
        if len(Machine_Operation_List[Machine_Choose]) == 0: 
            Sign_Array.remove(Machine_Choose)

    Temp_Machine_Chromosome = Idv.Machine_Chromosome.tolist()
    Temp_Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,Index)] = Insert[0]
    Temp_Machine_Chromosome = np.array(Temp_Machine_Chromosome)
    Change_Job_Chromosome = np.array(Change_Job_Chromosome)
    return Change_Job_Chromosome,Temp_Machine_Chromosome   


def Move_Ciritical_To_OtherMachine(Idv,Map):
        Critical_Block,_,_,End_Time,Reverse_Start_Time = Get_Critical_Block(Idv,Map)
        
        Neighbour_Member = []           
        Neighbour_Member_Value = []
        Neighbour_Member.append(Idv)
        Neighbour_Member_Value.append(Idv.Adaptability[0])

        for i in range(len(Critical_Block)):
            Temp_Block = Critical_Block[i]
            
            for j in range(len(Temp_Block)):
                Temp_Block_Operation = Temp_Block[j]
                Map_Machine = Map.Machine_Process_Map[Temp_Block_Operation[2]-1][Temp_Block_Operation[3]-1]
                Block_Operation_Pre_Post_Time = [-1] * 2
                Pre_Index,Index,Post_Index = Get_Pre_Operation_Post_Index(Idv.Job_Chromosome,
                                Temp_Block_Operation[2],Temp_Block_Operation[3])
                if Pre_Index == -1:    
                    Block_Operation_Pre_Post_Time[0] = 0
                    Post_Operation_Machine = Idv.Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,Post_Index)] - 1
                    Block_Operation_Pre_Post_Time[1] = Reverse_Start_Time[Post_Operation_Machine][Post_Index]
                elif Post_Index == -1:  
                    Block_Operation_Pre_Post_Time[1] = Idv.Adaptability[0]
                    Pre_Operation_Machine = Idv.Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,Pre_Index)] - 1
                    Block_Operation_Pre_Post_Time[0] = End_Time[Pre_Operation_Machine][Pre_Index]
                else:
                    Pre_Operation_Machine = Idv.Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,Pre_Index)] - 1
                    Post_Operation_Machine = Idv.Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,Post_Index)] - 1
                    Block_Operation_Pre_Post_Time[0] = End_Time[Pre_Operation_Machine][Pre_Index]      
                    Block_Operation_Pre_Post_Time[1] = Reverse_Start_Time[Post_Operation_Machine][Post_Index]
                Block_Machine_Pre_Post_Time = [] 
                for m in range(len(Map_Machine)):
                    if Map_Machine[m] == 9999:      
                        continue
                    if m == Temp_Block_Operation[4] - 1:   
                        continue
                    Insert_Index = []       
                    for n in range(Map.Chromosome_Length):                        
                        if End_Time[m][n] == 0:            
                            continue
                        Insert_Index.append(n)                    
                    Insertion_Location = 0                  
                    Temp = [] 
                    Temp.append(0)
                    if len(Insert_Index) == 0:              
                        Temp.append(Idv.Adaptability[0])  
                    else:   
                        Temp.append(Reverse_Start_Time[m][Insert_Index[0]])  
                    Temp.append(Map_Machine[m])
                    Temp.append(m+1)
                    Temp.append(Insertion_Location)
                    Block_Machine_Pre_Post_Time.append(Temp) 
                    Insertion_Location += 1

                    for k in range(len(Insert_Index)):                                              
                        if k == len(Insert_Index) - 1:  # 机器上最后一个工序 
                            Temp = []
                            Temp.append(End_Time[m][Insert_Index[k]])
                            Temp.append(Idv.Adaptability[0])                                               
                        else:        
                            Temp = []
                            Temp.append(End_Time[m][Insert_Index[k]])
                            Temp.append(Reverse_Start_Time[m][Insert_Index[k+1]])
                        Temp.append(Map_Machine[m])
                        Temp.append(m+1)
                        Temp.append(Insertion_Location)
                        Insertion_Location += 1
                        Block_Machine_Pre_Post_Time.append(Temp)

                Insertion = []  
                for p in range(len(Block_Machine_Pre_Post_Time)):
                        Temp_Pre_Post_Time = Block_Machine_Pre_Post_Time[p]
                        Time_Interval = [-1] * 2        
                        if Temp_Pre_Post_Time[0] <= Block_Operation_Pre_Post_Time[0]:
                            Time_Interval[0] = Block_Operation_Pre_Post_Time[0]
                        else:
                            Time_Interval[0] = Temp_Pre_Post_Time[0]

                        if Temp_Pre_Post_Time[1] <=  Block_Operation_Pre_Post_Time[1]:
                            Time_Interval[1] = Temp_Pre_Post_Time[1]
                        else:
                            Time_Interval[1] = Block_Operation_Pre_Post_Time[1]   

                        if  (Time_Interval[1] - Time_Interval[0]) >= Temp_Pre_Post_Time[2]:
                            Temp = []
                            Temp.append(Temp_Pre_Post_Time[3])      
                            Temp.append(Temp_Pre_Post_Time[4])     
                            Insertion.append(Temp)
                for q in range(len(Insertion)):
                    Temp_Insert = Insertion[q]
                    Temp_Idv = Individual()
                    Temp_Job_Chromosome,Temp_Machine_Chromosome = GanTeGraph_To_Operation(Idv,
                            Map,End_Time,Temp_Block_Operation,Index,Temp_Insert)                        
                    if len(Temp_Job_Chromosome) == 0 and len(Temp_Machine_Chromosome) == 0:
                        continue
                    Temp_Idv.Update_Chromosome(Temp_Job_Chromosome, Temp_Machine_Chromosome, Map)                                    
                    Neighbour_Member.append(Temp_Idv)
                    Neighbour_Member_Value.append(Temp_Idv.Adaptability[0])                                  
        Choose_Index = Neighbour_Member_Value.index(min(Neighbour_Member_Value))
        if Choose_Index != 0:
            New_Idv = Individual()
            New_Idv.Update_Chromosome(Neighbour_Member[Choose_Index].Job_Chromosome,
                    Neighbour_Member[Choose_Index].Machine_Chromosome, Map)
        return New_Idv

def Move_Ciritical_To_SameMachine(Idv,Map):
    Critical_Block,_,Start_Time,End_Time,Reverse_Start_Time = Get_Critical_Block(Idv,Map)
    Neighbour_Member = []
    Neighbour_Member_Value = []
    Neighbour_Member.append(Idv)
    Neighbour_Member_Value.append(Idv.Adaptability[0])

    for i in range(len(Critical_Block)):
        Temp_Block = Critical_Block[i]
        if len(Temp_Block) == 2:                       
            _,Block_First_Index,_ = Get_Pre_Operation_Post_Index(Idv.Job_Chromosome,Temp_Block[0][2],Temp_Block[0][3])
            Block_Machine_Index = Temp_Block[0][4]-1
            Index = 0
            for j in range(Map.Chromosome_Length):
                if End_Time[Block_Machine_Index][j] == 0:
                    continue
                else:
                    Index += 1
                if j == Block_First_Index:
                    break       
            Insertion = []
            Insertion.append(Block_Machine_Index+1)   
            Insertion.append(Index)   
            Temp_Idv = Individual()                         # 生成新个体
            Temp_Job_Chromosome,Temp_Machine_Chromosome = GanTeGraph_To_Operation(Idv,
                    Map,End_Time,Temp_Block[0],Block_First_Index,Insertion)            
            if len(Temp_Job_Chromosome) == 0 and len(Temp_Machine_Chromosome) == 0:
                    continue
            Temp_Idv.Update_Chromosome(Temp_Job_Chromosome, Temp_Machine_Chromosome, Map)
            Neighbour_Member.append(Temp_Idv)               # 将新个体加入
            Neighbour_Member_Value.append(Temp_Idv.Adaptability[0])                          
        else:
            _,Block_First_Index,_ = Get_Pre_Operation_Post_Index(Idv.Job_Chromosome,Temp_Block[0][2],Temp_Block[0][3])
            _,Block_Last_Index,_ = Get_Pre_Operation_Post_Index(Idv.Job_Chromosome,
                                    Temp_Block[len(Temp_Block)-1][2],Temp_Block[len(Temp_Block)-1][3])
            for j in range(len(Temp_Block)):
                if j == 0 or j == len(Temp_Block) - 1:
                        continue                
                Temp_Block_Operation = Temp_Block[j]                   
                Block_Machine_Index = Temp_Block_Operation[4]-1     
                Block_Operation_Pre_Time = [-1] * 2                               
                Block_Operation_Post_Time = [-1] * 2                
                Pre_Index,Index,Post_Index = Get_Pre_Operation_Post_Index(Idv.Job_Chromosome,
                                Temp_Block_Operation[2],Temp_Block_Operation[3])
                
                Pre_Operation_Machine = Idv.Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,Pre_Index)] - 1
                Post_Operation_Machine = Idv.Machine_Chromosome[Get_Machine_Index(Idv.Job_Chromosome,Post_Index)] - 1                
                Block_Operation_Pre_Time[1] = Start_Time[Block_Machine_Index][Block_First_Index]    # 这两个时间是固定的
                Block_Operation_Post_Time[0] = End_Time[Block_Machine_Index][Block_Last_Index]

                if Pre_Index == -1:        
                    Block_Operation_Pre_Time[0] = 0
                    Block_Operation_Post_Time[1] = Start_Time[Post_Operation_Machine][Post_Index]
                elif Post_Index == -1:    
                    Block_Operation_Pre_Time[0] = End_Time[Pre_Operation_Machine][Pre_Index]
                    Block_Operation_Post_Time[1] = Idv.Adaptability[0]
                else:                                         
                    Block_Operation_Pre_Time[0] = End_Time[Pre_Operation_Machine][Pre_Index]      
                    Block_Operation_Post_Time[1] = Start_Time[Post_Operation_Machine][Post_Index]
                Flag_Move_Forward = 1      
                Flag_Move_Backward = 1                
                if Block_Operation_Pre_Time[0] >= Block_Operation_Pre_Time[1]:  
                    Flag_Move_Forward = -1
                if Block_Operation_Post_Time[0] >= Block_Operation_Post_Time[1]:
                    Flag_Move_Backward = -1

                Block_Machine_Pre_Post_Time = []         
                Insert_Index = []                          
                for n in range(Map.Chromosome_Length):                             
                    if End_Time[Block_Machine_Index][n] == 0:
                        continue
                    Insert_Index.append(n)
                Insertion_Location = 0                     
                Temp.append(0)
                Temp.append(Reverse_Start_Time[Block_Machine_Index][Insert_Index[0]])  
                Temp.append(Insertion_Location)
                Block_Machine_Pre_Post_Time.append(Temp) 
                Insertion_Location += 1

                for k in range(len(Insert_Index)):                                              
                    if k == len(Insert_Index) - 1:         
                        Temp = []
                        Temp.append(End_Time[Block_Machine_Index][Insert_Index[k]])
                        Temp.append(Idv.Adaptability[0])                                               
                    else:        
                        Temp = []
                        Temp.append(End_Time[Block_Machine_Index][Insert_Index[k]])
                        Temp.append(Reverse_Start_Time[Block_Machine_Index][Insert_Index[k+1]])
                    Temp.append(Insertion_Location)
                    Insertion_Location += 1
                    Block_Machine_Pre_Post_Time.append(Temp)    

                Block_Operation_Process_Time = Map.Machine_Process_Map[Temp_Block_Operation[2]-1][Temp_Block_Operation[3]-1][Block_Machine_Index]
                Insertion = []  
                for p in range(len(Block_Machine_Pre_Post_Time)):
                    Temp_Pre_Post_Time = Block_Machine_Pre_Post_Time[p]
                    if (Temp_Pre_Post_Time[1] - Temp_Pre_Post_Time[0]) < Block_Operation_Process_Time:
                        continue
                    if Flag_Move_Forward != -1:                               
                        if Temp_Pre_Post_Time[0] < Block_Operation_Pre_Time[1]:                            
                            if Temp_Pre_Post_Time[0] < Block_Operation_Pre_Time[0]:   
                                continue
                            else:
                                Temp = []
                                Temp.append(Block_Machine_Index+1)  
                                Temp.append(Temp_Pre_Post_Time[2])
                                Insertion.append(Temp)
                    if Flag_Move_Backward != -1:       # 后移                                       
                        if Temp_Pre_Post_Time[0] > Block_Operation_Post_Time[0]:
                            if (Temp_Pre_Post_Time[0] +  Block_Operation_Process_Time) > Block_Operation_Post_Time[1]:
                                continue
                            else:
                                Temp = []
                                Temp.append(Block_Machine_Index+1)  
                                Temp.append(Temp_Pre_Post_Time[2]-1)
                                Insertion.append(Temp)                                                                    
                    if Temp_Pre_Post_Time[0] == Block_Operation_Post_Time[0]:  
                        Temp = []
                        Temp.append(Block_Machine_Index+1)  
                        Temp.append(Temp_Pre_Post_Time[2]-1)
                        Insertion.append(Temp)    

                for q in range(len(Insertion)):        
                    Temp_Insert = Insertion[q]
                    Temp_Idv = Individual()
                    Temp_Job_Chromosome,Temp_Machine_Chromosome = GanTeGraph_To_Operation(Idv,
                            Map,End_Time,Temp_Block_Operation,Index,Temp_Insert)                        
                    if len(Temp_Job_Chromosome) == 0 and len(Temp_Machine_Chromosome) == 0:
                            continue
                    Temp_Idv.Update_Chromosome(Temp_Job_Chromosome, Temp_Machine_Chromosome,Map)
                    Neighbour_Member.append(Temp_Idv)
                    Neighbour_Member_Value.append(Temp_Idv.Adaptability[0])
                                    
    Choose_Index = Neighbour_Member_Value.index(min(Neighbour_Member_Value))
    New_Idv = Individual()
    New_Idv.Update_Chromosome(Neighbour_Member[Choose_Index].Job_Chromosome,
                                Neighbour_Member[Choose_Index].Machine_Chromosome, Map)
    return New_Idv
        



