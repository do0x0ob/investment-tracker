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

    def open_file(self):
        file_name = self.config['spread_sheet']['filename']
        sheet_name = self.config['spread_sheet']['spreadsheet_name']
        sheet = self.client.open(file_name).worksheet(sheet_name)
        return sheet
        
    def read_data(self):
        sheet = self.open_file()
        data = sheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        return df
    
    def write_data(self, data):
        sheet = self.open_file()
        j = 2

        for i in data:
            sheet.update_acell(f'H{j}', i['Fund Price Latest'])
            j += 1