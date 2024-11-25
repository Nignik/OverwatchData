import numpy as np
import pandas as pd
import json
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication
import sys

import DataFrameModel

def main():
  with open("../data/scraped_data.json") as f:
    hero_data = json.load(f)
    
  hero_winrates_data = hero_data["hero winrates"]
  hero_names = [name for name, _ in hero_winrates_data.items()]
  hero_winrates = [winrate for _, winrate in hero_winrates_data.items()] 
  
  df = pd.DataFrame(hero_winrates, hero_names, ["winrate"])
  df.sort_values(by="winrate", ascending=[False], inplace=True)
  print(df)
  
  app = QApplication(sys.argv)
  viewer = DataFrameModel.DataFrameViewer(df)
  viewer.show()
  
  sys.exit(app.exec_())
  
  
if __name__ == "__main__":
  main()