import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3
import datetime

# Define the URL of the website to scrape
url = "https://www.theverge.com/"

# Send a GET request to the URL and parse the HTML content using BeautifulSoup
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find all the article elements on the page
articles = soup.find_all("ol")

# Create a list to store the data
data = []

# Loop through each article and extract the required information
for article in articles:
    headline = article.find(
        "a", {"class": "group-hover:shadow-underline-franklin"}).text.strip()
    
    
    link = article.find("a")["href"]
    author = article.find(
        "a", {"class": "text-gray-31 hover:shadow-underline-inherit dark:text-franklin mr-8"}).text.strip()
    date_str = article.find(
        "span", {"class": "text-gray-63 dark:text-gray-94"})
    # date = datetime.datetime.strptime(date_str, "%m-%dT%H:%M:%S.%fZ")
    data.append([link, headline, author, str(date_str)])

# Create a pandas DataFrame from the data
df = pd.DataFrame(data, columns=["URL", "Headline", "Author", "Date"])

# Generate the filename for the CSV file
filename = datetime.datetime.now().strftime("%d%m%Y_verge.csv")

# Save the DataFrame to a CSV file
df.to_csv(filename, index=False)

# Connect to the SQLite database
conn = sqlite3.connect("verge_articles.db")

# Create a table to store the data
conn.execute("""
CREATE TABLE IF NOT EXISTS articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    URL TEXT,
    Headline TEXT,
    Author TEXT,
    Date TIMESTAMP
)
""")

# Insert the data into the table
for row in data:
    conn.execute(
        "INSERT INTO articles (URL, Headline, Author, Date) VALUES (?, ?, ?, ?)", row)

# Commit the changes and close the connection
conn.commit()
conn.close()
