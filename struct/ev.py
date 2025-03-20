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
        'needed_energy': random.randint(20, 70),  # Random energy needs
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
        'needed_energy': random.randint(50, 500),  # Random energy needs
        'assigned_power': 0,
        'charger_index': None,
        'charger_slot': None
    }
    self.insertDataToTable(truck['needed_energy'])
    return truck

  def insertDataToTable(self, energy):
    self.energy_table.append(energy)

  def getTable(self):
     return self.energy_table