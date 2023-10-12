import gym
import gym_torcs
import numpy as np
from pynput import keyboard

#Global variable to store the current action
current_action = np.array([0.0,0.2,0.0])  # [steer, accel, brake]

#Keyboard input handling
def on_press(key):
    global current_action

    try:
        #steering left
        if key.char == 'a':
            current_action[0]=0.5
        #steering right
        elif key.char == 'd':
            current_action[0]=-0.5
        #accelerating
        elif key.char == 'w':
            current_action[1]=1.0
        #brake
        elif key.char == 's':
            current_action[2]=0.8
    except AttributeError:
        pass


def on_release(key):
    global current_action

    try:
        #Stop steering
        if key.char == 'a' or key.char == 'd':
            current_action[0] = 0.0
        #Stop accelerating
        elif key.char == 'w':
            current_action[1] = 0.0
        #Stop braking
        elif key.char == 's':
            current_action[2] = 0.0
    except AttributeError:
        pass

    #exit the game
    if key == keyboard.Key.esc:
        return False



#Start listening to keyboard inputs
listener=keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

try:
    #instantiate the environment
    env = gym.make("Torcs-v0")

    o, r, done = env.reset(), 0., False
    while not done:
        #use the current_action as the action
        o, r, done, _ = env.step(current_action)

except Exception as e:
    print(e)

finally:
    env.end()
    #stop listening to keyboard inputs
    listener.stop()
