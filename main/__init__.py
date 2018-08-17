# _*_ coding:utf-8 _*_
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
databaseurl = 'mysql+pymysql://%s:%s@%s:%s/%s' % ('root','123456', '127.0.0.1',3306,'jobsdata')
app.config['SQLALCHEMY_DATABASE_URI'] = databaseurl
app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', True)
db = SQLAlchemy(app)
def create_app():
    from main.home.home import homepage
    app.register_blueprint(homepage)
    from main.login.login import login as loginpage
    app.register_blueprint(loginpage)
    from main.companysdata.companys import companys
    app.register_blueprint(companys)
    from main.showdata.data_show import showdata
    app.register_blueprint(showdata)
    from main.getjobsdata.getjobsdata_run import getjobdata
    app.register_blueprint(getjobdata)
    from main.recommend.recommend import recommend
    app.register_blueprint(recommend)
    from main.analysis.analysis import analysis
    app.register_blueprint(analysis)
    from main.about.about import about
    app.register_blueprint(about)
    return app
