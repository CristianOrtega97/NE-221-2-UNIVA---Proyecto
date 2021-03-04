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
    return render_template('index.html')
 
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

@app.route('/login_auth', methods=['POST'])
def login_auth():
    if request.method == 'POST':
        user_name = request.form['user_name']
        password = request.form['password']
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT * FROM user_view WHERE user_name = '" + user_name + "'")
        data = my_cursor.fetchall()
        my_cursor.close()
        if len(data) > 0:
            if data[0][2] == user_name:
                if data[0][3] == password:
                    if data[0][4] == 1:
                        print("Company")
                        return render_template('customer.html')
                    elif data[0][4] == 2:
                        return render_template('agent.html')
                    else:
                        return render_template('admin.html')
                else:
                    auth = 0
                    return render_template('index.html',auth = auth)
            else:
                auth = 0
                return render_template('index.html',auth = auth)
        else:
            auth = 0
            return render_template('index.html',auth = auth)

if __name__ == '__main__':
    app.run(debug=True)