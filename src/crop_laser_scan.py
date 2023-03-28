#!/usr/bin/env python3
import rospy
from sensor_msgs.msg import LaserScan
import numpy as np
from math import pi
import pandas as pd
import jenkspy
from networktables import NetworkTables, NetworkTablesInstance


NetworkTables.initialize("10.0.0.107")

table = NetworkTablesInstance.getDefault().getTable('crop laser scan table')



ANGLE = pi/7 #originally 5 
cropped_pub = None



#def finding_pole(ranges):
        
        #first_calculations = z/y
        #first_calculations * 100
        #if first_calculations >= .30 and first_calculations <= .70:
        #    if first_calculations > .50:
         #       distance_away = -x/2
          #      print("right")
           # elif first_calculations < .50:
            #    print("left")
             #   distance_away = x/2
            #else:
             #   print("Middle")

def callback(msg):
    HALF_ANGLE=ANGLE/2
    index_count = int(HALF_ANGLE//msg.angle_increment)
    ranges = msg.ranges #Collective of all points
    right_ranges = ranges[len(msg.ranges)-index_count:]
    left_ranges = ranges[:index_count]
    res_ranges = np.concatenate((right_ranges, left_ranges), -1)
    res_ranges = res_ranges.tolist()
    #res_ranges = res_rantenate((right_ranges, left_ranges), -1)
    #res_ranges = res_ranges[~np.isnan(res_ranges)]

    for i in res_ranges:
        if i >= 0.9144:
            i = float("nan")
    if cropped_pub:
        msg.ranges = res_ranges
        cropped_pub.publish(msg)
    #finding_pole(res_ranges)
                #if i in right_ranges?
                #move right until i = 0
                #while i != 0:
                #   move.right() send command for robot to move, and will auto stop when i == 0 (position of pole?) 
		
        #This is to get the pole points to pass into getting_calculations
    new_res_ranges = [item for item in res_ranges if not(pd.isnull(item)) == True]
    #print(res_ranges)
    new_new_res_ranges = [*set(new_res_ranges)]
    grouping_ = {
        "Data":new_new_res_ranges
    }
    #print(type(res_ranges))
    #print(type([1.0950000286102295, float('nan'), 1.0950000286102295, 1.1109999418258667, 1.1109999418258667, 1.1109999418258667, 1.1260000467300415, 1.1260000467300415, 1.1260000467300415, 1.1260000467300415, 1.1419999599456787, 1.1419999599456787, 1.1260000467300415, 1.0950000286102295, 1.0640000104904175, 1.0329999923706055, 1.0019999742507935, 0.9869999885559082, 0.9399999976158142, 0.9089999794960022, 0.9089999794960022, 0.925000011920929,1.2350000143051147, 1.25, 1.2660000324249268, 4.372000217437744, 4.309999942779541, 4.294000148773193, 2.430999994277954, 2.384000062942505, 2.36899995803833, 2.384000062942505, 2.4149999618530273, 2.384000062942505, 2.384000062942505, 2.305999994277954, 2.305999994277954, 2.259999990463257, 2.24399995803833, 6.5]))
    df = pd.DataFrame(grouping_)
    df.sort_values(by="Data")
    print(df["Data"])
    labels=["Grouping1", "Grouping2", "Grouping3", "Grouping4", "Grouping5", "Grouping6", "Grouping7", "Grouping8", "Grouping9", "Grouping10"]
    df["grouping"] = pd.qcut(df["Data"], q=len(labels), labels=labels)
    #print(int(float(df["grouping"][0])))
    something = 1
    pole_list = []
    print("Here")
    print(df["Grouping1"])
    for i in df["grouping"]:
        print(len(res_ranges))
        print("Here")
        print(df["grouping"]=="Grouping1")
        #string_numbers = str(something)
        if len(i) <= 7:   
            #new_df_mean = (new_df["Data"].mean())
            #print(new_df_mean)
            #middle_value = (len(new_df)-1)/2
            print("The Winner is " + i + " The mean is, " + i.mean())
            pole_list.append(i)
            break
            
        else:
            print("Grouping1 is greater than 4 floats")
            print(len(i))
            #new_df["Data"] = float("nan")
            #string_numbers=int(string_numbers)+1
            print(i + " Has too many in a grouping")
            something+1
    if len(pole_list) == 0:
        print("No pole found")
        return
    
            


    def getting_calculations():
        print(pole_list)
        x = res_ranges.index(min(pole_list))
        print(x)
        y = len(res_ranges)
        print(y)
        first_calculations = x/y
        first_calculations*100
        if first_calculations > .60:
            #distance_away = -x/2
            table.putString("Move Direction:", "left") #was once right
            print("left")
            print(first_calculations)
        elif first_calculations < .40:
            table.putString("Move Direction:","right") #was once left
            print("right")
            print(first_calculations)
        elif first_calculations > .40 and first_calculations < .60:
            print(first_calculations)
            table.putString("More Direction:", "Middle")
            print("Middle")
        print(len(new_df))
    getting_calculations()
        #return leftright, distance, ideal_distance - distance 
    #if right angle then
#finding_pole()



if __name__ =='__main__':
    try:
        rospy.init_node('crop_laser_scan')

        rospy.Subscriber('/scan', LaserScan, callback)
        cropped_pub = rospy.Publisher('/scan_cropped', LaserScan, queue_size=1)

        rospy.spin()

    except rospy.ROSInterruptException:
        pass

#________________________________________________________________________________
#Jenks Natural Breaks Optimization

