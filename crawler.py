import aiohttp
import asyncio
from bs4 import BeautifulSoup


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