import matplotlib.pyplot as plt
import numpy as np
from tkinter import PhotoImage, filedialog  # Import filedialog for file selection
import os
import seaborn as sns
from PIL import Image, ImageTk
import sys
from datetime import date
import webbrowser  
import json  

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class Gui:
    def __init__(self):
        self.flag = 0
        self.path = self.getImagePath("Motus.ico")
        
    def insertSimulationParameter(self):
        root = tk.Tk()
        root.title("Simulation Parameters")
        root.geometry("675x400")  

        root.iconbitmap(self.path)

        text_font = ('Helvetica', 14)
        font = ('Helvetica', 11)
        edit_font = ('Helvetica', 10)

        text_frame1 = tk.Frame(root)
        frame1 = tk.Frame(root, relief="ridge", bd=2)

        text_frame2 = tk.Frame(root)
        frame2 = tk.Frame(root, relief="ridge", bd=2)

        text_frame3 = tk.Frame(root)
        frame3 = tk.Frame(root, relief="ridge", bd=2)

        frame4 = tk.Frame(root)

        text_frame1.grid(row=0, column=0, padx=10, pady=10, sticky="n")
        frame1.grid(row=1, column=0, padx=10, pady=10, sticky="n")

        text_frame2.grid(row=0, column=1, padx=10, pady=10, sticky="n")
        frame2.grid(row=1, column=1, padx=10, pady=10, sticky="n")

        text_frame3.grid(row=0, column=2, padx=10, pady=10, sticky="n")
        frame3.grid(row=1, column=2, padx=10, pady=10, sticky="n")

        frame4.grid(row=2, column=0, columnspan=3, pady=20, sticky="s")  

        # Set default values here
        default_station_load_cars = 100
        default_station_load_trucks = 20
        default_charging_time = 20
        default_time_from = 1
        default_time_to = 5
        default_battery_capacity = 645
        default_average_time = 14
        default_grid_power = 300
        default_chargers_quantity = 4
        default_modules_quantity = 8
        default_slots_quantity = 2
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

        tk.Label(frame1, text="Modules per charger", font=font).pack()
        entry14 = tk.Entry(frame1)
        entry14.insert(0, default_modules_quantity) 
        entry14.pack()

        tk.Label(frame1, text="Slots per charger", font=font).pack()
        entry15 = tk.Entry(frame1, width=8)
        entry15.insert(0, default_slots_quantity) 
        entry15.pack()

        tk.Label(text_frame2, text="Electrical parameters", font=text_font).pack()
    
        tk.Label(frame2, text="Single charger power [kW]:", font=font).pack()
        entry50 = tk.Entry(frame2)
        entry50.insert(0, default_chargers_power) 
        entry50.pack()

        tk.Label(frame2, text="\nBattery capacity [kWh]:", font=font).pack()
        entry5 = tk.Entry(frame2)
        entry5.insert(0, default_battery_capacity)
        entry5.pack()
        
        tk.Label(frame2, text="\nGrid power [kW]:", font=font).pack()
        entry51 = tk.Entry(frame2, width=8)
        entry51.insert(0, default_grid_power)
        entry51.pack()


        tk.Label(text_frame3, text="Time parameters", font=text_font).pack()

        tk.Label(frame3, text="Desired charging time [t.u]:", font=font).pack()
        entry2 = tk.Entry(frame3)
        entry2.insert(0, default_charging_time)  
        entry2.pack()

        tk.Label(frame3, text="\nGive average time [t.u]:", font=font).pack()
        entry41 = tk.Entry(frame3)
        entry41.insert(0, default_average_time) 
        entry41.pack()

        tk.Label(frame3, text="\nGenerate EV arriving time (alternatively):", font=font).pack()

        tk.Label(frame3, text="from [t.u]:", font=edit_font).pack(side=tk.LEFT)
        entry3 = tk.Entry(frame3, width=6)
        entry3.insert(0, default_time_from)
        entry3.pack(side=tk.LEFT)

        tk.Label(frame3, text=" to [t.u]:", font=edit_font).pack(side=tk.LEFT)
        entry4 = tk.Entry(frame3, width=6) 
        entry4.insert(0, default_time_to) 
        entry4.pack(side=tk.LEFT)


        result = []  

        def saveValues():
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
                modules_quantity = int(entry14.get())
                slots_quantity = int(entry15.get())
                chargers_power = int(entry50.get())

                print("Values saved")
                
                result.extend([
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
                    chargers_power
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
                    default_chargers_power, default_modules_quantity
                ])
                root.quit()
                root.destroy()

        save_button = tk.Button(frame4, text="Save", font=('Helvetica', 15), command=saveValues, bg="#f4fff3")
        save_button.pack(pady=10)
        def close():
            root.quit()  
            root.destroy()
            self.flag = 0
        root.protocol("WM_DELETE_WINDOW", close)
        root.mainloop()

        return result
   
    def showSimulationParametersWithPlots(self, battery_max, time_table, energy_table, station_load, desired_charging_time, charging_times_data, grid_power_data, battery_capacity_data, charging_times_cars, charging_times_trucks, station_load_cars, station_load_trucks):
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

        root = tk.Tk()
        root.title("Simulation Parameters")
        root.geometry(f"1800x900")
        root.iconbitmap(self.path)

        self.createMenuBar(root)
        self.createInputFrame(root, 10)
        self.createResultFrame(root, 370)  
        self.createPlotFrame(root)

        root.protocol("WM_DELETE_WINDOW", lambda: self.close(root))
        root.mainloop()

    def createMenuBar(self, root):
        menu_bar = tk.Menu(root)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Save", command=lambda: self.saveFile())
        menu_bar.add_cascade(label="File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Restart simulation", command=lambda: self.restart(root))
        edit_menu.add_command(label="Close", command=lambda: self.close(root))
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="View Help", command=lambda: self.showHelp())
        menu_bar.add_cascade(label="Help", menu=help_menu)

        root.config(menu=menu_bar)

    def createInputFrame(self, root, offset):
        input_frame = tk.Frame(root)
        input_frame.place(x=10, y=offset)

        font1 = ('Helvetica', 20, 'bold')
        font = ('Helvetica', 14)

        input_frame_label = tk.Label(input_frame, text="Simulation parameters", font=font1, anchor='w')
        input_frame_label.pack(fill='x', pady=15)

        
        tk.Label(input_frame, text=f"Average time between arrivals: {round(np.average(self.time_table), 2)} [t.u.]", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(input_frame, text=f"Desired charging time: {round(self.desired_charging_time, 2)} [t.u.]", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(input_frame, text=f"Battery capacity: {round(self.battery_capacity, 2)} [kWh]", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(input_frame, text=f"Cars quantity: {self.station_load_cars}", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(input_frame, text=f"Trucks quantity: {self.station_load_trucks}", font=font, anchor='w').pack(fill='x', pady=15)

    def createResultFrame(self, root, offset):
        result_frame = tk.Frame(root)
        result_frame.place(x=10, y=offset)

        font1 = ('Helvetica', 20, 'bold')
        font = ('Helvetica', 14)

        result_frame_label = tk.Label(result_frame, text="Result data", font=font1, anchor='w')
        result_frame_label.pack(fill='x', pady=15)
        tk.Label(result_frame, text=f"Max energy need: {round(max(self.energy_table), 2)} [kWh]", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(result_frame, text=f"Min energy need: {round(min(self.energy_table), 2)} [kWh]", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(result_frame, text=f"Average energy need: {round(np.average(self.energy_table), 2)} [kWh]", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(result_frame, text=f"Max charging time: {round(max(self.charging_times), 2)} [t.u.]", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(result_frame, text=f"Min charging time: {round(min(self.charging_times), 2)} [t.u.]", font=font, anchor='w').pack(fill='x', pady=15)
        tk.Label(result_frame, text=f"Average charging time: {round(np.average(self.charging_times), 2)} [t.u.]", font=font, anchor='w').pack(fill='x', pady=15)

    def createPlotFrame(self, root):
        plot_frame = tk.Frame(root, relief="ridge", bd=2)
        plot_frame.pack(side=tk.RIGHT, padx=10)

        fig, axes = plt.subplots(4, 1, figsize=(10, 15))

        axes[0].plot(self.grid_power_data, label="Grid Power (kW)")
        axes[0].set_xlabel('Time (t.u.)')
        axes[0].xaxis.set_label_coords(0.95, -0.1)
        axes[0].set_ylabel('Grid power (kW)')
        axes[0].set_title('Grid power over time')

        max_capacity = max(self.battery_capacity_data)
        lower_limit = 0.2 * self.battery_capacity

        axes[1].plot(self.battery_capacity_data, label="Battery Capacity (kWh)", color='orange')
        axes[1].axhline(y=max_capacity, color='red', linestyle='dashed', linewidth=1, label=f'Upper limit 80%')
        axes[1].axhline(y=lower_limit, color='blue', linestyle='dashed', linewidth=1, label=f'Lower Limit 20%')
        axes[1].set_xlabel('Time (t.u.)')
        axes[1].xaxis.set_label_coords(0.95, -0.1)
        axes[1].set_ylabel('Battery capacity (kWh)')
        axes[1].set_title('Capacity over time')
        axes[1].legend()

        axes[2].scatter(range(len(self.charging_times_cars)), self.charging_times_cars, label='Cars', color='blue', alpha=0.5, s=20)
        axes[2].scatter(range(len(self.charging_times_trucks)), self.charging_times_trucks, label='Trucks', color='orange', alpha=0.5, s=20)
        axes[2].get_xaxis().set_visible(False)
        axes[2].set_ylabel('Charging Time (t.u.)')
        axes[2].set_title('Charging time distribution')
        axes[2].legend()
        axes[2].grid(True)  # Add grid to the scatter plot

        sns.histplot(self.energy_table, bins=20, kde=True, ax=axes[3], color='blue', edgecolor='black')
        axes[3].set_xlabel("Energy [kWh]")
        axes[3].xaxis.set_label_coords(0.95, -0.1)
        axes[3].set_ylabel('Count')
        axes[3].set_title("EV's energy needs distribution")

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

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
        """Handle application closing gracefully."""
        print("Application is closing...")
        root.quit()
        root.destroy()
        self.flag = 0

    def showHelp(self):
        webbrowser.open("https://kerstentechniek.sharepoint.com/_layouts/15/sharepoint.aspx")  # TODO Replace with the actual help link

    def getFlag(self):
        return self.flag
    
    def getImagePath(self, filename):
        if getattr(sys, 'frozen', False):
            base_path = sys._MEIPASS  
        else:
            base_path = os.path.dirname(__file__)  

        return os.path.join(base_path, filename)