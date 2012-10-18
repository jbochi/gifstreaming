var fs = require('fs'),
    http = require('http');


function servePart(res, i, callback) {
  var filename = 'split/out' + i + '.part';
  fs.readFile(filename, function (err, data) {
    if (err) return callback(err);
    console.log('serving file ' + filename);
    res.write(data);
    callback();
  });
}

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'image/gif'});
  var done = false;
  var i = 0;
  var serveAll = function(err) {
    if (err) {
      console.log(err);
      //res.end();
    } else if (!done) {
      setTimeout(function() {      
        servePart(res, i, serveAll);
        i += 1;
      }, 110);
    }
  };
  req.on('close', function() {
    console.log('saiu!');
    done = true;
    res.end();
  })
  serveAll();
}).listen(8080, '127.0.0.1');


/*
http://nodejs.org/api/fs.html#fs_fs_watch_filename_options_listener
fs.watch('somedir', function (event, filename) {
  console.log('event is: ' + event);
  if (filename) {
    console.log('filename provided: ' + filename);
  } else {
    console.log('filename not provided');
  }
});
*/


console.log('Server running at http://127.0.0.1:8080/');
