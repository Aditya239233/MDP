import socket
import pickle
import time
from config import PI_IP,PORT

print("Connecting...")
HEADERSIZE = 20
clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#clientsocket.connect((socket.gethostname(),1234))
clientsocket.connect((PI_IP,PORT))#rpi


def sendData(msg,destination):
	status = True
	data = {"wifi_in_status":status,"wifi_in_msg":msg,"wifi_in_dest":destination}
	if(status):
		
		status =False
		msg = pickle.dumps(data)
		msg = bytes(f'{len(msg):<{HEADERSIZE}}',"utf-8")+msg #for pickle, convert to bytes header
		clientsocket.send(msg)
		print(f"Sent {msg}-----------------------")
		
	time.sleep(0.5)

def getAndroidData():
	#clientsocket.listen(5)
	while True:
		full_msg = b''#in bytes for pickle
		new_msg = True
		try:
			if clientsocket!=None:
				while True:
					print("Waiting for pi data")
					msg = clientsocket.recv(16) #buffer bytes stream chunk at a time
					if new_msg and len(msg)>0:
						msglen = msg[:HEADERSIZE]
						msglen = msglen.decode('UTF-8')
						msglen = int(msglen)
						new_msg = False
						#msglen = int(msg[:HEADERSIZE])

					full_msg+=msg #pickle

					if len(full_msg)-HEADERSIZE ==msglen:# after all have been combine
						
						d_receive = pickle.loads(full_msg[HEADERSIZE:])
						print(d_receive)
						new_msg = True
						full_msg=b''#in bytes for pickle
						print(f"full msg receive:{d_receive['wifi_out_msg']}")
						return d_receive['wifi_out_msg']
						#break
		except Exception as e:
			print(f"{type(e).__name__} at line {e.__traceback__.tb_lineno} of {__file__}: {e}")
			break;
			
	print("exited")

# def getAndroidData():
# 	while True:
# 		data = clientsock.recv(32).decode('utf-8')
# 		if len(data)>1:
# 			print("ProgramStarting")
# 			break;
# 		if str(data) == "message":
# 			print("Command from PC: xxxx ")
# 			sendmsg = random_data()
# 			x_encoded_data = sendmsg.encode('utf-8')
# 			clientsock.sendall(x_encoded_data)

# 		elif str(data) == "Quit":
# 			print("shutting down")
# 			break
# 		if not data:
# 			print('not data') 
# 			break
# 		else: 
# 			pass



#SendData({"msg":"Hello now----","status":True})

