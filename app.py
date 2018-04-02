from cloudant import cloudant
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result
from flask import Flask
from flask import render_template
from flask import request


app = Flask(__name__, template_folder='templates')
app.static_folder='templates'


db_user=None
db_pass=None
db_url=None

db_svc={}
firstNav=True

@app.route('/', methods=['POST', 'GET'])
def home():
       return render_template('index.html',getDBDtls=True)

@app.route('/getdbdtls', methods=['POST', 'GET'])
def getDBDtls():
    if request.method=='POST' and request.form['dbdtls'] == 'False':
       dbusername = request.form['username']
       dbpassword = request.form['password']
       dburl = request.form['url']
       global db_user
       global db_pass
       global db_url
       db_user=dbusername
       db_pass=dbpassword
       db_url=dburl
       client = Cloudant(db_user, db_pass, url=db_url)
       client.connect()
       try:
           myDatabase = client.create_database("user_db")
           global db_svc
           db_svc={"dbsvc":myDatabase}
       except CloudantException as err:
           print err
           client = Cloudant(db_user, db_pass, url=db_url)
           client.connect()
           client.delete_database("user_db")
           myDatabase=client.create_database("user_db")
           global db_svc
           db_svc={"dbsvc":myDatabase}
       return render_template('index.html',getUsrDtls=True)
   
@app.route('/getuserinfo', methods=['POST', 'GET'])
def getUserDtls():
    if request.method=='POST' and request.form['dbdtls'] == 'True':
       username = request.form['username']
       password = request.form['password']
       insertUser(username, password)
       users = retrieveUsers()
       return render_template('index.html', users=users,getUsrDtls=True)

    


def insertUser(username,password):
    print "insert invoked"
    user_json = {"username":username,"password":password}
    dbsvc = db_svc['dbsvc']
    dbsvc.create_document(data=user_json, throw_on_exists=False)
    
def retrieveUsers():
    print "retrieve invoked"
    dbsvc = db_svc['dbsvc']
    users={}
    for row in range(0,dbsvc.all_docs()['rows'].__len__()):
        users["username - "+dbsvc.get(dbsvc.all_docs()['rows'][row]['id'])['username']+", password - "+dbsvc.get(dbsvc.all_docs()['rows'][row]['id'])['password']]=dbsvc.get(dbsvc.all_docs()['rows'][row]['id'])['password']
    return users

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)