# python-light-web

python 환경에서 세션을 활용한 로그인과 build를 하여 실행파일을 만들어 보았습니다.


## 과정

### venv 사용

pip 환경분리
```bash
python3 -m venv .venv
```
실행
```bash
source .venv/bin/activate
```

### 서비스 python 파일 생성

```python
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

users = {
    'testuser': {'password': 'testpassword', 'name': 'Test User'}
}


@app.route('/')
def home():
    user = session.get('user')
    return render_template('home.html', user=user)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username]['password'] == password:
            session['user'] = users[username]['name']
            return redirect(url_for('home'))
        else:
            return '로그인 실패', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

@app.route('/mypage', methods=['GET', 'POST'])
def mypage():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # 마이페이지에서 사용자 데이터 수정 처리
        new_name = request.form['name']
        session['user'] = new_name  # 세션 업데이트
        return redirect(url_for('home'))
    
    return render_template('mypage.html', user=session['user'])

if __name__ == '__main__':
    app.run(debug=True)
```

### build

pyinstaller 사용
```bash
pip install pyinstaller
```
```bash
pyinstaller --onefile app.py
```

#### 생성 확인
![image](https://github.com/user-attachments/assets/ba378476-57d8-4d3f-a139-a01528d43be8)

### troubleshooting

```bash
./dist/app 생성된 exe파일 실행
```

error 발견
```bash
 * Serving Flask app 'app'
 * Debug mode: on
Address already in use
Port 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.
On macOS, try disabling the 'AirPlay Receiver' service from System Preferences -> General -> AirDrop & Handoff.
 * Debugger is active!
 * Debugger PIN: 105-348-553
Traceback (most recent call last):
  File "app.py", line 48, in <module>
    app.run(debug=True)
  File "flask/app.py", line 625, in run
  File "werkzeug/serving.py", line 1091, in run_simple
  File "werkzeug/serving.py", line 928, in make_server
  File "werkzeug/serving.py", line 790, in __init__
  File "socket.py", line 549, in fromfd
  File "socket.py", line 233, in __init__
OSError: [Errno 38] Socket operation on non-socket
[PYI-15076:ERROR] Failed to execute script 'app' due to unhandled exception!
```
해당 error는 debug모드를 true인 상태로 놓았기 때문에 발생하였습니다.
debug 모드를 false로 바꿔주면 정상 실행

```bash                 
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
```
