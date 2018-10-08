from utils import isValidInteger, updateCount, getLatestCount
import traceback
import socket
from urllib.parse import unquote
import datetime
import random
import re
import sys
import requests
import json

port = '80'
time_info_url = "http://172.22.0.222:5000"

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = socket.gethostbyname(local_hostname)

# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port
server_address = (ip_address, int(port))  
print ('starting up on %s port %s' % server_address)  
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)

def get_content_length(response):
	return len(response)

def get_bad_request_response(reason):
	response = '400 Bad Request: Reason: ' + reason + '\n'
	response = response.encode('utf-8')
	header = 'HTTP/1.1 400 Bad Request\n'
	mimetype = 'text/plain'
	header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
	header += 'Connection: close\n'
	contentLength = get_content_length(response)
	header += 'Content-Length: ' +  str(contentLength) + '\n\n'
	final_response = header.encode('utf-8')
	final_response += response
	return final_response

def get_not_found_request_response():
	response = '404 Not Found\n'
	response = response.encode('utf-8')
	header = 'HTTP/1.1 404 Not Found\n'
	mimetype = 'text/plain'
	header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
	header += 'Connection: close\n'
	contentLength = get_content_length(response)
	header += 'Content-Length: ' +  str(contentLength) + '\n\n'
	final_response = header.encode('utf-8')
	final_response += response
	return final_response

def get_not_implemented_request_response(reason):
	response = '501 Not Implemented: Reason:' + reason + '\n'
	response = response.encode('utf-8')
	header = 'HTTP/1.1 501 Not Implemented\n'
	mimetype = 'text/plain'
	header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
	header += 'Connection: close\n'
	contentLength = get_content_length(response)
	header += 'Content-Length: ' +  str(contentLength) + '\n\n'
	final_response = header.encode('utf-8')
	final_response += response
	return final_response


def get_redirect_to_hello_world_response(ip):
	response = '302 Found\n'.encode('utf-8')
	contentLength = get_content_length(response)
	header = 'HTTP/1.1 302 Found\n'
	header += 'Location: /hello-world\n'
	mimetype = 'text/plain'
	header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
	header += 'Connection: close\n'
	header += 'Content-Length: ' +  str(contentLength) + '\n\n'
	final_response = header.encode('utf-8')
	final_response += response
	return final_response







def get_status(status):
	if status == 200:
		return 'OK'
	elif status == 400:
		return 'Bad Request'
	elif status == 404:
		return 'Not Found'

def build_header(status, mimetype, response):
	response_status = str(status) + ' ' + get_status(status)
	header = 'HTTP/1.1 '+ response_status +'\n'
	header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
	header += 'Connection: close\n'
	header += 'Content-Length: ' + str(get_content_length(response)) + '\n\n'
	return header.encode('utf-8')

def build_hello_service_response(apiVersion, count, currentVisit, response):
	response = '{' + '"apiversion": {}, "count": {}, "currentvisit": "{}", "response": "{}"'.format(apiVersion, count, str(currentVisit), response) + '}'
	return response.encode('utf-8')

def build_plus_one_service_response(apiVersion, val):
	response = '{' + '"apiversion": {}, "plusoneret": {}'.format(apiVersion, val) + '}'
	return response.encode('utf-8')

def build_response_failed(status, description):
	response = '{' + '"detail": {}, "status": {}, "title": "{}"'.format(description, status, get_status(status)) + '}'
	return response.encode('utf-8')

count = getLatestCount()

