import asyncio
import websockets
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def scrape_data():
    try:
        url = 'https://www.livecharts.co.uk/currency-strength.php'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        currencies = ['EURO', 'GBP', 'USD', 'AUD', 'JPY', 'CHF', 'NZD', 'CAD']
        data = []
        now = datetime.now()
        for div in soup.find_all('div', id='rate-outercontainer'):
            currency_name = div.find('div', id='map-innercontainer-symbol').text
            if currency_name not in currencies:
                continue
            strength = 0
            if div.find('div', id='map-innercontainer-strong3'):
                strength = 3
            elif div.find('div', id='map-innercontainer-strong2'):
                strength = 2
            elif div.find('div', id='map-innercontainer-strong1'):
                strength = 1
            elif div.find('div', id='map-innercontainer-weak1'):
                strength = -1
            elif div.find('div', id='map-innercontainer-weak2'):
                strength = -2
            else:
                strength = -3
            data.append({'time': now.strftime('%d/%m %H:%M'), 'currency': currency_name, 'strength': strength})
        return data
    except Exception as e:
        print(f"Scraping error occurred: {e}")



async def broadcast_currency_updates(websocket, path):
    while True:
        data = scrape_data()
        json_data = json.dumps(data)
        print(json_data)
        await websocket.send(json_data)
        await asyncio.sleep(60)

if __name__ == "__main__":
    print("Starting Server...")
    start_server = websockets.serve(broadcast_currency_updates, '0.0.0.0', 5000)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


