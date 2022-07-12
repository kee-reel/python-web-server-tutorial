from flask import Flask, render_template, request, redirect, make_response
from db_helper import DB

db = DB('courses.db')

app = Flask('courses')
app.run(port=1234, debug=True)

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    print(request.form)
    login = request.form.get('login')
    password = request.form.get('password')
    if not login or not password:
        return redirect('/')
    new_user_id = db.add_user(login, password)
    res = make_response(redirect('/profile'))
    res.set_cookie('user_id', str(new_user_id))
    return res

@app.route('/profile')
def profile():
    user_id = request.cookies.get('user_id')
    if user_id == None:
        return redirect('/')
    print(db.get_user(int(user_id)))
    return render_template('profile.html')

