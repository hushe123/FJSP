
import Critical
import GA_Util
import Choose_Util

from Initial import *
from  Load_Process_Map import *


def Local_Search_Djaya(Idv,Map):
    R_Random = random.uniform(0,1)
    New_Idv = Individual()
    if R_Random <= 0.7:
        New_Idv = Critical.Move_Ciritical_To_SameMachine(Idv,Map)
        # New_Idv = Critical.Move_Ciritical_To_OtherMachine(New_Idv,Map)
    else:
        New_Idv = Local_Search_Operator2(Idv,Map)
    return New_Idv

def Local_Search_Operator2(Idv,Map):
    Critical_Flag,_,_,_,_ = Critical.Get_Critiacl_Operation(Idv,Map)
    Critical_Operator = []                     
    for i in range(Map.Chromosome_Length):      
        if Critical_Flag[i] != 0:
            Temp_Critical = []
            Temp_Critical.append(Idv.Job_Chromosome[i] - 1)                                 
            Temp_Critical.append(Critical.Get_Operation_Order(Idv.Job_Chromosome,i) - 1)   
            Critical_Operator.append(Temp_Critical)
    
    Machine_Workload,Machine_Assignment,Machine_Assignment_Time = GA_Util.Get_Machine_Process(Idv,Map)
    Max_Workload_Machine_Index = Choose_Util.Get_Max_Index(Machine_Workload)   

    Choose_Set =  Machine_Assignment[Max_Workload_Machine_Index]      
    for i in range(len(Choose_Set)):                                   
        if Choose_Set[i] in Critical_Operator:
            Choose_Critical_Set.append(Choose_Set[i])
    if len(Choose_Critical_Set) == 0:
        return Idv
    Ratio = [0] * len(Choose_Critical_Set)
    for i in range(len(Choose_Critical_Set)):
        Index = Choose_Set.index(Choose_Critical_Set[i])                
        Ratio[i] = Machine_Assignment_Time[Max_Workload_Machine_Index][Index] / (Choose_Critical_Set[i][1] + 1)

    Choose_Operator = Choose_Critical_Set[Choose_Util.Get_Max_Index(Ratio)]     
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

    Temp_Machine_Index += Choose_Operator[1]    
    Idv.Machine_Chromosome[Temp_Machine_Index] = Choose_Index + 1
    New_Idv = Individual()
    New_Idv.Update_Chromosome(Idv.Job_Chromosome, Idv.Machine_Chromosome, Map)

    return New_Idv






