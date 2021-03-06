from PixieBoardGPSLocation.PixieBoardGPSLocation import PixieBoardGPSLocation
import requests, json
import time

LOGGING_MSG_EXP_PING_TIMOUT = "Time Out"
LOGGING_MSG_EXP_REQUEST_EXCEPTION = "Request Exception"
LOGGING_MSG_EXP_HTTP_ERROR = "HTTPError: "
LOGGING_MSG_EXP_CONN_ERROR = "ConnectionError: "

API_GATEWAY = "Place api url here"

PIXIE_BOARD_ID = 13

def SendLocation(pixieboard_id, lat, lng):
	try:
		print("Send data")
		url = API_GATEWAY
		data = {'PixieBoardsLocation': { 'PixieBoardID': pixieboard_id, 'Latitude': lat, 'Longitude': lng}} 
		headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
		r = requests.post(url, data=json.dumps(data), headers=headers)		
		print(r.text)
	except requests.exceptions.Timeout:
		print(LOGGING_MSG_EXP_PING_TIMOUT)
	except requests.exceptions.RequestException as e:
		print(LOGGING_MSG_EXP_REQUEST_EXCEPTION + "%s",e)
	except requests.exceptions.HTTPError as err:
		print(LOGGING_MSG_EXP_HTTP_ERROR + "%s",err)
	except requests.exceptions.ConnectionError as err:
		print(LOGGING_MSG_EXP_CONN_ERROR + "%s",err)

def LocationLoop():
	print("Start")
	pxbdGPSLocation = PixieBoardGPSLocation()
	sessionStoped, raw, error = pxbdGPSLocation.EnableATCommands()
	print(raw)
	sessionStoped, raw, error = pxbdGPSLocation.StopSession()
	print(raw)
	sessionStoped, raw, error = pxbdGPSLocation.ConfigureGPSTracking()
	print(raw)
	print("Get Location")
	pxbdGPSLocation.WaitUntilGPSIsAvailablePretty()
	SendLocation(PIXIE_BOARD_ID, pxbdGPSLocation.Latitude, pxbdGPSLocation.Longitude)
	print("Location Sent")


LocationLoop()
