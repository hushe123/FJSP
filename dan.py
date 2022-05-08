from Population import *
import Critical
import copy
import math

MAX_Iteration = 500


def Attention(Member):
    Temp_Index = [0] * len(Member.Neighbor_Node)
    Temp_Simi = []
    for i in Member.Neighbor_Node:
        Temp_Simi.append(i[1])
    
    Temp_Simi.sort()
    for i in range(len(Member.Neighbor_Node)):
        index =  Temp_Simi.index(Member.Neighbor_Node[i][1])
        while Temp_Index[index] != 0:
            index += 1
        Temp_Index[index] = Member.Neighbor_Node[i][0]

    return Temp_Index    


def Show_Info(Pop,gen):

    Cluster_Member = SetEdge.Get_Cluster(Pop)

    Temp = []
    for i in range(Pop.Pop_Size):
        Temp.append(Pop.Population_Member[i].Adaptability[0])

    print("======================The Parato Solution Of %d Generation========================" % (gen+1))

    Cluster_Len = []
    Excet_Member = []
    Excet_Job = []
    Excet_Machine = []
    Temp3 = []
    for i in range(len(Cluster_Member)):
        Temp1 = []
        Temp5 = []
        Temp6 = []
        Temp2 = Cluster_Member[i]
        Cluster_Len.append(len(Temp2))
        B = []
        
        for j in range(len(Temp2)):
            A = []
            B.append(Pop.Population_Member[Temp2[j]].Adaptability[0])
            A.append(Pop.Population_Member[Temp2[j]].Job_Chromosome.tolist())
            A.append(Pop.Population_Member[Temp2[j]].Machine_Chromosome.tolist())
            if A not in Temp1:
                Temp1.append(A)
            if  Pop.Population_Member[Temp2[j]].Job_Chromosome.tolist() not in Temp5:
                Temp5.append(Pop.Population_Member[Temp2[j]].Job_Chromosome.tolist())
            if  Pop.Population_Member[Temp2[j]].Machine_Chromosome.tolist() not in Temp6:
                Temp6.append(Pop.Population_Member[Temp2[j]].Machine_Chromosome.tolist())               
        Temp3.append(B)
        Excet_Member.append(len(Temp1))
        Excet_Job.append(len(Temp5))
        Excet_Machine.append(len(Temp6))

    print(min(Temp))
    print(Temp)
    Index = Temp.index(min(Temp))
    a = Pop.Population_Member[Index]
    x = a.Adaptability[0]
    y = a.Adaptability[1]
    z = a.Adaptability[2]
    print("%s %s %d %s %d " % (
            a.Job_Chromosome.tolist(),
            a.Machine_Chromosome.tolist(),
            x, y, z))
    print()

    print(" %d Cluster"%(len(Cluster_Member)),end = ' ')
    for i in range(len(Cluster_Len)):
        print("  [[ %d / %d ]/[ %d ] [ %d ]]  "%(Excet_Member[i],Cluster_Len[i],Excet_Job[i],Excet_Machine[i]),end = ' ')
    print()




