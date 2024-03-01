from flask import Flask, render_template, session, request, redirect
import pymysql

app = Flask(__name__)

# session을 사용하기 위해서는 secret_key 지정이 필수
app.secret_key ='abcdefghijklmnopqrstuvwxyz'


conn = pymysql.connect(host='172.30.1.52',  user='root', password='1111', db="myapp", charset='utf8')

@app.route('/')
def index():
    if 'email' in session:
        return render_template('index.html', email=session['email'])
    else:
        return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        inputEmail = request.form['inputEmail']
        inputPassword = request.form['inputPassword']        
        with conn.cursor() as cur:
            cur.execute(f"select email, password from tbl_users where email = '{inputEmail}' and password = '{inputPassword}'")
            user = cur.fetchone()
            if user and inputPassword == user[1]:
                session['email'] = user[0]
                return redirect('/')
            else:
                return render_template('login.html', error="Invalid email and password")
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['inputName']
        email = request.form['inputEmail']
        password = request.form['inputPassword']
        with conn.cursor() as cur:
            cur.execute(f"insert into tbl_users (name, email, password) values ('{name}', '{email}', '{password}')")
            conn.commit()
        return redirect('/')
    else:
        return render_template('register.html')
    
@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)