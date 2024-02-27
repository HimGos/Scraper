import scrapy
from datetime import datetime
import json

class CurrencySpider(scrapy.Spider):
    name = 'currency'
    start_urls = ['https://www.livecharts.co.uk/currency-strength.php']

    def getCurrencyData(self, response):
        now = datetime.now()
        data = []
        to_check = ['EURO', 'USD', 'GBP', 'AUD', 'CAD', 'JPY', 'NZD', 'CHF']
        for currency in response.css('#rate-outercontainer'):
            currency_name = currency.css('#map-innercontainer-symbol::text').get()
            if not currency_name in to_check:
                continue
            strength = 0
            weak3 = True if currency.css('#map-innercontainer-weak3') else False
            weak2 = True if currency.css('#map-innercontainer-weak2') else False
            weak1 = True if currency.css('#map-innercontainer-weak1') else False
            strong1 = True if currency.css('#map-innercontainer-strong1') else False
            strong2 = True if currency.css('#map-innercontainer-strong2') else False
            strong3 = True if currency.css('#map-innercontainer-strong3') else False

            if strong3:
                strength = 3
            elif strong2:
                strength = 2
            elif strong1:
                strength = 1
            elif weak1:
                strength = -1
            elif weak2:
                strength = -2
            else:
                strength = -3

            data.append({'date': now.strftime("%d/%m %H:%M"), 
                         'currency':currency_name, 
                         'strength': strength})
            
        json_data = json.dumps(data)

        return json_data
