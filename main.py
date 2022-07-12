from flask import Flask

app = Flask('courses')

@app.route('/')
def test():
    return 'test'

app.run(port=1234)
