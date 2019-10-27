This is a web based quiz application implemented using flask and mongodb.


app.py : 
	flask app is initialised here. It generates the "home.html" template dynamically using config file. The performance is evaluated and displayed in the "end.html" template. 

home.html : 
	This displays the quiz.

end.html : 
	This webpage displays the result of the quiz.

config.json : 
	It contains a dictionary which stores the questions and a variable which is used to obtain the answer from the database.
