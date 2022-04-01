# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 21:04:41 2022

@author: pg45515
"""

#
# nodes: 2, max time: 27.000000, max x: 600.00, max y: 600.00
# nominal range: 300.00 link bw: 54000000.00
# pause: 30.00, min speed 1.50 max speed: 4.50

# $node_(14) set X_ 780.0
# $node_(14) set Y_ 228.0
# $node_(14) set Z_ 0.00
# $node_(15) set X_ 816.0
# $node_(15) set Y_ 348.0
# $node_(15) set Z_ 0.00
# $node_(16) set X_ 816.0
# $node_(16) set Y_ 348.0
# $node_(16) set Z_ 0.00
# $node_(17) set X_ 816.0
# $node_(17) set Y_ 348.0
# $node_(17) set Z_ 0.00
# $node_(18) set X_ 816.0
# $node_(18) set Y_ 348.0
# $node_(18) set Z_ 0.00
# $ns_ at 1.00 "$node_(14) setdest 500.0 178.0 25.0"
# $ns_ at 2.00 "$node_(15) setdest 400.0 288.0 15.0"
# $ns_ at 8.00 "$node_(15) setdest 600.0 350.0 10.0"
# $ns_ at 10.00 "$node_(14) setdest 600.0 108.0 10.0"
# $ns_ at 17.00 "$node_(15) setdest 816.0 348.0 20.0"
# $ns_ at 18.00 "$node_(14) setdest 780.0 228.0 25.0"


import numpy as np
import random as rd

max_x = 1500
max_y = 1000

not_allowed = np.array([[440,1100],[200,800]])
loc_x = 0
loc_y = 0
loc_z = 0
dest_x = 0
dest_y = 0
sim_time = 0

for n in range(15,25):
    while(1):
        rd.seed()
        loc_x = rd.randint(0, max_x)
        loc_y = rd.randint(0, max_y)
        dest_x = rd.randint(0, max_x)
        dest_y = rd.randint(0, max_y)
        #sim_time = sim_time + rd.randint(1,4)  
        
        
        if (dest_x != loc_x & dest_y != loc_y):
            if(((not_allowed[0][0] > loc_x) | (loc_x > not_allowed[0][1])) & ((not_allowed[1][0] > loc_y) | (loc_y > not_allowed[1][1]))):
                break
        
        
    print("$node_({}) set X_ {}".format(n, loc_x))
    print("$node_({}) set Y_ {}".format(n,loc_y))
    print("$node_({}) set Z_ {}".format(n,loc_z))
    
for i in range(0,5):    
    for n in range(15,25):
        while(1):
            rd.seed()
            loc_x = rd.randint(0, max_x)
            loc_y = rd.randint(0, max_y)
            dest_x = rd.randint(0, max_x)
            dest_y = rd.randint(0, max_y)  
            vel = rd.randint(10,40)
            
            
            if (dest_x != loc_x & dest_y != loc_y):
                if(((not_allowed[0][0] > loc_x) | (loc_x > not_allowed[0][1])) & ((not_allowed[1][0] > loc_y) | (loc_y > not_allowed[1][1]))):
                    break 
                
        sim_time = sim_time + rd.randint(1,4) 
        print ('$ns_ at {} "$node_({}) setdest {} {} {}"'.format(sim_time, n, dest_x,dest_y,vel))