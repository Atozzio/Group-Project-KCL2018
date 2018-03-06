from flask import Flask,request, render_template

app = Flask(__name__)
 
@app.route('/')
def render_static():
    return render_template('index.html')


@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/ObjectQuantity', methods=['POST', 'GET'])
def ObjectQuantity():
    if request.method == 'POST':
        quantity = request.form['mySelect']
        if quantity:
            return render_template('ObjectFeature.html',quantity=quantity)
        else:
            print "something went wrong"
    return render_template('ObjectQuantity.html')
 
if __name__ == '__main__':
    app.run()