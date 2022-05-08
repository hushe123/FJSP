import numpy as np
import SetAdp
import matplotlib.pyplot as plt
plt.rc('font', family='Times New Roman')
plt.rc('font', size=16)
plt.rc('font', weight='bold')
from mpl_toolkits.mplot3d import Axes3D
# 07
M = [
        [252,107,154],[25,202,173],[0,254,127],[30,144,254],[254,150,128],
        [244,208,0],[222,156,83],
        [38,157,128],[101,147,74],[38,188,213],
        [254,67,101],[160,238,225],[209,186,116],[190,237,199],[236,173,158],
        [254,205,207],[208,0,128],[248,147,29],[113,150,159],[160,102,211]
    ]
#02
# M = [
#         [252,107,154],[25,202,173],[0,254,127],[30,144,254],[254,150,128],
#         [244,208,0],[222,156,83],
#         [254,67,101],[160,102,211],[38,188,213],
#     ]


# color 都除以254
def Get_Color_RGB():
    Temp = []
    for i in range(len(M)):
        Temp.append((np.array(M[i]) / 254).tolist())
    return Temp

# 按照特定值调整，某些工序小，不好展示，找同机器大的借一点空间
def Adjust(Idv,Map):
    Start_time,End_time,_,_ = SetAdp.Decoder(Idv,Map)
    Start_Time1 = []
    End_Time1 = []
    for i in range(Map.Machine_Num):  # 某台机器
        Temp_Process = []
        for j in range(Map.Chromosome_Length):
            if End_time[i][j]!=0: 
                Temp_Process.append(End_time[i][j]-Start_time[i][j])

        Temp_Start_Time = []
        Temp_End_Time = []
        for m in range(len(Temp_Process)):
            if(Temp_Process[m] < 3.6):
                aaa = 3.6-Temp_Process[m]
                Temp_Process[m] = 3.6
                Temp_Process[Temp_Process.index(max(Temp_Process))] -= aaa       
        
        sign = 0
        for n in range(len(Temp_Process)):
            Temp_Start_Time.append(sign)
            sign += Temp_Process[n]
            Temp_End_Time.append(sign)

        Start_Time1.append(Temp_Start_Time)
        End_Time1.append(Temp_End_Time)
        print(Temp_Process)
    return Start_Time1,End_Time1

# 细调，某些需要的更大
def Adjust_Xi():
    Temp = [
            [4, 4, 13, 4, 13, 5, 4, 6, 4, 6, 13, 4, 4, 6, 12, 7, 13, 6, 4, 4, 4],
            [4, 4, 15, 4, 14, 4, 4, 4, 14, 4, 10, 4, 4, 4, 14, 4, 7, 7, 10, 4],
            [14, 4, 4, 10, 9, 16, 10, 9, 16, 4, 14, 16, 14],
            [18, 5, 5, 18, 18, 5, 5, 18, 18, 18, 5, 5],
            [4.4, 3.6, 3.6, 3.6, 3.6, 4.6, 4.4, 5.4, 3.6, 3.6, 4.4, 4.4, 4.4, 3.6, 5.2, 3.6, 5.4, 3.6, 3.6, 4.4, 3.6, 3.6, 4.6, 4.4, 3.6, 4.4, 4.6, 4.4, 3.6, 3.6, 5, 3.6, 3.6, 4.4]   
    ]
    Start_time = []
    End_time = []
    for m in range(len(Temp)):       
        Temp_Start_Time = []
        Temp_End_Time = [] 
        sign = 0
        for n in range(len(Temp[m])):
            Temp_Start_Time.append(sign)
            sign += Temp[m][n]
            Temp_End_Time.append(sign)

        Start_time.append(Temp_Start_Time)
        End_time.append(Temp_End_Time)
    return Start_time,End_time

# 工序各种信息
def Get_Gatt_Print_Info(Idv,Map):
    Start_time,End_time,_,_ = SetAdp.Decoder(Idv,Map)   # 每台机器全部加工信息 不加工为0
    # Start_time,End_time = Adjust(Idv,Map)             # 每台机器的加工信息 不包含0
    Start,End = Adjust_Xi()                             # 可以细调节，每个工序的宽度
    c_rgb = Get_Color_RGB()                             # 工序颜色

    Operations_Order = (np.array(End_time)).tolist()

    for i in range(Map.Machine_Num):
        for j in range(Map.Chromosome_Length):
            if End_time[i][j]!=0:       # 此机器上有个工序 找到他的工序号
                Sign = 1
                for m in range(j):      # Sign 即为工序号
                    if Idv.Job_Chromosome[m] == Idv.Job_Chromosome[j]:
                        Sign += 1
                Operations_Order[i][j] = Sign
                        
    return Start_time,End_time,Start,End,c_rgb,Operations_Order


