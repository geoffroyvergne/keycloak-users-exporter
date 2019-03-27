import requests
import json
import sys
import csv
import argparse
from types import SimpleNamespace
import configparser

def setConfig(configFile):
	config = configparser.ConfigParser()
	config.read(configFile)

	configMap = {
		"admimUrl": config['DEFAULT']['admimUrl'],
		"adminLogin": config['DEFAULT']['adminLogin'],
		"adminPassword": config['DEFAULT']['adminPassword'],
		"realm": config['DEFAULT']['realm'],
		"client": config['DEFAULT']['client'],

		"csvMap": {
			"firstName": config['CSV']['firstName'],
			"lastName": config['CSV']['lastName'],
			"userName": config['CSV']['userName'],
			"email": config['CSV']['email']
		}
	}

	configMapping = SimpleNamespace(**configMap)
	configMapping.csvMap = SimpleNamespace(**configMap["csvMap"])

	return configMapping

def getKcBearer(url, user, password):
  head={
  	"Accept":       "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
    "username":     user,
    "password":     password,
    "grant_type":   "password",
    "client_id":    "admin-cli",
  }

  result = requests.post(url+"/realms/master/protocol/openid-connect/token",head,proxies={'http':None})
  
  if result.status_code != 200:
  	print("error : " + str(result.status_code) + " " + result.text)

  return result.json()["access_token"]

def prepareKcApiHeaders(bearer):
  head = {
  	"Accept":       "application/json",
    "Content-Type": "application/json",
    "Authorization": "Bearer "+bearer
  }

  return head

def getUser(url,user,password,realm, username):
	bearer = getKcBearer(url, user, password)
	head = prepareKcApiHeaders(bearer)
	result = requests.get(url+"/admin/realms/" + realm + "/users?username=" + username, headers=head,proxies={'http':None})

	if result.status_code != 200:
  		print("getUser return : " + str(result.status_code) + " " + result.text)

	user = result.json()

	return user

def getUsers(url,user,password,realm):
	bearer = getKcBearer(url, user, password)
	head = prepareKcApiHeaders(bearer)
	result = requests.get(url+"/admin/realms/" + realm + "/users", headers=head,proxies={'http':None})

	if result.status_code != 200:
  		print("getUser return : " + str(result.status_code) + " " + result.text)

	users = result.json()

	return users

if __name__ == "__main__":
	
	parser = argparse.ArgumentParser(description='Export Keycloak users to CSV')
	parser.add_argument("-f", "--file", dest="filename", help="CSV file that will contains users", metavar="FILE")
	parser.add_argument("-c", "--config", dest="config", help="Config file", metavar="FILE")
	parser.add_argument("-l", "--limit", help="limit CSV user to export", type=int)

	args = parser.parse_args()

	csvFile = "users.csv"
	if args.filename:
		csvFile = args.filename

	configFile="config.ini"
	if args.config:
		configFile=args.config

	limit = 0
	if args.limit:
		limit = args.limit

	configMap = setConfig(configFile)

	users = getUsers(configMap.admimUrl, configMap.adminLogin, configMap.adminPassword, configMap.realm)

	with open(csvFile, mode='w') as csvFile:
		employee_writer = csv.writer(csvFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		employee_writer.writerow([
			configMap.csvMap.userName, 
			configMap.csvMap.email, 
			configMap.csvMap.firstName, 
			configMap.csvMap.lastName
		])

		for user in users: 
			print(user)
			employee_writer.writerow([
				user["username"], 
				user["email"], 
				user["firstName"], 
				user["lastName"]
			])
