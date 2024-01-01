import pandas as pd
import configparser
from IPython.display import display
from crawler import Crawler
from api_getter import Crypto_price_getter
from investmentsheet import InvestmentSheet

def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

async def get_fund_prices(config):
    fund_sheet = InvestmentSheet(config)
    fund_sheet.load_credentials()
    fund_code_df = fund_sheet.read_data('fund')
    crawler = Crawler(config)
    return await crawler.price_getter(fund_code_df)

async def get_crypto_prices(config):
    crypto_sheet = InvestmentSheet(config)
    crypto_sheet.load_credentials()
    crypto_code_df = crypto_sheet.read_data('crypto')
    crypto_engine = Crypto_price_getter(config)
    return crypto_engine.get_crypto_currency(crypto_code_df)

def show_prices(fund_data_price, crypto_data_price):
    if fund_data_price:
        fund_data_price_df = pd.DataFrame(fund_data_price)
        display(fund_data_price_df)
    if crypto_data_price:
        crypto_data_price_df = pd.DataFrame(crypto_data_price)
        display(crypto_data_price_df)

def update_prices(fund_data_price, crypto_data_price, config):
    fund_sheet = InvestmentSheet(config)
    crypto_sheet = InvestmentSheet(config)
    
    if fund_data_price:
        fund_sheet.write_data('fund', fund_data_price)
    if crypto_data_price:
        crypto_sheet.write_data('crypto', crypto_data_price)
    
    if fund_data_price or crypto_data_price:
        print('Data updated!')

async def update_all_price(update_fund=True, update_crypto=True, show_results=False):
    config = load_config('config.ini')
    fund_data_price = []
    crypto_data_price = []
    
    if update_fund:
        fund_data_price = await get_fund_prices(config)
    
    if update_crypto:
        crypto_data_price = await get_crypto_prices(config)
    
    if show_results:
        show_prices(fund_data_price, crypto_data_price)
    
    update_prices(fund_data_price, crypto_data_price, config)
    
    return None
