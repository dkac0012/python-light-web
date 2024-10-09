from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# 사용자 데이터 (실제 구현에서는 데이터베이스를 사용해야 함)
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
    app.run(debug=False)
