import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials

class InvestmentSheet:
    def __init__(self, config):
        self.config = config
        self.load_credentials()

    def load_credentials(self):
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            self.config['spread_sheet']['credentials_Path']
        )
        self.client = gspread.authorize(creds)

    def open_file(self, sheet_type):
        file_name = self.config['spread_sheet']['filename']
        # sheet_type option: fund, crypto
        if sheet_type == 'fund':
            sheet_name = self.config['spread_sheet']['fund_spreadsheet_name']
        elif sheet_type == 'crypto':
            sheet_name = self.config['spread_sheet']['crypto_id_spreadsheet_name']

        sheet = self.client.open(file_name).worksheet(sheet_name)
        return sheet
        
    def read_data(self, sheet_type):
        sheet = self.open_file(sheet_type)
        data = sheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    
    def write_data(self, sheet_type, data):
        sheet = self.open_file(sheet_type)
        j = 2

        for i in data:
            if sheet_type == 'fund':
                sheet.update_acell(f'H{j}', i['Fund Price Latest'])
                print(f'updating fund price: {i}')
            elif sheet_type == 'crypto':
                print(f'updating crypto price: {i}')
                sheet.update_acell(f'H{j}', i['Coin Price'])
            j += 1
