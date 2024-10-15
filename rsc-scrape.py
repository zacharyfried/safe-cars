from bs4 import BeautifulSoup
import requests

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
        suv_model = cells[1].get_text(strip=True)
        rsc_rating = cells[2].get_text(strip=True)
        fatality_risk = cells[3].get_text(strip=True)
        injury_risk = cells[4].get_text(strip=True)

        print(f"Rank: {rank}, SUV Model: {suv_model}, RSC Rating: {rsc_rating}, Fatality Risk: {fatality_risk}, Injury Risk: {injury_risk}")