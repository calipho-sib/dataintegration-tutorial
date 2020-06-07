var express = require('express');
var app = express();
const bodyParser = require("body-parser");

const ensembl_file = process.argv[2];

if(process.env.MODE === 'FILE') {

    var fs = require('fs');
    var ensembl_data = JSON.parse(fs.readFileSync(ensembl_file, 'utf8'));

    // Calls to process the file content
    console.log("processing ensembl data\n");
    processFile(ensembl_data);	
} else if(process.env.MODE === 'API') {

    app.use(bodyParser.urlencoded({
        extended: true
    }));
    app.use(bodyParser.json());

    var router = express.Router();
    router.post('/transform', function(req, res) {
    	const ensembl_data = req.body;
        console.log(req.body);
        if(ensembl_data) {
        	console.log( "Ensembl data received and loading in to the DB");
                processFile(ensembl_data);
                res.send("Done");
        } else {
                console.error("Empty data, something is wrong");
                res.send("Empty data");
        }   
    });

    app.use('/', router);	
    var server = app.listen(3000, function () {
        var host = server.address().address;
        var port = server.address().port;
        console.log("Transformer is at http://%s:%s", host, port)
    })
}


function processFile(content) {

    var MongoClient = require('mongodb').MongoClient;
    var url = 'mongodb://testuser:testpassword@172.31.29.142:27017/ensembl-transformed';
    console.log("Inserting " + content);
    MongoClient.connect(url, function(err, client) {

        var ensembl_collection = client.db('ensembl-transformed').collection('ensembl');
        ensembl_collection.insert(content, function(err, res) {
    		if (err) throw err;
    		console.log("Data inserted");
    		client.close();
    	});
    console.log("Loading done!");
   });
}
