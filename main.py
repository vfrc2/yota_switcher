#!/usr/bin/python

import sys
import web
import yota_dev
import argparse

arg = None

def main(args):

	#	print '\nExample:'
	#	print '   yota -lq <user> <pass> - show all devs on account'
	#	print '   yota -m <mac> -tq - show dev by <mac> and its tariffs'
	#	print '   yota -m <mac> -sq max <user> <pass> - set max speed for dev by <mac>'
	#	print '   yota <user> <pass> - interactive mode'
	#	exit()
	
	arg = ParseArgs()
	
	wb = web.Web()
	
	if not wb._auth(arg.login,arg.passw):
	  print 'Auth bad'
  
	if arg.device_mac:
	  devs = [yota_dev.yotaDev(wb, mac=arg.device_mac)]
	elif arg.device_name:
	  devs = [yota_dev.yotaDev(wb, name=arg.device_name)]
	else:
	  devs = [yota_dev.yotaDev(wb,mac) for mac in yota_dev.GetYotaDevMacs(wb)]
	  
	if len(devs)<1:
	  print 'No yota device for account!'
	  exit()
	
	if arg.set_speed or arg.set_tariff or arg.set_cost:
          if not arg.all and len(devs)>1:

            print 'Can\'t set teriff for more then one dev (use --all to override)'
            exit()

	  arg.list = False
	  arg.tariff = False
	  
	for dev in devs:
	  if arg.info:
	    PrintYotaDev(dev, arg.tariff)
	  if arg.set_speed or arg.set_tariff or arg.set_cost:
	    new_offer = dev.get_tariff(code = arg.set_tariff, cost = arg.set_cost, speed = arg.set_speed)
	    print 'Change offer to: '
	    PrintYotaOffer(new_offer)
	    dev.switch_offer(wb,new_offer)
	    print 'Change success'
	    
	      

def PrintYotaDev(yotaDev,withTariffs=False):
  print '#########'
  print 'Device  :', yotaDev._title
  print 'Mac     :', yotaDev._mac
  print 'Product :', yotaDev._product
  print 'Curret offer:'
  PrintYotaOffer(yotaDev.get_currentOffer())
  if withTariffs:
    print 'Avalible offers: '
    for offer in yotaDev._offers:
      PrintYotaOffer(offer)
  print '#########'

def PrintYotaOffer(yotaOffer):
  print ' - ',yotaOffer._offerCode,':',yotaOffer._desc,':',yotaOffer._remain  

def ParseArgs():
  parser = argparse.ArgumentParser(description='Yota tariff switcher',
    prog='yota')
  parser.add_argument('login', type=str)
  parser.add_argument('passw', type=str)
  
  parser.add_argument('-l', '--list', action='store_true', 
    help='list all yota devices (not in -q)', default = True)
  parser.add_argument('-i', '--info', action='store_true',
    help='show info (default) (not in -q)', default = True)
  parser.add_argument('-t', '--tariff', action='store_true', default = False,
    help='show info and tariffs (not in -q)')
  
  parser.add_argument('-m', '--device-mac',
    help='select device by mac')
  parser.add_argument('-n', '--device-name',
    help='select device by name')
  parser.add_argument('--all', help='select all devices', action='store_true',
	default = False)
  
  parser.add_argument('-s', '--set_speed', help='select tariff by speed')
  parser.add_argument('-r', '--set_tariff', help='select tariff by offer code')
  parser.add_argument('-c', '--set_cost', help='select tariff by cost')
  args = parser.parse_args()
  
  return args
                

if __name__ == '__main__':
	main(sys.argv)
