import sys
import os
import simpy

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from project.core.simulation import Simulation

if __name__ == "__main__":
    while True:  
        env = simpy.Environment()
        chargingStation = Simulation(env)
        env.run()
        
        flag = chargingStation.gui.getFlag()  
        if flag == 1:  
            print("Starting simulation again...")
        else:
            break