## Investment-tracker Overview
Combines Google Spreadsheets API and a web crawler to summarize currently investment values.

## How to Use

### 1. Create Venv and install depencency packages
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
- ***Put Key file:***
    - Drag your IAM key file into root directory.
- ***Configure Key Path:***
    - in `conif.ini`, specify the path for the key file.
- ***Configure Filename and Sheetname:*** 
    - in `config.ini`, specify your Google SpreadSheet's filename.

### 3. Make a Copy of Google SpreadSheet Template
- ***Duplicate from a template:***
    - Link: `-------`
- ***Rename the file and tab:*** 
    - Rename the file and tab name as your wish; this will be configured in  **step 4**. 

### 4. Obtain Brand / Code Info of Your Target Funds
- ***Open target website:*** 
    - Visit www.stockq.org.
- ***Get brand and code:*** 
    - Refer to the URL to extract brand and code.
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

### 6. Fill the Units to Calculate the Summary Value of All Listed Funds
- Refer to the template below:  
    ![image here]
- Use the built-in functions of spreadsheets to calculate the summerized value of all listed funds for today.  
    ![image here]
