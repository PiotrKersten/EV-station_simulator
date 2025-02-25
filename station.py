import simpy
import random
import matplotlib.pyplot as plt
import numpy as np
import time

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import gui

class Station:
    def __init__(self, env):
        self.env = env
        self.grid_power = 300  
        
        self.chargers = [simpy.Resource(env, capacity=2) for _ in range(4)]
        self.car_queue = []  
        self.modules = {i: [37.5] * 4 for i in range(8)}  
        self.car_priorities = []
        
        # Data for plotting
        self.grid_power_data = []
        self.battery_capacity_data = []
        self.charging_times_data = []
        self.time_table = []
        self.energy_table = []

        self.gui = gui.Gui()
        self.time_from, self.time_to, self.station_load, self.desired_charging_time, self.battery_capacity, self.average_time = self.gui.insertSimulationParameter()
        self.multiplier = 60 // self.desired_charging_time
        self.battery_max = self.battery_capacity
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
        self.gui.showSimulationParametersWithPlots(self.battery_max, self.time_table, self.energy_table, self.station_load, self.desired_charging_time, self.charging_times_data, self.grid_power_data, self.battery_capacity_data)
    
    def car(self, name, arriving_time, charge_duration):
        car = {
            'name': name,
            'driving_time': arriving_time,
            'charge_duration': charge_duration,
            'needed_energy': random.randint(20, 70),  # Random energy needs
            'assigned_power': 0,
            'charger_index': None,
            'charger_slot': None
        }

        yield self.env.timeout(arriving_time)
        self.energy_table.append(car['needed_energy'])
        # Desired time is always 15 minutes
        desired_power = car["needed_energy"] * self.multiplier
        print("\n")
        print(f"{name} arrived at {arriving_time} [t.u] with energy needed {car['needed_energy']} kWh")
        print(f"Desired power: {desired_power}")

        available_grid = self.checkGridState()
        available_station, available_slot = self.checkStationAvailability(desired_power)
        self.checkBatteryState()

        print(f"Grid power {available_grid} kW")

        # Check station first
        if available_station is not None:

            car['assigned_power'] = desired_power
            car['charger_index'] = available_station
            car['charger_slot'] = available_slot

            # Check if grid is enough
            if desired_power <= available_grid: 
                print(f"Charging with grid only {desired_power} kW")
                power_to_return = desired_power
                self.updateGridState(desired_power, False)
                if self.battery_capacity < self.battery_max:
                    self.updateBattery(available_grid - desired_power, True)

            # Add battery
            elif desired_power > available_grid:
                battery_power_demand = desired_power - available_grid

                if battery_power_demand * (1/self.multiplier) > self.battery_capacity:
                    battery_power_demand = self.battery_capacity * self.multiplier
                    demanded = desired_power - battery_power_demand - available_grid
                    power_to_attach = self.checkModuleToDetach(demanded)
                    max_power = power_to_attach + available_grid + battery_power_demand
                    if max_power != desired_power:
                        charge_duration = int(car['needed_energy'] / max_power * 60)
                        print(f"New charging time {charge_duration}")

                    print(f"Charging with grid {available_grid} kW battery: {battery_power_demand} kW modules: {power_to_attach} kW")

                print(f"Charging with grid {available_grid} kW and battery {battery_power_demand} kW")
                power_to_return = available_grid
                self.updateGridState(available_grid, False)
                self.updateBattery(battery_power_demand, False)

            self.car_priorities.append(car)
            with self.chargers[available_station].request() as req:
                yield req  
                print(f"[{self.env.now}] Vehicle {name} starts charging at charger {available_station} slot {available_slot}")
                charge_duration = self.checkIfModuleDetached(car, charge_duration)
                yield self.env.timeout(charge_duration)   
                print(f"[{self.env.now}] Vehicle {name} finished charging at charger {available_station} slot {available_slot}")
                self.updateGridState(power_to_return, True)

                # Collect data for plots
                self.grid_power_data.append(self.grid_power)
                self.battery_capacity_data.append(self.battery_capacity)
                self.charging_times_data.append(charge_duration)

        else:
            print(f"{name} is waiting in queue...")
            self.car_queue.append(car)
            return
    
        self.car_priorities.remove(car)

#MODULES
    def checkModuleToDetach(self, demanded_power):
        sum_power = 0
        for car in reversed(self.car_priorities):
            power = car['assigned_power']
            print('power',power)
            power_to_detach = (power % 37.5) + 5
            if demanded_power - sum_power < power_to_detach and sum_power != 0:
                print('early')
                return sum_power
            if power_to_detach <= 0:
                iter = power / 37.5
                if iter == 1:
                    power_to_detach = 0
                else:
                    power_to_detach = 37.5
            elif power < 37.5:
                power_to_detach = 0
            print('power to detach', power_to_detach)
            car['assigned_power'] = power - power_to_detach
            sum_power+=power_to_detach
            if sum_power <= 0:
                sum_power = self.detachModulePartly(demanded_power)
        print(f"Only {sum_power}/{demanded_power} kW can be applied")
        return sum_power
    
    def detachModulePartly(self, demanded_power):
        sum_power = 0
        for car in reversed(self.car_priorities):
            power = car['assigned_power']
            print('power',power)
            power_to_detach = 17.5
            if demanded_power - sum_power and sum_power  < power_to_detach != 0:
                return sum_power
            print('power to detach', power_to_detach)
            car['assigned_power'] = power - power_to_detach
            sum_power+=power_to_detach

        print(f"Only {sum_power}/{demanded_power} kW can be applied")
        return sum_power

    
    def checkIfModuleDetached(self, car, duration):
        search_name = car['name']
        ev = next((ev for ev in self.car_priorities if ev['name'] == search_name), None)

        if ev:
            if car['assigned_power'] != ev['assigned_power']:
                time = int(car['needed_energy'] / ev['assigned_power'] * 60)
                return time
        return duration

# GRID
    def updateGridState(self, power_cut, flag):
        if flag:
            self.grid_power = self.grid_power + power_cut
        else:
            self.grid_power = self.grid_power - power_cut
        print(f"Grid state {self.grid_power} kW")
        
    def checkGridState(self):
        print(f"Grid state {self.grid_power} kW")
        return self.grid_power
  

#BATTERY 
    def checkBatteryState(self):
        print(f"Battery state: { self.battery_capacity} kWh power ready: {self.battery_capacity*self.multiplier} kW")
        return self.battery_capacity


    def updateBattery(self, power_cut, flag):
        if flag:
            self.battery_capacity = self.battery_capacity + power_cut*(1/self.multiplier)
            if self.battery_capacity > self.battery_max: 
                self.battery_capacity = self.battery_max
        else:
            self.battery_capacity = self.battery_capacity - power_cut*(1/self.multiplier)
        print(f"Battery state {self.battery_capacity} kWh")
    
# STATION
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

        