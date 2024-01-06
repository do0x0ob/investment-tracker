## Investment-tracker Overview
Combines Google Spreadsheets API and a web crawler to summarize currently investment values.

## How to Use

### 1. Create Venv and Install Depencency Packages
- It's recommended to create a virtual enviroment. Follow these steps to create one:  
    ```bash
    # Skip this if 'venv' is already installed
    pip install venv

    # Change to your project directory
    cd <your_project_directory>

    # Create a virtual environment (you can name it as you wish)
    python -m venv <your_venv_name>

    # Activate the virtual environment
    source <your_venv_name>/bin/activate
    ```

- Use the following commands to install necessary packages.
    ```bash
    pip install -r requirements.txt
    ```


### 2. Read / Write data from Goolgle Spreadsheet
#### Spread Sheets Setup 
- ***Put Key file:***
    - Drag your IAM key file into root directory.
- ***Configure Key Path:***
    - in `config.ini [spread_sheet] >> credentials_Path `, specify the path for the key file.
- ***Configure Filename and Sheetname:*** 
    - in `config.ini [spread_sheet] >> filename`, specify your Google SpreadSheet's filename.
    - in `config.ini [spread_sheet] >> fund_spreadsheet_name`, specify the Google SpreadSheet's sheetname which included your fund codes.
#### CoinMarketcap API Key Setup
- ***Configure Key:***
    - in `config.ini [CoinMarketCap] >> key`, Enter your key.
- ***Configure Sheetname:***
    - in `config.ini [spread_sheet] >> crypto_id_spreadsheet_name`, specify the Google SpreadSheet's sheetname which included your crypto coin ids.

### 3. Make a Copy of Google SpreadSheet Template
- ***Duplicate from a template:***
    - [Investment Tracker Template.xlsx](https://github.com/do0x0ob/investment-tracker/files/13849644/Investment.Tracker.Template.xlsx)
- ***Rename the file and tab:***
    - Rename the file and tab name as your wish; this will be configured in  **step 4**.
- ***List Your Funds in the SpreadSheet:***
    - Customize your profolio with the fund name and currency ... etc.

### 4. Obtain Brand / Code Info of Your Target Funds
- ***Open target website:*** 
    - Visit www.stockq.org.
- ***Get brand and code:*** 
    - Refer to the URL to extract brand and code.  
      ![brand_and_code](https://github.com/do0x0ob/investment-tracker/assets/153002627/5223140c-6c8f-4eaa-adc9-cd7e8ada7def)
- ***Fill the Info in SpreadSheet:*** 
    - Populate the spreadsheet with the acquired information.

### 5. Run the main.py File to Get Latest Price
- ***Run Mode:*** 
    - In the last row of main.py, there's an optional parameter, that determines whether to display, write or do both. **Default is 1**.
        ```python
        result = loop.run_until_complete(main(0)) # show only
        result = loop.run_until_complete(main(1)) # write only
        result = loop.run_until_complete(main(2)) # both show and write
        ```
        - Result should look likw this if displayed:  
            ![result_display](https://github.com/do0x0ob/investment-tracker/assets/153002627/d69918b4-9714-4ebd-9c3c-800e7bff9e45)

        - If the paremeter was 1 or 2; SpreadSheet should Autofill the latest price like this:  
            ![result_only_write](https://github.com/do0x0ob/investment-tracker/assets/153002627/f475bc58-5e06-4251-a8ce-d842e018b91b)



### 6. Fill the Units to Calculate the Summary Value of All Listed Funds
- Use the built-in functions of spreadsheets to calculate the summerized value of all listed funds for today.
