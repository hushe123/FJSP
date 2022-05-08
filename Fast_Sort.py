import Evaluate

def Is_Dominate(Idv1, Idv2):
    Objective_Dim = len(Idv1.Adaptability)
    Objective1 = []
    Objective2 = []

    for i in range(Objective_Dim):
        Objective1.append(Idv1.Adaptability[i])
        Objective2.append(Idv2.Adaptability[i])

    Flag = [9999] * Objective_Dim

    for i in range(Objective_Dim):
        if Objective1[i] < Objective2[i]:
            Flag[i] = -1    # 目标值小
        elif Objective1[i] == Objective2[i]:
            Flag[i] = 0     # 目标值相等

    return True if sum(Flag) < 0  else False

def Get_First_Dominate(Population_Pub):
    Pop_Size = len(Population_Pub)       
    Np = [0] * Pop_Size                 
    Sp = [[] for _ in range(Pop_Size)]  
    First_Pareto = []                   
    for i in range(Pop_Size):
        for j in range(i+1,Pop_Size):              
                if Is_Dominate(Population_Pub[i], Population_Pub[j]):   
                    Np[j] += 1      
                    Sp[i].append(j)                 
                elif Is_Dominate(Population_Pub[j], Population_Pub[i]):  
                    Np[i] += 1       
                    Sp[j].append(i)  
        if Np[i] == 0:
            First_Pareto.append(i)
    return Np,Sp,First_Pareto               

def Fast_Nodominate_Sort(Population_Member):
    Np,Sp,First_Parato = Get_First_Dominate(Population_Member)
    Nodominate_Sort = []                      

    while(len(First_Parato) != 0):
        Nodominate_Sort.append(First_Parato)  
        Temp = []                            
        for j in First_Parato:
            p = Sp[j]                          
            for q in p:                      
                Np[q] -= 1   
                if Np[q] == 0:               
                    Temp.append(q)
        First_Parato = Temp
    return Nodominate_Sort


def Modified_Crowding_Distance(Pareto,Population_Member): 
    Pareto_Size = len(Pareto)
    Pop_Size = len(Population_Member)                 
    Di = []    
    for m in range(Pareto_Size):
        OS_Value = 1
        MS_Value = 1
        for n in range(Pop_Size):
            if Pareto[m] != n:
                if Population_Member[Pareto[m]].Job_Chromosome.tolist() == Population_Member[n].Job_Chromosome.tolist():
                    OS_Value += 1
                if Population_Member[Pareto[m]].Machine_Chromosome.tolist() == Population_Member[n].Machine_Chromosome.tolist():
                    MS_Value += 1

        di =  (Pop_Size - (OS_Value + MS_Value)/2) / Pop_Size
        Di.append(di)
    return Di    

def Crowd_Distance(Population_Member,Pareto):
    Pareto_Num = len(Pareto)    # Pareto 个体数量
    Object_Value = []           
    for m in Pareto:
        Temp = []
        for n in range(len(Population_Member[0].Adaptability)):
            Temp.append(Population_Member[m].Adaptability[n])
        Object_Value.append(Temp)   

    Normal_Population_Objection = Evaluate.Normal_Objective(Object_Value)    
    for i in range(Pareto_Num):
        Normal_Population_Objection[i].append(Pareto[i])
    Distance = []
    Normal_Population_Objection = sorted(Normal_Population_Objection)

    for i in range(Pareto_Num):
        Temp1 = []
        if Normal_Population_Objection[i][0] == 0 and Normal_Population_Objection[i][1] == 1 or Normal_Population_Objection[i][0] == 1 and Normal_Population_Objection[i][1] == 0:
            Temp1.append(9999)                
        else:
            distance_value = 0
            distance_value = (Normal_Population_Objection[i+1][0]-Normal_Population_Objection[i-1][0]) * (Normal_Population_Objection[i-1][1]-Normal_Population_Objection[i+1][1])
            Temp1.append(distance_value)
        Temp1.append(Normal_Population_Objection[i][2])
        Distance.append(Temp1)

    Distance = sorted(Distance)
    return Distance