# 画甘特图
def Draw_Gatt(Idv,Map):
    plt.figure(figsize=(22,8)) 
    # mk07
    _,End_time,Start,End,c_rgb,Operations_Order = Get_Gatt_Print_Info(Idv,Map)       
    for i in range(Map.Machine_Num-1):
        sign = 0       
        for j in range(Map.Chromosome_Length):
            if End_time[i][j]!=0:
                plt.barh(i,width=End[i][sign]-Start[i][sign],left=Start[i][sign],color=c_rgb[Idv.Job_Chromosome[j]-1],edgecolor='white')
                # plt.barh(i,width=End[i][sign]-Start[i][sign],left=Start[i][sign],color='white',edgecolor='black')           
                value = str(Idv.Job_Chromosome[j]) + "-" + str(Operations_Order[i][j]) 
                if Idv.Job_Chromosome[j] > 9 :          
                    plt.text(x=Start[i][sign] -1.8  + (End[i][sign]-Start[i][sign])/2,y=i-0.06,s=value)            
                else:
                    plt.text(x=Start[i][sign] -1.2  + (End[i][sign]-Start[i][sign])/2,y=i-0.06,s=value)
                sign += 1



    plt.barh(5,width=20,left=0,color='black',edgecolor='white')

    # mk02
    # Start,End,_,_,c_rgb,Operations_Order = Get_Gatt_Print_Info(Idv,Map)  
    # for i in range(Map.Machine_Num):
    #     for j in range(Map.Chromosome_Length):
    #         if End[i][j]!=0:
    #             # plt.barh(i,width=End[i][j]-Start[i][j],left=Start[i][j],color=c_rgb[Idv.Job_Chromosome[j]-1],edgecolor='white')
    #             plt.barh(i,width=End[i][j]-Start[i][j],left=Start[i][j],color='white',edgecolor='black')           
    #             value = str(Idv.Job_Chromosome[j]) + "-" + str(Operations_Order[i][j]) 
    #             if Idv.Job_Chromosome[j] > 9 :          
    #                 plt.text(x=Start[i][j] -0.35  + (End[i][j]-Start[i][j])/2,y=i-0.06,s=value)            
    #             else:
    #                 plt.text(x=Start[i][j] -0.25  + (End[i][j]-Start[i][j])/2,y=i-0.06,s=value)


    plt.xlabel("Time")
    plt.ylabel("Machine")
    plt.xticks(np.arange(0,150,10))
    plt.yticks(np.arange(i + 1), np.arange(1, i + 2))
    # plt.savefig('MK02_gante.pdf')
    plt.show()



# 绘制每代种群个体图
def Draw3D(Population):
    First_Parato = Population.Nodominate_Ship[0]
    ax = plt.axes(projection='3d')
    x_data = []
    y_data = []
    z_data = []
    x_first_data = []
    y_first_data = []
    z_first_data = []
    for i in range(Population.Pop_Size):
        x = Population.Population_Member[i].Adaptability[0]
        y = Population.Population_Member[i].Adaptability[1]
        z = Population.Population_Member[i].Adaptability[2]
        if i not in First_Parato:
            x_data.append(x)
            y_data.append(y)
            z_data.append(z)
        else:
            x_first_data.append(x)
            y_first_data.append(y)
            z_first_data.append(z)
    ax.set_xlabel('Finish Time', fontsize=15)
    ax.set_ylabel('Machine Load', fontsize=15)
    ax.set_zlabel('Energy Consume', fontsize=15)
    plt.title('FJSP')

    ax.scatter3D(x_data, y_data,z_data, c='black', s=5)
    ax.scatter3D(x_first_data, y_first_data,z_first_data, c='red', s=5)
    plt.show()



# 对比图
def Draw_Compare(Population1,Population2):
    First_Parato1 = Population1.Nodominate_Ship[0]
    First_Parato2 = Population2.Nodominate_Ship[0]
    ax = plt.axes(projection='3d')
    x1_data = []
    y1_data = []
    z1_data = []
    x2_data = []
    y2_data = []
    z2_data = []
    for i in range(Population1.Pop_Size):
        x = Population1.Population_Member[i].Adaptability[0]
        y = Population1.Population_Member[i].Adaptability[1]
        z = Population1.Population_Member[i].Adaptability[2]
        if i in First_Parato1:
            x1_data.append(x)
            y1_data.append(y)
            z1_data.append(z)

    for i in range(Population2.Pop_Size):
        x = Population2.Population_Member[i].Adaptability[0]
        y = Population2.Population_Member[i].Adaptability[1]
        z = Population2.Population_Member[i].Adaptability[2]
        if i in First_Parato2:
            x2_data.append(x)
            y2_data.append(y)
            z2_data.append(z)



    ax.set_xlabel('Finish Time', fontsize=15)
    ax.set_ylabel('Machine Load', fontsize=15)
    ax.set_zlabel('Energy Consume', fontsize=15)
    plt.title('FJSP')

    ax.scatter3D(x1_data, y1_data,z1_data, c='black', s=5)
    ax.scatter3D(x2_data, y2_data,z2_data, c='red', s=5)
    plt.show()



