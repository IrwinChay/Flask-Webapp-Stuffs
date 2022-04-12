from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


db = SQLAlchemy()
class User(UserMixin, db.Model):
    id =  db.Column(db.Integer,
                    primary_key=True) # Primary key required by SQLAlchemy
    username = db.Column(db.String(100), 
                        unique=True)
    password = db.Column(db.String(100) , 
                        primary_key = False,
                        unique = False)

    def set_password(self,password):
        self.password = generate_password_hash(password, 'sha256')

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "PAUL_SECRET_KEY"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    '''with app.app_context():
        user = User(username="AnonUser55")
        user.set_password('IHateSDP83913')
        db.session.add(user)
        db.session.commit()'''
    

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 

    from main import main as main_blueprint
    from auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)

    return app

if __name__ == "__main__":
    
    app = create_app()
    app.run(debug=True)
