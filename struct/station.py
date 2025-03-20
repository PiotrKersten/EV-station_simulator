import simpy
import random
import ev

class Station:
    def __init__(self, env):
        self.env = env
        self.vehicle = ev.EV()
        pass

    def stationRun(self, name, type, arriving_time, charge_duration):
        if type==1:
            self.vehicle.createCar(name, arriving_time, charge_duration)
        else:
            self.vehicle.createTruck(name, arriving_time, charge_duration)
            
        yield self.env.timeout(arriving_time)

        
    def checkStationAvailability(self, desired_power):
        for i, charger in enumerate(self.chargers):
            occupied_slots = charger.count  
            free_slots = charger.capacity - occupied_slots  

            total_power = sum(car['assigned_power'] for car in self.car_priorities if car['charger_index'] == i)

            print(f"Charger {i}: {occupied_slots}/{charger.capacity} slots occupied | Power: {total_power} kW")

            if free_slots > 0 and (total_power + desired_power) <= 300:
                for slot in range(charger.capacity):
                    if slot >= occupied_slots: 
                        print(f"Found free slot at charger {i}, slot {slot}")
                        return i, slot

        print("No suitable charger available (exceeds power limit or no slots).")
        return None, None

        