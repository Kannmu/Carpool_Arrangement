import numpy as np
import random
from sklearn.cluster import AffinityPropagation
# from sklearn.cluster import Birch
import matplotlib.pyplot as plt
import math

#TEST_DATA_PAEAMS
Order_Number = 101
Car_Number = 50
Order_Distance = 10
Car_Distance = 20
Reversed_Rate = 0.3

MAX_ORDER_PEOPLE = 20
MAX_COORDINATE_RANGE = 100
MAX_NUMBER_OF_SEATS = 20
#

Orders = []
# Order Format Every Row:[int:Bind_Car_ID, bool:Is_Grab, int:Number_Of_People, list:coordinate, float:ArriveTime, int:Order_ID]
Cars = []
# Car Format Every Row:[int:Car_ID, list:coordinate, int:Number_Of_Seat]
Params = []
# Params Format:[float:Order_Distance, float:Car_Distance, float:reverse_rate]
Results = [[0] for i in range(Car_Number)]
# 第一维Car_ID按顺序排列，第二维是每个Car分配的订单号

# print (np.array(Results_List).shape)

def Get_Info(): #Generate Test Data, Swap This Funcation To Real Data Latter

    # Create Test Fake Data
    Order_ID = list(range(1,Order_Number))
    
    
    Bind_Car_ID = list(range(Car_Number))
    Bind_Car_ID_Zero = [0]*(len(Order_ID)-Car_Number)
    Bind_Car_ID.extend(Bind_Car_ID_Zero)
    random.shuffle(Bind_Car_ID)
    # Bind_Car_ID = Bind_Car_ID[:100]
    # print(Bind_Car_ID)

    Is_Grab = [] # 0:Is_Grabed, 1:System_Distribute
    for i in Bind_Car_ID:
        if(i == 0):
            Is_Grab.append(0)
        else:
            Is_Grab.append(1)
    # print (Is_Grab)

    People = []
    for i in range(len(Order_ID)):
        People.append(random.randint(1,MAX_ORDER_PEOPLE))
    # print(People)s

    Coordinate_Order = (MAX_COORDINATE_RANGE*np.random.rand(len(Order_ID),2)).tolist()
    # print(Coordinate)

    ArriveTime = (24*np.random.rand(len(Order_ID),1)).reshape(-1).tolist()
    # print(ArriveTime)
    Orders = []
    Orders.append(Bind_Car_ID)
    Orders.append(Is_Grab)
    Orders.append(People)
    Orders.append(Coordinate_Order)
    Orders.append(ArriveTime)
    Orders.append(Order_ID)

    Orders = np.array(Orders,dtype=object).T
    # print(Orders)

    Car_ID = list(range(Car_Number))
    random.shuffle(Car_ID)
    # print(Car_ID)

    Coordinate_Car = (MAX_COORDINATE_RANGE*np.random.rand(len(Car_ID),2)).tolist()
    # print(len(Coordinate_Car))

    Number_Of_Seat = []
    for i in range(len(Car_ID)):
        Number_Of_Seat.append(np.random.randint(MAX_NUMBER_OF_SEATS))
    # print(Number_Of_Seat)

    Cars = []
    Cars.append(Car_ID)
    Cars.append(Coordinate_Car)
    Cars.append(Number_Of_Seat)
    Cars = np.array(Cars,dtype=object).T
    # print(Cars)

    Params = [Order_Distance,Car_Distance,Reversed_Rate]
    
    return Orders,Cars,Params
    # Return Fake Test Data

def Get_Distance(P0,P1):
    # print(P0,'\n\n',P1)
    Distance = math.sqrt((P1[0]-P0[0])**2 + (P1[1]-P0[1])**2)
    print(Distance)
    return Distance

def Arrangement(Orders,Cars,Params):
    
    # First Divide
    for i in Cars:
        for j in Orders:
            if (j[0] == i[0] and i[0] != 0):
                Results[i[0]].append(j[5])
    for i in Results:
        i.remove(0)
    Results.pop(0)
    #

    Total_People = sum(Orders[:,2])
    Total_Seats = sum(Cars[:,2])
    Reversed_Seat = int(sum([i*Params[2] for i in Cars[:,2]]))+1
    Available_Seats = Total_Seats - Reversed_Seat
    # print(Available_Seats)

    X = Orders[:,3].tolist()
    plt.subplot(1, 2, 1)
    plt.scatter([i[0] for i in X], [i[1] for i in X],c = 'blue')
    AP = AffinityPropagation(max_iter=300)
    AP.fit(X)
    Centers = AP.cluster_centers_indices_.tolist()
    Labels = AP.labels_
    Clusters = [[0] for i in range(len(Centers))]

    # print(AP.cluster_centers_indices_)
    # print(AP.labels_)
    
    for i in range(len(Centers)):
        for j in range(len(Labels)):
            if (i == Labels[j]):
                Clusters[i].append(j)
    for i in Clusters:
        i.pop(0)
    # print(Clusters)
    # print(Orders[Labels[1],3])
    Delete_List = []
    for i in Clusters:
        for j in i:
            if(Get_Distance(Orders[Centers[Clusters.index(i)],3], Orders[j,3]) > Order_Distance):
                Delete_List.append(j)
                # Orders = np.delete(Orders,[j],axis=0)
                # print(len(Delete_List))
            # print(i)
    print(Delete_List)
    Orders = np.delete(Orders,Delete_List,axis = 0)
    Labels = (np.array(Labels))
    Labels = np.delete(Labels,Delete_List)
    # print(Clusters)

    X = Orders[:,3].tolist()
    plt.subplot(1, 2, 2)
    plt.scatter([i[0] for i in X], [i[1] for i in X], c=Labels)
    
    
    plt.show()

if __name__ == '__main__':
    Orders,Cars,Params = Get_Info()
    Arrangement(Orders,Cars,Params)
