from flask import Flask, render_template, jsonify, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)




# İletişim mesaj modeli
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Message('{self.name}', '{self.email}', '{self.timestamp}')"

# Veritabanını oluştur
with app.app_context():
    db.create_all()

@app.route("/messages")
def messages():
    all_messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template("messages.html", messages=all_messages)



@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/projects")
def projects():
    return render_template("projects.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")  # .get() prevents KeyError
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email or not message:
            return "All fields are required!", 400  # Send a bad request response

        new_message = Message(name=name, email=email, message=message)
        db.session.add(new_message)
        db.session.commit()

        return redirect("/messages")  

    return render_template("contact.html")




@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/api/test")
def api_test():
    data = {"text": "Hello!"}
    return jsonify(data)

@app.route("/api/time")
def api_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    data = {"time": current_time}
    return jsonify(data)

@app.route("/index")
def hello1_world():
    return render_template("index.html")

@app.route("/images")
def image():
    image_filenames = ["car.jpg", "image2.jpg", "image3.jpg"]
    return render_template("image.html", images=image_filenames)


@app.route("/firstproject")
def first_project():                                           # page for my prjects details  1
    return render_template("firstproject.html")

@app.route("/secondproject")
def second_project():                                           # page for my prjects details  1
    return render_template("secondproject.html")

@app.route("/thirdproject")
def third_project():                                           # page for my prjects details  1
    return render_template("thirdproject.html")



if __name__ == '__main__':
    app.run(debug=True)
