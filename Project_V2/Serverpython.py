from flask import Flask, render_template, request


app=Flask(__name__)
ENV = "development"
DEBUG=False

@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        if(request.form['username'] == "admin") and (request.form['password'] == "admin"):
            return render_template('Meteo.html')
    return render_template('index2.html')



if __name__=="__main__":
	app.run()