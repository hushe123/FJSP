import numpy as np
import SetAdp
import Critical
# 种群个体类


class Individual:

    def __init__(self):
        
        self.Machine_Chromosome = []            
        self.Job_Chromosome = []                
        self.Adaptability = []                  
        

    def Update_Chromosome(self, Job_Chromosome, Machine_Chromosome, Map):
        self.Job_Chromosome = np.array(Job_Chromosome)
        self.Machine_Chromosome = np.array(Machine_Chromosome)
        self.Adaptability = SetAdp.Adaptability_For_Makespan_Load_Price(self,Map)

