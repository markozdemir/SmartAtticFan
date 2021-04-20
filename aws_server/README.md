Run `make` in this directory to run the server

Server currently handles:

	- Receiving and printing data
	- All android commands
		- CRUD user operations
		- Turn fan on/off
		- Sends fan data
		- Sends fan graphs
		- Sends info about fan's state (working/not)
	- Detects if fan is working
	- Error handling
	- Shell scripts to call other methods for:
		- Sending push notifications to Android
		- Sending emails
		- running AI
	- Geolocation API
	- Pusher and firebase (serverless functions) API
	- Hooks up with MongoDB
	- Communicates with ESP32:
		- Retrieves data from ESP32 and stores it in MongoDB to make graphics
		- Sends information to the fan about what the fan should do (on/off, slow, med, fast)
	- Much more!
		
