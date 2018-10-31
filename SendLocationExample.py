from PixieBoardGPSLocation import PixieBoardGPSLocation
import requests, json
import time

LOGGING_MSG_EXP_PING_TIMOUT = "Time Out"
LOGGING_MSG_EXP_REQUEST_EXCEPTION = "Request Exception"
LOGGING_MSG_EXP_HTTP_ERROR = "HTTPError: "
LOGGING_MSG_EXP_CONN_ERROR = "ConnectionError: "

API_GATEWAY = "https://k2j1e9ygt0.execute-api.us-west-1.amazonaws.com/prod/storelocation"

PIXIE_BOARD_ID = 113

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
	if sessionStoped:
		sessionStoped, raw, error = pxbdGPSLocation.ConfigureGPSTracking()
		print(raw)
	print("Get Location")
	while True:
		sessionStoped, raw, error = pxbdGPSLocation.GetGPSLocationPretty()
		if sessionStoped:
			SendLocation(PIXIE_BOARD_ID, pxbdGPSLocation.Latitude, pxbdGPSLocation.Longitude)
			print("Location Sent")
			break
		else:
			time.sleep(8)
		

LocationLoop()
