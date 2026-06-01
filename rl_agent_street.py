import serial
import time
import numpy as np
import random

class StreetLightEnv:
    def __init__(self, port, baud_r=115200):
        self.arduino = serial.Serial(port, baud_r, timeout=0.1)
        time.sleep(2) 

        self.pr_light = None
        self.cur_light = None

    def rd_sensor(self):
        self.arduino.reset_input_buffer()
        while True:
            if self.arduino.in_waiting > 0:
                try:
                    line = self.arduino.readline().decode('utf-8').strip()
                    if line.isdigit():
                        return int(line)
                except UnicodeDecodeError:
                    continue
            time.sleep(0.01)
    
    def get_state(self):
        r_light = self.rd_sensor()

        if r_light > 800: l_bin = 0
        elif r_light > 600: l_bin = 1
        elif r_light > 400: l_bin = 2
        elif r_light > 200: l_bin = 3
        else: l_bin = 4

        if self.pr_light is None:
            trend = 0
        else:
            delta = r_light - self.pr_light
            if delta < -150: trend = -2
            elif delta < -20: trend = -1
            elif delta > 50: trend = 1
            else: trend = 0

        self.pr_light = r_light
        self.cur_light = l_bin

        return (l_bin, trend)
    
    def step(self, action): 
        action_byte = str(action).encode('utf-8')
        self.arduino.write(action_byte)

        time.sleep(0.5)
        next_state = self.get_state()

        reward = self.calc_reward(next_state[0], next_state[1], action)
        return next_state, reward

    def calc_reward(self, l_bin, trend, action):
        t_action = l_bin
        vis_pen = -abs(t_action - action) * 2
        nrg_pen = -action * 0.5
        reward = vis_pen + nrg_pen
        
        if trend == -2 and action > 1:
            reward -= 5.0 
            
        return reward

class QAgent:
    def __init__(self, alpha=0.1, gamma=0.9, eps=0.2):
        self.alpha = alpha
        self.gamma = gamma
        self.eps = eps
        self.q_tab = {}

    def get_q(self, state, action):
        return self.q_tab.get((state, action), 0.0)

    def chs_action(self, state):
        if random.uniform(0, 1) < self.eps:
            return random.randint(0, 4)
        else:
            q_vals = [self.get_q(state, a) for a in range(5)]
            max_q = max(q_vals)
            b_actions = [a for a in range(5) if q_vals[a] == max_q]
            return random.choice(b_actions)

    def update(self, state, action, reward, n_state):
        cur_q = self.get_q(state, action)
        max_n_q = max([self.get_q(n_state, a) for a in range(5)])
        new_q = cur_q + self.alpha * (reward + self.gamma * max_n_q - cur_q)
        self.q_tab[(state, action)] = new_q


if __name__ == "__main__":
    env = StreetLightEnv(port='COM3', baud_r=115200)
    agent = QAgent(alpha=0.1, gamma=0.9, eps=0.3)
    
    state = env.get_state()
    
    try:
        ep = 1
        while True:
            action = agent.chs_action(state)
            n_state, reward = env.step(action)
            agent.update(state, action, reward, n_state)
            
            print(f"Ep: {ep} | St: {state} | Act: {action} | Rew: {reward:.1f}")
            
            state = n_state
            ep += 1
            
            if agent.eps > 0.01:
                agent.eps *= 0.999
                
    except KeyboardInterrupt:
        print(agent.q_tab)
        env.arduino.close()