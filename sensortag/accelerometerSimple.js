/*
  Simplified accelerometer example

  This example reads the accelerometer on a sensorTag.
  Rather than doing the sensor enable, configure, notify,
  and listen functions as each other's callbacks, this example
  simplifies the process by calling most of these asynchronously.

  created 12 Nov 2017
  by Tom Igoe
*/
var async = require('async');
var SensorTag = require('sensortag');					// sensortag library
var tags = new Array;						        // list of tags connected
SensorTag.SCAN_DUPLICATES = true;


var timeoutVar = 60000;
var timeoutID;
var timeoutCleared = true;
// ------------------------ sensorTag functions
function handleTag(tag) {
	stopTimed();
	console.log('new tag connected');
	var tagRecord = {};		// make an object to hold sensor values
	var current=Date.now();
	tags.push(tagRecord);	// add it to the tags array

	function disconnect() {
		console.log('tag disconnected!');
		if (timeoutCleared) {
			scanTimed();
		  }
	}
	/*
	This function enables and configures the sensors, and
	sets up their notification listeners. Although it only shows
	accelerometer data here, you could duplicate this pattern
	with any of the sensors.
	*/
	function enableSensors() {		// attempt to enable the sensors
		console.log('enabling sensors');
		// enable sensor:
		tag.enableAccelerometer();
		tag.enableGyroscope();
		tag.enableMagnetometer();
		tag.enableLuxometer();
		// make an object to hold this sensor's values:
		tag.readSystemId(function(error, systemId) {
			console.log('\tsystem id = ' + systemId);
			tagRecord.id=systemId;
		  });

		tagRecord.accel = {};
		tagRecord.gyro={};
		tagRecord.magnet={};
		tagRecord.lux={};
		// set its period:
		tag.setAccelerometerPeriod(100);
		tag.setGyroscopePeriod(100);
		tag.setMagnetometerPeriod(100);
		// then turn on notifications:
		tag.notifyAccelerometer();
		tag.notifyGyroscope();
		tag.notifyMagnetometer();
		tag.notifyLuxometer();

		scanTimed();		
	}

	function readAccelerometer (x, y, z) {
		// read the three values and save them in the
		// sensor value object:
		tagRecord.accel.x = x;
		tagRecord.accel.y = y;
		tagRecord.accel.z = z;
		console.log(tagRecord); // print it
		console.log("time",Date.now()-current);
		current=Date.now();
	}

	function readGyroscope(x,y,z){
		tagRecord.gyro.x=x;
		tagRecord.gyro.y=y;
		tagRecord.gyro.z=z;
		// console.log(tagRecord.gyro);
	}

	function readMagnetometer(x,y,z){
		tagRecord.magnet.x=x;
		tagRecord.magnet.y=y;
		tagRecord.magnet.z=z;
		// console.log(tagRecord.magnet);
	}

	function readLuxometer(lux){
		tagRecord.lux.v=lux;
		// console.log(tagRecord.lux);
	}

	// Now that you've defined all the functions, start the process.
	// connect to the tag and set it up:
	tag.connectAndSetUp(enableSensors);
	//set a listener for when the accelerometer changes:
	tag.on('accelerometerChange', readAccelerometer);
	tag.on('gyroscopeChange',readGyroscope);
	tag.on('magnetometerChange',readMagnetometer);
	tag.on('luxometerChange',readLuxometer);
	// set a listener for the tag disconnects:
	tag.on('disconnect', disconnect);
}

// listen for tags and handle them when you discover one:
// SensorTag.discoverAll(handleTag);


  
  // Start timed discovering
function scanTimed() {
	console.log('Start discovering');
	timeoutCleared = false;
	SensorTag.discoverAll(handleTag);
	timeoutID = setTimeout(function () {
	  stopTimed();
	}, timeoutVar);
  }
  
  //Stop timer and discovering
  function stopTimed() {
	SensorTag.stopDiscoverAll(handleTag);
	timeoutCleared = true;
	console.log('Stop discovering');
	clearTimeout(timeoutID);
  }
  
  // Start discovering
  
  
scanTimed();