import matplotlib.pyplot as plt
import numpy as np
from tkinter import filedialog 
import os
import sys
from datetime import date
import webbrowser  
import json  
from customtkinter import *




from CTkMenuBar import *
from PIL import Image
from CTkMenuBar import CTkMenuBar


from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self):
        self.flag = 0
        self.after_ids = []
        self.path = self.getImagePath("Motus.ico")
        self.motus_logo_png_path = self.getImagePath("Motus Open Remote Logo.png")

        self.dark_royal_blue = "#00194b"
        self.britisch_racing_green = "#004c54"
        self.min_lime = "#279D91"
        self.white = "#f7f7ee"
        self.action_blue = "#005ca6"
        self.soft_maranello = "#C1B72F"
        self.dark_grey = "#333938"

        self.tittle_font = ("Helvetica", 22, "bold")
        self.entry_font = ("Helvetica", 18)
        self.note_font = ("Helvetica", 14)
        self.save_button_font = ("Helvetica", 20, "bold")

        hidden = CTk()
        hidden.protocol("WM_DELETE_WINDOW", lambda: self.close(hidden))
        hidden.iconbitmap(self.path)
        hidden.withdraw()
    
    def insertSimulationParameter(self):
        
        #Default values
        self.default_station_load_cars = 100
        self.default_station_load_trucks = 20
        self.default_charging_time = 20
        self.default_time_from = 1
        self.default_time_to = 5
        self.default_battery_capacity = 645
        self.default_average_time = 14
        self.default_grid_power = 300
        self.default_chargers_quantity = 4
        self.default_modules_quantity = 8
        self.default_slots_quantity = 2
        self.default_chargers_power = 300
        self.result = []  



        self.root = CTkToplevel()
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.close(self.root))
        self.root.iconbitmap(self.path)


        # Configs
        self.root.title("EV station simulator")
        self.root.state('zoomed')
        self.root.configure(fg_color=self.britisch_racing_green)



        self.root.grid_columnconfigure(0, weight=2)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=2)

        self.root.grid_rowconfigure(1, weight=2)
        self.root.grid_rowconfigure(2, weight=4)
        self.root.grid_rowconfigure(3, weight=2)

        # Menu bar
        self.createMenuBar(self.root, False)

        # Frames
        image_frame = CTkFrame(self.root, fg_color=self.britisch_racing_green)
        image_frame.grid(row=3, column=0, padx=10, pady=(30, 10), sticky="nsew")

        text_frame1 = CTkFrame(self.root, fg_color=self.min_lime, border_color=self.white, border_width=1) 
        text_frame1.grid(row=1, column=0, padx=10, pady=15, sticky="nsew")
        text_frame1.grid_rowconfigure(0, weight=1)  
        text_frame1.grid_columnconfigure(0, weight=1)

        text_frame2 = CTkFrame(self.root, fg_color=self.min_lime, border_color=self.white, border_width=1) 
        text_frame2.grid(row=1, column=1, padx=10, pady=15, sticky="nsew")
        text_frame2.grid_rowconfigure(0, weight=1)
        text_frame2.grid_columnconfigure(0, weight=1)

        text_frame3 = CTkFrame(self.root, fg_color=self.min_lime, border_color=self.white, border_width=1) 
        text_frame3.grid(row=1, column=2, padx=10, pady=15, sticky="nsew")
        text_frame3.grid_rowconfigure(0, weight=1)
        text_frame3.grid_columnconfigure(0, weight=1)

        input_frame1 = CTkFrame(self.root, fg_color=self.min_lime, border_color=self.white, border_width=1)
        input_frame1.grid(row=2, column=0, padx=10, pady=(15, 10), sticky="nsew")


        input_frame2 = CTkFrame(self.root, fg_color=self.min_lime, border_color=self.white, border_width=1)
        input_frame2.grid(row=2, column=1, padx=10, pady=(15, 10), sticky="nsew")


        input_frame3 = CTkFrame(self.root, fg_color=self.min_lime, border_color=self.white, border_width=1)
        input_frame3.grid(row=2, column=2, padx=10, pady=(15, 10), sticky="nsew")

        # Images
        motus_logo = Image.open(self.motus_logo_png_path)

        ctk_motus_logo = CTkImage(light_image=motus_logo, dark_image=motus_logo, size=(500, 125))


        # Labels
        image_label = CTkLabel(image_frame, image=ctk_motus_logo, text="") 
        image_label.grid(row=0, column=0, padx=10, pady=10)  

        text_label1 = CTkLabel(text_frame1, text="Quantities", text_color=self.white, font=self.tittle_font)
        text_label1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 

        text_label2 = CTkLabel(text_frame2, text="Electrical parameters", text_color=self.white, font=self.tittle_font)
        text_label2.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 

        text_label3 = CTkLabel(text_frame3, text="Time parameters", text_color=self.white, font=self.tittle_font)
        text_label3.grid(row=0, column=0, padx=10, pady=10, sticky="nsew") 

        # Quantities
        distribution_label= CTkLabel(input_frame1, text="Vehicles distribution", text_color=self.white, font=self.entry_font)
        distribution_label.grid(row=0, column=1, padx=10, pady=(10,1), sticky="nw")
        self.distribution = CTkComboBox(input_frame1, values=["Normal", "Random"], text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, dropdown_fg_color=self.white, border_width=1, width=200)
        self.distribution.grid(row=1, column=1, padx=10, pady=(3,14), sticky="nw")


        cars_quantity_label = CTkLabel(input_frame1, text="Cars quantity", text_color=self.white, font=self.entry_font)
        cars_quantity_label.grid(row=0, column=0, padx=10, pady=(10,1), sticky="nw")
        self.cars_quantity_entry = CTkEntry(input_frame1, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.cars_quantity_entry.insert(0, self.default_station_load_cars)
        self.cars_quantity_entry.grid(row=1, column=0, padx=10, pady=(3,14), sticky="nw")

        trucks_quantity_label = CTkLabel(input_frame1, text="Trucks quantity", text_color=self.white, font=self.entry_font)
        trucks_quantity_label.grid(row=2, column=0, padx=10, pady=1, sticky="nw")
        self.trucks_quantity_entry = CTkEntry(input_frame1, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.trucks_quantity_entry.insert(0, self.default_station_load_trucks)
        self.trucks_quantity_entry.grid(row=3, column=0, padx=10, pady=(3,14), sticky="nw")

        chargers_quantity_label = CTkLabel(input_frame1, text="Chargers quantity", text_color=self.white, font=self.entry_font)
        chargers_quantity_label.grid(row=4, column=0, padx=10, pady=1, sticky="nw")
        self.chargers_quantity_entry = CTkEntry(input_frame1, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.chargers_quantity_entry.insert(0, self.default_chargers_quantity)
        self.chargers_quantity_entry.grid(row=5, column=0, padx=10, pady=(3,14), sticky="nw")

        modules_quantity_label = CTkLabel(input_frame1, text="Modules per charger quantity", text_color=self.white, font=self.entry_font)
        modules_quantity_label.grid(row=6, column=0, padx=10, pady=1, sticky="nw")
        self.modules_quantity_entry = CTkEntry(input_frame1, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.modules_quantity_entry.insert(0, self.default_modules_quantity)
        self.modules_quantity_entry.grid(row=7, column=0, padx=10, pady=(3,14), sticky="nw")

        slots_quantity_label = CTkLabel(input_frame1, text="Slots per charger quantity", text_color=self.white, font=self.entry_font)
        slots_quantity_label.grid(row=8, column=0, padx=10, pady=1, sticky="nw")
        self.slots_quantity_entry = CTkEntry(input_frame1, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1,  width=200)
        self.slots_quantity_entry.insert(0, self.default_slots_quantity)
        self.slots_quantity_entry.grid(row=9, column=0, padx=10, pady=(3,14), sticky="nw")

        # Electrical parameters
        charger_power_label = CTkLabel(input_frame2, text="Charger power [kW]", text_color=self.white, font=self.entry_font)
        charger_power_label.grid(row=0, column=0, padx=10, pady=(10,1), sticky="nw")
        self.charger_power_entry = CTkEntry(input_frame2, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.charger_power_entry.insert(0, self.default_chargers_power)
        self.charger_power_entry.grid(row=1, column=0, padx=10, pady=(3,14), sticky="nw")

        battery_capacity_label = CTkLabel(input_frame2, text="Battery capacity [kWh]", text_color=self.white, font=self.entry_font)
        battery_capacity_label.grid(row=2, column=0, padx=10, pady=1, sticky="nw")
        self.battery_capacity_entry = CTkEntry(input_frame2, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.battery_capacity_entry.insert(0, self.default_battery_capacity)
        self.battery_capacity_entry.grid(row=3, column=0, padx=10, pady=(3,14), sticky="nw")

        grid_power_label = CTkLabel(input_frame2, text="Grid power [kW]", text_color=self.white, font=self.entry_font)
        grid_power_label.grid(row=4, column=0, padx=10, pady=1, sticky="nw")
        self.grid_power_entry = CTkEntry(input_frame2, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.grid_power_entry.insert(0, self.default_grid_power)
        self.grid_power_entry.grid(row=5, column=0, padx=10, pady=(3,14), sticky="nw")


        # Time parameters
        charging_time_label = CTkLabel(input_frame3, text="Desired charging time [t.u]", text_color=self.white, font=self.entry_font)
        charging_time_label.grid(row=0, column=0, padx=10, pady=(10,1), sticky="nw")
        self.charging_time_entry = CTkEntry(input_frame3, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.charging_time_entry.insert(0, self.default_charging_time)
        self.charging_time_entry.grid(row=1, column=0, padx=10, pady=(3,14), sticky="nw")

        average_time_label = CTkLabel(input_frame3, text="Average arriving time [t.u]*", text_color=self.white, font=self.entry_font)
        average_time_label.grid(row=2, column=0, padx=10, pady=1, sticky="nw")
        self.average_time_entry = CTkEntry(input_frame3, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=200)
        self.average_time_entry.insert(0, self.default_average_time)
        self.average_time_entry.grid(row=3, column=0, padx=10, pady=(3,14), sticky="nw")


        time_range_label1 = CTkLabel(input_frame3, text="Generate ev arriving time instead of giving average [t.u.]", text_color=self.white, font=self.entry_font)
        time_range_label1.grid(row=4, column=0, padx=10, pady=1, sticky="nw")

        time_from_label = CTkLabel(input_frame3, text="from", text_color=self.white, font=self.entry_font)
        time_from_label.grid(row=5, column=0, padx=(10,0), pady=1, sticky="w")
        self.time_from_entry = CTkEntry(input_frame3, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=70)
        self.time_from_entry.insert(0, self.default_time_from)
        self.time_from_entry.grid(row=5, column=0, padx=(60,0), pady=(3,14), sticky="nw")

        time_to_label = CTkLabel(input_frame3, text="to ", text_color=self.white, font=self.entry_font)
        time_to_label.grid(row=5, column=0, padx=(140, 0), pady=1, sticky="w")
        self.time_to_entry = CTkEntry(input_frame3, text_color=self.white, fg_color=self.britisch_racing_green, border_color=self.white, border_width=1, width=70)
        self.time_to_entry.insert(0, self.default_time_to)
        self.time_to_entry.grid(row=5, column=0, padx=(170, 0), pady=(3,14), sticky="nw")

        note_label1 = CTkLabel(input_frame3, text="*If 0 [t.u] inserted, simulator will generate arriving time between interval inserted above", text_color=self.white, font=self.note_font)
        note_label1.grid(row=6, column=0, padx=10, pady=(150,0), sticky="nw")

        # Save button
        save_button = CTkButton(self.root, text="Save", text_color=self.white, font=self.save_button_font, fg_color=self.action_blue, hover_color=self.dark_royal_blue, border_color=self.white, border_width=2 ,command=lambda:self.saveValues(), width=250, height=70)
        save_button.grid(row=3, column=2, padx=10, pady=(40, 10), sticky="n")
        self.root.mainloop()
        
        return self.result
    
    def saveValues(self):
        try:
            station_load_cars = int(self.cars_quantity_entry.get()) 
            station_load_trucks = int(self.trucks_quantity_entry.get()) 
            chargers_quantity = int(self.chargers_quantity_entry.get())
            modules_quantity = int(self.modules_quantity_entry.get())
            slots_quantity = int(self.slots_quantity_entry.get())
            how_to_generate = self.distribution.get()
            if how_to_generate == "Random":
                generation_choice = False
            else:
                generation_choice = True

            chargers_power = int(self.charger_power_entry.get())
            battery_capacity = int(self.battery_capacity_entry.get())
            grid_power = int(self.grid_power_entry.get())

            desired_charging_time = int(self.charging_time_entry.get()) 
            average_time = int(self.average_time_entry.get())
            time_from = int(self.time_from_entry.get())
            time_to = int(self.time_to_entry.get())
            
            
            print("Values saved")
            
            self.result.extend([
                time_from, 
                time_to, 
                station_load_cars, 
                station_load_trucks, 
                desired_charging_time, 
                battery_capacity, grid_power, 
                average_time, 
                chargers_quantity,
                modules_quantity,
                slots_quantity,
                chargers_power, 
                generation_choice
            ])

        except ValueError:
            print("Invalid input! Generic values inserted.")
            self.result.extend([
                self.default_time_from, 
                self.default_time_to, 
                self.default_station_load_cars, 
                self.default_station_load_trucks, 
                self.default_charging_time, 
                self.default_battery_capacity, 
                self.default_grid_power, 
                self.default_average_time, 
                self.default_chargers_quantity, 
                self.default_chargers_power, 
                self.default_modules_quantity,
                generation_choice
            ])
        self.close(self.root)

    def close(self, root):
        print("Closing window...")
        self.flag = 0
        root.quit()
        root.destroy()

        print("Window closed.")
        
    def showSimulationParametersWithPlots(self, battery_max, time_table, energy_table, station_load, desired_charging_time, charging_times_data, grid_power_data, battery_capacity_data, charging_times_cars, charging_times_trucks, station_load_cars, station_load_trucks, arrival_times, type_time):
        self.battery_capacity = battery_max
        self.time_table = time_table
        self.energy_table = energy_table
        self.station_load = station_load
        self.desired_charging_time = desired_charging_time
        self.charging_times = charging_times_data
        self.grid_power_data = grid_power_data
        self.battery_capacity_data = battery_capacity_data
        self.charging_times_cars = charging_times_cars
        self.charging_times_trucks = charging_times_trucks
        self.station_load_cars = station_load_cars 
        self.station_load_trucks = station_load_trucks
        self.arrival_times = arrival_times  
        self.type_time = type_time

        self.app = CTkToplevel()
        self.app.protocol("WM_DELETE_WINDOW", lambda: self.close(self.app))

        self.app.iconbitmap(self.path)

        self.app.title("EV station simulator")
        self.app.state('zoomed')
        self.app.configure(fg_color=self.britisch_racing_green)

        self.app.grid_columnconfigure(0, weight=2)  
        self.app.grid_columnconfigure(1, weight=1) 
        self.app.grid_columnconfigure(2, weight=7) 

        self.app.grid_rowconfigure(1, weight=1)
        self.app.grid_rowconfigure(2, weight=1)
        self.app.grid_rowconfigure(3, weight=1)

        self.app.grid_rowconfigure(4, weight=1)
        
        self.createMenuBar(self.app, True)

        #Frames
        text_frame1 = CTkFrame(self.app, fg_color=self.min_lime, border_color=self.white, border_width=2) 
        text_frame1.grid(row=1, column=0, padx=10, pady=(15, 10), sticky="nsew")
        text_frame1.grid_rowconfigure(0, weight=1)  
        text_frame1.grid_columnconfigure(0, weight=1)

        inputs_frame = CTkFrame(self.app, fg_color=self.min_lime, border_color=self.white, border_width=2)
        inputs_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        text_frame2 = CTkFrame(self.app, fg_color=self.min_lime, border_color=self.white, border_width=2) 
        text_frame2.grid(row=3, column=0, padx=10, pady=(15, 10), sticky="nsew")
        text_frame2.grid_rowconfigure(0, weight=1)
        text_frame2.grid_columnconfigure(0, weight=1)

        result_frame = CTkFrame(self.app, fg_color=self.min_lime, border_color=self.white, border_width=2)
        result_frame.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")

        plot_frame = CTkFrame(self.app, fg_color=self.min_lime, border_color=self.white, border_width=2)
        plot_frame.grid(row=1, column=2, rowspan=4, padx=10, pady=10, sticky="nsew")
        plot_frame.grid_rowconfigure(0, weight=4)  
        plot_frame.grid_columnconfigure(0, weight=1)


        input_frame_label = CTkLabel(text_frame1, text="Simulation parameters", text_color=self.white, font=self.tittle_font)
        input_frame_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        average_time_label = CTkLabel(inputs_frame, text=f"Average time between arrivals: {round(np.average(self.time_table), 2)} [t.u.]", text_color=self.white, font=self.entry_font)
        average_time_label.grid(row=0, column=0, padx=10, pady=8, sticky="nw")

        desired_charging_time_label = CTkLabel(inputs_frame, text=f"Desired charging time: {round(self.desired_charging_time, 2)} [t.u.]", text_color=self.white, font=self.entry_font)
        desired_charging_time_label.grid(row=1, column=0, padx=10, pady=8, sticky="nw")

        battery_capacity_label = CTkLabel(inputs_frame, text=f"Battery capacity: {round(self.battery_capacity, 2)} [kWh]", text_color=self.white, font=self.entry_font)
        battery_capacity_label.grid(row=2, column=0, padx=10, pady=8, sticky="nw")

        station_load_label = CTkLabel(inputs_frame, text=f"Cars quantity: {self.station_load_cars}", text_color=self.white, font=self.entry_font)
        station_load_label.grid(row=3, column=0, padx=10, pady=8, sticky="nw")

        station_load_label = CTkLabel(inputs_frame, text=f"Trucks quantity: {self.station_load_trucks}", text_color=self.white, font=self.entry_font)
        station_load_label.grid(row=4, column=0, padx=10, pady=8, sticky="nw")

        result_frame_label = CTkLabel(text_frame2, text="Result data", text_color=self.white, font=self.tittle_font)
        result_frame_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")  

        max_energy_label = CTkLabel(result_frame, text=f"Max energy need: {round(max(self.energy_table), 2)} [kWh]", text_color=self.white, font=self.entry_font)
        max_energy_label.grid(row=0, column=0, padx=10, pady=8, sticky="nw")

        min_energy_label = CTkLabel(result_frame, text=f"Min energy need: {round(min(self.energy_table), 2)} [kWh]", text_color=self.white, font=self.entry_font)
        min_energy_label.grid(row=1, column=0, padx=10, pady=8, sticky="nw")

        average_energy_label = CTkLabel(result_frame, text=f"Average energy need: {round(np.average(self.energy_table), 2)} [kWh]", text_color=self.white, font=self.entry_font)
        average_energy_label.grid(row=2, column=0, padx=10, pady=8, sticky="nw")

        max_charging_time_label = CTkLabel(result_frame, text=f"Max charging time: {round(max(self.charging_times), 2)} [t.u.]", text_color=self.white, font=self.entry_font)
        max_charging_time_label.grid(row=3, column=0, padx=10, pady=8, sticky="nw")

        min_charging_time_label = CTkLabel(result_frame, text=f"Min charging time: {round(min(self.charging_times), 2)} [t.u.]", text_color=self.white, font=self.entry_font)
        min_charging_time_label.grid(row=4, column=0, padx=10, pady=8, sticky="nw")

        average_charging_time_label = CTkLabel(result_frame, text=f"Average charging time: {round(np.average(self.charging_times), 2)} [t.u.]", text_color=self.white, font=self.entry_font)
        average_charging_time_label.grid(row=5, column=0, padx=10, pady=8, sticky="nw")

        # Plotting
        fig, axes = plt.subplots(4, 1, figsize=(14, 11))
        fig.set_facecolor(self.min_lime)
        min_length = min(len(self.arrival_times), len(self.energy_table))
        arrival_times_synced = self.arrival_times[:min_length]
        energy_table_synced = self.energy_table[:min_length]

        axes[0].plot(self.arrival_times, self.grid_power_data, label="Grid power (kW)", color=self.britisch_racing_green)
        axes[0].set_xlabel('Simulation time (t.u.)', fontsize=10, loc='right', color=self.white) 
        axes[0].set_ylabel('Grid power (kW)', fontsize=10, color=self.white)
        axes[0].tick_params(axis='x', size=8, colors=self.white) 
        axes[0].tick_params(axis='y', size=8, colors=self.white)  
        axes[0].set_title('Grid power over time', fontsize=12, color=self.white)
        axes[0].grid(True)

        max_capacity = max(self.battery_capacity_data)
        lower_limit = 0.2 * self.battery_capacity
        axes[1].plot(self.arrival_times, self.battery_capacity_data, label="Battery capacity (kWh)", color=self.soft_maranello)
        axes[1].set_xlabel('Simulation time (t.u.)', fontsize=10, loc='right', color=self.white)  
        axes[1].set_ylabel('Battery capacity (kWh)', fontsize=10, color=self.white)  
        axes[1].tick_params(axis='x', size=8, colors=self.white) 
        axes[1].tick_params(axis='y', size=8, colors=self.white) 
        axes[1].set_title('Capacity over time', fontsize=12, color=self.white)
        axes[1].axhline(y=max_capacity, color='red', linestyle='dashed', linewidth=1, label=f'Upper limit 80%')
        axes[1].axhline(y=lower_limit, color='blue', linestyle='dashed', linewidth=1, label=f'Lower limit 20%')
        axes[1].legend(fontsize=9) 
        axes[1].grid(True)


        keys = list(self.type_time.keys())
        charge_duration = [entry['charge_duration'] for entry in self.type_time.values()]
        vehicle_types = ['Car' if 'Car' in entry['name'] else 'Truck' for entry in self.type_time.values()]
        car_keys = [keys[i] for i in range(len(keys)) if vehicle_types[i] == 'Car']
        cars_charge_duration= [charge_duration[i] for i in range(len(charge_duration)) if vehicle_types[i] == 'Car']
        truck_keys = [keys[i] for i in range(len(keys)) if vehicle_types[i] == 'Truck']
        trucks_charge_duration = [charge_duration[i] for i in range(len(charge_duration)) if vehicle_types[i] == 'Truck']

        axes[2].bar(
            car_keys, 
            cars_charge_duration, 
            label='Cars', 
            color=self.action_blue, 
            alpha=0.7, 
            width=9.0, 
            align='center'
        )
        axes[2].bar(
            truck_keys, 
            trucks_charge_duration, 
            label='Trucks', 
            color=self.soft_maranello, 
            alpha=0.7, 
            width=9.0, 
            align='center'
        )
        axes[2].set_xlabel('Simulation time (t.u.)', fontsize=10, loc='right', color=self.white)
        axes[2].set_ylabel('Charging time (t.u.)', fontsize=10, color=self.white)  
        axes[2].tick_params(axis='x', size=8, colors=self.white) 
        axes[2].tick_params(axis='y', size=8, colors=self.white) 
        axes[2].set_title('Charging time distribution', fontsize=12, color=self.white)
        axes[2].legend(fontsize=9) 
        axes[2].grid(True)
        


        axes[3].bar(
            arrival_times_synced, 
            energy_table_synced, 
            label="Energy needs (kWh)", 
            color=self.britisch_racing_green, 
            alpha=0.7, 
            width=9.0,  
            align='center'
        )
        axes[3].set_xlabel("Simulation time (t.u.)", fontsize=10, loc='right', color=self.white)
        axes[3].set_ylabel('Energy (kWh)', fontsize=10, color=self.white)
        axes[3].tick_params(axis='x', size=8, colors=self.white) 
        axes[3].tick_params(axis='y', size=8, colors=self.white) 
        axes[3].set_title("Energy needs over time", fontsize=12, color=self.white)
        axes[3].grid(True)
        axes[3].legend(fontsize=9) 

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0,  padx=3, pady=3, sticky="nsew")

        self.plot_canvas = canvas
        self.plot_figure = fig
        
        self.app.mainloop()

    def createMenuBar(self, root, option=True):
        menu = CTkMenuBar(master=root, bg_color=self.dark_grey, height=15)
        menu.grid(row=0, columnspan=3, padx=0, pady=0, sticky="ew")
        match option:
            case True:
                button_1= menu.add_cascade("File", fg_color=self.dark_grey, text_color=self.white)
                dropdown1 = CustomDropdownMenu(widget=button_1, bg_color=self.britisch_racing_green, fg_color=self.britisch_racing_green, border_color=self.britisch_racing_green, text_color=self.white, hover_color=self.dark_royal_blue)
                dropdown1.add_option(option="Save", command=lambda: self.saveFile())

                button_2= menu.add_cascade("Edit", fg_color=self.dark_grey, text_color=self.white)
                dropdown2 = CustomDropdownMenu(widget=button_2, bg_color=self.britisch_racing_green, fg_color=self.britisch_racing_green, border_color=self.britisch_racing_green, text_color=self.white, hover_color=self.dark_royal_blue)
                dropdown2.add_option(option="Restart simulation", command=lambda: self.restart(root))
                dropdown2.add_option(option="Close simulation", command=lambda: self.close(root))

                button_3= menu.add_cascade("Help", fg_color=self.dark_grey, text_color=self.white)
                dropdown3 = CustomDropdownMenu(widget=button_3, bg_color=self.britisch_racing_green, fg_color=self.britisch_racing_green, border_color=self.britisch_racing_green, text_color=self.white, hover_color=self.dark_royal_blue)
                dropdown3.add_option(option="Documenation", command=lambda: self.showHelp())
            case False:
                button_3= menu.add_cascade("Help", fg_color=self.dark_grey, text_color=self.white)
                dropdown3 = CustomDropdownMenu(widget=button_3, bg_color=self.britisch_racing_green, fg_color=self.britisch_racing_green, border_color=self.britisch_racing_green, text_color=self.white, hover_color=self.dark_royal_blue)
                dropdown3.add_option(option="Documenation", command=lambda: self.showHelp())

    def saveFile(self):
        try:
            initial_filename = f"t{self.station_load_trucks}c{self.station_load_cars}_{date.today()}.png"
            plot_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG files", "*.png")],
                initialfile=initial_filename,
                title="Save Plot"
            )
            if plot_path:
                plt.savefig(plot_path)
                print(f"Plots saved as '{plot_path}'")
            else:
                print("Plot save canceled.")
        except Exception as e:
            print(f"Error saving plots: {e}")

        try:
            initial_filename = f"t{self.station_load_trucks}c{self.station_load_cars}_{date.today()}.json"
            json_path = filedialog.asksaveasfilename(
                defaultextension=".json",
                filetypes=[("JSON files", "*.json")],
                initialfile=initial_filename,
                title="Save Data"
            )
            if json_path:
                base, ext = os.path.splitext(json_path)
                counter = 1
                while os.path.exists(json_path):
                    json_path = f"{base}_{counter}{ext}"
                    counter += 1

                data = {
                    "Input Data": {
                        "Battery Capacity (kWh)": self.battery_capacity,
                        "Average Time Between Arrivals (t.u.)": round(np.average(self.time_table), 2),
                        "Desired Charging Time (t.u.)": self.desired_charging_time,
                        "Total Vehicles": self.station_load,
                        "Cars Quantity": self.station_load_cars,
                        "Trucks Quantity": self.station_load_trucks
                    },
                    "Result Data": {
                        "Max Energy Need (kWh)": round(max(self.energy_table), 2),
                        "Min Energy Need (kWh)": round(min(self.energy_table), 2),
                        "Average Energy Need (kWh)": round(np.average(self.energy_table), 2),
                        "Max Charging Time (t.u.)": round(max(self.charging_times), 2),
                        "Min Charging Time (t.u.)": round(min(self.charging_times), 2),
                        "Average Charging Time (t.u.)": round(np.average(self.charging_times), 2)
                    }
                }

                with open(json_path, "w") as file:
                    json.dump(data, file, indent=4)
                print(f"Parameters saved as '{json_path}'")
            else:
                print("Data save canceled.")
        except Exception as e:
            print(f"Error saving parameters: {e}")

    def restart(self, root):
        root.quit()
        root.destroy()
        self.flag = 1

    def close(self, root):
        root.quit()
        root.destroy()
        self.flag = 0

    def showHelp(self):
        webbrowser.open("https://github.com/PiotrKersten/EV-station_simulator/blob/main/dev/helper/Simulator%20manual.pdf") 
    def getFlag(self):
        return self.flag
    
    def getImagePath(self, filename):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  
        else:
            base_path = os.path.dirname(__file__)  

        return os.path.join(base_path, filename)