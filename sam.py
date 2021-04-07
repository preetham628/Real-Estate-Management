from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
import yaml
from collections import defaultdict


sam=Flask(__name__)

#DB Configure
db = yaml.load(open('db.yaml'))
sam.config['MYSQL_HOST'] = db['mysql_host']
sam.config['MYSQL_USER'] = db['mysql_user']
sam.config['MYSQL_PASSWORD'] = db['mysql_password']
sam.config['MYSQL_DB'] = db['mysql_db']

mysql=MySQL(sam)

@sam.route('/aboutus', methods=['GET','POST'])
def about():
    return render_template('aboutus.html')

#HomePage
@sam.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

#All Customers
@sam.route('/cust')
def cust():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM customer")
    if resultValue > 0:
        custDetails = cur.fetchall()
        return render_template('customer.html',custDetails=custDetails)

#All Owners
@sam.route('/owner')
def owner():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM owners")
    if resultValue > 0:
        ownerDetails = cur.fetchall()
        return render_template('owner.html',ownerDetails=ownerDetails)

#All Requirements
@sam.route('/req')
def req():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM requirements")
    if resultValue > 0:
        requirements = cur.fetchall()
        return render_template('req.html',requirements=requirements)

#All Enquiries
@sam.route('/enq')
def enq():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM enquires")
    if resultValue > 0:
        enquires = cur.fetchall()
        return render_template('enq.html',enquires=enquires)

#All customer requirements
@sam.route('/has')
def has():
    cur=mysql.connection.cursor()
    resultValue = cur.execute("SELECT * FROM has")
    if resultValue > 0:
        requirement = cur.fetchall()
        return render_template('has.html',requirement=requirement)

#All Agents
@sam.route('/agents', methods=['GET','POST'])
def dis():
    agents=defaultdict(list)
    if request.method == 'POST':
        if request.form['btn'] == "Add Agent":
            return redirect('/agentinsert')
    cur=mysql.connection.cursor()
    resultVaue=cur.execute("SELECT * FROM agent")
    if resultVaue > 0:
        agentDetails = cur.fetchall()
    return render_template('agents.html', agentDetails=agentDetails)

#Adding new agent
@sam.route('/agentinsert', methods=['GET', 'POST'])
def agentin():
    if request.method == 'POST':
        #userDetails = request.form
        id = request.form['id']
        name = request.form['name']
        dept = request.form['dept']
        role = request.form['role']
        gender = request.form['gender']
        age = int(request.form['age'])
        ph_no = request.form['ph_no']
        cur=mysql.connection.cursor()

        try:
            cur.execute("INSERT INTO agent(agent_id, dept, aname, age, gender, ph_no, agent_role) VALUES(%s, %s, %s, %s, %s, %s, %s)",(id, dept, name, age, gender, ph_no, role))
        except:
            return 'Agent ID already exists'

        mysql.connection.commit()
        cur.close()
        return redirect('/agents')
    return render_template('agentin.html')

#Removing Agent
@sam.route('/rem_agent', methods=['GET', 'POST'])
def remagent():
    if request.method == 'POST':
        id = request.form['agent_id']
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM agent WHERE agent_id=(%s)",[id])
        mysql.connection.commit()
        cur.close()
        return redirect('/agents')

#All Properties
@sam.route('/props', methods=['GET','POST'])
def disp():
    properties=defaultdict(list)
    if request.method == 'POST':
        if request.form["btn"] == "Add Property":
            return redirect('/propinsert')
    cur=mysql.connection.cursor()
    resultVaue=cur.execute("SELECT * FROM property")
    if resultVaue > 0:
        properties = cur.fetchall()
    return render_template('props.html', properties=properties)

#Inserting new property
@sam.route('/propinsert', methods=['GET', 'POST'])
def propin():
    if request.method == 'POST':
        #userDetails = request.form
        site = int(request.form['site'])
        dim = request.form['dim']
        area = request.form['area']
        city = request.form['city']
        price = int(request.form['price'])
        face = request.form['price']
        cust = request.form['cust']
        owner = request.form['owner']
        agent = request.form['agent']
        cur=mysql.connection.cursor()

        try:
            cur.execute("INSERT INTO property(site_no, dimension, area, city, price, facing, cust_id, owner_id, agent_id) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",(site, dim, area, city, price, face, cust, owner, agent))
        except:
            return 'Property already exists'
        mysql.connection.commit()
        cur.close()
        return redirect('/props')
    return render_template('propin.html')

#Removing property
@sam.route('/rem_prop', methods=['GET', 'POST'])
def remprop():
    if request.method == 'POST':
        id = request.form['site']
        cur=mysql.connection.cursor()
        cur.execute("DELETE FROM property WHERE site_no=(%s)",[id])
        mysql.connection.commit()
        cur.close()
        return redirect('/props')


#Main function
if __name__ == '__main__':
    sam.run(debug=True)