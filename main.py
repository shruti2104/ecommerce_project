#from flask import Flask
from app import create_app

#app = Flask(__name__) #Creates the web application

#@app.route('/') #Defines a URL route
#def home(): #Function executed when user visits
#	return "Welcome to my E-Commerce Store!" #Response sent to browser


#app.run() #required to run the main app
#if __name__ == "__main__":
#	app.run(debug=True)


app = create_app()
if __name__ == "__main__":
    app.run(debug=True, port=8080)
