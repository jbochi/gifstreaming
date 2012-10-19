var fs = require('fs'),
    http = require('http');

var INPUT_PATH = "parts";

Array.prototype.remove = function(e) {
  for (var i = 0; i < this.length; i++) {
    if (e == this[i]) { return this.splice(i, 1); }
  }
};

var subscribers = [];

function servePart(res, filename, callback) {
  fs.readFile(filename, function (err, data) {
    if (err) return callback(err);
    console.log('serving file ' + filename);
    res.write(data);
    callback && callback();
  });
}

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'image/gif'});
  subscribers.push(res);
  console.log('New subscriber: ' + subscribers.length + " total.\n")
  fs.readdir(INPUT_PATH, function(err, files) {
    if (err) throw err;
    var i = 0;
    var exited = false;
    var serveFiles = function (err) {
      if (err) res.end();
      else if (!exited && i < files.length) servePart(res, INPUT_PATH + "/" + files[i++], serveFiles);
    };
    serveFiles();
    req.on('close', function() {
      exited = true;
      res.end();
      subscribers.remove(res);
      console.log('Subscriber left: ' + subscribers.length + " total.\n");
    });
  });
}).listen(8080, '0.0.0.0');


var onNewFile = function (filename) {
  subscribers.forEach(function(res) {
    servePart(res, filename);
  });
};

var last_seen_file;
fs.watch(INPUT_PATH, function (event, filename) {
  fs.readdir(INPUT_PATH, function(err, files) {
    for (var i = 0; i < files.length; i++) {
      if (!last_seen_file || files[i] > last_seen_file) {
        console.log("New file: " + files[i]);
        onNewFile(INPUT_PATH + "/" + files[i]);
        last_seen_file = files[i];
      }
    }
  });
});

console.log('Server running at http://127.0.0.1:8080/');
