import requests
import os
import configparser
import json
from utils import *

# for test
config = load_config('config.ini')


def get_crypto_currency(platform_name, coin_name):
    """
    platform name: CoinMarketCap
    """
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config[platform_name]['key']
    }
    options = {
        'amount': 1,
        'id': config[platform_name][coin_name],
        'convert': 'TWD'
    }
    url = config[platform_name]['url']
    response = requests.get(url, headers=headers, params=options)
    
    if response.status_code == 200:
        data = response.json()
        
        if 'data' in data:
            price = data['data']['quote']['TWD']['price']
            print(f'{coin_name} Price is {price}')
        else:
            print('No data found in response.')
    else:
        print('Request failed with status code', response.status_code)
    

    
    
get_crypto_currency('CoinMarketCap', 'CAKE')
