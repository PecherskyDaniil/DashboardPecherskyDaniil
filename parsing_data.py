from bs4 import BeautifulSoup
import requests
url="https://jojo.fandom.com/ru/wiki/%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%81%D1%82%D0%B5%D0%BD%D0%B4%D0%BE%D0%B2"
html = requests.get(url).text
soup = BeautifulSoup(html, 'html')
def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
    return alphabet.isdisjoint(text.lower())

chars=soup.find_all('div', {'class':'chars'})[:-3]
all_links=[]
for char in chars:
  x=char.find_all("a")
  all_links+=x
stand_names=[]
for link in all_links:
  if len(link.get_text())>2 and (match(link.get_text())) and link.get_text()!="Cat Size":# or "стенд" in link.get_text().lower()):
    stand_names.append(link.get_text())
stand_names=list(set(stand_names))

names=[]
power=[]
speed=[]
radius=[]
endurance=[]
accuracy=[]
potential=[]
manga=[]
anime=[]
url_to_stand="https://jojo.fandom.com/ru/wiki/"
for sn in stand_names:
  html = requests.get(url_to_stand+(sn.replace(" ","_"))).text
  soup = BeautifulSoup(html, 'html')
  if not(soup.find("div",{"data-source":"Пользователь"}) is None):
    names.append(soup.find("div",{"data-source":"Пользователь"}).find("a").get_text())
  else:
    names.append(soup.find("div",{"data-source":"Пользователи"}).find("a").get_text())
  if soup.find("div",{"class":"po"}) is None:
    power.append(None)
    speed.append(None)
    radius.append(None)
    endurance.append(None)
    accuracy.append(None)
    potential.append(None)
  else:
    power.append(soup.find("div",{"class":"po"}).div.get_text())
    speed.append(soup.find("div",{"class":"sp"}).div.get_text())
    radius.append(soup.find("div",{"class":"ra"}).div.get_text())
    endurance.append(soup.find("div",{"class":"ps"}).div.get_text())
    accuracy.append(soup.find("div",{"class":"pr"}).div.get_text())
    potential.append(soup.find("div",{"class":"dp"}).div.get_text())
  if not(soup.find("div",{"data-source":"Манга"}) is None):
    manga.append(soup.find("div",{"data-source":"Манга"}).div.get_text())
  else:
    manga.append(None)
  if not(soup.find("div",{"data-source":"Аниме"}) is None):
    anime.append(soup.find("div",{"data-source":"Аниме"}).div.get_text())
  else:
    anime.append(None)

import pandas as pd
df=pd.DataFrame()
df["Stand"]=stand_names
df["User"]=names
df["Power"]=power
df["Speed"]=speed
df["Radius"]=radius
df["Endurance"]=endurance
df["Precision"]=accuracy
df["Potential"]=potential
df["Manga"]=manga
df["Anime"]=anime
print(df.head())
df.to_csv("stands.csv")