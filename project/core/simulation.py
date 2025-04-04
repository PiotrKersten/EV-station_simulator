import sys
import os
import simpy
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from project.gui.gui import Gui
from project.models.battery import Battery
from project.models.grid import Grid
from project.models.ev import EV
from project.models.modules import Modules

class Simulation:
    def __init__(self, env):
        self.env = env
        self.gui = Gui()
        try:
            (
                self.time_from, 
                self.time_to, 
                self.station_load_cars, 
                self.station_load_trucks, 
                self.desired_charging_time, 
                self.battery_capacity, 
                self.grid_power, 
                self.average_time,
                self.chargers_quantity,
                self.modules_quantity,
                self.slots,
                self.chargers_power,
                self.generation_choice,
            ) = self.gui.insertSimulationParameter()

        except ValueError:
            print('Aborted. Closing app')
            return

        self.grid  = Grid(self.grid_power)
        self.battery = Battery(self.battery_capacity, self.desired_charging_time)
        self.ev = EV()
        self.modules = Modules()

        self.multiplier = 60 // self.desired_charging_time
        self.module_power = self.chargers_power / self.modules_quantity
        self.station_load = self.station_load_cars + self.station_load_trucks
        self.chargers = [simpy.Resource(env, capacity=self.slots) for _ in range(self.chargers_quantity)]
        self.charger_modules = {i: [self.module_power] * self.modules_quantity for i in range(self.chargers_quantity)}  

        
        self.time_table = []
        self.type_time = {}
        self.arrival_time = []
        self.charging_times = []
        self.charging_times_cars = []
        self.charging_times_trucks = []
        self.car_priorities = []
        self.car_queue = []

        self.time_between = random.randint(self.time_from, self.time_to)
        if self.average_time != 0:
            self.time_between = self.average_time
        
        self.env.process(self.run())  

    def run(self):
        processes = []  

        if self.generation_choice:
            self.distributeEvenly()
        else:
            self.distributeRandomly()
        cars_count = 0
        trucks_count = 0

        for i, el in enumerate(self.distributed_vehicles):
            yield self.env.timeout(self.time_between)
            self.time_table.append(self.time_between)

            if 'car' in el:
                process = self.env.process(self.stationRun(f'Car {cars_count}', 1, i * 1, self.desired_charging_time))
                cars_count += 1
            if 'truck' in el:
                process = self.env.process(self.stationRun(f'Truck {cars_count}', 2, i * 1, self.desired_charging_time))
                trucks_count += 1


            processes.append(process)

        yield self.env.all_of(processes)
        self.energy_table = self.ev.getTable()
        self.battery_capacity_data = self.battery.getTable()
        self.grid_power_data = self.grid.getTable()


        self.gui.showSimulationParametersWithPlots(
            self.battery_capacity,
            self.time_table, 
            self.energy_table, 
            self.station_load, 
            self.desired_charging_time, 
            self.charging_times, 
            self.grid_power_data, 
            self.battery_capacity_data,
            self.charging_times_cars,
            self.charging_times_trucks,
            self.station_load_cars,  # Pass the number of cars
            self.station_load_trucks,  # Pass the number of trucks
            self.arrival_time,
            self.type_time
        )

    def distributeEvenly(self):

        self.distributed_vehicles = []
        ratio_cars = self.station_load_trucks / self.station_load_cars if self.station_load_cars > 0 else 0 
        ratio_trucks = self.station_load_cars / self.station_load_trucks if self.station_load_trucks > 0 else 0 

        i, j = 0, 0
        for k in range(self.station_load):
            if i < self.station_load_cars and (j >= ratio_cars* i or j >= self.station_load_trucks): 
                self.distributed_vehicles.append('car')
                i += 1
            elif j < self.station_load_trucks:  
                self.distributed_vehicles.append('truck')
                j += 1

    def distributeRandomly(self):

        cars = ['car'] * self.station_load_cars
        trucks = ['truck'] * self.station_load_trucks
        combined = cars + trucks
        random.shuffle(combined)  
        self.distributed_vehicles = combined


    def stationRun(self, name, type, arriving_time, charge_duration):
        if type==1:
            vehicle = self.ev.createCar(name, arriving_time, charge_duration)
        else:
            vehicle = self.ev.createTruck(name, arriving_time, charge_duration)
            
        yield self.env.timeout(arriving_time)

        desired_power = vehicle['needed_energy']*self.multiplier

        if type != 1:
            percent_of_usage = int(self.modules_quantity * 0.65)
            
            power_assumption = percent_of_usage*self.module_power 
            if power_assumption < desired_power:
                desired_power = power_assumption
                charge_duration=self.ev.manageTruck(vehicle['needed_energy'], power_assumption)

        available_grid = self.grid.checkGridState()
        available_station, available_slot = self.checkStationAvailability(desired_power, type)
        available_battery = self.battery.checkBatteryState()
        lower_limit = self.battery.getLower()

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
                self.battery.chargeBattery(available_grid, available_battery, power_to_return)
                battery_power_demand = 0

            elif desired_power > available_grid:

                battery_power_demand = desired_power - available_grid
                energy_demand = battery_power_demand * (1/self.multiplier)
                print(f"Energy demanded {energy_demand}, available battery {available_battery - lower_limit}")

                if  energy_demand > available_battery or (available_battery-energy_demand) < lower_limit:

                    print("Module managing")

                    battery_to_use = (available_battery - lower_limit)*self.multiplier
                    demanded = desired_power - battery_to_use - available_grid

                    print(f"Power demanded from modules: {demanded}")

                    power_to_attach = self.modules.checkModuleToDetach(demanded, self.car_priorities)
                    max_power = power_to_attach + battery_to_use + available_grid
                    if max_power != desired_power:
                        charge_duration = int((vehicle['needed_energy'] / max_power) * 60)
                        print(f"New charging time {charge_duration}")

                    print(f"Charging with grid {available_grid} kW battery: {battery_power_demand} kW modules: {power_to_attach} kW")

                    battery_power_demand = battery_to_use #update to battery state
                else:

                    print("Battery managing")
                    battery_power_demand = desired_power - available_grid
                    print(f"Charging with grid {available_grid} kW and battery {battery_power_demand} kW")

            self.battery.updateBattery(battery_power_demand, False)
            self.grid.updateGridState(available_grid, False)
            power_to_return=available_grid
            

            self.car_priorities.append(vehicle)
            with self.chargers[available_station].request() as req:
                yield req  
                print(f"[{self.env.now}] Vehicle {name} starts charging at charger {available_station} slot {available_slot}")
                charge_duration = self.modules.checkIfModuleDetached(vehicle, charge_duration, self.car_priorities)
                yield self.env.timeout(charge_duration)   
                print(f"[{self.env.now}] Vehicle {name} finished charging at charger {available_station} slot {available_slot}")
                self.grid.updateGridState(power_to_return, True)
            
            
        else:
            print(f"{name} is waiting in queue...")
            self.car_queue.append(vehicle)
            return 
        vehicle['charge_duration'] = charge_duration
        self.updateData(charge_duration, arriving_time, type, vehicle)
        self.car_priorities.remove(vehicle)
        
                    
    def checkStationAvailability(self, desired_power, type):
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


    def updateData(self, charging_time, arrived_at, type, vehicle):
        self.battery.insertDataToTable()
        self.grid.insertDataToTable()
        self.charging_times.append(charging_time)
        if type == 1:
            self.charging_times_cars.append(charging_time)
        else:
            self.charging_times_trucks.append(charging_time)
        self.type_time[self.env.now] = vehicle
        self.arrival_time.append(self.env.now)