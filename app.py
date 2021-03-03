from flask import Flask, render_template, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'leadmanager'

mysql = MySQL(app)

@app.route('/')
def index():
    return 'Hello World'

@app.route('/read_leads')
def read_leads(date):
    my_cursor = mysql.connection.cursor()
    my_cursor.execute('SELECT * FROM lead_view WHERE ')
    data = my_cursor.fetchall()
    my_cursor.close()
    return render_template('customer.html',data = data)

if __name__ == '__main__':
    app.run(debug=True)