import pandas as pd
import configparser
from IPython.display import display
from crawler import *
from investmentsheet import *

def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config


async def update_all_price(show_or_write=1):
    config = load_config('config.ini')
    sheet = InvestmentSheet(config)
    sheet.load_credentials()
    fund_code_df = sheet.read_data('fund')
    
    crawler = Crawler(config)
    
    fund_data_price = await crawler.price_getter(fund_code_df)
    
    # show or write
    if show_or_write == 0: # show only
        fund_data_price_df = pd.DataFrame(fund_data_price)
        display(fund_data_price_df)

    elif show_or_write == 1: # write only
        sheet.write_data('fund', fund_data_price)
        print('Data updated!')

    elif show_or_write == 2: # do both
        fund_data_price_df = pd.DataFrame(fund_data_price)
        display(fund_data_price_df)
        sheet.write_data('fund', fund_data_price)
        print('Data updated!')
        
    return None

