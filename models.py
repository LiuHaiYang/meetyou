# -*- coding: utf-8 -*-
from main import db
import sqlalchemy.dialects.mysql
#boss
class Bossjob(db.Model):
    __tablename__ = 'bossjob'
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100), nullable=True)#发布平台
    companyname = db.Column(db.String(100), nullable=True)#招聘公司
    companytype = db.Column(db.String(100), nullable=True)  # 公司类型
    companylevel = db.Column(db.String(100), nullable=True)  # 公司级别

    jobname = db.Column(db.String(100), nullable=True)#职位名称
    releasetime = db.Column(db.String(100), nullable=True) #发布时间
    date = db.Column(db.String(100), nullable=True)#拉取数据时间
    address = db.Column(db.String(100), nullable=True)#地点
    requirements = db.Column(db.Text, nullable=True)  # 招聘要求
    worddata = db.Column(db.Text, nullable=True)  # 工作职责
    welfare = db.Column(db.String(100), nullable=True)  # 福利
    degree = db.Column(db.String(100), nullable=True)  # 学历
    money = db.Column(db.String(100), nullable=True)  # 薪资
    worktime = db.Column(db.String(100), nullable=True)  # 工作时间
    jobdesc  = db.Column(db.Text, nullable=True)  # 职位描述
    companydesc = db.Column(db.Text, nullable=True)  # 公司类型
    status = db.Column(db.String(10), nullable=True)  # job 状态
    label = db.Column(db.String(10), nullable=True)  # job 标签



    def __init__(self, platform, companyname, companytype, companylevel, jobname, releasetime,date,\
        address,requirements ,worddata,welfare,degree,money,worktime,jobdesc,companydesc,status,label):
        self.platform = platform
        self.companyname = companyname
        self.companytype = companytype
        self.companylevel = companylevel
        self.jobname = jobname
        self.releasetime = releasetime
        self.date = date
        self.address = address
        self.requirements = requirements
        self.worddata = worddata
        self.welfare = welfare
        self.degree = degree

        self.money = money
        self.worktime = worktime
        self.jobdesc = jobdesc
        self.companydesc = companydesc
        self.status = status
        self.label = label


    def __repr__(self):
        return '<bossjob {}>'.format(self.id)

#拉勾
class Lagoujob(db.Model):
    __tablename__ = 'lagoujob'
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100), nullable=True)  # 发布平台
    companyname = db.Column(db.String(100), nullable=True)  # 招聘公司
    companytype = db.Column(db.String(100), nullable=True)  # 公司类型
    companylevel = db.Column(db.String(100), nullable=True)  # 公司级别

    jobname = db.Column(db.String(100), nullable=True)  # 职位名称
    releasetime = db.Column(db.String(100), nullable=True)  # 发布时间
    date = db.Column(db.String(100), nullable=True)  # 拉取数据时间
    address = db.Column(db.String(100), nullable=True)  # 地点
    requirements = db.Column(db.Text, nullable=True)  # 招聘要求
    worddata = db.Column(db.Text, nullable=True)  # 工作职责
    welfare = db.Column(db.String(100), nullable=True)  # 福利
    degree = db.Column(db.String(100), nullable=True)  # 学历
    money = db.Column(db.String(100), nullable=True)  # 薪资
    worktime = db.Column(db.String(100), nullable=True)  # 工作时间
    jobdesc = db.Column(db.Text, nullable=True)  # 职位描述
    companydesc = db.Column(db.Text, nullable=True)  # 公司描述
    status = db.Column(db.String(10), nullable=True)  # job 状态
    label = db.Column(db.String(10), nullable=True)  # job


    def __init__(self, platform, companyname, companytype, companylevel, jobname, releasetime, date, \
                 address, requirements, worddata, welfare, degree, money, worktime, jobdesc, companydesc,status,label):
        self.platform = platform
        self.companyname = companyname
        self.companytype = companytype
        self.companylevel = companylevel
        self.jobname = jobname
        self.releasetime = releasetime
        self.date = date
        self.address = address
        self.requirements = requirements
        self.worddata = worddata
        self.welfare = welfare
        self.degree = degree

        self.money = money
        self.worktime = worktime
        self.jobdesc = jobdesc
        self.companydesc = companydesc
        self.status = status
        self.label = label

    def __repr__(self):
        return '<lagoujob {}>'.format(self.id)
