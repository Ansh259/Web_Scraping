BASE_URL = "https://www.scrapethissite.com/pages/forms/"
HTML_DIR = "html_files"

# Function to scrape an individual page content
async def scrape_page(session, page_number):
    url = f"{BASE_URL}?page={page_number}"
    async with session.get(url) as response:
        html = await response.text()
        # Save HTML to a file
        filename = f"{page_number}.html"
        os.makedirs(HTML_DIR, exist_ok=True)
        with open(os.path.join(HTML_DIR, filename), 'w') as f:
            f.write(html)
        return html

# Function to download all pages
async def scrape_all_pages():
    async with aiohttp.ClientSession() as session:
        tasks = []
        # As there are 24 pages
        for i in range(1, 25):  
            tasks.append(scrape_page(session, i))
        html_data = await asyncio.gather(*tasks)
    return html_data

# Function to parse the HTML data
def parse_data(html_data: List[str]) -> List[dict]:
    stats = []
    for html in html_data:
      soup = BeautifulSoup(html, 'html.parser')
      # To skip the header row
      rows = soup.find_all('tr')[1:]
      for row in rows:
        cols = row.find_all('td')
        stats.append({
            'Team Name': cols[0].text.strip(),
            'Year': cols[1].text.strip(),
            'Wins': int(cols[2].text.strip()),
            'Losses': int(cols[3].text.strip()),
            'OT Losses': int(cols[4].text.strip() or 0),
            'Win %': float(cols[5].text.strip()), 
            'Goals For(GF)': int(cols[6].text.strip()),
            'Goals Against(GA)': int(cols[7].text.strip()),
            '+/-': int(cols[8].text.strip())
        })
    return stats

#Function To Create Zip Of HTML Files
def save_html_to_zip(html_data: List[str]) -> None:
  with zipfile.ZipFile('hockey_stats.zip','w')as zipf:
        for i, content in enumerate(html_data, start=1):
            filename = f"{i+1}.html"
            with open(filename,'w')as f:
                f.write(content)
            zipf.write(filename)
            os.remove(filename)
  print("HTML files have been successfully zipped and saved as 'hockey_stats.zip'.")

#Function To Create The Excel-File With The Two Sheets
def generate_excel(stats) -> None:
    wb = Workbook()
    ws1 = wb.active
    ws1.title = "NHL Stats 1990-2011"

    #Write headers for NHL Stats
    headers = ["Team Name","Year","Wins","Losses","OT Losses","Win %","Goals For(GF)","Goals Against(GA)","+/-"]
    ws1.append(headers)

    #Writing all the data
    for stat in stats:
      ws1.append([
            stat['Team Name'],
            stat['Year'],
            stat['Wins'],
            stat['Losses'],
            stat['OT Losses'],
            stat['Win %'],
            stat['Goals For(GF)'],
            stat['Goals Against(GA)'],
            stat['+/-']
        ])
    
    #Creating second sheet for winner and looser per year
    ws2 = wb.create_sheet(title="Winner and Loser per Year")

    #Adding the data to sheet2
    ws2.append(["Year","Winner","Winner Num. of Wins","Loser Num. of Wins"])

    year_data = {}
    for stat in stats:
        year = stat['Year']
        if year not in year_data:
            year_data[year] = {'winner': stat, 'loser': stat}
        else:
            if stat['Wins'] > year_data[year]['winner']['Wins']:
                year_data[year]['winner'] = stat
            if stat['Wins'] < year_data[year]['loser']['Wins']:
                year_data[year]['loser'] = stat

    for year, teams in year_data.items():
        ws2.append([year, teams['winner']['Team Name'], teams['winner']['Wins'], teams['loser']['Team Name'], teams['loser']['Wins']])

    #Saving excel file
    wb.save("hockey_stats.xlsx")
    print("Excel file 'hockey_stats.xlsx' has been successfully created.")


# Main function to run the scraping process
async def main():
  # Scrape all pages
  html_data = await scrape_all_pages()
  # Parse the scraped data
  stats = parse_data(html_data)
  # Save HTML files as a zip
  save_html_to_zip(html_data)
  # Create the Excel file
  generate_excel(stats)

# Run the main function using await directly in Jupyter/interactive shell
await main()