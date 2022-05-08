import numpy as np

def Decoder(Idv,Map):
        Machine_Set = Idv.Machine_Chromosome  
        Job_Set = Idv.Job_Chromosome    
        Job_List_Time = []   
        Job_List_Order = np.array(np.zeros(Map.Job_Num,dtype=int))   
        Job_List_Last_Time = np.array(np.zeros(Map.Job_Num,dtype=int))     
        Start_Time = np.array(np.zeros((Map.Machine_Num,Map.Chromosome_Length),dtype=int))    
        End_Time = np.array(np.zeros((Map.Machine_Num,Map.Chromosome_Length),dtype=int))
        
        Temp_M = 0
        for i in range(Map.Job_Num):       
                Job = Map.Machine_Process_Map[i]
                for j in range(len(Job)):
                        Job_List = Job[j]
                        Job_List_Time.append(Job_List[Idv.Machine_Chromosome[Temp_M] - 1])
                        Temp_M = Temp_M + 1
        Job_List_Time = np.array(Job_List_Time,dtype=int)
        
        for i in range(Map.Chromosome_Length):
                Pre_Job_List_Time = 0 
                Machine_Release_Time = 0 
                Pre_All_List = 0       
                for m in range(Map.Job_Num):
                        if m == Job_Set[i] - 1:
                                break
                        Pre_All_List += len(Map.Machine_Process_Map[m])
                Machine_Index = int(Pre_All_List + Job_List_Order[Job_Set[i] - 1]) 
                Machine_Num = Machine_Set[Machine_Index] 
                End_Time[Machine_Num - 1][i] = Job_List_Time[Machine_Index]    
                if(i == 0):  
                        Machine_Release_Time = 0        
                else:
                        j = i - 1
                        while(j != -1 and End_Time[Machine_Num - 1][j] == 0):   
                                j = j - 1
                        if j == -1:     
                                Machine_Release_Time = 0
                        else:   
                                Machine_Release_Time = End_Time[Machine_Num - 1][j]       
                Pre_Job_List_Time = Job_List_Last_Time[Job_Set[i] - 1] 
                if Pre_Job_List_Time >= Machine_Release_Time:
                      Start_Time[Machine_Num - 1][i]  = Pre_Job_List_Time
                else:
                      Start_Time[Machine_Num - 1][i]  = Machine_Release_Time  
                End_Time[Machine_Num - 1][i] = End_Time[Machine_Num - 1][i] + Start_Time[Machine_Num - 1][i]
                Job_List_Order[Job_Set[i] - 1] += 1    
                Job_List_Last_Time[Job_Set[i] - 1] = End_Time[Machine_Num - 1][i]     
        return Start_Time,End_Time,Job_List_Time,Job_List_Last_Time


def Adaptability_For_Energy_MLoad(Machine_Process_Map,Idv,Machine_Cost,Chromosome_Size,Job_Num,Machine_Num):
        _,_,Job_List_Time,Job_List_Last_Time = Decoder(Machine_Process_Map,Idv,Chromosome_Size,Job_Num,Machine_Num)
        Machine_Set = Idv.Machine_Chromosome 
        Max_Finish_Time = 0 
        Machine_All_Load = 0.0 
        Machine_All_Energy = 0 
        Machine_Using_Num = np.array(np.zeros(Machine_Num,dtype=int)) 
        Machine_Using_Time = np.array(np.zeros(Machine_Num,dtype=int)) 

        Max_Finish_Time = max(Job_List_Last_Time)      
        for i in range(Chromosome_Size):
                Machine_Using_Num[Machine_Set[i] - 1]  += 1     
                Machine_Using_Time[Machine_Set[i] - 1] += Job_List_Time[i]
        for i in range(Machine_Num):
                Machine_All_Energy += Machine_Cost[i] * Machine_Using_Time[i] + Max_Finish_Time - Machine_Using_Time[i]
                if Machine_Using_Time[i] != 0:
                        Machine_All_Load += Machine_Using_Num[i] / Machine_Using_Time[i]
        return [Max_Finish_Time,Machine_All_Load,Machine_All_Energy]


