var express = require('express');
var app = express();
var fs = require("fs");

if(process.env.MODE === 'FILE') {
    const fs = require('fs');
    fs.readFile('./Index.html', function read(err, data) {
        if (err) {
            throw err;
        }
        const content = data;

        // Invoke the next step here however you like
        console.log(content);   // Put all of the code here (not the best solution)
        processFile(content);   // Or put the next step in a function and invoke it
    });
} else if(process.env.MODE === 'API') {
    app.get('/listUsers', function (req, res) {

            console.log( "HELLO" );
            res.json("DONE");

    })

    var server = app.listen(8081, function () {
        var host = server.address().address
        var port = server.address().port
        console.log("Example app listening at http://%s:%s", host, port)
    })
}


function processFile(content) {
    console.log(content);
}