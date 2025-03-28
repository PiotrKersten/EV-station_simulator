class Battery:
    def __init__(self, battery_capacity, desired_charging_time):
        self.battery_capacity = battery_capacity

        self.upper_limit = 0.8*battery_capacity
        self.battery_state = self.upper_limit #variable to manipulate battery state

        self.lower_limit = 0.2*battery_capacity

        self.multiplier = 60 // desired_charging_time
        self.battery_capacity_data = []

    def checkBatteryState(self):
        print(f"Battery state: {self.battery_state}/{self.upper_limit} kWh power ready: {(self.battery_state-self.lower_limit)*self.multiplier} kW")
        return self.battery_state

    def chargeBattery(self, available_grid, available_battery, power_to_return):
        if available_battery < self.upper_limit:
            self.updateBattery(available_grid - power_to_return, True)
        
    def updateBattery(self, power_cut, flag):
        if flag:
            print("Charging battery")
            self.battery_state = self.battery_state + power_cut*(1/self.multiplier)
            if self.battery_capacity > self.upper_limit: 
                self.battery_capacity = self.upper_limit
        else:
            self.battery_state = self.battery_state - power_cut*(1/self.multiplier)
        print(f"Battery state {self.battery_state} kWh")

    def getLower(self):
        return self.lower_limit
    
    def getUpper(self):
        return self.upper_limit

    def insertDataToTable(self):
        self.battery_capacity_data.append(self.battery_state)

    def getTable(self):
        return self.battery_capacity_data