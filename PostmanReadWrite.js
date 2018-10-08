'use strict';

var moment = require('moment'); 
var timestamp = new moment().format("YYYYMMDDHHmmssSSS");
var directory = 'C:\postman';
var filenameR = 'datar.ini';
var filenameW = 'dataw.ini';
var fs = require('fs');
var ini  = require('ini');
var shell = require('shelljs');
var inhoud = '';

function access_file(directory,filename){
	try{
		fs.accessSynch(directory);
		openfile(filename);
	}
	catch (e)	{
		shell.mkdir('-p', directory);
		openfile(filename);
	}
}

//fs.readFileSync


function openfile(filename){
	var fd = fs.openSync(filename, 'w');
}


class readWrite {
	
	constructor(emitter, reporterOptions, options) {
        this.reporterOptions = reporterOptions;
        this.options = options;
        const events = 'start done'.split(' ');
        events.forEach((e) => { if (typeof this[e] == 'function') emitter.on(e, (err, args) => this[e](err, args)) });
    }

    start(err, args) {
		access_file(directory,filenameR);
		inhoud = ini.parse(fs.readFileSync(filenameR, 'utf-8'));
	
    }
	
    done(err, args) {
		access_file(directory,filenameW);
		inhoud.database.nieuwegegevens = 'timestamp';
		fs.writeFileSynch(filenameW,ini.stringify(inhoud));
    }
}

module.exports = readWrite;