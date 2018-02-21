import time
import World
import random
import threading

#initiate hyperparameters
epsilon = 0.0
discount = 0.3

actions = World.actions
states = []
Q = {}

#initiate states list and Q dictionary
for i in range(World.x):
    for j in range(World.y):
        states.append((i,j))
        temp_dic = {}
        for a in actions:
            temp_dic[a] = 0.1
        Q[(i,j)] = temp_dic

def do_move(action):
    s = World.player
    r = -World.score
    if action == actions[0]:
        World.try_move(0,-1)
    elif action == actions[1]:
        World.try_move(0,1)
    elif action == actions[2]:
        World.try_move(-1,0)
    elif action == actions[3]:
        World.try_move(1,0)
    else:
        return
    s2 = World.player
    r += World.score       
    return s, action, r, s2

def policy(max_act):
    #global epsilon
    if random.random() > epsilon:
        return max_act
    else:
        ind = random.randint(0, len(actions)-1)
        return actions[ind]

def maxQ(s):
    maxQval = None
    max_act = None
    for a, q in Q[s].items():
        if max_act is None or (q > maxQval):
            maxQval = q
            max_act = a
    return max_act, maxQval

def incQ(s, a, alpha, inc):
    Q[s][a] = (1-alpha)*Q[s][a] + alpha*inc
    
def run():
    alpha = 1.0
    t = 1.0
    while(True):
        s = World.player
        max_act, maxQval = maxQ(s)
        action_fin = policy(max_act)
        s, a, r, s2  = do_move(action_fin)
        max_act2, maxQval2= maxQ(s2)
        inc = r + discount*maxQval2
        incQ(s, a, alpha, inc)
        
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            t = 1.0
            
        alpha = pow(t, -0.1)
        
        time.sleep(0.1)
      
t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()