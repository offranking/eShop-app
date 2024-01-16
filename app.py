from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html', title='Home')

@app.route('/goods')
def goods():
    return render_template('goods.html', title='Goods')

@app.route('/services')
def services():
    return render_template('services.html', title='Services')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
