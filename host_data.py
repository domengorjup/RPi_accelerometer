from time import sleep
from flask import Flask, render_template
from MPU6050_test import acc_data

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('index.html')

@app.route("/function/<function_name>")
def function(function_name):
    if str(function_name) == "acc_data":
        while True:
            x, y, z, rx, ry = acc_data()
            data = {
                'x': x,
                'y': y,
                'z': z,
                'x_rotation' : rx,
                'y_rotation' : ry
                }
            return render_template('data.html', **data)
            #sleep(0.5)

    else:
        value = {'error_message' : "Invalid function! See home page for info."}
        return render_template('error.html', **value)
        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