def Evlo_Detail(Copy_Pop,Pop,Select_Member):
    print("UpperNetwork:",end=' ')
    for i in Select_Member:
        print("[%d|%d->%d]"%(i,Copy_Pop.Population_Member[i].Adaptability[0],Pop.Population_Member[i].Adaptability[0]),end=' ')
    print()
    print()

    All_Better_Rate = 0
    All_Lower_Rate = 0
    All_Stagger_Rate = 0
    for i in range(Pop.Pop_Size):
        if Pop.Population_Member[i].Adaptability[0] < Copy_Pop.Population_Member[i].Adaptability[0]:
            All_Better_Rate += 1
        elif Pop.Population_Member[i].Adaptability[0] > Copy_Pop.Population_Member[i].Adaptability[0]:
            All_Lower_Rate += 1
        else:
            All_Stagger_Rate += 1
    All_Better_Rate = All_Better_Rate / Pop.Pop_Size
    All_Lower_Rate = All_Lower_Rate / Pop.Pop_Size
    All_Stagger_Rate = All_Stagger_Rate / Pop.Pop_Size
    print("Better_Rate[%f] Lower_Rate[%f] Stagger_Rate[%f]"%(All_Better_Rate,All_Lower_Rate,All_Stagger_Rate))
    print()
    All_Strct_Rate = 0
    for i in range(Pop.Pop_Size):
        if ((Pop.Population_Member[i].Job_Chromosome.tolist() == Copy_Pop.Population_Member[i].Job_Chromosome.tolist()) 
            and (Pop.Population_Member[i].Machine_Chromosome.tolist() == Copy_Pop.Population_Member[i].Machine_Chromosome.tolist())):
            All_Strct_Rate += 1    
    All_Strct_Rate = All_Strct_Rate / Pop.Pop_Size
    print("Struct_Stagger_Rate[%f]"%(All_Strct_Rate))
    print()

    Cluster_Member = SetEdge.Get_Cluster(Pop)
    for i in range(len(Cluster_Member)):
        Cluster = Cluster_Member[i]
        Cluster_Better_Rate = 0
        Cluster_Lower_Rate = 0
        Cluster_Stagger_Rate = 0
        ALL = []
        ALL_b = []
        if len(Cluster) != 0:
            for j in Cluster:
                if Pop.Population_Member[j].Adaptability[0] < Copy_Pop.Population_Member[j].Adaptability[0]:
                    Cluster_Better_Rate += 1
                elif Pop.Population_Member[j].Adaptability[0] > Copy_Pop.Population_Member[j].Adaptability[0]:
                    Cluster_Lower_Rate += 1
                else:
                    Cluster_Stagger_Rate += 1

                Temp1 = []
                Temp1.append(Copy_Pop.Population_Member[j].Job_Chromosome.tolist())
                Temp1.append(Copy_Pop.Population_Member[j].Machine_Chromosome.tolist())
                if Temp1 not in ALL_b:
                    ALL_b.append(Temp1)

                Temp = []
                Temp.append(Pop.Population_Member[j].Job_Chromosome.tolist())
                Temp.append(Pop.Population_Member[j].Machine_Chromosome.tolist())
                if Temp not in ALL:
                    ALL.append(Temp)


            Cluster_Better_Rate = Cluster_Better_Rate / len(Cluster)
            Cluster_Lower_Rate = Cluster_Lower_Rate / len(Cluster)
            Cluster_Stagger_Rate = Cluster_Stagger_Rate / len(Cluster)
            print("%d cluster:Cluster_Better[%f] Cluster_Lower[%f] Cluster_Stagger[%f] Diversity-B[%d/%d] Diversity-F[%d/%d]"%
                (i,Cluster_Better_Rate,Cluster_Lower_Rate,Cluster_Stagger_Rate,len(ALL_b),len(Cluster),len(ALL),len(Cluster)))

    print()
    for i in range(len(Cluster_Member)):
        Cluster = Cluster_Member[i]
        if len(Cluster) != 0:
            for j in Cluster:
                print("[%d|%d->%d]"%(j,Copy_Pop.Population_Member[j].Adaptability[0],Pop.Population_Member[j].Adaptability[0]),end=' ')
            print()
            print()

    ALL = []
    ALL_b = []
    for i in range(Pop.Pop_Size):
        Temp = []
        Temp.append(Pop.Population_Member[i].Job_Chromosome.tolist())
        Temp.append(Pop.Population_Member[i].Machine_Chromosome.tolist())
        if Temp not in ALL:
            ALL.append(Temp)

        Temp1 = []
        Temp1.append(Copy_Pop.Population_Member[i].Job_Chromosome.tolist())
        Temp1.append(Copy_Pop.Population_Member[i].Machine_Chromosome.tolist())
        if Temp1 not in ALL_b:
            ALL_b.append(Temp1)
    print()
    print("Pop_diversity:[%f|%d/%d]"%(len(ALL)/Pop.Pop_Size,len(ALL),Pop.Pop_Size))
    print("After_Pop_diversity:[%f|%d/%d]"%(len(ALL_b)/Pop.Pop_Size,len(ALL_b),Pop.Pop_Size))



