import web
import parser
import my_exceptions

class yotaDev:

  def __init__(self, web, mac='', name=''):
    self._title = None #Yota Dev Name
    self._product = None 
    self._mac = None
    self._currentOfferCode = None
    self._offers = None
    
    if web and (mac or name):
      self.loadDev(web, mac, name)
  
  def loadDev(self, web, mac='',name=''):
    page = web._get_main_page_content()
    sliders = parser.parse_html_for_divs(page)
    
    for slider in sliders:
      if (mac and parser.parse_div_for_mac(slider) == mac) or (name and parser.parse_div_for_name(slider) == name): 
        self._title = parser.parse_div_for_name(slider)
        self._product = parser.parse_div_for_product(slider)
        self._mac = parser.parse_div_for_mac(slider)
        self._currentOfferCode = parser.parse_div_for_currentOffer(slider)
        self._offers = parser.parse_html_for_tariffs(page,self)

        return
    raise my_exceptions.YotaDevNotFound 
            
  def updateDev(self, web):
    self.loadDev(web, self._mac)    
  
  def get_currentOffer(self):
    return self.get_tariff(code = self._currentOfferCode)
  
  def get_tariff(self, code='', cost='', speed=''):
    for offer in self._offers:
      if (code and offer._offerCode == code) or (cost and offer._cost == cost) or (speed and offer._speed == speed):
        return offer
        
    raise my_exceptions.YotaDevOfferNotFound
  
  def switch_offer(self, web, newOffer):
    
    r = web._change_tariff(self._product, newOffer._offerCode)
    
    self.updateDev(web)

    if not newOffer._offerCode == self._currentOfferCode:
        raise my_exceptions.TariffChangeError

    return r

class yotaOffer:
  def __init__(self, device):
    self._device = device
    self._offerCode = None
    self._cost = None
    self._remain = None
    self._speed = None
    self._desc = None

#Global fuctions
def GetYotaDevMacs(web):
  page = web._get_main_page_content()
  sliders = parser.parse_html_for_divs(page)
  return [parser.parse_div_for_mac(slider) for slider in sliders]
  
    
