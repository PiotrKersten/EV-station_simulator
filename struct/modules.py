class Modules:
  def __init__(self):
    pass

  def checkModuleToDetach(self, demanded_power, priorities):
      sum_power = 0
      for car in reversed(priorities):
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
      print(f"{sum_power}/{demanded_power} kW can be applied")
      return sum_power
  
  def detachModulePartly(self, demanded_power, priorities):
      sum_power = 0
      for car in reversed(priorities):
          power = car['assigned_power']
          print('power',power)
          power_to_detach = 17.5
          if demanded_power - sum_power and sum_power  < power_to_detach != 0:
              return sum_power
          print('power to detach', power_to_detach)
          car['assigned_power'] = power - power_to_detach
          sum_power+=power_to_detach

      print(f"{sum_power}/{demanded_power} kW can be applied")
      return sum_power

  
  def checkIfModuleDetached(self, car, duration, priorities):
      search_name = car['name']
      ev = next((ev for ev in priorities if ev['name'] == search_name), None)

      if ev:
          if car['assigned_power'] != ev['assigned_power']:
              time = int(car['needed_energy'] / ev['assigned_power'] * 60)
              return time
      return duration