def Precise_Neighbour_Search(Idv,Machine_Process_Map,Machine_Cost):
    Job =Idv.Job_Chromosome.tolist()
    Job = np.array(Job)
    Mach = Idv.Machine_Chromosome.tolist()
    Mach = np.array(Mach)                            
    Temp_Idv = Individual()
    Temp_Idv.Init_Next( Job, Mach,Machine_Process_Map, Machine_Cost)
    Critical.Move_Ciritical_To_OtherMachine(Machine_Process_Map,Machine_Cost,
            Temp_Idv,len(Temp_Idv.Job_Chromosome),
            len(Machine_Process_Map),len(Machine_Process_Map[0][0]))

    if Temp_Idv.Adaptability[0] <= Idv.Adaptability[0]:
        Idv.Init_Next(Temp_Idv.Job_Chromosome, Temp_Idv.Machine_Chromosome,
                        Machine_Process_Map, Machine_Cost)  
        return 1
    else:   
        Critical.Move_Ciritical_To_SameMachine(Machine_Process_Map,Machine_Cost,
                Temp_Idv,len(Temp_Idv.Job_Chromosome),
                len(Machine_Process_Map),len(Machine_Process_Map[0][0])) 
        if Temp_Idv.Adaptability[0] <= Idv.Adaptability[0]:
            Idv.Init_Next(Temp_Idv.Job_Chromosome, Temp_Idv.Machine_Chromosome,
                            Machine_Process_Map, Machine_Cost)                   
            return 1
    return 0



