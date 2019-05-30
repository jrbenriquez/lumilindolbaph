from datetime import datetime, date
from bs4 import BeautifulSoup
from urllib.request import urlopen


# Main Flow
# Get copy of website every 5 minutes
# If no saved instance (i.e 1st ping) save html_page text to Database
# If soups are the same > DO NOTHING
# ELSE do below

HOMEPAGE = 'https://earthquake.phivolcs.dost.gov.ph/'

html_page = urlopen(HOMEPAGE)

soup = BeautifulSoup(html_page)


EARTHQUAKE_CLASSES = {
    'Micro': [1.0, 1.9],
    'Minor': [2.0, 3.9],
    'Light': [4.0, 4.9],
    'Moderate': [5.0, 5.9],
    'Strong': [6.0, 6.9],
    'Major': [7.0, 7.9],
    'Great': [8.0, 999999],
}

for tr in soup.findAll('tr'):

    valid_row = tr.findChild('td', attrs={'class': 'auto-style91'})

    if valid_row:
        table_data = tr.findAll('td')
        link_cell = table_data[0]
        latitude_cell = table_data[1]
        longitude_cell = table_data[2]
        depth_cell = table_data('td')[3]
        magnitude_cell = table_data('td')[4]
        location_cell = table_data('td')[5]
        working_date = None
        a_tag = link_cell.find('a')
        date_span = a_tag.find('span')
        if date_span:
            working_date = date_span.get_text()
        if not date_span:
            working_date = a_tag.get_text(strip=True)
        if working_date:
            proper_date = datetime.strptime(working_date, '%d %B %Y - %I:%M %p')
            print(proper_date)
            # Print Link
            print('{}{}'.format(HOMEPAGE, a_tag.get('href').replace('\\', '/')))
            # LATITUDE
            print(latitude_cell.get_text(strip=True))
            # LONGITUDE
            print(longitude_cell.get_text(strip=True))
            # DEPTH
            print(depth_cell.get_text(strip=True))
            # MAGNITUDE
            print(magnitude_cell.get_text(strip=True))
            # LOCATION
            print(location_cell.get_text(strip=True))