#智联
class Zhilianjob(db.Model):
    __tablename__ = 'zhilianjob'
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(100), nullable=True)  # 发布平台
    companyname = db.Column(db.String(100), nullable=True)  # 招聘公司
    companytype = db.Column(db.String(100), nullable=True)  # 公司类型
    companylevel = db.Column(db.String(100), nullable=True)  # 公司级别

    jobname = db.Column(db.String(100), nullable=True)  # 职位名称
    releasetime = db.Column(db.String(100), nullable=True)  # 发布时间
    date = db.Column(db.String(100), nullable=True)  # 拉取数据时间
    address = db.Column(db.String(100), nullable=True)  # 地点
    requirements = db.Column(db.Text, nullable=True)  # 招聘要求
    worddata = db.Column(db.Text, nullable=True)  # 工作职责
    welfare = db.Column(db.String(100), nullable=True)  # 福利
    degree = db.Column(db.String(100), nullable=True)  # 学历
    money = db.Column(db.String(100), nullable=True)  # 薪资
    worktime = db.Column(db.String(100), nullable=True)  # 工作时间
    jobdesc = db.Column(db.Text, nullable=True)  # 职位描述
    companydesc = db.Column(db.Text, nullable=True)  # 公司类型
    status = db.Column(db.String(10), nullable=True)  # job 状态
    label = db.Column(db.String(10), nullable=True)  # job 标签


    def __init__(self, platform, companyname, companytype, companylevel, jobname, releasetime, date, \
                 address, requirements, worddata, welfare, degree, money, worktime, jobdesc, companydesc,status,label):
        self.platform = platform
        self.companyname = companyname
        self.companytype = companytype
        self.companylevel = companylevel
        self.jobname = jobname
        self.releasetime = releasetime
        self.date = date
        self.address = address
        self.requirements = requirements
        self.worddata = worddata
        self.welfare = welfare
        self.degree = degree

        self.money = money
        self.worktime = worktime
        self.jobdesc = jobdesc
        self.companydesc = companydesc
        self.status = status
        self.label = label

    def __repr__(self):
        return '<zhilianjob {}>'.format(self.id)

#用户
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    login_ac = db.Column(db.String(100), nullable=True)  # 登录账号
    passwd = db.Column(db.String(100), nullable=True)  # 密码
    number = db.Column(db.String(100), nullable=True)  # 手机号
    user_level = db.Column(db.String(100), nullable=True)  # 用户级别
    create_time = db.Column(db.String(100), nullable=True)  # 注册时间
    last_time = db.Column(db.String(100), nullable=True)  # 上次登录时间
    status = db.Column(db.String(100), nullable=True)  # 状态
    love_list = db.Column(db.Text, nullable=True)
    def __init__(self, login_ac, passwd,number,user_level,create_time,last_time,status,love_list):
        self.login_ac = login_ac
        self.passwd = passwd
        self.number = number
        self.user_level = user_level
        self.create_time = create_time
        self.last_time = last_time
        self.status = status
        self.love_list = love_list

    def __repr__(self):
        return '<user {}>'.format(self.id)

