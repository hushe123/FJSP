
import numpy as np
import Data

class Load_Process_Map:

    def __init__(self):

        self.Machine_Process_Map = Data.MK07


        self.Job_Num = 0    
        self.Machine_Num = 0    
        self.Operation_Num = []  
        self.Chromosome_Length = 0  
        self.Operation_Accessible_Machine_Index = []    
        self.Operation_Accessible_Machine_Time = []     
        self.Operation_Min_Machine_Index = []          
        self.Operation_Min_Machine_Time = []            

        self.Get_Info_from_Map()        

    def Update_Map(self,Map):
        self.Machine_Process_Map = Map
        self.Reset()
        self.Get_Info_from_Map()        

    def Reset(self):
        self.Job_Num = 0    
        self.Machine_Num = 0    
        self.Operation_Num = [] 
        self.Chromosome_Length = 0  
        self.Operation_Accessible_Machine_Index = []    
        self.Operation_Accessible_Machine_Time = []     
        self.Operation_Min_Machine_Index = []          
        self.Operation_Min_Machine_Time = []                

    def Get_Info_from_Map(self):
        self.Job_Num = len(self.Machine_Process_Map) 
        self.Machine_Num = len(self.Machine_Process_Map[0][0])  
 
        for i in range(self.Job_Num):
            Temp_Job = self.Machine_Process_Map[i]  

            self.Operation_Num.append(len(Temp_Job)) 

            Temp_Operation_Machine_Index_All = []   
            Temp_Operation_Machine_Time_All = []  

            Temp_Min_Machine_Index_All = []         
            Temp_Min_Machine_Time_All = []          

            for j in range(len(Temp_Job)):
                Temp_Opeartion = Temp_Job[j]        
                Temp_Operation_Machine_Index = []   
                Temp_Operation_Machine_Time = []    

                Temp_Min_Machine_Index = []         
                Temp_Min_Machine_Time = []          

                for m in range(self.Machine_Num):   
                    if(Temp_Opeartion[m] != 9999):
                        Temp_Operation_Machine_Index.append(m)
                        Temp_Operation_Machine_Time.append(Temp_Opeartion[m])

                Min_Value = min(Temp_Operation_Machine_Time)   
                Temp_Min_Machine_Time.append(Min_Value)
                for n in range(len(Temp_Operation_Machine_Time)):
                    if(Temp_Operation_Machine_Time[n] == Min_Value):
                        Temp_Min_Machine_Index.append(Temp_Operation_Machine_Index[n])
                 
                Temp_Operation_Machine_Index_All.append(Temp_Operation_Machine_Index)
                Temp_Operation_Machine_Time_All.append(Temp_Operation_Machine_Time)

                Temp_Min_Machine_Index_All.append(Temp_Min_Machine_Index)
                Temp_Min_Machine_Time_All.append(Temp_Min_Machine_Time)

            self.Operation_Accessible_Machine_Index.append(Temp_Operation_Machine_Index_All)
            self.Operation_Accessible_Machine_Time.append(Temp_Operation_Machine_Time_All)
            self.Operation_Min_Machine_Index.append(Temp_Min_Machine_Index_All)
            self.Operation_Min_Machine_Time.append(Temp_Min_Machine_Time_All)

            self.Chromosome_Length = sum(self.Operation_Num)  




