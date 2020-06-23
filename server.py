import io
import socket
import struct 
from PIL import Image
import matplotlib.pyplot as pl

# step 1: setup the socket.
server_socket = socket.socket()
server_socket.bind(('192.168.1.66', 8000))      # Put your IP HERE !
server_socket.listen(0)

# Step 2: create file object
connection = server_socket.accept()[0].makefile('rb') #accept a single connection, make a file object
try:
    img = None
    while True: # loop grabbing data
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0] # read length of image as 32-bit unsigned int
        if not image_len:
            break           # break loop if length = 0 bits
        image_stream = io.BytesIO()     # make a stream to hold the image data
        image_stream.write(connection.read(image_len))      # read image data from the connection
        #
        image_stream.seek(0)                # rewind the stream
        image = Image.open(image_stream)    # open image with PIL
        #
        if img is None:
            img = pl.imshow(image)      # display our image
        else:
            img.set_data(image)
            
        pl.pause(0.01)
        pl.draw()
        
        print('Image is %dx%d' % image.size)
        image.verify()
        print('image is verified')
finally:
     connection.close()
     server_socket.close()
     
     
     
     
     
     ########################
#If you want the frames to be much faster and smoother do this:
#In the client file:
#When you define the for loop that iterates over the camera frames from the raspberry pi
#add the following parameter:
#camera.capture_continuous(stream, 'jpeg',  use_video_port = True)
#*use_video_port = True*
#This will provide almost a live loading of the frames from the camera.