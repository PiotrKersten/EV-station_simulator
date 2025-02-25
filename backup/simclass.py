import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Station:
    def __init__(self, env):
        self.env = env
        self.grid_power = 300  
        self.battery_capacity = 645  # 80%
        self.battery_max = 645
        self.chargers = [simpy.Resource(env, capacity=2) for _ in range(4)]
        self.car_queue = []  
        self.modules = {i: [37.5] * 4 for i in range(8)}  
        self.car_priorities = []
        
        # Data for plotting
        self.grid_power_data = []
        self.battery_capacity_data = []
        self.charging_times_data = []

        #Sim parameters
        self.time_between = random.randint(5, 15)
        self.desired_charging_time = 15
        self.station_load = 100
        self.time_table = []
        self.energy_table = []
        self.insertSimulationParameter()
        self.env.process(self.run())  

    def run(self):
        for i in range(self.station_load):
            yield self.env.timeout(self.time_between)
            self.time_table.append(self.time_between)
            self.env.process(self.car(f'Car {i}', i * 1, self.desired_charging_time)) 

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
        desired_power = car["needed_energy"] * 4
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

                if battery_power_demand * 0.25 > self.battery_capacity:
                    battery_power_demand = self.battery_capacity * 4
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
        print(f"Battery state: { self.battery_capacity} kWh power ready: {self.battery_capacity*4} kW")
        return self.battery_capacity


    def updateBattery(self, power_cut, flag):
        if flag:
            self.battery_capacity = self.battery_capacity + power_cut*0.25
            if self.battery_capacity > self.battery_max: 
                self.battery_capacity = self.battery_max
        else:
            self.battery_capacity = self.battery_capacity - power_cut*0.25
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

    def insertSimulationParameter(self):
        root = tk.Tk()
        root.title("Simulation Parameters")
        root.geometry("400x400")  # Ustawienie rozmiaru okna

        font = ('Helvetica', 14)

        frame1 = tk.Frame(root)
        frame1.pack(pady=10)

        frame2 = tk.Frame(root)
        frame2.pack(pady=10)

        frame3 = tk.Frame(root)
        frame3.pack(pady=10)

        tk.Label(frame1, text="EVs quantity for simulation", font=font).pack()
        entry1 = tk.Entry(frame1)
        entry1.pack()

        tk.Label(frame2, text="Desired charging time", font=font).pack()
        entry2 = tk.Entry(frame2)
        entry2.pack()

        tk.Label(frame3, text="Generate EV arriving time from:", font=font).pack()
        entry3 = tk.Entry(frame3)
        entry3.pack()

        tk.Label(frame3, text="to:", font=font).pack()
        entry4 = tk.Entry(frame3)
        entry4.pack()

        def save_values():
            try:
                self.time_between = random.randint(int(entry3.get()), int(entry4.get()))
                self.desired_charging_time = int(entry2.get())  # Jeśli liczba
                self.station_load = int(entry1.get())  # Jeśli liczba
                print("Saved values:", self.time_between, self.desired_charging_time, self.station_load)
                root.destroy()  # Zamknięcie okna
            except ValueError:
                print("Invalid input! Please enter numbers.")

        save_button = tk.Button(root, text="Save", font=('Helvetica', 15), command=save_values, bg="#b2fab4")
        save_button.pack(pady=10)

        close_button = tk.Button(root, text="Close", font=('Helvetica', 15), command=root.destroy, bg="#dfdcdb")
        close_button.pack(pady=10)

        root.mainloop()
        
    def showSimulationParametersWithPlots(self):
        # Create the Tkinter window
        root = tk.Tk()
        root.title("Sim res")

        # Create a frame inside canvas for labels 
        main_frame = tk.Frame(root)
        main_frame.place(x=10, y=10)

        label_frame = tk.Frame(root)
        label_frame.place(x=10, y=100)


        label_frame1 = tk.Frame(root)
        label_frame1.place(x=10, y=600)

        # Create a frame for the close button (at the bottom)
        close_frame = tk.Frame(root)
        close_frame.place(x=100, y=900)

        # Add labels inside the frame
        font = ('Helvetica', 14) 
        font1 = ('Helvetica', 20, 'bold') 

        main_frame_label = tk.Label(main_frame, text="Simulation parameters", font=font1, anchor='w')
        main_frame_label.pack(fill='x', pady=15)

        time_label = tk.Label(label_frame, text=f"Average time between arrivals: {np.average(self.time_table)} [t.u.]", font=font, anchor='w')
        time_label.pack(fill='x', pady=15)

        desired_time_label = tk.Label(label_frame, text=f"Desired charging time: {self.desired_charging_time} [t.u.]", font=font, anchor='w')
        desired_time_label.pack(fill='x', pady=15)

        battery_label = tk.Label(label_frame, text=f"Battery capacity: {self.battery_max} [kWh]", font=font, anchor='w')
        battery_label.pack(fill='x', pady=15)

        car_queue_label = tk.Label(label_frame, text=f"EVs quantity: {self.station_load}", font=font, anchor='w')
        car_queue_label.pack(fill='x', pady=15)

        empty_label = tk.Label(label_frame)
        empty_label.pack(fill='x', pady=15)

        car_enMax_label = tk.Label(label_frame, text=f"Max energy need: {max(self.energy_table)} [kWh]", font=font, anchor='w')
        car_enMax_label.pack(fill='x', pady=15)

        car_enMin_label = tk.Label(label_frame, text=f"Min energy need: {min(self.energy_table)} [kWh]", font=font, anchor='w')
        car_enMin_label.pack(fill='x', pady=15)

        car_enAvg_label = tk.Label(label_frame, text=f"Average energy need: {np.average(self.energy_table)} [kWh]", font=font, anchor='w')
        car_enAvg_label.pack(fill='x', pady=15)

        chargMax_label = tk.Label(label_frame1, text=f"Max charging time: {max(self.charging_times_data)} [t.u.]", font=font, anchor='w')
        chargMax_label.pack(fill='x', pady=15)

        chargMin_label = tk.Label(label_frame1, text=f"Min charging time: {min(self.charging_times_data)} [t.u.]", font=font, anchor='w')
        chargMin_label.pack(fill='x', pady=15)

        chargAvg_label = tk.Label(label_frame1, text=f"Average charging time: {np.average(self.charging_times_data)} [t.u.]", font=font, anchor='w')
        chargAvg_label.pack(fill='x', pady=15)

        # Create a frame for the plots
        plot_frame = tk.Frame(root)
        plot_frame.pack(side=tk.RIGHT, padx=10)

        # Plot data
        fig, axes = plt.subplots(3, 1, figsize=(10, 15))

        axes[0].plot(self.grid_power_data, label="Grid Power (kW)")
        axes[0].set_xlabel('Time (t.u.)')
        axes[0].xaxis.set_label_coords(0.95, -0.1)
        axes[0].set_ylabel('Grid power (kW)')
        axes[0].set_title('Grid power over time')
        axes[0].legend()

        axes[1].plot(self.battery_capacity_data, label="Battery Capacity (kWh)", color='orange')
        axes[1].set_xlabel('Time (t.u.)')
        axes[1].xaxis.set_label_coords(0.95, -0.1)
        axes[1].set_ylabel('Battery capacity (kWh)')
        axes[1].set_title('Capacity over time')
        axes[1].legend()

        axes[2].hist(self.charging_times_data, bins=20, edgecolor='black')
        axes[2].set_xlabel('Time (t.u.)')
        axes[2].xaxis.set_label_coords(0.95, -0.1)
        axes[2].set_ylabel('Vehicles quantity')
        axes[2].set_title('Charging time distribution')

        plt.tight_layout()

        # Create a canvas to display the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        # Button to close the window (positioned at the bottom)
        close_button = tk.Button(close_frame, text="Close", font=('Helvetica', 15), command=root.destroy, bg="#dfdcdb")
        close_button.pack(side=tk.BOTTOM, pady=10)

        # Start Tkinter loop
        root.mainloop()


        
if __name__=="__main__":
    env = simpy.Environment()
    chargingStation = Station(env)
    env.run()

    chargingStation.showSimulationParametersWithPlots()