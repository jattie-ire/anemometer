#! /bin/python
#from sys import path
#path.append('/home/jattie/.local')
import RPi.GPIO as GPIO
from time import sleep, time
from datetime import datetime
from numpy import pi
from os.path import exists
import logging
from yaml import unsafe_load as yaml_load


def setup_logging(config):
  '''
  Logging is a stanbdard python library and this code is for setting 
  up logger from yaml configuration section logger
  INFO or DEBUG logs more or less datailsed data, the default is info
  The three options for file stream of bot selects logging to file or 
  printing to the console or doing both. 
  The last option os the logging string format. The string format is 
  covered in detaoils in the logger documentation.
  '''
    
  #print(f'logger config: {config}')
  if config['level']=='INFO':
    lvl=logging.INFO
  elif config['level']=='DEBUG':
    lvl=logging.DEBUG
  else:
    lvl=logging.NOTSET
  if config['handler'] == 'file':
    lhandlers=[
      logging.FileHandler(filename=config['filepath'], mode=config['filemode'])
    ]
  elif config['handler'] == 'stream':
    lhandlers=[
      logging.StreamHandler()
    ]
  elif config['handler'] == 'both':
    lhandlers=[
      logging.FileHandler(filename=config['filepath'], mode=config['filemode']),
      logging.StreamHandler()
    ]
  logging.basicConfig(
    level=lvl,
    format=config['format'],
    handlers=lhandlers
    )
  #logging.getLogger().addHandler(logging.StreamHandler())
  logging.getLogger(__name__)
  #iFormat=IndentFormatter(config['format'])
  #lhandlers[0].setFormatter(iFormat)
  #lhandlers[1].setFormatter(iFormat)
  return logging


def calculate_wind_speed(channel):
  #logging.debug(f'calculate windspeed routine triggered')
  global c, t0, t1,cwd
  c+=1
  iv=GPIO.input(channel)
  if iv==0:
    if t1==None: t1=t0 # the time the application was launched
    t=time()-t1
    rpm=60/t
    #wind speed (m/s) = (π * cup diameter * rpm) / (60 * cup center distance)
    radial_speed = 2*pi*0.2*(rpm/60)
    #wind_speed = (pi * 0.08 * rpm) / (60 * 0.160)
    wind_speed = (pi * 0.08 * rpm) / (60 * 0.100)
    knots=wind_speed * 1.94384
    dts=datetime.now().date().strftime('%y%m%d')
    if not exists(f'{cwd}/log/{dts}.csv'):
      with open(f'{cwd}/log/{dts}.csv', 'a') as fp:
        fp.write('datetime,seconds_per_rpm,radial_speed,rpm,wind_speed_ms,wind_speed_kmh,knots\n')
    if wind_speed < 15: # a debounce issue occured at slow speeds, 
      marker=''
      with open(f'{cwd}/log/{dts}.csv', 'a') as fp:
        fp.write(f'{datetime.now()},{t},{radial_speed},{rpm},{wind_speed},{wind_speed*3.6},{knots}\n')
    else: 
      marker='<=============='
    logging.debug(f'time: {t:6.3f}s radial_speed: {radial_speed:6.3f} rpm: {rpm:6.3f} wind speed: {wind_speed:6.3f}m/s wind speed: {wind_speed*3.6:6.3f}km/h knots: {knots:6.3f} {marker}')
    t1=time()


def calculate_rainfall(channel):
  logging.debug(f'rainfall input was triggered')

if __name__ == '__main__':

  GPIO.cleanup()
  cwd='/home/jattie'
  with open(f'{cwd}/gpio_interrupt.yaml') as fp:
    config=yaml_load(fp)
  logging = setup_logging(config['logger'])
  logging.info('='*100)
  logging.info(f'Config Loaded, loggining initialised...')
  logging.debug(f'cwd: {cwd}')

  logging.info(f'Setting up GPIO')
  GPIO.setmode(GPIO.BCM) # GPIO pins referred to by their Broadcom SOC channel numbers
  #set up the counter for the anemometer
  GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # sets up GPIO pin 23 as an input pin with a pull-down resistor
  GPIO.add_event_detect(23, GPIO.FALLING, callback=calculate_wind_speed, bouncetime=100)
  #set up the counter for the rainmeter
  #GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # sets up GPIO pin 23 as an input pin with a pull-down resistor
  #GPIO.add_event_detect(24, GPIO.FALLING, callback=calculate_rainfall)#, bouncetime=100

  c=0
  t0,t1=time(),None
  logging.info(f'{datetime.now()} Wait for interrupts to calculate wind speed')
  while 1:
    sleep(1)

  GPIO.cleanup()
  logging.info(f'{datetime.now()} exiting...')
