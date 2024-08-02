import requests
from bs4 import BeautifulSoup

# URL of the webpage you want to scrape
url = 'https://www.pikalytics.com/pokedex/gen9ou'

# Send a GET request to the webpage
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content
    gen9ou = []
    soup = BeautifulSoup(response.text, 'html.parser')
    # Find elements on the webpage using BeautifulSoup
    list = soup.find_all('ul')
    
    # Print the text of each heading
    for item in list:
        member = item.find_all('a')
        for item in member:
            poke = item.find_all('div')
            for item in poke: 
                name = item.find('span', class_='pokemon-name')
                if name:
                    gen9ou.append(name.text[:-1])

    for item in gen9ou:
        print(item.title() + ":")
        url = f'https://www.pikalytics.com/pokedex/gen9ou/{item.lower().replace(" ", "%20")}'
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            # Moves-related data
            moves = {
                "Move": [],
                "Move Type": [],
                "Usage Percentage": []
            }
            teammates = {
                "Teammate": [],
                "Teammate Types": [],
                "Usage Percentage": [],
            }
            move_data = soup.find('div', id='moves_wrapper')
            movelist = move_data.find_all('div', class_='pokedex-move-entry-new')
            for item in movelist:
                move = item.find('div', style='margin-left:10px;display:inline-block;')
                move_type = item.find('span')
                m_usage_percentage = item.find('div', style='display:inline-block;float:right;')
                moves['Move'].append(move.text)
                moves['Move Type'].append(move_type.text)
                moves['Usage Percentage'].append(m_usage_percentage.text)
            # Teammates-related data
            partner_data = soup.find('div', id='teammate_wrapper')
            partnerlist = partner_data.find_all('a', class_='teammate_entry pokedex-move-entry-new')     
            for item in partnerlist:
                types = []
                partner = item.find('div', style='display:inline-block;')
                partnertypes = item.find_all('span')
                for type in partnertypes:
                        types.append(type.text)
                p_usage_percentage = item.find('div', style='display:inline-block;float:right;')
                teammates['Teammate'].append(partner.text.strip('\n'))
                teammates['Teammate Types'].append(types)
                teammates['Usage Percentage'].append(p_usage_percentage.text)
            print(moves)
            print(teammates)
                                   
        else:
            continue
                
else:
    print('Failed to retrieve the webpage')