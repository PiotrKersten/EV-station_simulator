import matplotlib.pyplot as plt
import numpy as np
from tkinter import PhotoImage
import os
import seaborn as sns
from PIL import Image, ImageTk
import sys

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self):
        self.flag = 0
        self.path = self.get_image_path("Motus.ico")
        
    def insertSimulationParameter(self):
        root = tk.Tk()
        root.title("Simulation Parameters")
        root.geometry("700x750") 

        root.iconbitmap(self.path)


        text_font = ('Helvetica', 14)
        font = ('Helvetica', 11)

        text_frame1 = tk.Frame(root)
        text_frame1.pack(pady=10)

        frame1 = tk.Frame(root, relief="ridge", bd=2)
        frame1.pack(pady=10)

        text_frame2 = tk.Frame(root)
        text_frame2.pack(pady=10)

        frame2 = tk.Frame(root, relief="ridge", bd=2)
        frame2.pack(pady=10)

        text_frame3 = tk.Frame(root)
        text_frame3.pack(pady=10)

        frame3 = tk.Frame(root, relief="ridge", bd=2)
        frame3.pack(pady=10)

        frame4 = tk.Frame(root, relief="ridge", bd=2)
        frame4.pack(pady=10)

        # Set default values here
        default_station_load_cars = 80
        default_station_load_trucks = 0
        default_charging_time = 15
        default_time_from = 1
        default_time_to = 5
        default_battery_capacity = 645
        default_average_time = 14
        default_grid_power = 300
        default_chargers_quantity = 4
        default_chargers_power = 300

        tk.Label(text_frame1, text="Quantities", font=text_font).pack()

        tk.Label(frame1, text="Electric cars quantity", font=font).pack()
        entry1 = tk.Entry(frame1)
        entry1.insert(0, default_station_load_cars) 
        entry1.pack()
    
        tk.Label(frame1, text="Electric trucks quantity", font=font).pack()
        entry12 = tk.Entry(frame1)
        entry12.insert(0, default_station_load_trucks) 
        entry12.pack()

        tk.Label(frame1, text="Chargers quantity", font=font).pack()
        entry13 = tk.Entry(frame1)
        entry13.insert(0, default_chargers_quantity) 
        entry13.pack()



        tk.Label(text_frame2, text="Electrical parameters", font=text_font).pack()
    
        tk.Label(frame2, text="Single charger power [kW]:", font=font).pack()
        entry14 = tk.Entry(frame2)
        entry14.insert(0, default_chargers_power) 
        entry14.pack()

        tk.Label(frame2, text="Battery capacity [kWh]:", font=font).pack()
        entry5 = tk.Entry(frame2)
        entry5.insert(0, default_battery_capacity)
        entry5.pack()
        
        tk.Label(frame2, text="Grid power [kW]:", font=font).pack()
        entry51 = tk.Entry(frame2)
        entry51.insert(0, default_grid_power)
        entry51.pack()


        tk.Label(text_frame3, text="Time parameters", font=text_font).pack()

        tk.Label(frame3, text="Desired charging time [t.u]:", font=font).pack()
        entry2 = tk.Entry(frame3)
        entry2.insert(0, default_charging_time)  
        entry2.pack()

        tk.Label(frame3, text="Give average time [t.u]:", font=font).pack()
        entry41 = tk.Entry(frame3)
        entry41.insert(0, default_average_time) 
        entry41.pack()

        tk.Label(frame3, text="\nGenerate EV arriving time (alternatively):", font=font).pack()

        tk.Label(frame3, text="from [t.u]:", font=font).pack(side=tk.LEFT)
        entry3 = tk.Entry(frame3, width=6)
        entry3.insert(0, default_time_from)
        entry3.pack(side=tk.LEFT)

        tk.Label(frame3, text=" to [t.u]:", font=font).pack(side=tk.LEFT)
        entry4 = tk.Entry(frame3, width=6)
        entry4.insert(0, default_time_to) 
        entry4.pack(side=tk.LEFT)


        result = []  

        def save_values():
            try:
                time_from = int(entry3.get())
                time_to = int(entry4.get())
                desired_charging_time = int(entry2.get())  
                station_load_cars = int(entry1.get()) 
                station_load_trucks = int(entry12.get()) 
                battery_capacity = int(entry5.get())
                average_time = int(entry41.get())
                grid_power = int(entry51.get())
                chargers_quantity = int(entry13.get())
                chargers_power = int(entry14.get())

                print("Values saved")
                
                result.extend([
                    time_from, time_to, station_load_cars, station_load_trucks, 
                    desired_charging_time, battery_capacity, grid_power, 
                    average_time, chargers_quantity, chargers_power
                ])
                root.quit() 
                root.destroy()

            except ValueError:
                print("Invalid input! Generic values inserted.")
                result.extend([
                    default_time_from, default_time_to, default_station_load_cars, 
                    default_station_load_trucks, default_charging_time, 
                    default_battery_capacity, default_grid_power, 
                    default_average_time, default_chargers_quantity, 
                    default_chargers_power
                ])
                root.quit()
                root.destroy()

        save_button = tk.Button(root, text="Save", font=('Helvetica', 15), command=save_values, bg="#f4fff3")
        save_button.pack(pady=10)
        def close():
            root.quit()  
            root.destroy()
            self.flag = 0
        root.protocol("WM_DELETE_WINDOW", close)
        root.mainloop()

        return result

        
        
    def showSimulationParametersWithPlots(self, battery_max, time_table, energy_table, station_load, desired_charging_time, charging_times_data, grid_power_data, battery_capacity_data):
        root = tk.Tk()
        root.title("Simulation Parameters")
        screen_width = root.winfo_screenwidth()  
        screen_height = root.winfo_screenheight()  
        root.geometry(f"{screen_width}x{screen_height}") 

        root.iconbitmap(self.path)

        main_frame = tk.Frame(root)
        main_frame.place(x=10, y=10)

        label_frame = tk.Frame(root)
        label_frame.place(x=10, y=70)


        label_frame1 = tk.Frame(root)
        label_frame1.place(x=10, y=550)

        close_frame = tk.Frame(root)
        close_frame.place(x=100, y=750)

        font = ('Helvetica', 14) 
        font1 = ('Helvetica', 20, 'bold') 

        main_frame_label = tk.Label(main_frame, text="Simulation parameters", font=font1, anchor='w')
        main_frame_label.pack(fill='x', pady=15)

        time_label = tk.Label(label_frame, text=f"Average time between arrivals: {round(np.average(time_table), 2)} [t.u.]", font=font, anchor='w')
        time_label.pack(fill='x', pady=15)

        desired_time_label = tk.Label(label_frame, text=f"Desired charging time: {round(desired_charging_time, 2)} [t.u.]", font=font, anchor='w')
        desired_time_label.pack(fill='x', pady=15)

        battery_label = tk.Label(label_frame, text=f"Battery capacity: {round(battery_max, 2)} [kWh]", font=font, anchor='w')
        battery_label.pack(fill='x', pady=15)

        car_queue_label = tk.Label(label_frame, text=f"EVs quantity: {station_load}", font=font, anchor='w')
        car_queue_label.pack(fill='x', pady=15)

        empty_label = tk.Label(label_frame)
        empty_label.pack(fill='x', pady=15)

        car_enMax_label = tk.Label(label_frame, text=f"Max energy need: {round(max(energy_table), 2)} [kWh]", font=font, anchor='w')
        car_enMax_label.pack(fill='x', pady=15)

        car_enMin_label = tk.Label(label_frame, text=f"Min energy need: {round(min(energy_table), 2)} [kWh]", font=font, anchor='w')
        car_enMin_label.pack(fill='x', pady=15)

        car_enAvg_label = tk.Label(label_frame, text=f"Average energy need: {round(np.average(energy_table), 2)} [kWh]", font=font, anchor='w')
        car_enAvg_label.pack(fill='x', pady=15)

        chargMax_label = tk.Label(label_frame1, text=f"Max charging time: {round(max(charging_times_data), 2)} [t.u.]", font=font, anchor='w')
        chargMax_label.pack(fill='x', pady=15)

        chargMin_label = tk.Label(label_frame1, text=f"Min charging time: {round(min(charging_times_data), 2)} [t.u.]", font=font, anchor='w')
        chargMin_label.pack(fill='x', pady=15)

        chargAvg_label = tk.Label(label_frame1, text=f"Average charging time: {round(np.average(charging_times_data), 2)} [t.u.]", font=font, anchor='w')
        chargAvg_label.pack(fill='x', pady=15)


        plot_frame = tk.Frame(root)
        plot_frame.pack(side=tk.RIGHT, padx=10)

    
        fig, axes = plt.subplots(4, 1, figsize=(10, 15))

        axes[0].plot(grid_power_data, label="Grid Power (kW)")
        axes[0].set_xlabel('Time (t.u.)')
        axes[0].xaxis.set_label_coords(0.95, -0.1)
        axes[0].set_ylabel('Grid power (kW)')
        axes[0].set_title('Grid power over time')

        max_capacity = max(battery_capacity_data)
        lower_limit = 0.25 * max_capacity # max_capacity = 0.8 * battery_capacity, lower = 0.2* 1.25* max_capacity = 0.25 * max_capacity

        axes[1].plot(battery_capacity_data, label="Battery Capacity (kWh)", color='orange')
        axes[1].axhline(y=max_capacity, color='red', linestyle='dashed', linewidth=1, label=f'Upper limit 80%')
        axes[1].axhline(y=lower_limit, color='blue', linestyle='dashed', linewidth=1, label=f'Lower Limit 20%')

        axes[1].set_xlabel('Time (t.u.)')
        axes[1].xaxis.set_label_coords(0.95, -0.1)
        axes[1].set_ylabel('Battery capacity (kWh)')
        axes[1].set_title('Capacity over time')
        axes[1].legend()

        axes[2].hist(charging_times_data, bins=20, edgecolor='black')
        axes[2].set_xlabel('Time (t.u.)')
        axes[2].xaxis.set_label_coords(0.95, -0.1)
        axes[2].set_ylabel('Vehicles quantity')
        axes[2].set_title('Charging time distribution')

        sns.histplot(energy_table, bins=20, kde=True, ax=axes[3], color='blue', edgecolor='black')
        axes[3].set_xlabel("Energy [kWh]")
        axes[3].xaxis.set_label_coords(0.95, -0.1)
        axes[3].set_ylabel('Count')
        axes[3].set_title("EV's energy needs distribution")


        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

        def close():
            root.quit()  
            root.destroy()
            self.flag = 0

        close_button = tk.Button(close_frame, text="Close", font=('Helvetica', 15), command=close, bg="#dfdcdb")
        close_button.grid(row=0, column=0, padx=10, pady=10) 

        def restart():
            root.quit()  
            root.destroy()
            self.flag = 1

        restart_button = tk.Button(close_frame, text="Restart", font=('Helvetica', 15), command=restart, bg="#dfdcdb")
        restart_button.grid(row=0, column=1, padx=10, pady=10)
        
        root.protocol("WM_DELETE_WINDOW", close)
        root.mainloop()
    
    def getFlag(self):
        return self.flag
    
    def get_image_path(self, filename):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  
        else:
            base_path = os.path.dirname(__file__)  

        return os.path.join(base_path, filename)