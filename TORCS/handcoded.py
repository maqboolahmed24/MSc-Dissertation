import numpy as np
import gym
import gym_torcs
import matplotlib.pyplot as plt

class TorcsAgent:
    def __init__(self, env):
        self.env = env
        #initialize the total displacement to zero
        self.totalDisplacement=0
        self.total_displacement = 0
        self.track_positions = []
        self.current_direction=0
    def inputlol_fn(self, dict_obs):
        return np.hstack((dict_obs['angle'],# this is reletive terack car angle
                          dict_obs['track'],# think this is scanners array? 
                          dict_obs['trackPos'],# [-1,1 : -1 for right and +1 for left ]
                          dict_obs['speedX'],
                          dict_obs['speedY'],
                          dict_obs['speedZ'],
                          dict_obs['wheelSpinVel'],
                          dict_obs['rpm'],
                          dict_obs['opponents']))

    def act(self, obs):
        inputlol = self.inputlol_fn(obs)
        angle = inputlol[0]
        trackPos = inputlol[2]
              
        speedX = obs['speedX']
        speedY = obs['speedY']
    
    
        self.calculate_displacement(speedX, speedY)
    
    
        action = np.zeros((3,))

        if angle > 0.01: 
            action[0] = 0.8  
        elif angle < -0.01: 
            
            action[0] = -0.8   
        else:  
            action[0] = 0  
            action[1] = 10
            
        if trackPos > 0.5:  
            action[0] += 0.8  #steer to the left
        #of car is off to the left
        elif trackPos < -0.5:  
            #steer to the right
            action[0] += -0.8  


        
        
        action[0] = np.tanh(action[0])
        

       
        action[1] = 10.3
        if self.total_displacement>=95 and self.total_displacement<=98:
            action[0] =0.05
        
        self.track_positions.append(trackPos)
        
        
        
        if angle>0.01:
            self.current_direction+=angle
        elif angle<-0.01:
            self.current_direction+=angle
        #self.current_direction = angle
        self.track_positions.append(self.current_direction)
        #self.track_positions.append(self.current_direction)
        print(len(self.track_positions), " ", self.current_direction)

        return action
        
        
        
        
        
    def calculate_displacement(self, speedX, speedY):
    #using the pythagorean theirm 
    	displacement=np.sqrt((speedX**2)+ (speedY**2))
    	self.total_displacement+=displacement
    	return displacement
    	

try:
    # Instantiate the environment
    env = gym.make('Torcs-v0', rendering=True)
    agent = TorcsAgent(env)

    obs, reward, done = env.reset(), 0., False
    
    x = 0
    print("X", "Track Position")

    while not done:
        action = agent.act(obs)
        obs, reward, done, _ = env.step(action)
        #print("Angle:", obs["angle"])
        print
        #"SpeedX:", obs["speedX"], "SpeedY:", obs["speedY"],"SpeedZ:", obs["speedZ"])
        #, "Angle:", obs["angle"], "track:", obs["track"], "TrackPos:", obs["trackPos"], "WheelSpinVel:", obs["wheelSpinVel"], "RPM:", obs["rpm"], "Opponents:", obs["opponents"])

        #print(agent.total_displacement) 
        x += obs["angle"]
       # print(x, obs["trackPos"])
        
        


except Exception as e:
    print(e)

finally:
    env.end()
