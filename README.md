Video streaming using Animated GIFs
-----------------------------------

You need to create one gif image per frame at the input directory

If you have ffmpeg and a input video, you can do it like this:

    $ mkdir input
    $ ffmpeg -i video.mp4 -pix_fmt rgb24 -s 159x97 -r 5 input/in%d.gif

After that, create the gif frames that will be served executing the `trans.py` script

	$ mkdir parts
    $ python trans.py

The server is a node.js script:

    $ node server.js


With your browser, visit `http://localhost:8080/`

Enjoy!
