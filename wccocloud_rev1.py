#!/usr/bin/env python

import json, requests 
import time

from time import localtime, strftime

from neopixel import *

# LED strip configuration:
LED_COUNT      = 21      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 120
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.WS2811_STRIP_RGB

heartbeat      = 0
colorHeart     = Color(0,200,0)

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

#Theater chase display to show activity
def theaterChase(strip, color, wait_ms=50, iterations=10):
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

# Sets the strip colors
def colorAll(strip, colorLeft, colorRight, colorHeart):
#        print 'Setting Left Colors: ', colorLeft
        for i in range((strip.numPixels())/2):
            strip.setPixelColor(i, colorLeft)
#        print 'Setting Right Colors: ', colorRight
	for i in range((strip.numPixels())/2+1,strip.numPixels()):
	    strip.setPixelColor(i, colorRight)
#        print 'Setting Hearbeat Colors: ', heartbeat

        strip.setPixelColor(10, colorHeart)

#        print 'Show Strip'
        strip.show()
#        print 'Showed Strip'

# Gets weather forecast
def getWeather():
    # Change to your location
#    print '--> Setting Location'
    url = requests.get('https://query.yahooapis.com/v1/public/yql?q=select item.forecast from weather.forecast where woeid in (select woeid from geo.places(1) where text="excelsior, mn")&format=json')
    global weather
    weather = json.loads(url.text)
    print weather

    # Gets todays High and Low
#    print '--> Getting Todays Temps'
    global today_high
    today_high = (weather['query']['results']['channel'][0]['item']['forecast']['high'])
    global today_low
    today_low = (weather['query']['results']['channel'][0]['item']['forecast']['low'])

    # Get weather code for today
#    print '--> Getting Todays Weather Code'
    global today_code
    today_code = (weather['query']['results']['channel'][0]['item']['forecast']['code'])
    
    # Gets tomorrows High and Low
#    print '--> Getting Tomorrows Temps'
    global next_high
    next_high = (weather['query']['results']['channel'][1]['item']['forecast']['high'])
    global next_low
    next_low = (weather['query']['results']['channel'][1]['item']['forecast']['low'])

    # Get weather code of tomorrows forecast
#    print '--> Getting Tomorrows Weather Code'
    global next_forecast 
    next_forecast = (weather['query']['results']['channel'][1]['item']['forecast']['code'])

#    print "--> updated weather"
#    print strftime("%a, %d %b %Y %H:%M:%S")
#    print "    todays high is", int(today_high)
#    print "    todays low is", int(today_low)
#    print "    todays code is", int(today_code)
#    print "    tomorrows code is", int(next_forecast)
#    print "    next high is", int(next_high)
#    print "    next low is", int(next_low)
    
###   MAIN   ### 

#initialize lights
theaterChase(strip, Color(153,0,153))
getWeather()
timer = time.time()
timer1 = time.time()

while True:
    # Check time to see if we should be in night mode
    if 8 < int(time.strftime("%H",localtime())) <= 19:
#        print "8 < ",time.strftime("%H",localtime())," <= 19....bright"
        brightness = 1
    elif (19 < int(time.strftime("%H",localtime())) <= 21) or (5 < int(time.strftime("%H",localtime())) <= 8):
#        print "19 < ",time.strftime("%H",localtime()), " <= 21.....dim"
        brightness = 0.2
    else:
        brightness = 0
#        print int(time.strftime("%H",localtime()))

    # Update weather once an hr
#    print '--> Weather Timer: ',time.time() - timer
    if time.time() - timer > 3600:
        getWeather()
        timer = time.time()

    # Heartbeat once per 3 sec
#    print '--> Heartbeat Timer',time.time()-timer1
    if time.time() - timer1 > 3 and heartbeat==0:
	heartbeat = 1
        colorHeart = Color(int(brightness*153),0,int(brightness*153))
        timer1 = time.time()
    elif time.time() - timer1 > 3 and heartbeat==1:
        heartbeat = 0
	colorHeart = Color(int(brightness*150),0,0)
        timer1 = time.time()

    # Check forecast codes to make sure none are rain or snow https://developer.yahoo.com/weather/documentation.html
#    print '--> Check for green'
    if next_forecast == "24" or next_forecast == "26" or next_forecast == "27" or next_forecast == "28" or next_forecast == "29" or next_forecast == "30" or next_forecast == "31" or next_forecast == "32" or next_forecast == "33" or next_forecast == "34" or next_forecast == "36" or next_forecast == "44":
        green_cloud = 0
    else:
        green_cloud = 1
    
    # Adds 10% to todays high than checks to see if that is less than tomorrows high.
    # If tomorrow is more than 10% hotter cloud should be red
#    print '--> Check for red'
    if ((int(today_high)*0.1) +int(today_high)) < int(next_high):
        red_cloud = 1
    else:
        red_cloud = 0

    # Subtracts 10% from todays low than checks to see if that is greater than tomorrows low.
    # If tomorrow is more than 10% colder the cloud should be blue
#    print '--> Check for blue'
    if (int(today_high) -(int(today_high)*0.1)) > int(next_high):
        blue_cloud = 1
    else:
        blue_cloud = 0

    # Check if right cloud should be red
    if red_cloud == 1:
        colorRight = Color(0, int(brightness*90), 0)  # Solid Red Cloud
#        print "--> Set Right Red"

    # Check if right cloud should be blue, we will let red always overide blue
    if blue_cloud == 1 and red_cloud == 0:
         colorRight = Color(0, 0, int(brightness*90))  # Solid Blue Cloud
#         print "--> Set Right Blue"


    # If right cloud is not blue or red or green it should then be white
    if blue_cloud == 0 and red_cloud == 0:
        colorRight=Color(int(brightness*27),int(brightness*27),int(brightness*27))  # Solid white Cloud
#         print "--> Set Right White"

    # If precipitation is forecasted, left side green, otherwise white
    if green_cloud == 1:
#        print '--> Set Left Green'
        colorLeft = Color(int(brightness*50),0,0)
    else:
#        print '--> Set Left White'
        colorLeft=Color(int(brightness*27),int(brightness*27),int(brightness*27))  # Solid white Cloud
     
#    print '--> Set Strip Colors',colorLeft, colorRight
    colorAll(strip, colorLeft, colorRight, colorHeart)
    time.sleep(1)
    
