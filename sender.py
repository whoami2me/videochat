import cv2
import socket
import pickle
import struct

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

afm = socket.AF_INET
ss = socket.SOCK_STREAM

host = 'localhost'
port = 8089

clientsocket=socket.socket(afm,ss)
clientsocket.connect((host,port))

data = b''
payload_size = struct.calcsize("L") 

while True:
    try:

        ret,frame=video.read()
        clientdata = pickle.dumps(frame)
        message_size = struct.pack("L", len(clientdata)) 
        clientsocket.sendall(message_size + clientdata)
  

        while len(data) < payload_size:
            data += clientsocket.recv(4096)

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0] 

        while len(data) < msg_size:
            data += clientsocket.recv(4096)

        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)
        cv2.imshow('rec frames', frame)

        if cv2.waitKey(1) == 27:
            print("windows closed")
            clientsocket.shutdown(2)    
            clientsocket.close()
            cv2.destroyAllWindows()
            break
    except:
        cv2.destroyAllWindows()
        print("others closed")     
        break    
      
video.release()