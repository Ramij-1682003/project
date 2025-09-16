import requests
from bs4 import BeautifulSoup
import csv 

url = "https://www.cars24.com/buy-used-cars-mumbai/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
response = requests.get(url, headers=headers)

all_cars_data = []

if response.status_code == 200:
    soup = BeautifulSoup(response.content, 'html.parser')
    car_cards = soup.find_all('div', class_='styles_normalCardWrapper__qDZjq')
    
   
    for car in car_cards:
        name_tag = car.find('div', class_='sc-kwhYVV icdwSu')
        car_name = name_tag.text if name_tag else "Name not found"
    

        price_tag = car.find('p', class_='cyPhJl')
        car_price = price_tag.text if price_tag else "Price not found"
    
        details_list = car.find('ul', class_='sc-ggPNws ctMNSL')
        if details_list:
            details = details_list.find_all('p')
            km_driven = details[0].text
            fuel_type = details[1].text
            transmission = details[2].text
        else:
            km_driven = "N/A"
            fuel_type = "N/A"
            transmission = "N/A"
        
        car_data = {
            "Name": car_name,
            "Price": car_price,
            "Kilometers": km_driven,
            "Fuel Type": fuel_type,
            "Transmission": transmission
        }
        all_cars_data.append(car_data)

if all_cars_data:
    keys = all_cars_data[0].keys()
    
    with open('cars24_mumbai.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(all_cars_data)
    
    print("Success! Data for all cars has been saved to 'cars24_mumbai.csv'")
else:
    print("No data was collected to save.")