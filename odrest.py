import requests

url_session_login = "https://dev.opendrive.com/api/v1/session/login.json"
url_file_permission = "https://dev.opendrive.com/api/v1/file/access.json"

def login(username, password):
	data = '{ "username": "' + username + '", "passwd": "' + password + '" }'
	response = requests.post(url_session_login, data=data)
	return response

def set_file_permission_public(SID, fileid):
	data = '{ "session_id": "' + SID + '", "file_id": "' + fileid + '", "file_ispublic": 1 }'
	response = requests.post(url_file_permission, data=data)