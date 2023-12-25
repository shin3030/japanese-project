from flask import Flask,render_template,request,redirect,url_for,session,jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from datetime import datetime
import requests
from flask_socketio import SocketIO,emit,send
url = 'http://lingpu.im.tku.edu.tw:35130/api/chat'

app=Flask(__name__)

app.secret_key='BK'
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='bk_japanese'
mysql=MySQL(app)
socketio = SocketIO(app)
name_space='/SendVocEx'
# 登入
@app.route("/")
@app.route("/login",methods=['GET','POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE Email = % s AND Password = % s', (email, password, ))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['User_id'] = user['User_id']
            session['name'] = user['UserName']
            session['email'] = user['Email']
            mesage = 'Logged in successfully !'
           
            
            return render_template('beginpage.html', mesage = mesage)
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

# 註冊
@app.route('/register', methods =['GET', 'POST'])
def register():
    mesage = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE Email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            mesage = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            mesage = 'Invalid email address !'
        elif not userName or not password or not email:
            mesage = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            mesage = 'You have successfully registered !'
    elif request.method == 'POST':
        mesage = 'Please fill out the form !'
    return render_template('register.html', mesage = mesage)

# 登出
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('User_id', None)
    session.pop('email', None)
    return redirect(url_for('login'))


#機器人對話
@app.route("/get",methods=["GET","POST"])
def get():
    msg=request.form["msg"]
    # print("Received message:", msg)
    return chat_respone(msg)

def chat_completion(prompt, model_engine="gpt35", temperature=0.7, top_p=0.95, max_tokens=1024):
    args = {
        'prompt': prompt,
        'model_engine': model_engine,
        'temperature': temperature,
        'top_p': top_p,
        'max_tokens': max_tokens
    }
    response = requests.post(url, json=args)
    response_json = response.json()
    message = response_json['message']
    return message

def chat_respone(text):
        current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        prompt = text+"只能用日文回答我"
        response=chat_completion(prompt)
        Chat_history(text,current_time,response)
        return response
@app.route("/translate",methods=["GET","POST"])
def translate():
    msg=request.form["msg"]
    print("tramslate message:", msg)
    input=msg
    response=chat_translate_respone(input)
    return response

def chat_translate_respone(text):
    prompt="把"+text+"翻譯成繁體中文"
    response=chat_completion(prompt)
    return response

def Chat_history(content,senttime,response):
    User_ID=session['User_id']
    zh_response=chat_translate_respone(response)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('INSERT INTO chat_history VALUES (% s, % s, % s, % s,% s)', (User_ID,senttime, content,response,zh_response ))
    mysql.connection.commit()
    return 0

def get_message():
    User_ID=int(session['User_id'])
    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM chat_history WHERE User_id = % s', (User_ID, ))
    messages=cursor.fetchall()
    return messages



@app.route("/selectvoc",methods=["POST"])
def selectvoc():
    JapaneseVoc=request.form.get('voc')#選取的單字
    prompt="請給我'"+JapaneseVoc+"'的例句"#傳入機器人的提示詞
    print(prompt)
    socketio.emit('send_prompt', {'prompt': prompt})
    Ex_response=chat_respone(prompt)
    socketio.emit('send_Expample', {'Example': Ex_response})
    return ""


#頁面
@app.route("/begin")
def Homepage():
    return render_template("beginpage.html")

@app.route("/chatbot")
def chatbot():
    messages=get_message()
    return render_template("chatbot.html", messages=messages)

@app.route("/50")
def letter():
    return render_template("50.html")
@app.route("/map")
def jmap():
    return render_template("map.html")


@app.route("/N5voc")
def N5voc():
    page='a'
    return render_template("N5voc.html",Voc=getvoc(page))
@app.route("/NewTable",methods=["GET","POST"])
def NewTabke():
    if request.method=='POST':
        page = request.form.get('char')
    return render_template("/N5vocTable.html",Voc=getvoc(page))
@app.route('/getvoc')
def getvoc(page):
    VOC_Result = {}
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM voc WHERE Page_index=% s',(page,))
    VOC_ALL = cursor.fetchall()
    for row in VOC_ALL:
        char = row['Voc_index']
        if char not in VOC_Result:
            VOC_Result[char] = []
        VOC_Result[char].append(row)
    return VOC_Result



@app.route("/N5gra")
def N5gra():
    return render_template("N5gra.html")
@app.route("/story")
def story():
    return render_template("story.html")
@app.route("/ReadAloud")
def read():
    return render_template("ReadAloud.html")

if __name__=='__main__':
    # app.run(debug=True)
    socketio.run(app,debug=True)

