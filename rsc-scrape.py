from bs4 import BeautifulSoup
import requests
import pandas as pd

# Create dataframe to store safety data
df = pd.DataFrame(columns=['rank', 'year', 'make', 'model', 'rsc_rating', 'fatality_risk', 'injury_risk'])
# Fetch webpage content
url = "https://realsafecars.com/sedans/all"
response = requests.get(url)
html_content = response.content

# Parse HTML with bs4
soup = BeautifulSoup(html_content, "html.parser")

pagination_links = soup.find_all("a", class_="MuiPaginationItem-page")
page_nums = []
for i in range(len(pagination_links)):
    page_value =  pagination_links[i].text
    if page_value == '':
        continue
    page_nums.append(int(page_value))

max_pages = max(page_nums)

for row in soup.find_all("tr", class_="Tables__TR-f84ad0-2 dxGljX"):
    cells = row.find_all("td", class_="Tables__TD-f84ad0-3")
    
    if len(cells) >= 5:  # Check that the row has the expected number of cells
        rank = cells[0].get_text(strip=True)
        name = cells[1].get_text(strip=True).split()
        year = name[0]
        make = name[1]
        model = name[2:]
        rsc_rating = cells[2].get_text(strip=True)
        fatality_risk = cells[3].get_text(strip=True)
        injury_risk = cells[4].get_text(strip=True)

        new_row = pd.DataFrame({
            'rank': [rank],
            'year': [year],
            'make': [make],
            'model': " ".join(name[2:]),
            'rsc_rating': [rsc_rating],
            'fatality_risk': [fatality_risk],
            'injury_risk': [injury_risk]
        })

        df = pd.concat([df, new_row], ignore_index=True)

print(df)