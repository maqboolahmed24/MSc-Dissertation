#importing necessary libraries and modules
import gym
import gym_torcs
import random
import os
import ignorewarning
import atexit#to fix the training, used to kill the environment when I wante to pause the training
#import pickle
import json
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt

#path to save the trained agent
PATH = "Save/trained_agent"
print("\n      --------------------------------------------\n       Please press F2 for preffered camera angle \n      --------------------------------------------\n")

#define the neural network agent 
class GenAgent(tf.keras.Model):
    def __init__ (self, input_size , hidden_size , output_size):
        super(GenAgent, self).__init__()
        self.fc1=tf.keras.layers.Dense(hidden_size , input_shape=(input_size,))#defining the layers
        self.fc2=tf.keras.layers.Dense(output_size)

#forward propogation
    def call(self, x):
        x=tf.nn.relu(self.fc1(x))
        x= self.fc2(x)
        return x

#function to introduce mutation to an agent
def mutation(agent):
    for variables in agent.variables:
        variables.assign_add(tf.random.normal(shape=variables.shape, stddev=0.1))

#function to create a child agent through crossover of two parent agents
def crossover(agent1, agent2):
    child_agent =GenAgent(agent1.fc1.units, agent1.fc2.units, agent2.fc2.units)
    for parameter1 , parameter2 , child_parameter in zip(agent1.variables , agent2.variables , child_agent.variables):
        mask = tf.random.uniform(shape=parameter1.shape) > 0.5
        child_parameter.assign(tf.where(mask, parameter1, parameter2))
    return child_agent

#function to create the next generation agents
def nextGen(agents, fitness, elitism_size=2):
    #sorting the agents based on the fitness score
    sorted_indices = np.argsort(fitness)[::-1]  #get the indices that would sort the list
    new_agents = []

    #Elitism- directly take top performing agents
    for i in range(elitism_size):
        new_agents.append(agents[sorted_indices[i]])

    #create a new agent based on fitness probabilitues
    fitness = np.array(fitness)
    probas = fitness / fitness.sum()
    for lol in range(len(agents) - elitism_size):
        parents = np.random.choice(agents, size=2, p=probas)
        child_agent = crossover(*parents)
        if random.random() < 0.1:
            mutation(child_agent)
        new_agents.append(child_agent)

    return new_agents


# Function to simulate one episode and get the total reward
def run_episode(agent, env):
    observation_dict = env.reset()
    total_reward = 0
    done = False
    while not done:
    #input observations, just taking only three out of 9 others
        observation = np.concatenate([
                [observation_dict['angle']], 
                 observation_dict['track'],
                [observation_dict['trackPos']],
        ])
        action= agent(observation[None, ...]).numpy()[0] # Numpy array indices for 2D tensor
        action= np.tanh(action)
        observation_dict, reward, done, x = env.step(action)
        total_reward += reward
    return total_reward

#function to clean the environmetn after training is fininshed or intrupted by user
def cleanup():
    print("\nCleaning up, Goodbye. \n")
    env.close()
atexit.register(cleanup)


#helper function to initialize the agent
def initialize_agent(agent, input_size):
    #Initializes the agent's architecture by passing some placeholder data
    placeholder_data = tf.zeros((1, input_size))
    agent(placeholder_data)

#initializing the varoius parameteres
input_size = 21
output_size = 3
hidden_size = 128
population_size = 50
maximum_generations = 1000
start_generation = 1

#check if a trained agent already exists
if os.path.exists(PATH):
    print("Trained agent found! Loading and running it...\n")
    loaded_trained_agent = tf.keras.models.load_model(PATH)
    with ignorewarning.suppress_torcs_output():
        env = gym.make('Torcs-v0', rendering=True)
    reward = run_episode(loaded_trained_agent, env)
    print(f"Reward obtained by the loaded best agent: {reward}")
    env.close()
    exit(0)  # This ends the program here and prevents it from going to the training part

#if no trained agent, start the training process
else:
    print("No pre-trained agent found! Starting training...")
    agents = [GenAgent(input_size, hidden_size, output_size) for _ in range(population_size)]
    for agent in agents:
        initialize_agent(agent, input_size)
    with ignorewarning.suppress_torcs_output():
        env = gym.make('Torcs-v0', rendering=False)

#main training loop
try:
    for generation in range(start_generation, maximum_generations):
        fitness = [run_episode(agent, env) for agent in agents]
        print(f'Generation  {generation}, maxFitness {max(fitness)}')
        agents = nextGen(agents, fitness)

#message to show if user intrupts the training process
except KeyboardInterrupt:
    print('Training interrupted by the user. See you later')
    
    #after training, save the best agent and display its performance
finally:
    trained_agent_idx = np.argmax(fitness)
    trained_agent = agents[trained_agent_idx]
    trained_agent.save(PATH)
    print('Training completed successfully.')
    env.close()
    with ignorewarning.suppress_torcs_output():
        env = gym.make('Torcs-v0', rendering=True)
    reward = run_episode(trained_agent, env)
    print(f"Reward obtained by the loaded trained agent: {reward}")
    env.close()
