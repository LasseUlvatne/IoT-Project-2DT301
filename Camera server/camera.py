'''
Camera streaming server. Can save and fetch image from disk, start stream
by getting a valid stream ID, to use at one connection. End stream, by
requesting endstream url.
Source code from official PiCamera package:
http://picamera.readthedocs.io/en/latest/recipes2.html#web-streaming

Authors:
Lars Petter Ulvatne,
Findlay Forsblom

For course 2DV301 at Linnaeus University.
'''

import io
import picamera
import logging
import socketserver
import urllib
import lib.functions as func
import ssl
import json
import random
import string
import time

from threading import Condition
from http import server
from PIL import Image

PORT = 8081
auth_strings = { 'dev_admin': 'Admin stream id.'}

'''
Writes data to buffer.
'''
class BufferOutput(object):
    def __init__(self):
        self.frame = None
        self.buffer = io.BytesIO()
        self.condition = Condition()

    def write(self, buf):
        if buf.startswith(b'\xff\xd8'):
            # New frame, copy the existing buffer's content and notify all
            # clients it's available
            self.buffer.truncate()
            with self.condition:
                self.frame = self.buffer.getvalue()
                self.condition.notify_all()
            self.buffer.seek(0)
        return self.buffer.write(buf)

'''
Handles all incoming requests.
'''
class RequestHandler(server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        print(self.client_address[0])

        if parsed_url.path == '/setstream' and len(parsed_url.query) > 0:
            # Url is used to get a valid stream ID.
            try:
                rand_int = random.randint(1,9)

                # Create random string for authentication.
                rand_string = str(rand_int) + func.random_string(30) + urllib.parse.parse_qs(parsed_url.query)['id'][0]

                authstring = rand_string[rand_int:]
                auth_strings[authstring] = rand_string

                dict = { 'auth': rand_string }
                json_format = json.dumps(dict)

                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', len(json_format))
                self.end_headers()
                self.wfile.write(json_format.encode('utf-8'))
            except Exception as e:
                print(e, ': ERROR')
                func.send_err(self)
        elif parsed_url.path == '/endstream' and len(parsed_url.query) > 0:
            # Url used to end stream and remove stream ID.
            try:
                streamUrl = urllib.parse.parse_qs(parsed_url.query)['id'][0]
                del auth_strings[streamUrl]
                self.send_response(200)
                self.end_headers()
            except Exception as e:
                print(e, ': ERROR')
                func.send_err(self)
        elif parsed_url.path == '/stream' and len(parsed_url.query) > 0:
            # Url to start stream. Valid stream ID needed.
            try:
                streamid = urllib.parse.parse_qs(parsed_url.query)['id'][0]
                auth = auth_strings[streamid]
            except Exception as e:
                print(e, ': ERROR')
                func.send_err(self)
                
            if(not auth):
                # Send error if stream id is not authorized
                func.send_err(self)
            else:
                # Send succes header to client.
                func.success_header(self, 'multipart/x-mixed-replace; boundary=FRAME')
                try:
                    while True:
                        # Check for content in camera buffer.
                        with output.condition:
                            output.condition.wait()
                            frame = output.frame
                            
                        # Write frame to client.
                        func.write_frame(self, frame)
                        
                except Exception as e:
                    logging.warning(
                        'Removed streaming client %s: %s',
                        self.client_address, str(e))
 
        elif parsed_url.path == '/img' and len(parsed_url.query) > 0:
            # Url used to fetch image by name.
            try:
                # Fetch a saved image from disk.
                func.fetch_img(self, urllib.parse.parse_qs(parsed_url.query))
                
            except Exception as e:
                func.send_err(self, 'Wrong input')            
        elif parsed_url.path == '/img/save' and len(parsed_url.query) > 0:
            # Url used to save image to disk.
            try:
                # Parse query in url.
                parsed_query = urllib.parse.parse_qs(parsed_url.query)

                # Check condition of camera.
                with output.condition:
                    output.condition.wait()
                    frame = output.frame

                # Save image to disc.
                func.save_img(self, parsed_query, frame)
                
            except Exception as e:
                func.send_err(self, str(e))
        else:
            # Not valid url.
            func.send_err(self)

'''
Uses multiple threads to handle multiple incoming requests.
'''
class ThreadingServer(socketserver.ThreadingMixIn, server.HTTPServer):
    # Multiple thread for many connections
    allow_reuse_address = True
    daemon_threads = True

'''
Starts recording of camera to buffer where frames are read upon different http-
requests. When recording is up, the server is started.
'''
with picamera.PiCamera(resolution='640x480', framerate=90) as camera:
    # Setup camera buffer.
    output = BufferOutput()

    # Rotate camera and start recording.
    camera.rotation = 180

    camera.start_recording(output, format='mjpeg')

    try:
        # Server multithreaded server on port 8081.
        address = ('', PORT)
        server = ThreadingServer(address, RequestHandler)

        # Path to SSL/TLS certificate.
        path = '/etc/letsencrypt/live/linnaeus.asuscomm.com/'
        
        # Uncomment next line to enable HTTPS
        server.socket = ssl.wrap_socket(server.socket, keyfile=path + 'privkey.pem', certfile=path+'fullchain.pem', server_side=True, ssl_version=ssl.PROTOCOL_TLSv1_2)
        server.serve_forever()
    except Exception as e:
        print('Got here')
        print(str(e))
    finally:
        camera.stop_recording()            
