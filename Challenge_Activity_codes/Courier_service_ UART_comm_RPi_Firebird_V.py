# -*- coding: cp1252 -*-
import cv2
import numpy as np
from decimal import *
import math
import time
import RPi.GPIO as GPIO
import package_client
import fipi as pi
package_client.package_server_ip='192.168.10.16'
link_time=2.7
node_time=0.6
back_turn_time=1.5
turn_time=0.4
rev_time=2.65
black_par=100
red_thresh=85
green_thresh=30
blue_thresh=50
black_threshold=102
red_threshold=
blue_threshold=100
green_threshold=

strt1=time.time()

pi.forward()
time.sleep(1)
pi.stop()


global hl,vl
global current_path
global current_node
traffic_signal_nodes=[]
k1=3.2
k2=1.5
pick_ind=0
delivery_ind=0




def delivery_sequence(packages_nodes):
    array=[[[2,1],[2,5],[5,5],[5,1]],[[2,5],[5,5],[5,1],[2,1]],[[5,5],[5,1],[2,1],[2,5]],[[5,1],[2,1],[2,5],[5,5]]]
    k=0
    combinations=[]
    while k<4:
        packagenodes=packages_nodes[:]
        l=0
        comb=[]
        while l<4:
            sequence=[]
            i=0
            while i<4:
                m=50
                j=0
                while j<len(packagenodes):
                    t=(abs(array[k][l][0]-packagenodes[j][0]))+(abs(array[k][l][1]-packagenodes[j][1]))
                    if t<m:
                        m=t
                        pt=packagenodes[j]
                    j=j+1
                i=i+1
                if len(packagenodes)==0:
                    break
                sequence.append(pt)
                packagenodes.remove(pt)
            if len(sequence)==0:
                break
            sequence=sorted(sequence)
            comb.append(sequence)
            l=l+1
        comb=sorted(comb)
        combinations.append(comb)
        k=k+1
    return combinations



############################################################################
############################################################################
def turns(path):                                           #function to find number of turns in a path
    if len(path)<=1:
      return 0
    i=1
    n=0
    if path[0][0]==path[1][0]:
        j=0
    else:
        j=1
    while i<len(path):
        if path[i][j]!=path[i-1][j]:
            n=n+1
            if j==0:
                j=1
            else:
                j=0
        i=i+1
    return n
#################################################################################
#################################################################################
def rearrange(pt,array):                            #arranging array of adjacent nodes with links in ascending order of closeness to the end point
    rearrange=[]
    while 1:
        m=12
        j=0
        while j<len(array):
            t=(abs(pt[0]-array[j][0]))+(abs(pt[1]-array[j][1]))
            if t<m:
                m=t
                pt1=array[j]
            j=j+1
        if array==[]:
            break
        rearrange.append(pt1)
        array.remove(pt1)
    return rearrange
#############################################################################################
#############################################################################################
def traffic_signal_nodes(img):
    h,w,c = img.shape
    img1 = cv2.resize(img,(w/10, h/10), interpolation = cv2.INTER_CUBIC)

    height,width,colour = img1.shape
    h1=height-1
    w1=width-1
    signal_nodes=[] 
    i=0
    while i<7:
        roi=img1[:,((i*(w1/6))):((i*(w1/6))+7),:]
        j=0
        while j<7:
            roi1=roi[((j*(h1/6))):((j*(h1/6))+7),:,:]
            gray = cv2.cvtColor(roi1, cv2.COLOR_BGR2GRAY)
            ret,thresh2 = cv2.threshold(gray,250,255,cv2.THRESH_BINARY)
            contours, hierarchy = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            if len(contours)>0:
                signal_nodes.append([j,i])
            j=j+1
        i=i+1
    return signal_nodes
##############################################################################################
##############################################################################################

