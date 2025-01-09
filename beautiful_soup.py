import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://www.ea.com/en/games/nhl/ratings"


response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')

item_names = []
item_ratings = []

items = soup.find('tbody', class_='Table_tbody__q3fMn')

for item in items:
  name = item.find('div', class_='Table_profileContent__Lna_E').text
  rating = item.find('span', class_='Table_statCellValue__0G9QI').text

  item_names.append(name)
  item_ratings.append(rating)

data = {"Item Name": item_names, "Rating": item_ratings}
df = pd.DataFrame(data)
print(df)
