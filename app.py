from flask import Flask, render_template, url_for, request
from flask_mysqldb import MySQL
from flask_datepicker import datepicker
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
datepicker(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'leadmanager'

mysql = MySQL(app)

@app.route('/')
def index():
    return 'Hello World'
 
@app.route('/customer')
def customer():
    return render_template('customer.html')

@app.route('/read_leads', methods=['POST'])
def read_leads():
    if request.method == 'POST':
        date = request.form['date']
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT * FROM lead_view WHERE date = '" + date + "'")
        data = my_cursor.fetchall()
        my_cursor.close()
        return render_template('customer.html', data = data)
        
@app.route('/login')
def login():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)