def grid_to_arrays(img):
    img = cv2.resize(img,(300,300), interpolation = cv2.INTER_CUBIC) 
    h,w,c = img.shape                                             #identify the height and width of the given image
    imghl=img.copy()                                              #to avoid changes in original image
    img_1=img.copy()
    gray = cv2.cvtColor(imghl,cv2.COLOR_BGR2GRAY)
    ret,thresh2 = cv2.threshold(gray,90,255,cv2.THRESH_BINARY_INV) #convert image to binary form
    ret,thresh3 = cv2.threshold(gray,90,255,cv2.THRESH_BINARY_INV)
    i=0
    while i<7:                                                   #removing vertical links to find horizontal links using draw-image
        cv2.line(thresh2,(int(round(Decimal(i)*Decimal(w)/Decimal(6.24)+Decimal(w)/Decimal(62.4))),0),(int(round(Decimal(i)*Decimal(w)/Decimal(6.24)+Decimal(w)/Decimal(62.4))),h),(0,0,0),w/25)
        i=i+1
    ret,thresh55 = cv2.threshold(thresh2,127,255,cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(thresh2,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img_1,contours,-1,(0,255,0),3)                   #contours to detect horizontal links only
    i=0
    hl=[[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]#initializing horizontal links array
    while i<len(contours):                                      #determination of contour centroids of horizontal links
        area=cv2.contourArea(contours[i])
        if area>(h*w/750):
            M = cv2.moments(contours[i])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cx=cx-(63*w/650)
            m=int(round(Decimal(6)*Decimal(cy)/Decimal(h)))       #calculating indices of links using their centroids
            n=int(round(Decimal(6)*Decimal(cx)/Decimal(w)))
            hl[m][n]=1                                              #assigning 1 to indices of the horizontal link array when link is detected
        i=i+1
    j=0
    while j<7:                                                  #removing horizontal links to find vertical links using draw-image
        cv2.line(thresh3,(0,int(round(Decimal(j)*Decimal(h)/Decimal(6.2)+Decimal(h)/Decimal(62.4)))),(w,int(round(Decimal(j)*Decimal(h)/Decimal(6.24)+Decimal(h)/Decimal(62.4)))),(0,0,0),h/25)
        j=j+1
    ret,thresh56 = cv2.threshold(thresh3,127,255,cv2.THRESH_BINARY_INV) 
    contours, hierarchy = cv2.findContours(thresh3,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(0,255,0),3)                #contours to detect vertical links only
    i=0
    vl=[[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]] #initializing vertical links array
    while i<len(contours):
        area=cv2.contourArea(contours[i])
        if area>(h*w/750):#determination of contour centroids of vertical links
            M = cv2.moments(contours[i])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cy=cy-(63*h/650)
            m=int(round(Decimal(6)*Decimal(cy)/Decimal(h)))       #calculating indices of links using their centroids
            n=int(round(Decimal(6)*Decimal(cx)/Decimal(w)))
            vl[m][n]=1                                              #assigning 1 to indices of the vertical link array when link is detected
        i=i+1
    horizontal_links=hl
    vertical_links=vl   
    return horizontal_links, vertical_links

#####################################################################
## Experiment 2
#####################################################################


#########################################################
#########################################################
def shortest_path(hl,vl,spt,ept,traffic_pts):
    '''
    * Function Name: shortest_path
    * Input: img – Any one of the test images
    * Output: length – length of shortest path
              shortest_path – the shortest path as a list of coordinates of form (x,y)
    * Example Call: l, sp = shortest_path(img)
                    >>> l = length, sp = shortest_path 
    '''
    

    def find_adjecent(pta):                                                     #program to find adjacent nodes of a node
        adj=[[pta[0],pta[1]+1],[pta[0],pta[1]-1],[pta[0]+1,pta[1]],[pta[0]-1,pta[1]]]
        j=0
        adjecent=[]
        while j<4:
            i=0
            n=0
            while i<2:
                if ((adj[j][i]>=0)&(adj[j][i]<=6)):
                    n=n+1                
                i=i+1
            if n==2:
                adjecent.append(adj[j])
            j=j+1
        q=0
        fnladj=[]
        while q<len(adjecent):
            n=0
            for w in path:
                if (w==adjecent[q]):
                    n=n+1    
            if n==0:
                fnladj.append(adjecent[q])
            q=q+1
        q=0
        fnl_adj=[]
        while q<len(fnladj):
            n=0
            for w in traffic_pts:
                if (w==fnladj[q]):
                    n=n+1    
            if n==0:
                fnl_adj.append(fnladj[q])
            q=q+1
        return fnl_adj

    def find_pts_with_link(spt,array):                                          #to find adjacent nodes having links with given node
        i=0
        adjlink=[]
        while i<len(array):
            if spt[0]==array[i][0]:
                if spt[1]<array[i][1]:
                    h=spt[1]
                else:
                    h=array[i][1]
                if hl[spt[0]][h]==1:
                    adjlink.append(array[i])
            else:
                if spt[0]<array[i][0]:
                    v=spt[0]
                else:
                    v=array[i][0]
            
                if vl[v][spt[1]]==1:
                    adjlink.append(array[i])
            i=i+1
        return adjlink

    def find_closest(sp,ep):                            #arranging array of adjacent nodes with links in ascending order of closeness to the end point
        array=find_adjecent(sp)
        adjlink=find_pts_with_link(sp,array)
        closest=[]
        while 1:
            m=50
            j=0
            while j<len(adjlink):
                t=(abs(ep[0]-adjlink[j][0]))+(abs(ep[1]-adjlink[j][1]))
                if t<m:
                    m=t
                    pt1=adjlink[j]
                j=j+1
            if adjlink==[]:
                break
            closest.append(pt1)
            adjlink.remove(pt1)
        return closest

    def turns(path):                                             #function to find number of turns in a path
        i=1
        n=0
        if path[0][0]==path[1][0]:
            j=0
        else:
            j=1
        while i<len(path):
            if path[i][j]!=path[i-1][j]:
                n=n+1
                if j==0:
                    j=1
                else:
                    j=0
            i=i+1
        return n
    def find_path(sp,ep):                                     #function to find shortest path with minimum number of turns    
        if sp==ep:
            return
        closest=find_closest(sp,ep)   
        if len(closest)==0:
            return
        i=0
        while i<len(closest):
           
            tmp=closest[i]
            path.append(tmp)
            if ((len(path)+turns(path))>k):
                path.remove(tmp)
                return
            find_path(tmp,ep)
            if ((path[len(path)-1]!=ep)):       #please see algorithm provided
                path.remove(tmp)
            else:
                break
            i=i+1
        return
    if spt==ept:
        return 1,[spt]
    k=abs(ept[0]-spt[0])+abs(ept[1]-spt[1])#calculating minimum no of steps of path
    path=[spt]    
    while k<15:      
        find_path(spt,ept)
        k=k+1
        if len(path)>1:
            break
    length=len(path)
    
    return length, path


#########################################################################################################################
#########################################################################################################################
def find_PUJ_and_DJ(image):
    h,w,c=image.shape
    img1 = cv2.resize(image,(600,600), interpolation = cv2.INTER_CUBIC)
    H,W,C=img1.shape
    img=img1.copy()
#cv2.imshow('orginal',img)
    color_parameters=[[[0,10,0],[10,255,10]],[[10,10,0],[255,255,10]],[[10,0,10],[255,0,255]],[[0,10,10],[0,130,255]]]
#green blue pink orange
    c_p=0
    company_s=[]
    company_t=[]
    company_c=[]
    null=[]
    while c_p<len(color_parameters):
        param1 =color_parameters[c_p][0]
        param2 =color_parameters[c_p][1]

        lower = np.array(param1)
        upper = np.array(param2)
        mask  = cv2.inRange(img, lower, upper)
        res1   = cv2.bitwise_and(img, img, mask= mask)
 

        gray = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)   
        ret,thresh1 = cv2.threshold(gray,60,255,cv2.THRESH_BINARY)
        contours,hierarchy=cv2.findContours(thresh1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        cv2.drawContours(img1,contours,-1,(0,255,0),3)
        package=[]
        i=0
        package_area=[]
        while i<len(contours):
            area=cv2.contourArea(contours[i])
            if (area>150)&(area<650):
                package_area.append(area)
                package.append(contours[i])
    
            i=i+1

        square=[]
        circle=[]
        triangle=[]
        i=0
        while i<len(package):
            if (package_area[i]>501):                
               square.append(package[i])
            if (package_area[i]>150)&(package_area[i]<375):
                triangle.append(package[i])
            if (package_area[i]>400)&(package_area[i]<500):
                circle.append(package[i])
            i=i+1
    
        company_s.append(square)
        company_t.append(triangle)
        company_c.append(circle)
        c_p=c_p+1

    company=[]
    company.append(company_s)
    company.append(company_t)
    company.append(company_c)


    pu_list=[]
    i=0
    while i<3:
        j=0
        while j<4:
       
            if len(company[i][j])!=0:
                #print company[i][j]
                a=company[i][j][1][0][0][0]
                x=int(math.ceil((Decimal(a)/Decimal(100))))
                pu_list.append([1,x])
            
                j=j+1
            else:
                pu_list.append(null)
                j=j+1
        i=i+1
    #pick up junctions
    i=0
    pickup_junctions=[]
    while i<3:
        j=0
        while j<4:
            if len(company[i][j])!=0:
                a=company[i][j][1][0][0][0]
                x=int(math.ceil((Decimal(a)/Decimal(100))))
                pickup_junctions.append([1,x])
                break
            else:
                j=j+1
        i=i+1
    #delivery junctions
    null=[]
    i=0
    delivery_junctions=[]
    while i<3:
        j=0
        c_n=[]
        while j<4:
       
            if len(company[i][j])!=0:
                node=[]
                y=int(round(Decimal(company[i][j][0][0][0][1])/Decimal(100)))
                node.append(y)
                x=int(round(Decimal(company[i][j][0][0][0][0])/Decimal(100)))
                node.append(x)               
                c_n.append(node)            
                j=j+1
            else:
                c_n.append(null)
                j=j+1
        delivery_junctions.append(c_n)
        i=i+1
    return pu_list,pickup_junctions,delivery_junctions
################################################################################################################################
################################################################################################################################

def path_planning(img,traffic_signal_nodes):
    pick_up,puj,dj=find_PUJ_and_DJ(img)
    djarray=[pt for w in dj for pt in w if len(pt)>0 ]
    array=[pt for w in dj for pt in w ]
    combinations=delivery_sequence(djarray)
    d=[]
    for sequence in combinations:
        c=[]
        array=[pt for w in dj for pt in w ]
        for order in sequence:
            b=[]
            for pt in order:
                ind=array.index(pt)
                if ind<4:
                    a=puj[0]
                    array[ind]=[]
                if (ind>3)&(ind<8):
                    a=puj[1]
                    array[ind]=[]
                if ind>7:
                    a=puj[2]
                    array[ind]=[]
                b.append(a)
            c.append(b)
        d.append(c)
    possible_paths=[]
    i=0
    while i<len(d):
        j=0
        track=[]
        while j<len(d[i]):
            if j==0:
                pt=[6,0]
            else:
                pt=track[(len(track)-1)] 
            track.extend(rearrange(pt,d[i][j]))
            pt=track[(len(track)-1)]        
            track.extend(rearrange(pt,combinations[i][j]))
            j=j+1
        possible_paths.append(track)
        i=i+1
    
    
    hl,vl=grid_to_arrays(img)
    mn=500
    i=0
    while i<4:
        j=0
        fnl_path=[]
        while j<len(possible_paths[i]):
            if j==0:
                sp=[6,0]
            else:
                sp=ep
            ep=possible_paths[i][j]
            tr_sign_nodes=traffic_signal_nodes
            traffic_pts=[]
            l1,path=shortest_path(hl,vl,sp,ep,traffic_pts)
            if len(path)>0:
                if len(path)>1:
                    k1=3*l1+2*turns(path)
                    for x in tr_sign_nodes:
                        for y in path:
                            if x==y:
                                traffic_pts.append(y)
                                #print 'sp',sp,'ep',ep,'traffic_pts',traffic_pts
            
                    for pt in traffic_pts:
                        l2,path2=shortest_path(hl,vl,sp,ep,[pt])
                        k2=3*l2+2*turns(path2)
                        #if pt==[5,1]:
                            #print 'k1,k2',k1,k2
                        if k1==k2:
                            #print 'tr_sign_nodes',tr_sign_nodes
                            #print 'path 2',path2
                            path=path2
                            break
                fnl_path.append(path)
            j=j+1
        
        cont_path=[pt for w in fnl_path for pt in w]
        k=3*len(cont_path)+2*turns(cont_path)
        #print k
        if k<mn:
            fnl_shortest_path=fnl_path
            mn=k
            final_path_index=i
        i=i+1
    pick_up,puj,dj=find_PUJ_and_DJ(img)
    array=[pt for w in dj for pt in w ]
    pick_up_colour_array=['GS1','BS1','PS1','OS1','GT1','BT1','PT1','OT1','GC1','BC1','PC1','OC1']
    delivery_colour_array=['GS0','BS0','PS0','OS0','GT0','BT0','PT0','OT0','GC0','BC0','PC0','OC0']
    output0=[]
    i=0
    while i<len(fnl_shortest_path):
        for pt in array:
            if pt==fnl_shortest_path[i][len(fnl_shortest_path[i])-1]:
                ind=array.index(pt)
                array[ind]=[]
                output0.append(delivery_colour_array[ind])
                break
        i=i+1
    output1=[]
    aray=[]
    i=0
    for string in output0:
        ind=delivery_colour_array.index(string)
        aray.append(pick_up_colour_array[ind])
    for pt in possible_paths[final_path_index]:
        if puj.count(pt)>=1:
            ind=puj.index(pt)
            for x in aray:
                if ind==0:
                    if x[1]=='S':
                        output1.append(x)
                        aray.remove(x)
                        break
                if ind==1:
                    if x[1]=='T':
                        output1.append(x)
                        aray.remove(x)
                        break
                if ind==2:
                    if x[1]=='C':
                        output1.append(x)
                        aray.remove(x)
                        break
    
    return output1,output0,fnl_shortest_path
    
##############################################################################################################
#############################################################################################################
def decision_on_encountering_tr_signal(current_path,current_node):
    #global current_path
    sp=current_node
    ep=current_path[len(current_path)-1]
    ind=current_path.index(sp)
    path1=current_path[ind:]
    l1=len(path1)
    t1=turns(path1)
    Time1=k1*l1+k2*t1+30
    l2,path2=shortest_path(hl,vl,sp,ep,traffic_signal_nodes)
    #print path2
    if l2==1:
        time.sleep(30)
        pi.forward()
        time.sleep(1)
        return 's',[]
    
    if l2>1:
        t2=turns(path2)
    else :
        t2=0
    Time2=k1*l2+k2*t2
    #print Time1,Time2
    if Time1>Time2:
        current_path=path2
        pi.stop()
        time.sleep(0.1)
        pi.back()
        time.sleep(rev_time)
        pi.stop()
        time.sleep(0.1)
        #print 'a'
        return 'a',current_path
        
    else:
        
        time.sleep(30)
        pi.forward()
        time.sleep(1.5)
        #print 's'
    return 's',[]









def turn_left(prev_motion,alert,green_alert):
    #cap = cv2.VideoCapture(1)
    #print 'turning left'
    pi.stop()
    if prev_motion==0:
        pi.left()
    if prev_motion==1:
        pi.right()
    time.sleep(turn_time)
    while(1):
        left_sensor_value = int(pi.adc_conversion(3))
        centre_sensor_value = int(pi.adc_conversion(2))
        right_sensor_value = int(pi.adc_conversion(1))
        if ((left_sensor_value > black_threshold) and (centre_sensor_value > black_threshold) and (right_sensor_value > black_threshold)):
            pi.stop()
            break
    time.sleep(0.4)
    turn_flag=0
    alt_path=line_follow(2,0,alert,green_alert)
    return alt_path
#######################################################
def turn_right(prev_motion,alert,green_alert):
    #cap = cv2.VideoCapture(1)
    #print 'turning rigt'
    pi.stop()
    if prev_motion==0:
        pi.right()
    if prev_motion==1:
        pi.left()
    time.sleep(turn_time)
    while(1):
        left_sensor_value = int(pi.adc_conversion(3))
        centre_sensor_value = int(pi.adc_conversion(2))
        right_sensor_value = int(pi.adc_conversion(1))
        if ((left_sensor_value > black_threshold) and (centre_sensor_value > black_threshold) and (right_sensor_value > black_threshold)):
            pi.stop()
            break
    time.sleep(0.4)
    turn_flag=1
    alt_path=line_follow(3,0,alert,green_alert)
    return alt_path

############################################################################
##########################################################################################
def line_follow(prev_motion,motion,alert,green_alert):
    while(1):
        if (alert==1):
            while(1):
                left_sensor_value = int(pi.adc_conversion(3))
                centre_sensor_value = int(pi.adc_conversion(2))
                right_sensor_value = int(pi.adc_conversion(1))
                red_average=int((left_sensor_value+centre_sensor_value+right_sensor_value)/3)
                if (red_average<red_threshold):
                    pi.stop()
                    break
            pi.stop()
            decision,alternate_path=decision_on_encountering_tr_signal(current_path,current_node)
            if decision=='a':
                return alternate_path
            else:
                pi.stop()
                return []   
            pi.back()
            '''
            left_sensor_value = int(adc_conversion(3))
            centre_sensor_value = int(adc_conversion(2))
            right_sensor_value = int(adc_conversion(1))
            if ((left_sensor_value > black_threshold) and (centre_sensor_value > black_threshold-20) and (right_sensor_value > black_threshold)):
                pi.stop()
                break
            
        if (green_alert==1):
            while(1):
                left_sensor_value = int(pi.adc_conversion(3))
                centre_sensor_value = int(pi.adc_conversion(2))
                right_sensor_value = int(pi.adc_conversion(1))
                green_average=int((left_sensor_value+centre_sensor_value+right_sensor_value)/3)
                if (green_average<green_threshold):
                    pi.stop()
                    break
            pi.forward()
            time.sleep(0.5)
            pi.stop()
            time.sleep(0.1)
            return []
         '''   
          
        if(green_alert==0):
            while(1):
                left_sensor_value = int(pi.adc_conversion(3))
                centre_sensor_value = int(pi.adc_conversion(2))
                right_sensor_value = int(pi.adc_conversion(1))
                blue_average=int((left_sensor_value+centre_sensor_value+right_sensor_value)/3)
                if (blue_average<blue_threshold):
                    pi.stop()
                    break
            pi.stop()
            time.sleep(0.1)
            pi.forward()
            time.sleep(0.4)
            return []
        
##################################################################################3
def forward(prev_motion,alert,green_alert):
    alt_path=line_follow(prev_motion,0,alert,green_alert)
    return alt_path

def backward(prev_motion,alert,green_alert):
    #cap = cv2.VideoCapture(1)
    #print 'on the spot 180'
    pi.right()
    time.sleep(1.5)
    while(1):
        left_sensor_value = int(pi.adc_conversion(3))
        centre_sensor_value = int(pi.adc_conversion(2))
        right_sensor_value = int(pi.adc_conversion(1))
        if ((left_sensor_value > black_threshold) and (centre_sensor_value > black_threshold-20) and (right_sensor_value > black_threshold)):
            pi.stop()
            break
    pi.stop()
    turn_flag=0
    alt_path=line_follow(2,0,alert,green_alert)
    return alt_path
    

def robot_motion(prev_motion,current_angle,path,path_index,traffic_pts):
    alert=0      # to alert robot to check status of signal
    green_alert=0
    global current_node,p,d
    current_node=path[path_index]    
    if path_index==len(path)-1:
        if path[path_index][0]==1:
            package_client.Message(pick_output[p])
            p=p+1
        else:
            package_client.Message(delivery_output[d])
            d=d+1
            
        return [],p,d,prev_motion,current_angle
    for pt in traffic_pts:
        if pt==path[path_index+1]:
            alert=1
            #print alert
            break
    if (path[path_index+1]==[6,0]):
        green_alert=1
    x=path[path_index+1][0]-path[path_index][0]
    y=path[path_index+1][1]-path[path_index][1]
    if x==0:
        if y>0:
            next_angle=-90
        if y<0:
            next_angle=90
    if y==0:
        if x>0:
            next_angle=180
        else:
            next_angle=0
    motion=next_angle-current_angle
    if motion>180:
        motion=motion-360
    if motion<=-180:
        motion=motion+360
    if motion==0:
        alt_path=forward(prev_motion,alert,green_alert)
        prev_motion=0
    if motion==180:
        alt_path=backward(prev_motion,alert,green_alert)
        prev_motion=0
    if motion==90:
        alt_path=turn_left(prev_motion,alert,green_alert)
        prev_motion=0
    if motion==-90:
        alt_path=turn_right(prev_motion,alert,green_alert)
        prev_motion=0
    if motion==180:
        return alt_path,p,d,prev_motion,next_angle
    else:
        return alt_path,p,d,prev_motion,next_angle

img=cv2.imread('Test_Image_Finals.jpg')
hl,vl=grid_to_arrays(img)
traffic_signal_nodes=traffic_signal_nodes(img)
pick_output,delivery_output,path=path_planning(img,traffic_signal_nodes)
print pick_output,delivery_output
print path
#time.sleep(60)


#print (time.time()-strt1)
p=0
d=0
i=0
current_angle=0
prev_motion=0
alt_path=[]
while i<len(path):
    if len(alt_path)>0:
        current_path=alt_path
        alt_path=[]
    else:
        current_path=path[i]
    current_path_op=[]
    for x in current_path:
        point=[6-x[0],x[1]]
        current_path_op.append(point)
    print current_path_op
    j=0
    while j<len(current_path):
        alt_path,p,d,prev_motion,current_angle=robot_motion(prev_motion,current_angle,current_path,j,traffic_signal_nodes)
        if len(alt_path)>0:
            i=i-1
            break
        j=j+1
    i=i+1
pi.stop() 
package_client.Message('GS1')
package_client.Message('OS1')
package_client.Message('BS1')
package_client.Message('PS1')
package_client.Message('CCC')


        
        
    





