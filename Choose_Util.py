import random
  
def  Get_Min_Index(Select):
    if len(Select) <= 1:    
        return 0    

    Min = min(Select)   
    Special_Selected = []   
    for i in range(len(Select)):
        if Select[i] == Min:
            Special_Selected.append(i)
    Index = random.choice(Special_Selected)
    return Index

  
def  Get_Max_Index(Select):
    if len(Select) <= 1:    
        return 0    

    Max = max(Select)   
    Special_Selected = []  
    for i in range(len(Select)):
        if Select[i] == Max:
            Special_Selected.append(i)
    Index = random.choice(Special_Selected)
    return Index
  
def Get_Min_Info_Without(Select):
    Index = Get_Min_Index(Select)
    return Select[Index],Index
  
def Get_Max_Info_Without(Select):
    Index = Get_Max_Index(Select)
    return Select[Index],Index
  
def Get_Mid_Info_Without(Select):
    pass


def Get_Min_Info_With(Select,Select_To_Return):
    Min,Index = Get_Min_Info_Without(Select)
    return Min,Index,Select_To_Return[Index]


def Get_Max_Info_With(Select,Select_To_Return):
    Max,Index = Get_Max_Info_Without(Select)
    return Max,Index,Select_To_Return[Index]


def Get_Mid_Info_With(Select,Select_To_Return):
    pass