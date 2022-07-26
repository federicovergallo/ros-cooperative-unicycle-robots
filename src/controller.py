#!/usr/bin/env python

import rospy
import numpy as np
import rosnode
from comunicating_robots.msg import *
from costants import *

#calcolo distanza 
def distanza(x1,y1,x2,y2):
    return (np.sqrt(np.power(x2-x1,2)+np.power(y2-y1,2))) 

#calcolo phi
def get_phi(x,y, xdes, ydes): 
    return (np.arctan2((ydes-y),(xdes-x)))

#callback posizione desiderata   
def callback_des(data):

    if not hasattr(callback_des, "pdes"):
       callback_des.pdes = None
    callback_des.pdes = data

#callback simulatore
def callback(data,pub):
    #dall'header del messaggio ricevuto ottengo il nome del mittente e salvo le posizioni dei robot
    robot_name = data._connection_header['callerid'] 
    robot_name = robot_name[16:]
    if not hasattr(callback, "pub_var"):
       callback.pub_var =  rospy.Publisher('/varTopic_'+robot_name, Variable, queue_size=10)
    if not hasattr(callback, "p_robot"):
       callback.p_robot = Position()
    if not hasattr(callback, "theta_old"):
       callback.theta_old = 0.0  # it doesn't exist yet, so initialize t
    if not hasattr(callback, "theta_old_old"):
       callback.theta_old_old = callback.theta_old
    if not hasattr(callback, "int_time"):
       callback.int_time = start_t #tempo d'integrazione
   
    con_rate=rospy.Rate(rate)
    con_rate.sleep()
    #aspetto che ci sia il simulatore in ascolto sul topic
    while pub.get_num_connections() != 2:
       con_rate.sleep()
    #aspetto finche' venga comunicata la posizione desiderata
    while not hasattr(callback_des, "pdes"):
       con_rate.sleep()

    callback.p_robot.x=data.x
    callback.p_robot.y=data.y
    callback.p_robot.theta=data.theta
    
    theta_des = K*(get_phi(callback.p_robot.x,callback.p_robot.y,callback_des.pdes.x,callback_des.pdes.y))
    theta_array = np.array([callback.theta_old_old, callback.theta_old, theta_des])
    theta_array_new = np.unwrap(theta_array)

    callback.theta_old_old = callback.theta_old
    callback.theta_old = theta_array_new[2]

    print theta_array
    print theta_array_new
    print ('ydes-y= '+str(callback_des.pdes.y-callback.p_robot.y)+' xdes-x= '+str(callback_des.pdes.x-callback.p_robot.x))

    #calcolo i parametri normalmente
    rospy.loginfo('destinazione '+robot_name+': x=' +str(callback_des.pdes.x)+' y='+str(callback_des.pdes.y))
    msg = Input()
    msg.v = v
    msg.w = K*(theta_array_new[2]-data.theta)

    
msg_var = Variable()
    #verifiche su distanza 
    rospy.loginfo(str(distanza(callback.p_robot.x, callback.p_robot.y, callback_des.pdes.x, callback_des.pdes.y)))
    if distanza(callback.p_robot.x, callback.p_robot.y, callback_des.pdes.x, callback_des.pdes.y ) < dist_des:
       msg.v = v_des
       rospy.loginfo('Intorno a destinazione ')
       msg_var.t_intorno = callback.int_time
    if callback_des.pdes.safe_flag:
       msg.v = v_safe
       rospy.loginfo('Robot troppo vicini')
    if distanza(callback.p_robot.x, callback.p_robot.y, callback_des.pdes.x, callback_des.pdes.y) < 0.01:
       msg.v = v_stop
       msg_var.t_arrivo = callback.int_time
       rospy.loginfo('Arrivati a destinazione')


    msg_var.t_int = callback.int_time
    msg_var.xdes = callback_des.pdes.x
    msg_var.ydes = callback_des.pdes.y
    msg_var.phi = theta_array_new[2]
    msg_var.phinowrap = K*(get_phi(callback.p_robot.x,callback.p_robot.y,callback_des.pdes.x,callback_des.pdes.y))
    msg_var.theta = data.theta
    callback.int_time+=delta

    rospy.loginfo(robot_name+' params t integrazione: '+str(msg_var.t_int)+' v='+str(msg.v)+' w='+str(msg.w))
    callback.pub_var.publish(msg_var)
    pub.publish(msg)

if __name__ == '__main__':
    try:
       name_space = rospy.get_namespace()
       robot_name = rospy.get_param(name_space)
       pub = rospy.Publisher('/inputTopic_'+robot_name, Input, queue_size=0)
       rospy.init_node('controller_'+robot_name, anonymous=False)
       rospy.loginfo(rospy.get_name())
       con_rate=rospy.Rate(rate)
       sub = rospy.Subscriber('/stateTopic_'+robot_name, Position, callback,(pub))
       sub_pdes = rospy.Subscriber('/pdesTopic_'+robot_name, PdesPosition, callback_des)
       #spin() simply keeps python from exiting until this node is stopped
       rospy.spin()
    except rospy.ROSInterruptException:
        print "errore"