def Run():
    Pop = Population()
    Pop.Creat_Population()
    Machine_List = Pop.Get_Machine_Set()
    gen = 0

    Evalue_Times = 100
    while gen < MAX_Iteration:
        
        Population_Pub = []
        for i in range(Pop.Pop_Size):
            Population_Pub.append(Pop.Population_Member[i])
        Pop.Set_Population_Cluster()
        SetEdge.Set_Local_Edge(Pop)
        Show_Info(Pop,gen)
        Select_Member,Abandon_Member = SetEdge.Set_Upper_Network(Pop)

        for i in range(Pop.Pop_Size):
            if i not in Select_Member:
                Random = random.uniform(0,1)
                if Random <= 0.1:
                    Temp = Pop.Population_Member[i].Adaptability[0]
                    GA_Util.Variation_Neighbour(Pop.Population_Member[i],Pop.Machine_Process_Map,Pop.Machine_Cost)
                    Critical.Change_Critical_Order(Pop.Population_Member[i],Pop.Machine_Process_Map, Pop.Machine_Cost)
                    Critical.Change_Critical_Machine(Pop.Population_Member[i],Pop.Machine_Process_Map, Pop.Machine_Cost)

        for i in range(len(Select_Member)):
            if Select_Member[i] == -1:
                continue
            for j in range(len(Select_Member)):
                if Select_Member[j] == -1:
                    continue
                if i != j:
                    idv_1,idv_2 = GA_Util.Cross_Population_Pox1(
                        Pop.Population_Member[Select_Member[i]],
                        Pop.Population_Member[Select_Member[j]],Machine_List,
                        Pop.Machine_Process_Map,Pop.Machine_Cost,2)
                    Evalue_Times += 2
                    Population_Pub.append(idv_1)
                    Population_Pub.append(idv_2)

                    Flag = [-1] * 2     
                    if idv_1.Adaptability[0] < Pop.Population_Member[Select_Member[i]].Adaptability[0]:
                        Flag[0] = 1
                    elif idv_1.Adaptability[0] == Pop.Population_Member[Select_Member[i]].Adaptability[0]:
                        Flag[0] = 0

                    if idv_2.Adaptability[0] < Pop.Population_Member[Select_Member[i]].Adaptability[0]:
                        Flag[1] = 1
                    elif idv_2.Adaptability[0] == Pop.Population_Member[Select_Member[i]].Adaptability[0]:
                        Flag[1] = 0
                    

                    if 1 in Flag:
                        Choose_Index = Flag.index(1)
                        Choose_Index1 = len(Flag) - Choose_Index - 1
                        if Choose_Index == 0:
                            Pop.Population_Member[Select_Member[i]].Init_Next(
                                                idv_1.Job_Chromosome, idv_1.Machine_Chromosome,
                                                Pop.Machine_Process_Map, Pop.Machine_Cost)    
                            if Flag[Choose_Index1] != -1:
                                Pop.Population_Member[Abandon_Member[i]].Init_Next(
                                                    idv_2.Job_Chromosome, idv_2.Machine_Chromosome,
                                                    Pop.Machine_Process_Map, Pop.Machine_Cost)
                            else:
                                Precise_Neighbour_Search(Pop.Population_Member[Abandon_Member[i]],
                                                Pop.Machine_Process_Map,Pop.Machine_Cost)                                                               
                            break
                        else:
                            Pop.Population_Member[Select_Member[i]].Init_Next(
                                                idv_2.Job_Chromosome, idv_1.Machine_Chromosome,
                                                Pop.Machine_Process_Map, Pop.Machine_Cost)                                 
                            if Flag[Choose_Index1] != -1:
                                Pop.Population_Member[Abandon_Member[i]].Init_Next(
                                                    idv_2.Job_Chromosome, idv_2.Machine_Chromosome,
                                                    Pop.Machine_Process_Map, Pop.Machine_Cost) 
                            else:
                                Precise_Neighbour_Search(Pop.Population_Member[Abandon_Member[i]],
                                                Pop.Machine_Process_Map,Pop.Machine_Cost)                                                   
                            break
                    else:
                        if 0 in Flag:
                            Choose_Index = Flag.index(0)
                            if Choose_Index == 0:
                                Pop.Population_Member[Abandon_Member[i]].Init_Next(
                                                    idv_1.Job_Chromosome, idv_2.Machine_Chromosome,
                                                    Pop.Machine_Process_Map, Pop.Machine_Cost)                                          
                            else:
                                Pop.Population_Member[Abandon_Member[i]].Init_Next(
                                                    idv_2.Job_Chromosome, idv_2.Machine_Chromosome,
                                                    Pop.Machine_Process_Map, Pop.Machine_Cost)   
                            break                                                         
                        else:   
                            Precise_Neighbour_Search(Pop.Population_Member[Abandon_Member[i]],
                                                Pop.Machine_Process_Map,Pop.Machine_Cost)  
                            break                                     

        for i in range(Pop.Pop_Size):
            if i not in Select_Member:
                Flag = 0
                if len(Pop.Population_Member[i].Neighbor_Node ) != 0:
                    Attention_Index = Attention(Pop.Population_Member[i])                   
                    if len(Attention_Index) > 1:
                        jj = np.random.randint(0,len(Attention_Index)-1)
                        j = Attention_Index[jj]
                    else:
                        j = Attention_Index[0]
                    idv1,idv2 = GA_Util.Cross_Population_Pox1(Pop.Population_Member[i],Pop.Population_Member[j],
                    Machine_List,Pop.Machine_Process_Map,Pop.Machine_Cost,2)
                    Population_Pub.append(idv1)
                    Population_Pub.append(idv2)

                    if idv1.Adaptability[0] < Pop.Population_Member[i].Adaptability[0]:
                        Pop.Population_Member[i].Init_Next(
                                                idv1.Job_Chromosome, idv1.Machine_Chromosome,
                                                Pop.Machine_Process_Map, Pop.Machine_Cost)                                                  

                    if idv2.Adaptability[0] < Pop.Population_Member[i].Adaptability[0]:
                        Pop.Population_Member[i].Init_Next(
                                                idv2.Job_Chromosome, idv2.Machine_Chromosome,
                                                Pop.Machine_Process_Map, Pop.Machine_Cost)

                if Flag == 0:  
                    aaa = Precise_Neighbour_Search(Pop.Population_Member[i],
                                                Pop.Machine_Process_Map,Pop.Machine_Cost)  
                    Sum_Critical_Excet += aaa

    

if __name__ == "__main__":
    Run()