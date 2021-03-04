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

@app.route('/agent', methods=['GET','POST'])
def agent():
    #Agent
    inputName = request.form['inputName']
    inputSurname = request.form['inputSurname']
    inputPhone = request.form['inputPhone']
    inputDate = request.form['inputDate']
    inputInsurance = request.form.get('inputInsurance')
    inputCampaign = request.form.get('inputCampaign')
    if str(inputInsurance) == 'Yes':
        inputInsurance = 1
    else:
        inputInsurance = 0
    my_cursor = mysql.connection.cursor()
    my_cursor.execute("SELECT id FROM user WHERE name = '" + inputCampaign + "'")
    data = my_cursor.fetchall()
    my_cursor.close()
    inputCampaign = data[0][0]
    my_cursor = mysql.connection.cursor()
    my_cursor.execute("INSERT INTO `lead` (`id`, `first_name`, `last_name`, `phone`, `insurance`, `date`, `company_id`, `is_active`, `created_at`, `updated_at`)  VALUES(NULL,'"+str(inputName)+"','"+str(inputSurname)+"',"+str(inputPhone)+","+str(inputInsurance) +",'"+str(inputDate)+"'," + str(inputCampaign)+", '1', current_timestamp(), current_timestamp())")
    my_cursor.connection.commit()
    my_cursor.close()
    my_cursor = mysql.connection.cursor()
    my_cursor.execute("SELECT name FROM user_view WHERE role = 1")
    campaigns = my_cursor.fetchall()
    my_cursor.close()
    return render_template('agent.html',campaigns = campaigns)
    

@app.route('/read_leads', methods=['POST'])
def read_leads():
    if request.method == 'POST':
        date = request.form['date']
        company_name = request.values.get("company_name") 
        print("DATE: "+ date)
        print("COMPANY NAME: "+ company_name)
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT * FROM lead_view WHERE date = '" + str(date) + "'AND company_name = '" +str(company_name)+"'")
        data = my_cursor.fetchall()
        my_cursor.close()
        return render_template('customer.html', data = data, company_name = company_name)

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
                        #Company
                        company_name =  data[0][1]
                        return render_template('customer.html',company_name = company_name)
                    elif data[0][4] == 2:
                        #Agent
                        my_cursor = mysql.connection.cursor()
                        my_cursor.execute("SELECT name FROM user_view WHERE role = 1")
                        campaigns = my_cursor.fetchall()
                        my_cursor.close()
                        company_name =  str(data[0][1])
                        return render_template('agent.html', campaigns = campaigns,company_name = company_name)
                    else:
                        #Admin
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