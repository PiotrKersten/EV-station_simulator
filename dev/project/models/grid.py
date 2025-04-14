class Grid:
  def __init__(self, grid_power):
    self.grid_power = grid_power
    self.grid_power_data = []
    pass

  def updateGridState(self, power_cut, flag): 
    if flag:
        self.grid_power = self.grid_power + power_cut
    else:
        self.grid_power = self.grid_power - power_cut
    print(f"Grid state {self.grid_power} kW")

        
  def checkGridState(self):
      print(f"Grid state {self.grid_power} kW")
      return self.grid_power
  
  def insertDataToTable(self):
     self.grid_power_data.append(self.grid_power)

  def getTable(self):
     return self.grid_power_data