while True:  
	
	connection, client_address = sock.accept()

	try:

		request = connection.recv(1024).decode('utf-8')
		string_list = re.split(' |\n',request)
		method = string_list[0].strip()
		path = string_list[1].strip()
		protocol = string_list[2].strip()

		if protocol != 'HTTP/1.0' and protocol != 'HTTP/1.1':
			final_response = get_bad_request_response(protocol)            
			connection.send(final_response)

		elif method != 'GET' and method != 'POST':
			final_response = get_not_implemented_request_response(method) 
			connection.send(final_response)

		else:
			if method == 'GET':
				if path == '/':

					final_response = get_redirect_to_hello_world_response(ip_address)
					connection.send(final_response)

				elif path == '/hello-world':

					file = open('hello-world.html', 'rb')
					response = file.read()
					response = response.decode().replace('__HELLO__', 'World')
					response = response.encode('utf-8')
					contentLength = get_content_length(response)
					file.close()
					header = 'HTTP/1.1 200 OK\n'
					mimetype = 'text/html'
					header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
					header += 'Connection: close\n'
					header += 'Content-Length: ' +  str(contentLength) + '\n\n'
					final_response = header.encode('utf-8')
					final_response += response

					connection.send(final_response)

				elif path == '/style':

					file = open('style.css', 'rb')
					response = file.read()
					file.close()
					header = 'HTTP/1.1 200 OK\n'
					mimetype = 'text/css'
					header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
					header += 'Connection: close\n'
					contentLength = get_content_length(response)
					header += 'Content-Length: ' +  str(contentLength) + '\n\n'
					final_response = header.encode('utf-8')
					final_response += response

					connection.send(final_response)

				elif path == '/background':

					file = open('background.jpg', 'rb')
					response = file.read()
					file.close()
					header = 'HTTP/1.1 200 OK\n'
					mimetype = 'image/jpeg'
					header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
					header += 'Connection: close\n'
					contentLength = get_content_length(response)
					header += 'Content-Length: ' +  str(contentLength) + '\n\n'
					final_response = header.encode('utf-8')
					final_response += response

					connection.send(final_response)
					
				elif path.startswith('/info'):

					info_type = request.split("type=")[1].split()[0]
					info_type = unquote(info_type)
					response = None
					if info_type == 'time':
						response = datetime.datetime.now()
					elif info_type == 'random':
						response = random.randint(1,101)
					else:
						response = 'No Data'

					response = str(response).encode('utf-8')

					contentLength = get_content_length(response)
					header = 'HTTP/1.1 200 OK\n'
					mimetype = 'text/plain'
					header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
					header += 'Connection: close\n'
					header += 'Content-Length: ' +  str(contentLength) + '\n\n'
					final_response = header.encode('utf-8')
					final_response += response

					connection.send(final_response)

				elif path.startswith('/api/'):
					subPath = path.split('/')
					if subPath[2] == 'plus_one' and len(subPath) == 4:
						val = path.split('/')[3]

						response = None
						header = None

						if not isValidInteger(val):
							response = build_response_failed(400, "Not a number")
							header = build_header(400, 'application/json', response)
						else:
							response = build_plus_one_service_response(1, int(val) + 1)
							header = build_header(200, 'application/json', response)

						final_response = header + response
						connection.send(final_response)
					elif subPath[2] == 'spesifikasi.yaml' and len(subPath) == 3:
						file = open('spesifikasi.yaml', 'rb')
						response = file.read()
						file.close()
						header = build_header(200, 'text/plain', response)
						final_response = header + response
						connection.send(final_response)
					else:
						response = build_response_failed(404, "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.")
						header = build_header(404, 'application/json', response)
						final_response = header + response
						connection.send(final_response)

				else:
					response = build_response_failed(404, "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.")
					header = build_header(404, 'application/json', response)
					final_response = header + response
					connection.send(final_response)

			elif method == 'POST':
				if path == '/':
					final_response = get_redirect_to_hello_world_response(ip_address)
					connection.send(final_response)
				elif path == '/hello-world':
					
					content_type = request.split("Content-Type:")[1].split()[0]
					if content_type != 'application/x-www-form-urlencoded' :
						final_response = get_bad_request_response(content_type) 
						connection.send(final_response)
					else:
						name = request.split("name=")[1].split()[0]
						name = unquote(name)
						file = open('hello-world.html', 'rb')
						response = file.read()
						response = response.decode().replace('__HELLO__', name)
						response = response.encode('utf-8')
						contentLength = get_content_length(response)
						file.close()
						header = 'HTTP/1.1 200 OK\n'
						mimetype = 'text/html'
						header += 'Content-Type: ' + str(mimetype) + '; charset=UTF-8' + '\n'
						header += 'Connection: close\n'
						header += 'Content-Length: ' +  str(contentLength) + '\n\n'
						final_response = header.encode('utf-8')
						final_response += response

						connection.send(final_response)

				elif path.startswith('/api/'):
					subPath = path.split('/')
					if subPath[2] == 'hello' and len(subPath) == 3:
						currentVisit = datetime.datetime.now()
						requestBody = request.split('\r\n\r\n')[1]
						requestBody = json.loads(requestBody)

						name = requestBody.get('request')
						response = None
						header = None

						if(name is None):
							response = build_response_failed(400, "'request' is a required property")
							header = build_header(400, 'application/json', response)
						else:
							r = requests.get(url = time_info_url)
							data = r.json()
							greeting = 'Good {}, {}'.format(data['state'], name)
							count += 1
							response = build_hello_service_response(1, count, currentVisit, greeting)
							header = build_header(200, 'application/json', response)

						final_response = header + response
						connection.send(final_response)
						updateCount(count)
					else:
						response = build_response_failed(404, "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.")
						header = build_header(404, 'application/json', response)
						final_response = header + response
						connection.send(final_response)
				else:
					response = build_response_failed(404, "The requested URL was not found on the server.  If you entered the URL manually please check your spelling and try again.")
					header = build_header(404, 'application/json', response)
					final_response = header + response
					connection.send(final_response)

		connection.close()
	except Exception as e:
		# Clean up the connection
		print ('An error occured, ' + str(e))
		traceback.print_exc()
		