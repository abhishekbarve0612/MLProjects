import speech_recognition as sr
from gtts import gTTS
import playsound
import os
import requests
import math

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import time
import json

def get_location():
  options = Options()
  options.add_argument("--use--fake-ui-for-media-stream")
  driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=options)
  timeout = 20
  driver.get("https://mycurrentlocation.net/")
  wait = WebDriverWait(driver, timeout)
  time.sleep(3)
  longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
  longitude = [x.text for x in longitude]
  longitude = str(longitude[0])
  latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
  latitude = [x.text for x in latitude]
  latitude = str(latitude[0])
  driver.quit()
  return (latitude, longitude)

r = sr.Recognizer()

def voice_command_processor():
  with sr.Microphone() as source:
    audio = r.listen(source, phrase_time_limit = 10)
    text = ""
    try:
      text = r.recognize_google(audio)
    except sr.UnknownValueError as e:
      print(e)
    except sr.RequestError as e:
      print("service is down with error: ", e)

    return text.lower()

def audio_playback(text):
  filename = "./output/test.mp3"
  tts = gTTS(text=text, lang="en-us")
  tts.save(filename)
  playsound.playsound(filename)
  os.remove(filename)

def text_match(text, list):
  if len(set(text.split(" ")) &  set(list)) > 0:
    return True 
  return False

def execute_voice_command(text):
  if "what are you" in text:
    audio_playback("I am an Eagle Sight Assistant, here to assist you while driving")
  elif text_match(text, ["weather", "whether", "How is the weather today", "sunny", "rain", "cloud"]):
    audio_playback("Checking Weather Please Wait...")
    get_weather()
  elif text_match(text, ["corona", "covid", "covid 19", "crisis"]):
    audio_playback("Getting Corona Updates. Please Wait...")
    get_corona_updates()
  elif "exit" in text or "quit" in text or "shut down" in text or "turn off" in text:
    audio_playback("Shutting Down! Good Bye")
    quit()
  else:
    audio_playback("Pardon Me! I didn't get you. Can you please repeat your command?")

def get_corona_updates():
  url = "https://api.covid19india.org/data.json"
  payload={}
  headers = {}
  audio_playback("Getting Covid Updates. Please Wait")
  response = requests.request("GET", url, headers=headers, data=payload)
  data = json.loads(response.text)
  total = data["statewise"][0]
  total_active_cases = total["active"]
  total_recovered_cases = total["recovered"]
  total_confirmed_cases = total["confirmed"]
  total_deaths = total["deaths"]
  updated_on = total["lastupdatedtime"]
  text = "Corona Update In India: There are total " + total_active_cases + " active cases among them " + total_confirmed_cases + " are confirmed to be positive. Till now India suffered with " + total_deaths + " losses of our people. " + total_recovered_cases + " people have successfully fought and recovered from the corona till now. This statistics was last updated on " + updated_on
  print(text)
  audio_playback(text) 

# get_corona_updates()

def get_weather():
  lat, long = get_location()
  url = "https://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + long +"&appid=3c538755f0dc5548066c57d94287ad6a&units=metric"
  payload={}
  headers = {}

  response = requests.request("GET", url, headers=headers, data=payload)
  data = json.loads(response.text)
  print(data)
  description = data["weather"][0]['description']
  city = data["name"]
  temp = data["main"]["temp"]
  wind = data["wind"]["speed"]
  text = "Currently there are " + description + " in " + city + " with average temperature of " + str(temp) + " degree celsius and wind speed of approximately " + str(wind) + " meter per second."
  audio_playback(text)  
  print(text)

# # get_weather()
def runAssistant():
  while True:
    command = voice_command_processor()
    print(command)
    execute_voice_command(command)

def find_new_coordinate(latitude, longitude, dist):
  earth = 6378.137
  pi = math.pi
  m = (1 / ((2 * pi / 360) * earth)) / 1000;
  new_latitude = latitude + (dist * m);
  new_longitude = longitude + (dist * m) / math.cos(latitude * (pi / 180));
  print("+", dist ,":",new_latitude, new_longitude)

# find_new_coordinate(21.22209216843815, 79.18742460654845, 5000)
# find_new_coordinate(21.22209216843815, 79.18742460654845, -5000)

# while True:
#     command = voice_command_processor()
#     print(command)
#     execute_voice_command(command)
