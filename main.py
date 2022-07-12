from db_helper import DB
from flask import Flask, render_template, request, redirect, make_response

db = DB('courses.db')
app = Flask('courses')

@app.route('/', methods=['GET'])
def main():
    user_id = request.cookies.get('user_id')
    if user_id is None:
        return render_template('index.html')

    user = db.get_user_by_id(int(user_id))
    if user:
        return redirect('/profile')
    else:
        res = make_response(render_template('index.html'))
        res.delete_cookie('user_id')
        return res

@app.route('/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    if not login or not password:
        return redirect('/')
    user = db.get_user_by_login(login)
    if user:
        if user.password != password:
            return redirect('/')
    else:
        user = db.add_user(login, password)
    res = make_response(redirect('/profile'))
    res.set_cookie('user_id', str(user.id))
    return res

@app.route('/logout', methods=['POST'])
def logout():
    res = make_response(redirect('/'))
    res.delete_cookie('user_id')
    return res

@app.route('/profile')
def profile():
    user_id = request.cookies.get('user_id')
    if user_id is None:
        return redirect('/')
    user = db.get_user_by_id(int(user_id))
    if user is None:
        return redirect('/')
    return render_template('profile.html', user=user)

app.run(port=1234, debug=True)

