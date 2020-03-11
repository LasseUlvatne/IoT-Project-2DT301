'''
Functions for camera.py, which is a server with video streaming options.

Author:
Lars Petter Ulvatne.
'''

import io
import picamera
import logging
import socketserver
import urllib
import random
import string

from threading import Condition
from http import server
from PIL import Image

'''
Fetches an image from disk and reads into byte buffer and sends to client.
'''
def fetch_img(server, parsed_query):
    img_id = parsed_query['id'][0]
    img = Image.open('img/%s.jpg' % img_id)

    # create file-object in memory
    img_bytes = io.BytesIO()

    # Save jpeg file into bytes buffer
    img.save(img_bytes, 'jpeg')

    # Move to beginning of buffer and write to client.
    img_bytes.seek(0)
    server.send_response(200)
    server.send_header('Content-Type', 'image/jpeg')
    server.end_headers()
    server.wfile.write(img_bytes.read())

'''
Saves a frame/image to disk. Upon success, a message is sent to client.
'''
def save_img(server, parsed_query, frame):
    # Save image buffer to file
    img_buf = Image.open(io.BytesIO(frame))
    img_buf.save('img/%s.jpg' % parsed_query['id'][0])

    # Send success response to client.
    success_header(server, 'text/plain')
    server.wfile.write(('Successfully uploaded %s.jpg' % parsed_query['id'][0]).encode('utf-8'))

'''
Writes a frame to request and sends.
'''
def write_frame(server, frame):
    server.wfile.write(b'--FRAME\r\n')
    server.send_header('Content-Type', 'image/jpeg')
    server.send_header('Content-Length', len(frame))
    server.end_headers()
    server.wfile.write(frame)
    server.wfile.write(b'\r\n')

'''
Sends a success header to client.
'''
def success_header(server, content_type):
    server.send_response(200)
    server.send_header('Age', 0)
    server.send_header('Cache-Control', 'no-cache, private')
    server.send_header('Pragma', 'no-cache')
    server.send_header('Content-Type', content_type)
    server.end_headers()

'''
Sends 404 response to the client.
'''
def send_err(resp, message = 'Message not found.'):
    resp.send_error(404, message)
    resp.end_headers()

'''
Generates a random string of upper/lowercase letters.
'''
def random_string(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))
