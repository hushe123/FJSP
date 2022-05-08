
from Load_Process_Map import *
from Population import *
from Individual import *
import random
import Choose_Util

class Initial:

    def __init__(self):
        self.Map = Load_Process_Map()

    def Initial_Population(self):
        Pop = Population()

        for _ in range(Pop.Pop_Size):
            Idv = Individual()
            R_Random = random.uniform(0,1)
            if R_Random <= 0.1:
                Machine_Chromosome = self.Global_Selection_Init_Machine()
                Job_Chromosome = self.Random_Init_Job()
            elif R_Random > 0.1 and R_Random <= 0.2:
                Machine_Chromosome = self.Wordload_Considered_Init_Machine()
                Job_Chromosome = self.Random_Init_Job()
            else:
                Machine_Chromosome = self.Random_Init_Machine()
                Job_Chromosome = self.Random_Init_Job()                     

            Idv.Update_Chromosome(Job_Chromosome, Machine_Chromosome, self.Map)  
            Pop.Population_Member.append(Idv)
        return Pop

    def Random_Initial_Population(self):
        Pop = Population()
        for _ in range(Pop.Pop_Size):
            Idv = Individual()
            Machine_Chromosome = self.Random_Init_Machine()
            Job_Chromosome = self.Random_Init_Job()                     
            Idv.Update_Chromosome(Job_Chromosome, Machine_Chromosome, self.Map)  
            Pop.Population_Member.append(Idv)
        return Pop

    def Random_Init_Job(self):
        Job_Chromosome = []
        for i in range(self.Map.Job_Num):      
            Temp = self.Map.Operation_Num[i]  
            while Temp != 0:
                Job_Chromosome.append(i+1)
                Temp = Temp - 1
        random.shuffle(Job_Chromosome)  
        return Job_Chromosome
      
    def Random_Init_Machine(self):
        Machine_Chromosome = []        
        for m in range(self.Map.Job_Num):       
            for n in range(self.Map.Operation_Num[m]):      
                Machine_Index = random.choice(self.Map.Operation_Accessible_Machine_Index[m][n])
                Machine_Chromosome.append(Machine_Index + 1)
        return Machine_Chromosome

    def Global_Selection_Init_Machine(self):
        Array_Time = [0] * self.Map.Machine_Num   
        Job_List = list(range(0,self.Map.Job_Num))  
        Temp_Machine_Chromosome = [[] for _ in range(self.Map.Job_Num)] 
        while len(Job_List) != 0:               
            Job_Index = random.choice(Job_List)     
            for i in range(self.Map.Operation_Num[Job_Index]):  
                Temp_Array_Time = []       
                for j in range(len(self.Map.Operation_Accessible_Machine_Index[Job_Index][i])):
                        Temp_Machine_Index =  self.Map.Operation_Accessible_Machine_Index[Job_Index][i][j]
                        Temp_Array_Time.append(Array_Time[Temp_Machine_Index] +
                                         self.Map.Operation_Accessible_Machine_Time[Job_Index][i][j])  # 时间相加

                Min,_,Mach_Set_Index = Choose_Util.Get_Min_Info_With(Temp_Array_Time,
                                                        self.Map.Operation_Accessible_Machine_Index[Job_Index][i])  
                                
                Array_Time[Mach_Set_Index] = Min   
                Temp_Machine_Chromosome[Job_Index].append( Mach_Set_Index + 1)
            Job_List.remove(Job_Index)        
        
        Machine_Chromosome = []
        for Mach in Temp_Machine_Chromosome:  
            Machine_Chromosome.extend(Mach)

        return Machine_Chromosome
               

    def Local_Selection_Init_Machine(self):
        Job_List = list(range(0,self.Map.Job_Num))
        Temp_Machine_Chromosome = [[] for _ in range(self.Map.Job_Num)] 
        while len(Job_List) != 0:    
            Array_Time = [0] * self.Map.Machine_Num              
            Job_Index = random.choice(Job_List)    
            for i in range(self.Map.Operation_Num[Job_Index]):  
                Temp_Array_Time = []       
                for j in range(len(self.Map.Operation_Accessible_Machine_Index[Job_Index][i])):
                        Temp_Machine_Index =  self.Map.Operation_Accessible_Machine_Index[Job_Index][i][j]
                        Temp_Array_Time.append(Array_Time[Temp_Machine_Index] +
                                         self.Map.Operation_Accessible_Machine_Time[Job_Index][i][j])  # 时间相加
                    
                                
                Min,_,Mach_Set_Index = Choose_Util.Get_Min_Info_With(Temp_Array_Time,
                                                        self.Map.Operation_Accessible_Machine_Index[Job_Index][i])   
                Array_Time[Mach_Set_Index] = Min   
                Temp_Machine_Chromosome[Job_Index].append( Mach_Set_Index + 1)
            Job_List.remove(Job_Index)        
        
        Machine_Chromosome = []
        for Mach in Temp_Machine_Chromosome:  
            Machine_Chromosome.extend(Mach)

        return Machine_Chromosome



    def Wordload_Considered_Init_Machine(self):  
        Job_List = list(range(0,self.Map.Job_Num))  
        Array_Time = [0] * self.Map.Machine_Num   
        Temp_Machine_Chromosome = [[] for _ in range(self.Map.Job_Num)] 

        while len(Job_List) != 0:             
            Job_Index = random.choice(Job_List)   

            Temp_Sorted_Job_Map_Time = self.Map.Operation_Accessible_Machine_Time[Job_Index]
            Temp_Sorted_Determination = []  
            for i in range(self.Map.Operation_Num[Job_Index]):
                Temp = []
                Temp.append(min(Temp_Sorted_Job_Map_Time[i]))
                Temp.append(i)
                Temp_Sorted_Determination.append(Temp)

            Temp_Sorted_Determination = sorted(Temp_Sorted_Determination)

            Sorted_Job_Map_Time = []
            Sorted_Job_Map_Index = []
            for i in range(self.Map.Operation_Num[Job_Index]):
                Index = Temp_Sorted_Determination[i][1]   
                Sorted_Job_Map_Time.append(self.Map.Operation_Accessible_Machine_Time[Job_Index][Index])
                Sorted_Job_Map_Index.append(self.Map.Operation_Accessible_Machine_Index[Job_Index][Index])

            
            Temp_Machine_PutBack = [0] * self.Map.Operation_Num[Job_Index]  
            for i in range(self.Map.Operation_Num[Job_Index]):  
                Index = Temp_Sorted_Determination[i][1] 
                Temp_Array_Time = []       
                for j in range(len(Sorted_Job_Map_Index[i])):
                        Temp_Machine_Index =  Sorted_Job_Map_Index[i][j]
                        Temp_Array_Time.append(Array_Time[Temp_Machine_Index] + Sorted_Job_Map_Time[i][j])  

                Min,_,Mach_Set_Index = Choose_Util.Get_Min_Info_With(Temp_Array_Time,Sorted_Job_Map_Index[i])                                   
                Array_Time[Mach_Set_Index] = Min   
                Temp_Machine_PutBack[Index] = Mach_Set_Index + 1 

            Temp_Machine_Chromosome[Job_Index] = Temp_Machine_PutBack
            Job_List.remove(Job_Index)        
        
        Machine_Chromosome = []
        for Mach in Temp_Machine_Chromosome:  
            Machine_Chromosome.extend(Mach)

        return Machine_Chromosome            

    def Most_Work_Init_Job(self,Machine_Chromosome):
        Process_Time_Operator = []  
        Sign = 0 
        for i in range(self.Map.Job_Num):
            Temp_Process_Time = []  
            for j in range(self.Map.Operation_Num[i]):
                Process_Machine_Index = self.Map.Operation_Accessible_Machine_Index[i][j].index(Machine_Chromosome[Sign] - 1)
                Temp_Process_Time.append(self.Map.Operation_Accessible_Machine_Time[i][j][Process_Machine_Index])    
                Sign += 1
            Process_Time_Operator.append(Temp_Process_Time)

        Job_Process_All_Time = []  
        Job_Process_All_Index = [0] * self.Map.Job_Num   
        for i in range(self.Map.Job_Num):
            Job_Process_All_Time.append(sum(Process_Time_Operator[i]))
        Job_Chromosome = []  
        while(sum(Job_Process_All_Time) > 0):  
            Max_Index = Choose_Util.Get_Max_Index(Job_Process_All_Time) 
            Job_Chromosome.append(Max_Index + 1)  
            Job_Process_All_Time[Max_Index] -= Process_Time_Operator[Max_Index][Job_Process_All_Index[Max_Index]]
            Job_Process_All_Index[Max_Index] += 1  

        return Job_Chromosome


    def Most_Operator_Init_Job(self):
        Job_All_Operators_Num = self.Map.Operation_Num   # 工件的工序数量
        Job_Chromosome = []
        while(sum(Job_All_Operators_Num) > 0):  
            Max_Index = Choose_Util.Get_Max_Index(Job_All_Operators_Num) 
            Job_Chromosome.append(Max_Index + 1)
            Job_All_Operators_Num[Max_Index] -= 1

        return Job_Chromosome





