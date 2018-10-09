def isValidInteger(s):
    try: 
        number = int(s)
        if number >= 1:
        	return True

        return False
    except ValueError:
        return False

def updateCount(count):
	with open("state.txt", "w") as text_file:
		text_file.write("count={0}".format(count))

def getLatestCount():
	try:
		with open("state.txt") as text_file:  
			count = text_file.read()
			count = count.split("=")[1]
			return int(count)
	except FileNotFoundError as e:
		updateCount(0)
		return 0

def getApiVersion():
	with open("spesifikasi.yaml") as text_file:  
		spesifikasi = text_file.read()
		version = spesifikasi.split("version: ")[1].split()[0].replace("'", "")
		return int(version)