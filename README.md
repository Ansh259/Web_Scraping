# Hockey Team Stats Scraper
This project scrapes hockey team stats from the website https://www.scrapethissite.com/pages/forms/ and processes the data to generate:
  1) A ZIP file containing all original HTML pages collected from the site.
  2) An Excel file with two sheets:
     
     a) NHL Stats 1990-2011: Contains the original data.
     
     b) Winner and Loser per Year: A summary of the teams with the most wins and the least wins for each year.

# Table of Contents

  Installation
  
  Usage
  
  Testing

# Installation
To run this project, you'll need Python 3.7+ installed on your system. Follow these steps to install the dependencies:

1. Clone the repository:
git clone https://github.com/yourusername/hockey-team-stats-scraper.git
cd hockey-team-stats-scraper

2. Install the dependencies:
   
a) Create and activate a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate

b) Install the required dependencies:

pip install -r requirements.txt

# Usage
Once the dependencies are installed, you can run the scraper and generate the files.
1. Run the script
To scrape the data and generate the output files (hockey_team_stats.zip and hockey_team_stats.xlsx), copy the folowing python file code in colab cell and execute the code:
My_Program.py

This will:

  a) Download the HTML pages from the website.

  b) Save them in a ZIP file.
  
  c) Parse the data and create an Excel file with two sheets.

2. Files Generated
After running the script, you'll find two output files:

  a) hockey_team_stats.zip: A ZIP file containing the HTML files from each page (named 1.html, 2.html, ..., 24.html).
  
  b) hockey_team_stats.xlsx: An Excel file with two sheets:
  
    b.1) Sheet 1: NHL Stats 1990-2011 (all scraped rows).
    
    b.2) Sheet 2: Winner and Loser per Year (summary of teams with the most and least wins).

Check the Colab output: After running the code, the two files (hockey_stats.zip and hockey_stats.xlsx) will be generated in the working directory. If you're running the code in Google Colab, you can download them directly from the file explorer or use the following code to download the files:

from google.colab import files
files.download("hockey_stats.zip")
files.download("hockey_stats.xlsx")

# Testing

The project includes unit tests for data transformation. You can run the tests to verify the correctness of the core logic.

Step 1: Install pytest if you haven't already using bash command: !pip install pytest

Step 2: Created Unit Tests for Core Logic for the core logic of parsing and processing data without hitting the actual website and save the file as TestCases.py

Step 3: Running the Tests on the colab cells using the command - !pytest TestCases.py

This will run all the tests and output the results.

# NOTE
Run the script in My_Program.py file on colab cell and do remember to import all the lib/packages mentioned in the requirements.txt file.

The tests mock the HTML data to avoid actual HTTP requests, ensuring faster execution during testing. No live web scraping occurs while running the tests.











