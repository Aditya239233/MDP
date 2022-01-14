import socket
import pickle
import time

class PiServer()
HEADERSIZE = 20
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#clientsocket.connect((socket.gethostname(),1234))
clientsocket.connect(("192.168.26.27",1231))#rpi

def SendData(d):
	status = d["status"]
	msg = d["msg"]
	data = {"wifi_in_status":status,"wifi_in_msg":msg}
	if(status):
		
		status =False
		msg = pickle.dumps(data)
		msg = bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8")+msg #for pickle, convert to bytes header
		clientsocket.send(msg)
		print(f"Sent {status}")
		d["msg"] = ""
		d["status"] = False
	time.sleep(0.5)



#SendData({"msg":"Hello now----","status":True})

