from flask import Flask, request, redirect, url_for,jsonify,session
from flask import render_template
import requests
import creds
from models.models import db, User

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite3'
app.config['SECRET_KEY'] = 'Assignment' 

# Silence the deprecation warning
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/",methods=["GET"])
def hello_world():
    city = "London"
    weather = get_weather(city)
    if weather:
        temperature_k = weather['main']['temp']
        temperature = round(temperature_k - 273.15,2)
        weather_description = weather['weather'][0]['description']
        
    return render_template("mainpage.html",temperature=temperature, weather_description=weather_description)


@app.route('/register_page')
def register_page():
    return render_template("register.html")

@app.route("/register",methods=["POST"])
def register():
    
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists, try another username"
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return render_template("register_success.html")
    
    return render_template("register.html")


@app.route("/login_page")
def login_page():
    return render_template("login.html")

@app.route("/login",methods=["POST"])
def login():
    if 'username' in session and 'id' in session:
        return render_template("already_logged.html")  
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not username or not password:
            return jsonify({'error': 'Missing fields'}), 400
        
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = user.username
            session['id'] = user.id
            return redirect(url_for("display_login_info"))
            
        else:
            return redirect(url_for("login_page"))
        
    return redirect(url_for("login"))

@app.route("/display_login_info")
def display_login_info():
 
    if 'username' in session and 'id' in session:
        username = session['username']
        user_id = session['id']
        return render_template("display_login_info.html", username=username, user_id=user_id)
    else:
        return redirect(url_for("login"))  # 




@app.route("/logout")
def logout():
    session.clear()  
    
    
    return redirect(url_for("hello_world"))  


def get_weather(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={creds.api_key}"
    response = requests.get(url)
    return response.json()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)