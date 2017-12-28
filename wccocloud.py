import json, requests
import time

from neopixel import *

# LED strip configuration:
LED_COUNT      = 20      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = 60
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0
LED_STRIP      = ws.WS2811_STRIP_RGB

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
# Intialize the library (must be called once before other functions).
strip.begin()

# Generate rainbow colors across 0-255 positions
def wheel(pos):
        if pos < 85:
                return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
                pos -= 85
                return Color(255 - pos * 3, 0, pos * 3)
        else:
                pos -= 170
                return Color(0, pos * 3, 255 - pos * 3)


# Rainbow movie theater light style chaser animation
def theaterChaseRainbow(strip, wait_ms=50):
        for j in range(256):
                for q in range(3):
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, wheel((i+j) % 255))
                        strip.show()
                        time.sleep(wait_ms/1000.0)
                        for i in range(0, strip.numPixels(), 3):
                                strip.setPixelColor(i+q, 0)


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

# Sets the strip all one color
def colorAll(strip, color):
        for i in range(strip.numPixels()/2):
            strip.setPixelColor(i, color)
	for i in range(strip.numPixels()/2,strip.numPixels()):
	    strip.setPixelColor(i, Color(30,30,0))
        strip.show()

# Flickers the cloud blue
def blueFlicker():
    colorAll(strip, Color(0, 0, 90))
    time.sleep(.1)
    colorAll(strip, Color(0, 0, 70))
    time.sleep(.1)
    colorAll(strip, Color(0, 0, 50))
    time.sleep(.1)
    colorAll(strip, Color(0, 0, 30))
    time.sleep(.1)
    colorAll(strip, Color(0, 0, 50))
    time.sleep(.1)
    colorAll(strip, Color(0, 0, 70))
    time.sleep(.1)

# Flickers the cloud red
def redFlicker():
    colorAll(strip, Color(0, 90, 0))
    time.sleep(.1)
    colorAll(strip, Color(0, 70, 0))
    time.sleep(.1)
    colorAll(strip, Color(0, 50, 0))
    time.sleep(.1)
    colorAll(strip, Color(0, 30, 0))
    time.sleep(.1)
    colorAll(strip, Color(0, 50, 0))
    time.sleep(.1)
    colorAll(strip, Color(0, 70, 0))
    time.sleep(.1)

# Flickers the cloud green
def greenFlicker():
    colorAll(strip, Color(90, 0, 0))
    time.sleep(.1)
    colorAll(strip, Color(70, 0, 0))
    time.sleep(.1)
    colorAll(strip, Color(50, 0, 0))
    time.sleep(.1)
    colorAll(strip, Color(30, 0, 0))
    time.sleep(.1)
    colorAll(strip, Color(50, 0, 0))
    time.sleep(.1)
    colorAll(strip, Color(70, 0, 0))
    time.sleep(.1)

# Gets weather forecast
def getWeather():
    # Change to your location
    url = requests.get('https://query.yahooapis.com/v1/public/yql?q=select item.forecast from weather.forecast where woeid in (select woeid from geo.places(1) where text="excelsior, mn")&format=json')
    global weather
    weather = json.loads(url.text)

    # Gets todays High and Low
    global today_high
    today_high = (weather['query']['results']['channel'][0]['item']['forecast']['high'])
    global today_low
    today_low = (weather['query']['results']['channel'][0]['item']['forecast']['low'])

    # Get weather code for today
    global today_code
    today_code = (weather['query']['results']['channel'][0]['item']['forecast']['code'])
    
    # Gets tomorrows High and Low
    global next_high
    next_high = (weather['query']['results']['channel'][1]['item']['forecast']['high'])
    global next_low
    next_low = (weather['query']['results']['channel'][1]['item']['forecast']['low'])

    # Get weather code of tomorrows forecast
    global next_forecast 
    next_forecast = (weather['query']['results']['channel'][1]['item']['forecast']['code'])

    print "--> updated weather"
    print "    todays high is", int(today_high)
    print "    todays low is", int(today_low)
    print "    todays code is", int(today_code)
    print "    tomorrows code is", int(next_forecast)
    print "    next high is", int(next_high)
    print "    next low is", int(next_low)
    
###   MAIN   ### 

#initialize lights
theaterChase(strip, Color(0,64,64))
getWeather()
timer = time.time()

while True:
    # Update weather once an hr
    if time.time() - timer > 3600:
        getWeather()
        timer = time.time()

    # Check forecast codes to make sure none are rain or snow https://developer.yahoo.com/weather/documentation.html
    if next_forecast == "24" or next_forecast == "26" or next_forecast == "27" or next_forecast == "28" or next_forecast == "29" or next_forecast == "30" or next_forecast == "31" or next_forecast == "32" or next_forecast == "33" or next_forecast == "34" or next_forecast == "36" or next_forecast == "44":
        green_cloud = 0
    else:
        green_cloud = 1
    
    # Adds 10% to todays high than checks to see if that is less than tomorrows high.
    # If tomorrow is more than 10% hotter cloud should be red
    if ((int(today_high)*0.1) +int(today_high)) < int(next_high):
        red_cloud = 1
    else:
        red_cloud = 0

    # Subtracts 10% from todays low than checks to see if that is greater than tomorrows low.
    # If tomorrow is more than 10% colder the cloud should be blue
    if (int(today_low) -(int(today_low)*0.1)) > int(next_low):
        blue_cloud = 1
    else:
        blue_cloud = 0

    # Check if cloud should be red
    if red_cloud == 1:
#        if flicker == 0:
        colorAll(strip, Color(0, 90, 0))  # Solid Red Cloud
#        print "Red Cloud"
#        else:
#            redFlicker()

    # Check if cloud should be blue, we will let red always overide blue
    if blue_cloud == 1 and red_cloud == 0:
#        if flicker == 0:
         colorAll(strip, Color(0, 0, 90))  # Solid Blue Cloud
#         print "Blue Cloud"
#        else:
#            blueFlicker()


    # If cloud is not blue or red or green it should then be white
    if blue_cloud == 0 and red_cloud == 0 and green_cloud == 0:
#        if flicker == 0:
         colorAll(strip, Color(50, 50, 50))  # Solid white Cloud
#         print "White Cloud"
#        else:
#            greenFlicker()

    # If precipitation is forecasted, green flickering cloud overrides everything
    if green_cloud == 1:
	greenFlicker()
#        print "Green Flicker"
