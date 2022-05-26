from genericpath import exists
import requests
from bs4 import BeautifulSoup
import os
import csv

url = 'https://starwars.fandom.com/wiki/'
data_folder = './data'

# go through each file in the data folder as long as it's a csv
for filename in os.listdir(data_folder):
    f = os.path.join(data_folder, filename)
    if os.path.isfile(f) and f.endswith('.csv'):
        folder = filename[:-4]
        folder_path = './images/'+folder
        # make image folders if they don't already exist
        if not os.path.exists(folder_path):
            os.mkdir(folder_path)
        # begin parsing the csv file
        with open(f, 'r') as data_file:
            file_reader = csv.reader(data_file)
            for row in file_reader:
                # skip the header row
                if row[0]  != "name":
                    name = row[0]
                    name = name.replace(' ', '_')
                    page_link = url+name
                    page = requests.get(page_link)
                    # extract the main image from the page
                    html = BeautifulSoup(page.text, 'html.parser')
                    image = html.find("figure", {"class": "pi-image"})
                    try:
                        image = image.select('a > img')[0]
                        image = image.get('src')
                        image = requests.get(image)
                        # Save the image
                        with open('./images/'+folder+'/'+name+'.jpg', 'wb') as img:
                            img.write(image.content)
                    except:
                        print(name)

