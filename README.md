Live Video streaming using Animated GIFs
========================================

Preview
-------

![Sample](https://raw.github.com/jbochi/gifstreaming/master/doc/sample.gif)

This sample video is just a fragment of a live video served by gifstreaming.

Warning
-------

This is a toy project and it's not production ready. If you are seriously considering 
live video streaming using images, take a look at [live_thumb](https://github.com/jbochi/live_thumb).
It uses much less bandwidth because the images are encoded as JPEG and it is more
stable, since it uses nginx-push-stream to serve the images instead of this poorly
tested node.js app.

Browser Support
---------------

All modern browsers since IE 5, that display the animation while download is in progress.

Usage
-----

You need to have a stream of gif images (one per frame) at the input directory.

If you have ffmpeg and a input video, you can do it like this, to loop it continuously:

    $ mkdir input
    $ ffmpeg -i video.mp4 -loop 1 -pix_fmt pal8 -s 159x97 -r 10 input/in%d.gif

If you have a live RTMP stream handy:

    $ ffmpeg -re -i rtmp://server/app/stream -pix_fmt pal8 -s 159x97 -r 10 input/in%d.gif

After that, run the Python script that will extract the gif frames and prepare then to be served:

    $ mkdir parts
    $ python transform.py

The server is a simple node.js script:

    $ node server.js


With your browser, visit `http://localhost:8080/`

How it works
------------

When a HTTP request is received, the node.js server delivers the Animated GIF Header, and frames
for the first 10 seconds of video, but does not close the connection. After that, it watches the
local directory for new frames and pushes then to all connected users. Since the GIF file format
does not specify the number of frames and the Trailer is never delivered, the browser will keep
the connection open (at least while it has enough memory :-).

The Python server creates the animated GIF header (Header, Logical Screen Descriptor, Application Extension)
based on the first frame. For all the subsequent frames, it removes the Header, and transform the Global
Color Table into a Local Color Table.

![GIF file](http://www.matthewflickinger.com/lab/whatsinagif/images/gif_file_stream.gif)

A good explanation of the GIF spec can be found here: http://www.matthewflickinger.com/lab/whatsinagif/bits_and_bytes.asp



Enjoy!