# 用户详情
class Userinfo(db.Model):
    __tablename__ = 'userinfo'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=True)  # 用户名
    sex = db.Column(db.String(20), nullable=True)  # 性别
    intersert_hangye = db.Column(db.String(100), nullable=True)  # 兴趣行业
    hope_money = db.Column(db.String(100), nullable=True)  # 期望薪资
    hope_city = db.Column(db.String(100), nullable=True)  # 期望城市
    worktime = db.Column(db.String(100), nullable=True)  # 工作经验
    live_city = db.Column(db.String(100), nullable=True)  # 居住城市
    per_do = db.Column(db.String(200), nullable=True)  #个人技能
    job_key = db.Column(db.String(50), nullable=True)  #关键词
    user_id = db.Column(db.Integer, nullable=True)  # 用户id
    hpone_number = db.Column(db.String(100), nullable=True)  # 用户手机号码
    email = db.Column(db.String(100), nullable=True)  # 邮箱
    user_level = db.Column(db.String(100), nullable=True)  # 用户级别
    user_type = db.Column(db.String(100), nullable=True)  # 用户类型
    user_status = db.Column(db.String(100), nullable=True)  # 用户状态
    script_status = db.Column(db.String(100), nullable=True)  # 脚本状态
    stop_time = db.Column(db.String(100), nullable=True)  # 停止时间

    def __init__(self, username, sex,intersert_hangye,hope_money,hope_city,worktime,live_city,
                 per_do,job_key,user_id,hpone_number, email,user_level, user_type,
                 user_status,script_status,stop_time):
        self.sex = sex
        self.intersert_hangye = intersert_hangye
        self.hope_money = hope_money
        self.hope_city = hope_city
        self.worktime = worktime
        self.live_city = live_city
        self.per_do = per_do
        self.job_key = job_key
        self.user_id = user_id
        self.email = email

        self.username = username
        self.hpone_number = hpone_number
        self.user_level = user_level
        self.user_type = user_type
        self.user_status = user_status
        self.script_status = script_status
        self.stop_time = stop_time

    def __repr__(self):
        return '<userinfo {}>'.format(self.id)

#操作归档
class Runhistory(db.Model):
    __tablename__ = 'runhistory'
    id = db.Column(db.Integer, primary_key=True)
    data_web = db.Column(db.String(100), nullable=True)  # 数据源网站
    data_tianjian = db.Column(db.String(100), nullable=True)  # 数据条件
    every_time = db.Column(db.String(100), nullable=True)  # 时间间隔
    start_time = db.Column(db.String(100), nullable=True)  # 启动时间
    operator = db.Column(db.String(100), nullable=True)  # 操作人员
    status = db.Column(db.String(100), nullable=True)  # 状态
    stop_time = db.Column(db.String(100), nullable=True)  # 停止时间

    # def __init__(self, data_web, data_tianjian,every_time,start_time,operator,status,stop_time):
    #     self.data_web = data_web
    #     self.data_tianjian = data_tianjian
    #     self.every_time = every_time
    #     self.start_time = start_time
    #     self.operator = operator
    #     self.status = status
    #     self.stop_time = stop_time
    def __repr__(self):
        return '<runhistory {}>'.format(self.id)

#推荐归档
class Recommenddata(db.Model):
    __tablename__ = 'recommenddata'
    id = db.Column(db.Integer, primary_key=True)
    re_id = db.Column(db.Integer, nullable=True)
    platom = db.Column(db.String(100), nullable=True)  # 数据源网站
    user_id = db.Column(db.String(100), nullable=True)  # 推荐用户id
    jobname = db.Column(db.String(100), nullable=True)  # 职位名称
    companyname = db.Column(db.String(100), nullable=True)  # 公司名称
    money = db.Column(db.String(100), nullable=True)  # 薪资
    worktime = db.Column(db.String(100), nullable=True)  # 工作经验
    city = db.Column(db.String(100), nullable=True)  # 城市
    youhuo = db.Column(db.Text, nullable=True)  #
    zhize = db.Column(db.Text, nullable=True)  #
    yaoqiu= db.Column(db.Text, nullable=True)  #
    recommend_type= db.Column(db.String(100), nullable=True)  #
    re_time= db.Column(db.String(100), nullable=True)  #
    def __init__(self, re_id,platom, user_id,jobname,companyname,money,worktime,city,youhuo,zhize,yaoqiu,recommend_type,re_time):
        self.re_id = re_id
        self.platom = platom
        self.user_id = user_id
        self.jobname = jobname
        self.companyname = companyname
        self.money = money
        self.worktime = worktime
        self.city = city
        self.youhuo = youhuo
        self.zhize = zhize
        self.yaoqiu = yaoqiu
        self.recommend_type = recommend_type
        self.re_time = re_time

    def __repr__(self):
        return '<recommenddata {}>'.format(self.id)
db.create_all()