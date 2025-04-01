import random

class EV:
  def __init__(self):
    self.energy_table = []

    pass

  def createCar(self, name, arriving_time, charge_duration):
    car = {
        'name': name,
        'driving_time': arriving_time,
        'charge_duration': charge_duration,
        'needed_energy': random.randint(20, 70), 
        'assigned_power': 0,
        'charger_index': None,
        'charger_slot': None
    }
    self.insertDataToTable(car['needed_energy'])
    return car

  def createTruck(self, name, arriving_time, charge_duration):
    truck = {
        'name': name,
        'driving_time': arriving_time,
        'charge_duration': charge_duration,
        'needed_energy': random.randint(50, 500), 
        'assigned_power': 0,
        'charger_index': None,
        'charger_slot': None
    }
    self.insertDataToTable(truck['needed_energy'])
    return truck
  
  def manageTruck(self, energy_need, power_to_achieve):
      new_time = (energy_need/power_to_achieve)*60
      print(f"New desired time {new_time:.2f} [t.u], with available power {power_to_achieve} kW")
      return new_time
  
  def insertDataToTable(self, energy):
    self.energy_table.append(energy)

  def getTable(self):
     return self.energy_table