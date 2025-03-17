import station
import simpy

if __name__=="__main__":
    while True:  
        env = simpy.Environment()
        chargingStation = station.Station(env)
        env.run()
        
        flag = chargingStation.gui.getFlag()  
        if flag == 1:  
            print("Starting simulation again...")
        else:
            break        


