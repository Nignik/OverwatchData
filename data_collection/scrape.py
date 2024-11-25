from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import numpy as np
import json
import copy

def make_serializable(obj):
  if isinstance(obj, np.ndarray):
      return obj.tolist()  # Convert numpy array to list
  raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def main():
  options = Options()
  options.headless = True
  options.add_experimental_option("prefs", {"profile.managed_default_content_settings.javascript": 2})
  driver = webdriver.Chrome(options=options)

  with open("../data/base_data.json") as f:
    hero_names = json.load(f)["hero_names"]
    
  with open("../data/scraped_data.json") as f:
    scraped_data = json.load(f)

  scraped_data["hero winrates"] = {}
  
  try: 
    driver.get("https://www.overbuff.com/heroes")

    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Cassidy')]"))
    )

    for name in hero_names:
      name_element = driver.find_element(By.XPATH, f"//a[contains(text(), '{name}')]")
      root_element = name_element.find_element(By.XPATH, ".//ancestor::tr[1]")
      win_rate_bar_element = root_element.find_element(By.XPATH, f".//descendant::div[contains(@class, 'bg-stat-win')]")
      win_rate_element = win_rate_bar_element.find_element(By.XPATH, ".//ancestor::td[1]/descendant::span[contains(text(), '.')]")
      win_rate = win_rate_element.text
      
      name_copy = copy.copy(name)
      # handle weird names
      if (name == "Lúcio"):
        name_copy = "Lucio"
      elif (name == "Torbjörn"):
        name_copy = "Torbjorn"
        
      scraped_data["hero winrates"][name_copy] = float(win_rate[:-1])

  finally:
    driver.quit()

  with open("../data/scraped_data.json", "w") as f:
    json.dump(scraped_data, f, indent=2, default=make_serializable)
  
if __name__ == "__main__":
  main()