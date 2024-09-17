import requests
from bs4 import BeautifulSoup
import pandas as pd
import ErrorLogger

logger = ErrorLogger()

# Step 1: Fetch the webpage content
url = 'https://www.pro-football-reference.com/years/2003/passing.htm'
response = requests.get(url)

#Check if the request was successful
if response.status_code == 200:
    print("Successfully fetched the webpage")
    logger.send_debug("Successfully fetched the webpage.", "WebScrapper.py (SportStatsProject)", "NetworkListener")
else:
    print(f"Failed to fetch the webpage. Status Code: {response.status_code}")
    logger.send_error(f"Failed to fethc the webpage. Status Code: {response.status_code}", "Webscrapper.py (SportsStatsProject)", "NetworkListener")
    exit()

# Step 2: Parse the webpage content with BS (BeautifulSoup Library)
soup = BeautifulSoup(response.content, 'html.parser')

# Step 3: Find the stats table
table = soup.find('table', {'id': 'passing'})

# Step 4: Read the table into Pandas DataFrame
# Using pandas' built-in read_html method to read tables from HTML
df = pd.read_html(str(table))[0]

# Step 5: Data Cleaning 
# Remove rows with headers (ex// mid-table repeated headers)
df = df[df['Player'] != 'Player']

# Step 6: Display the first few rows of the DataFrame
print(df.head())

# Step 7: Save the data to a CSV file
df.to_csv('nfl_passing_stats_2003.csv', index = False)
print("Data saved to: 'nfl_passing_stats_2023.csv'")
logger.send_debug("Data saved to: 'nfl_passing_stats_2023.csv'", "WebScrapper.py (SportsStatsProj)", "NetworkListener")