def Get_Price_For_Operation(Start_Time,End_Time):
        Elec_Price = np.array([[0.4,0,7],
                      [0.8,7,10],
                      [1.3,10,15],
                      [0.8,15,18],
                      [1.3,18,21],
                      [0.8,21,23],
                      [0.4,23,24]])
        All_Day_Money = 0
        for i in range(len(Elec_Price)):
                All_Day_Money += Elec_Price[i][0] * (Elec_Price[i][2] - Elec_Price[i][1])
        
        Money = 0

        Time_Interval  = End_Time - Start_Time  


        if int(Time_Interval / 24) > 0:
                Money += int(Time_Interval / 24) * All_Day_Money
                End_Time -= (int(Time_Interval / 24) * 24)

        Start_Time = Start_Time % 24
        End_Time = End_Time % 24
        if Start_Time > End_Time:                   
                Money += Functional_Price(End_Time,Start_Time,Elec_Price)              
        elif Start_Time < End_Time: 
                Money += (All_Day_Money - Functional_Price(Start_Time,End_Time,Elec_Price) )  
        return Money

def Functional_Price(End_Time,Start_Time,Elec_Price):
        Money = 0
        for i in range(len(Elec_Price)):  

                if End_Time > int(Elec_Price[i][1]): 
                        if End_Time >= int(Elec_Price[i][2]):
                                Money += Elec_Price[i][0] * (Elec_Price[i][2] - Elec_Price[i][1])
                        else:
                                Money += Elec_Price[i][0] * (End_Time - Elec_Price[i][1])

                if Start_Time < int(Elec_Price[i][2]): # 计算第二段 [开始时间,24]
                        if Start_Time <= int(Elec_Price[i][1]):
                                Money += Elec_Price[i][0] * (Elec_Price[i][2] - Elec_Price[i][1])
                        else:
                                Money += Elec_Price[i][0] * (Elec_Price[i][2] - Start_Time)

        return Money  


def Adaptability_For_Elec_Price(Idv,Map):

        Start_Time,End_Time,Job_List_Time,Job_List_Last_Time = Decoder(Idv,Map)


        Max_Finish_Time = max(Job_List_Last_Time)
        All_Elec_Price = 0 

        for i in range(Map.Machine_Num):
                Temp_End_Time = End_Time[i]
                for j in range(Map.Chromosome_Length):
                        if Temp_End_Time[j] != 0:
                               All_Elec_Price += Get_Price_For_Operation(Start_Time[i][j],End_Time[i][j]) 

        return [Max_Finish_Time, All_Elec_Price]


def Adaptability_For_MLoad_MCLoad(Idv,Map):
        _,_,Job_List_Time,Job_List_Last_Time = Decoder(Idv,Map)
        Machine_Set = Idv.Machine_Chromosome  
        Max_Finish_Time = 0 
        Machine_All_Load = 0.0 
        Critical_Machine_Load = 0.0

        Machine_Using_Time = np.array(np.zeros(Map.Machine_Num,dtype=int)) 

        Max_Finish_Time = max(Job_List_Last_Time)       
        for i in range(Map.Chromosome_Length):
                Machine_Using_Time[Machine_Set[i] - 1] += Job_List_Time[i]

        Machine_All_Load = sum(Machine_Using_Time.tolist())
        Critical_Machine_Load = max(Machine_Using_Time.tolist())
        return [Max_Finish_Time,Critical_Machine_Load,Machine_All_Load]


def Adaptability_For_Makespan_Load_Price(Idv,Map):
        _,_,Job_List_Time,_ = Decoder(Idv,Map)
        Machine_Set = Idv.Machine_Chromosome
        Machine_All_Load = 0.0 

        Temp = Adaptability_For_Elec_Price(Idv,Map)   

        Machine_Using_Time = np.array(np.zeros(Map.Machine_Num,dtype=int))

        for i in range(Map.Chromosome_Length):
                Machine_Using_Time[Machine_Set[i] - 1] += Job_List_Time[i] 

        Machine_All_Load = sum(Machine_Using_Time.tolist())
        Temp.append(Machine_All_Load)
        return Temp






