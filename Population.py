# 种群类
import Fast_Sort

class Population:

    def __init__(self):
            
        self.Pop_Size = 200               
        self.Population_Member = []         
        self.Nodominate_Ship = []            
        self.Unduplicated_Pareto_Num = 0     
        self.Unduplicated_Pareto = []       
        self.Unduplicated_Pareto_Obj = []    
        self.Unduplicated_Pop_Num = 0       
        self.Unduplicated_Pop = []          
        self.Crowding_Distance = []           

    def Update_Pop(self,Pop_Member):
        self.Population_Member = []        
        for i in range(self.Pop_Size):
            self.Population_Member.append(Pop_Member[i])


    def Determine_Nodominate_Ship(self):
        self.Nodominate_Ship = Fast_Sort.Fast_Nodominate_Sort(self.Population_Member)
        self.Determine_Pareto_Info()    


    def Determine_Pareto_Info(self):
        Temp_Pub = []
        Pareto = self.Nodominate_Ship[0]
        Unduplicated_Pareto = []  
        for i in range(len(Pareto)):
            Temp = []
            Temp.append(self.Population_Member[Pareto[i]].Job_Chromosome.tolist())
            Temp.append(self.Population_Member[Pareto[i]].Machine_Chromosome.tolist())
            if Temp not in Temp_Pub:
                Temp_Pub.append(Temp)
                Unduplicated_Pareto.append(Pareto[i])
        # 目标值
        Unduplicated_Pareto_Obj = []
        for i in Unduplicated_Pareto:
            Unduplicated_Pareto_Obj.append(self.Population_Member[i].Adaptability)

        self.Unduplicated_Pareto = Unduplicated_Pareto
        self.Unduplicated_Pareto_Num = len(Unduplicated_Pareto)
        self.Unduplicated_Pareto_Obj = Unduplicated_Pareto_Obj





