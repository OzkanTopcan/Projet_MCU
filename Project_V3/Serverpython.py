from flask import Flask, render_template, request
from db import *
from standard import *
app=Flask(__name__)
ENV = "development"
DEBUG=False


@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        if(request.form['username'] == "admin") and (request.form['password'] == "admin"):
        #appel de fonction 1 et 2
            rowcount, records = select_current()
            generate_history()
        
        #variables
            a,b,c,e,d = records[0]
            return render_template('Meteo.html', capteur1=c, capteur2=e, capteur3=d)
    return render_template('index2.html')



if __name__=="__main__":
	app.run()
