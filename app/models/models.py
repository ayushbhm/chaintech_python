from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password_hash = db.Column(db.String(20), nullable=False)
    
    
    def set_password(self, password):
        
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        
        return check_password_hash(self.password_hash, password)  #

    def __repr__(self):
        return f'<User {self.username}>'