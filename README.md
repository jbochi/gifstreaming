Video streaming using M-JPEG
----------------------------

Node.js will watch for jpeg frames on parts/ directory and stream them to all subscribers.

If you have ffmpeg and a input video, you can do it like this:

    $ mkdir input
    $ ffmpeg -re -i video.mp4 -r 1 parts/teste%9d.jpg

If you have a RTMP stream handy:

    $ ffmpeg -re -i rtmp://server/app/stream -r 1 parts/teste%9d.jpg

The server is a node.js script:

    $ node server.js


With your browser, visit `http://localhost:8080/`

Enjoy!
