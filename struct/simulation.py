import simpy
import random

import gui
import battery
import grid
import ev
import modules

class Simulation:
    def __init__(self, env):
        self.env = env
        self.gui = gui.Gui()
        try:
            (
                self.time_from, 
                self.time_to, 
                self.station_load_cars, 
                self.station_load_trucks, 
                self.desired_charging_time, 
                self.battery, 
                self.grid_power, 
                self.average_time,
                self.chargers_quantity,
                self.chargers_power,
            ) = self.gui.insertSimulationParameter()

        except ValueError:
            print('Aborted. Closing app')
            return

        self.grid  = grid.Grid(self.grid_power)
        self.battery = battery.Battery(self.battery, self.desired_charging_time)
        self.ev = ev.EV()
        self.modules = modules.Modules()

        self.multiplier = 60 // self.desired_charging_time
        module_power = self.chargers_power / self.chargers_quantity 
        self.chargers = [simpy.Resource(env, capacity=2) for _ in range(self.chargers_quantity)]
        self.modules = {i: [module_power] * self.chargers_quantity for i in range(self.chargers_quantity * 2)}  
        self.car_priorities = []
        self.car_queue = []

        self.time_between = random.randint(self.time_from, self.time_to)
        if self.average_time != 0:
            self.time_between = self.average_time
        
        self.env.process(self.run())  

    def run(self):
        processes = []  
        for i in range(self.station_load):
            yield self.env.timeout(self.time_between)
            self.time_table.append(self.time_between)
            process = self.env.process(self.car(f'Car {i}', i * 1, self.desired_charging_time)) 
            processes.append(process) 

        yield self.env.all_of(processes)
        self.gui.showSimulationParametersWithPlots(self.battery, self.time_table, self.energy_table, self.station_load, self.desired_charging_time, self.charging_times_data, self.grid_power_data, self.battery_capacity_data)

    def stationRun(self, name, type, arriving_time, charge_duration):
        if type==1:
            vehicle = self.ev.createCar(name, arriving_time, charge_duration)
        else:
            vehicle = self.ev.createTruck(name, arriving_time, charge_duration)
            
        yield self.env.timeout(arriving_time)

        desired_power = vehicle['needed_energy']*self.multiplier

        print("\n")
        print(f"{name} arrived at {arriving_time} [t.u] with energy needed {vehicle['needed_energy']} kWh")
        print(f"Desired power: {desired_power}")

        available_grid = self.grid.checkGridState()
        available_station, available_slot = self.checkStationAvailability(desired_power)
        available_battery = self.battery.checkBatteryState()

        print("\n")
        print(f"{name} arrived at {arriving_time} [t.u] with energy needed {vehicle['needed_energy']} kWh")
        print(f"Desired power: {desired_power}")
        print(f"Grid power {available_grid} kW")

        if available_station is not None:
            vehicle['assigned_power'] = desired_power
            vehicle['charger_index'] = available_station
            vehicle['charger_slot'] = available_slot

            if desired_power <= available_grid: 
                print(f"Charging with grid only {desired_power} kW")
                power_to_return = desired_power

                #start here
                self.battery.chargeBattery(available_grid, power_to_return)

    def checkStationAvailability(self, desired_power):
        for i, charger in enumerate(self.chargers):
            occupied_slots = charger.count  
            free_slots = charger.capacity - occupied_slots  

            total_power = sum(car['assigned_power'] for car in self.car_priorities if car['charger_index'] == i)

            print(f"Charger {i}: {occupied_slots}/{charger.capacity} slots occupied | Power: {total_power} kW")

            if free_slots > 0 and (total_power + desired_power) <= self.grid_power:
                for slot in range(charger.capacity):
                    if slot >= occupied_slots: 
                        print(f"Found free slot at charger {i}, slot {slot}")
                        return i, slot

        print("No suitable charger available (exceeds power limit or no slots).")
        return None, None

    def updateData(self):
        self.battery.u
        pass