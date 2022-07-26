#!/usr/bin/env python
leader_name = 'robot1'
rob_number = 2
#stato iniziale simulatori
state0 = {"/sim1/":[4.0, 4.0, 0.0], "/sim2/":[2.0, 1.5, 0.0]}
#state0 = {"/sim1/":[4.0, 5.0, 0.0], "/sim2/":[2.0, 3.0, 0.0], "/sim3/":[0.0, 2.0, 0.0]}
#state0 = {"/sim1/":[4.0, 5.0, 0.0], "/sim2/":[-1.0, -1.0, 0.0],  "/sim3/":[-3.0, 5.0, 0.0], "/sim4/":[4.0, -5.0, 0.0]}
#rate comunicazione
rate = 100
#starting time, step e delta d'integrazione
start_t = 0.0 
step = 0.001
delta = 0.01
#punto P desiderato robot1
xdes=3
ydes=3
#distanza desiderata
dist_des=1
#distanza sicurezza robot
safe_dist=0.2
#velocita simulatore
K=1
#condizioni controllore
v=1
#velocita intorno pdes
v_des=0.1
#velocita a pdes
v_stop=0
w_stop=0
#velocita safe
v_safe=0.05
