# Install MetaTrader4
## Debian
```bash
    wget https://download.mql5.com/cdn/web/metaquotes.software.corp/mt4/mt4debian.sh ; chmod +x mt4debian.sh ; ./mt4debian.sh
```
## Windows
1. Download the installer from the official website: https://download.mql5.com/cdn/web/metaquotes.software.corp/mt4/mt4setup.exe
2. Run the installer

# Run a export data script
1. Open MetaTrader4
2. In navigator, right click on "Scripts" and click "Create in MetaEditor"
3. Paste the [script](data_export.mq4) and save it
4. Drag the script to the chart
The csv file is created in the folder "Files" in the MetaTrader4 folder (Path: File -> Open Data Folder -> MQL4 -> Files)

# Run the indicator
1. Put the csv file in the data folder
2. Run indicator.py your_csv_file.csv
```bash
    python indicator.py <<your_csv_file.csv>>
```

# Compare indicators with the custom indicator
