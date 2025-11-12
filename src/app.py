from flask import Flask, render_template
from routes import fraud_routes
from database import init_db

app = Flask(__name__, template_folder='templates')
init_db()

app.register_blueprint(fraud_routes, url_prefix='/api')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
