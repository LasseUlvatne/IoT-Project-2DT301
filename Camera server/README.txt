The project uses a Raspberry Pi3 and a raspicam to take pictures and stream video through a server.
The server will only accept requests from a specific server/IP.

CREATORS: 
Lars Petter Ulvatne
Findlay Forsblom

-----------------------------------------------------------------------
SAVE PICTURES:
To save pictures(JPEG) to disk the following url will be used:

"/img/save?id=NAME_OF_IMG"

NAME_OF_IMG: The wanted name of image to save on disk.
-----------------------------------------------------------------------

FETCH IMAGE: 
To fetch an image from disk the following url will be used:

"/img?id=NAME_OF_IMG"

NAME_OF_IMG: The name of image to fetch from disk.
-----------------------------------------------------------------------

GET STREAM ID:
Get a valid stream id to start stream. This will return a random integer
concatenated with random string + CLIENT_SOCKET_ID sent as query from 
client request. The random integer indicates where the valid stream id 
starts as a substring.

"/setstream?id=CLIENT_SOCKET_ID"

-----------------------------------------------------------------------

START STREAM:
Start stream by adding a valid STREAM_ID fetched from /setstream url.

"/stream?id=STREAM_ID"

-----------------------------------------------------------------------
