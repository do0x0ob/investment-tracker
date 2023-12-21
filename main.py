#!/usr/bin/env python
# coding: utf-8

import gspread
import pandas as pd
import configparser
from oauth2client.service_account import ServiceAccountCredentials
from IPython.display import display
import aiohttp
import asyncio
from bs4 import BeautifulSoup

# use these code if run in jupyternotebook
# if 'IPKernelApp' in get_ipython().config:
#     import nest_asyncio
#     nest_asyncio.apply()


def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

class InvestmentSheet:
    def __init__(self, config):
        self.config = config
        self.load_credentials()

    def load_credentials(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.config['spread_sheet']['credentials_Path']
        )
        self.client = gspread.authorize(creds)
        
    def read_data(self):
        file_name = self.config['spread_sheet']['filename']
        sheet_name = self.config['spread_sheet']['spreadsheet_name']
        sheet = self.client.open(file_name).worksheet(sheet_name)
        data = sheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    
    def write_data(self, data):
        file_name = self.config['spread_sheet']['filename']
        sheet_name = self.config['spread_sheet']['spreadsheet_name']
        sheet = self.client.open(file_name).worksheet(sheet_name)
        
        j = 2
        for i in data:
            sheet.update_acell(f'H{j}', i['Fund Price Latest'])
            j += 1

class Crawler:
    def __init__(self, config):
        self.config = config
        
    async def handle_error(self, error_msg):
        print(f'An error occurred: {error_msg}')

    async def fetch_data(self, url):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    return await response.text()
        except aiohttp.ClientError as e:
            await self.handle_error(e)


    async def get_fund_data(self, brand, code):
        url = self.config['web_crawler']['target_website_url'] + f'/{brand}/{code}'
        try:
            html = await self.fetch_data(url)
            if html:
                soup = BeautifulSoup(html,'lxml')
                fund_name = soup.title.text.split(' ')[0]
                raw_fund_price_dated = soup.select(self.config['web_crawler']['target_data_position'])
                if raw_fund_price_dated: 
                    fund_price_dated = raw_fund_price_dated[0].text.replace('[[[', '').replace(']]]','')
                    return fund_name, fund_price_dated
                else:
                    print(f'No data found for {brand}/{code}')
                    return 'NA', 'NA'
            else:
                print(f'Fail to fetch data {brand}/{code}')
                return None, None
        except (aiohttp.ClientError, ValueError, IndexError) as e:
            await self.handle_error(e)
    
    async def fetch_and_format_fund_data(self, fund_code_df):
        tasks = []
        for index, row in fund_code_df.iterrows():
            brand = row['Brand']
            code = row['Code']
            tasks.append(self.get_fund_data(brand,code))
        
        results = await asyncio.gather(*tasks)
        fund_data = [{'Fund Name': name, 'Fund Price Latest': price} for name, price in results if name and price]
        return fund_data
    
    async def price_getter(self, dataframe):
        fund_data_price_df = await self.fetch_and_format_fund_data(dataframe)
        return fund_data_price_df

async def main(show_or_write=1):
    config = load_config('config.ini')
    sheet = InvestmentSheet(config)
    sheet.load_credentials()
    fund_code_df = sheet.read_data()
    
    crawler = Crawler(config)
    
    fund_data_price = await crawler.price_getter(fund_code_df)
    
    # show or write
    if show_or_write == 0: # show wonly
        fund_data_price_df = pd.DataFrame(fund_data_price)
        display(fund_data_price_df)
    elif show_or_write == 1: # write only
        sheet.write_data(fund_data_price)
    elif show_or_write == 2: # do both
        fund_data_price_df = pd.DataFrame(fund_data_price)
        display(fund_data_price_df)
        sheet.write_data(fund_data_price)
    return None

loop = asyncio.get_event_loop()
result = loop.run_until_complete(main(1))





