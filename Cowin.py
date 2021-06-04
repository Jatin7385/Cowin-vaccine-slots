import requests
import datetime
import time

def getDate():
  current_time = datetime.datetime.now()
  day =  str(current_time.day)
  month = str(current_time.month)
  year = str(current_time.year)
  if int(day)<10:
      day = '0' + day
  if int(month)<10:
      month = '0' + month

  date = day + "-"+month + "-" + year
  return date

def getStatesId():
  Url = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
  header = {
          'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
  response = requests.get(Url,headers = header).json()
  data = response["states"]
  print("The states are :-")
  for each in data:
    print(str(each['state_id'])+". "+each['state_name'])
  print("Enter the state number")
  state = input()  
  return state

def getDistrictId(state):
  Url = 'https://cdn-api.co-vin.in/api/v2/admin/location/districts/'+state
  header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'}
  response = requests.get(Url,headers = header).json()
  data = response['districts']
  print()
  print("District-Id,District Name")
  for each in data:
    print(each['district_id'],each['district_name'])
  print("Enter the district id")
  districtId = input()
  return districtId

def available(districtId,age):
  date = getDate()
  Url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict?district_id={}&date={}".format(districtId,date)
  header = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
  response = requests.get(Url,header).json()
  data = response["sessions"]
  counter = 0
  print("Vaccines available at:-")
  for each in data:
    if(each["available_capacity"]>0 and each["min_age_limit"] == age): 
      counter += 1
      print("Name : ",each["name"])
      print("Pincode : ",each["pincode"])
      print("Vaccine : ",each["vaccine"])
      print("Available Capacity : ",each["available_capacity"])
      return True
      if(counter == 0):
          print("No Available Slots")
          return False

state = getStatesId()
districtId = getDistrictId(state)
print()
print("Enter your age : ")
age = int(input())
print()
ageGroup = 0
if(age>=60):
  ageGroup = 60
elif(age>=45):
  ageGroup = 45
elif(age>=18):
  ageGroup = 18
while(available(districtId,ageGroup)!=True):
  time.sleep(5)
  available(districtId,ageGroup)

