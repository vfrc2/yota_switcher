import re
import lxml.html as html 
import yota_dev
import my_exceptions
import json
__author__ = 'rdvlip'

def _clear_slider_data(string):
    match = re.search('var sliderData\s*=\s*({.*});', string)
    
    if not match:
      raise my_exceptions.YotaDevParseError

    return json.loads(match.group(1))

def parse_html_for_divs(string):
    page = html.fromstring(string)
    return page.find_class('slider-type-device-wrapper')

def parse_div_for_mac(div):
    elmMac = div.find_class('mac')
    if len(elmMac)< 1:
      raise my_exceptions.YotaDevParseError
    
    return trim_string(elmMac[0].text)

def parse_div_for_name(div):
    elmTitle = div.find_class('device-title')
    if len(elmTitle) < 1:
      raise my_exceptions.YotaDevParseError
    
    return trim_string(elmTitle[0].text)

def parse_div_for_product(div):
    elmProduct = div.xpath("div/form/input[@name='product']")
    if len(elmProduct)<1:
      raise my_exceptions.YotaDevParseError
    
    return elmProduct[0].get('value')

def parse_div_for_currentOffer(div):
    elmCurrentOffer = div.xpath("div/form/input[@name='offerCode']")
    if len(elmCurrentOffer)<1:
      raise my_exceptions.YotaDevParseError
    
    return elmCurrentOffer[0].get('value')
    
def parse_html_for_tariffs(string, yotaDev):
    data =_clear_slider_data(string)
    
    offers = data[yotaDev._product]['steps']
    
    result =[]
    
    for offer in offers:
      result.append(parse_json_offer(offer, yotaDev))

    return result

def parse_json_offer(data, yotaDev):
    yotaOffer = yota_dev.yotaOffer(yotaDev)
    yotaOffer._offerCode = data['code']
    yotaOffer._remain = data['remainNumber'] + ' ' + data['remainString']
    yotaOffer._cost = data['amountNumber']
    yotaOffer._costName = data['amountNumber'] + ' ' + data['amountString']
    yotaOffer._speed = data['speedNumber'] 
    yotaOffer._speedName = data['speedNumber'] + ' ' + data['speedString']
    yotaOffer._desc = data['name']
    return yotaOffer
  

def trim_string(string):
    return string.strip(' \t\n\r')

def string_to_speed(string):
    if string == 'max':
        return 20.0
    elif '.' in string:
        speed = float(string)
    else:
        speed = int(string)
    return speed
