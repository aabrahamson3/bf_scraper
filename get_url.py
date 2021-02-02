from bs4 import BeautifulSoup
import csv
import pandas as pd
import random
import requests
import time

def get_recipes_html(r):
    soup = BeautifulSoup(r.content, 'html.parser')
    recipes = soup.select('.recipetitle')
    return recipes

def add_to_recipe_dict(recipes, recipe_dict):
    for recipe in recipes:
        recipe_dict[recipe['href']] = recipe.get_text()
    return recipe_dict

recipe_dict = {}
base_url = "https://www.brewersfriend.com/homebrew-recipes/page/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox 84.0'}
for i in range(10187,10273):
    print(f'scraping new page, on page {i}')
    url = f"{base_url}{i}"
    r = requests.get(url, headers=headers)
    recipes = get_recipes_html(r)
    print(recipes[0])
    add_to_recipe_dict(recipes, recipe_dict)
    print('sleeping...')
    time.sleep(10 + random.uniform(0,2))

    if i % 10272 == 0:
        with open(f'recipe_list_{i}.csv', 'w', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            for k, v in recipe_dict.items():
                writer.writerow([k, v])
