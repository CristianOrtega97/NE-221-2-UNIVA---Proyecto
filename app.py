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

@app.route('/administrator')
def administrator():
    return render_template('administrator.html')

@app.route('/find_user',methods=['GET','POST'])
def find_user():
    if request.method == 'POST':
        user_name = request.form['user_name']
        my_cursor = mysql.connection.cursor()
        query = "SELECT * FROM user_view WHERE user_name = '" + str(user_name) + "'"
        print("query: "+query)
        my_cursor.execute("SELECT * FROM user_view WHERE user_name = '" + str(user_name) + "'")
        data = my_cursor.fetchall()
        my_cursor.close()
        print("DATA 4: " + str(data[0][4]))
        print("DATA: " + str(data))
        if len(data) > 0:
            #User exists
            if data[0][5] == 1:
                user_name = data[0][2]
                found = 1
                return render_template('/administrator.html',found = found, user_name = user_name,data=data)
            else:
                user_name = data[0][2]
                found = 0
                return render_template('/administrator.html',found = found, user_name = user_name,data=data)
        else:
            #User doesn't exist
            found = 0
            return render_template('/administrator.html',found = found)

@app.route('/update_user',methods=['POST'])
def update_user():
    if request.method == 'POST':
        user = request.values.get('user')
        password = request.values.get('password')
        password_confirm = request.values.get('password_confirm')
        input_role = request.values.get('input_role')
        if password != password_confirm:
            password_confirm = 0
            return render_template('administrator.html', data = data, password_confirm = password_confirm)
        else:
            my_cursor = mysql.connection.cursor()
            print("INFO: "+user)
            query = "UPDATE user SET `password` = '" + str(password) +"', `role`= " + str(input_role) + " WHERE name = '" + user + "'"
            print("query: " + query)
            my_cursor.execute(query)
            my_cursor.connection.commit()
            my_cursor.close()
            confirmed = 1
            return render_template('administrator.html',confirmed = confirmed)

@app.route('/delete_db',methods=['GET','POST'])
def delete_db():
    if request.method == 'POST':
        user_name = request.values.get('user_name')
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("UPDATE user SET `is_active` = 0 WHERE user_name = '" + user_name + "'")
        my_cursor.connection.commit()
        my_cursor.close()
        deleted = 1
        return render_template('administrator.html',deleted = deleted ,user_name = user_name)

@app.route('/new_user',methods=['POST'])
def new_user():
    user_name = request.values.get('user_name')
    name = request.values.get('name')
    password = request.values.get('password')
    password2 = request.values.get('password2')
    input_role = request.values.get('input_role')
    if request.method == 'POST':
        my_cursor = mysql.connection.cursor()
        my_cursor.execute("SELECT * FROM `user_view` WHERE user_name = '" + str(user_name) + "'")
        data = my_cursor.fetchall()
        my_cursor.close()
        if len(data) > 0:
            if data[0][5] == 0:
                if password == password2:
                    my_cursor = mysql.connection.cursor()
                    query = "UPDATE user SET `password` = '" + str(password) +"', `role`= " + str(input_role) + ",`name` = '" + str(name) +"', `user_name` = '" + str(user_name) + "',`is_active` = 1 WHERE id = " + str(data[0][0])
                    my_cursor.execute(query)
                    my_cursor.connection.commit()
                    my_cursor.close()
                    create = 1
                    return render_template('administrator.html',create = create)
                else:
                    password = 1
                    return render_template('administrator.html',password = password) 
            else:
                active = 1
                return render_template('administrator.html',active = active) 
        else:
            if password == password2:
                my_cursor = mysql.connection.cursor()
                query = "INSERT INTO `user` (`id`, `name`, `user_name`, `password`, `role`, `is_active`, `created_at`, `updated_at`)  VALUES(NULL,'"+str(name)+"','"+str(user_name)+"','"+str(password)+"',"+str(input_role) +","+" 1, current_timestamp(), current_timestamp())"
                print("QUERY: " + query)
                my_cursor.execute(query)
                my_cursor.connection.commit()
                my_cursor.close()
                # my_cursor.execute("INSERT INTO `lead` (`id`, `first_name`, `last_name`, `phone`, `insurance`, `date`, `company_id`, `is_active`, `created_at`, `updated_at`)  VALUES(NULL,'"+str(inputName)+"','"+str(inputSurname)+"',"+str(inputPhone)+","+str(inputInsurance) +",'"+str(inputDate)+"'," + str(inputCampaign)+", '1', current_timestamp(), current_timestamp())")
                # my_cursor.connection.commit()
                # my_cursor.close()
                # create = 2
                create = 2
                return render_template('administrator.html',create = create)
            else:
                password = 1
                return render_template('administrator.html',password = password)

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
        my_cursor = mysql.connection.cursor()
        query = "SELECT * FROM lead_view WHERE date = '" + str(date) + "' AND company_name = '" +str(company_name)+"'"
        print("QUERY: " + query)
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
                        #Administrator
                        return render_template('administrator.html')
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