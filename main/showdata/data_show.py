from flask import Blueprint,render_template,request,session,make_response,redirect
import json
from models import Bossjob,Lagoujob,Zhilianjob
import datetime
from main import auth
showdata = Blueprint('showdata', __name__)

@showdata.route('/showdata/index',methods=["GET"])
@auth.require_login
def showdata_zhexian():
    if request.method == 'GET':
        return render_template('show_all.html')

@showdata.route('/show_figure_data',methods=["GET","POST"])
@auth.require_login
def show_figure_data():
    if request.method == 'POST':
        data = request.get_json(force=True)
        # 处理数据
        data_range = data['datarange_data']
        jobname_keyword = data['keyword']
        y_data = data['y_data']
        if jobname_keyword:
            if ';' in jobname_keyword:
                jobname = jobname_keyword.split(';')[0]
            else:
                jobname = jobname_keyword
        else:
            jobname = '%'
        data_start = data_range.split(' - ')[0]+str(' 00:00:01')
        data_end = data_range.split(' - ')[1]+str(' 23:59:59')
        print(data_start,data_end)
        if data['figure_data'] =='折线图':
            try:
                datas_boss = []
                datas_lagou = []
                datas_zhilian = []

                bossjobs = Bossjob.query.filter(Bossjob.jobname.like('%'+jobname+'%'),Bossjob.status == '0', Bossjob.releasetime >= data_start,Bossjob.releasetime<=data_end).all()
                for i in bossjobs:
                    datas_boss.append(
                        [i.jobname, i.companyname, i.companytype, i.degree, i.money, i.worktime, i.address, i.platform,
                         i.releasetime, i.id])
                lagoujobs = Lagoujob.query.filter(Lagoujob.jobname.like('%'+jobname+'%'),Lagoujob.status == '0', Lagoujob.releasetime >= data_start,Lagoujob.releasetime<=data_end).all()
                for i in lagoujobs:
                    datas_lagou.append(
                        [i.jobname, i.companyname, i.companytype, i.degree, i.money, i.worktime, i.address, i.platform,
                         i.releasetime, i.id])
                zhilianjobs = Zhilianjob.query.filter(Zhilianjob.jobname.like('%'+jobname+'%'),Zhilianjob.status == '0', Zhilianjob.releasetime >= data_start,Zhilianjob.releasetime<=data_end).all()
                for i in zhilianjobs:
                    datas_zhilian.append(
                        [i.jobname, i.companyname, i.companytype, i.degree, i.money, i.worktime, i.address, i.platform,
                         i.releasetime, i.id])
                datas = datas_boss + datas_lagou + datas_zhilian
                dgrees_l = []
                xinzi_l = []
                address_l = []
                worktime_l = []
                dgree_x = []
                xinzi_x = []
                worktime_x=[]
                address_x =[]
                for d in datas:
                    dgrees_l.append(d[3])
                    xinzi_l.append(d[4])
                    worktime_l.append(d[5])
                    address_l.append(d[6])
                dgree_x = list(set(dgrees_l))
                xinzi_x = list(set(xinzi_l))
                worktime_x = list(set(worktime_l))
                address_x = list(set(address_l))
                y_show_num = []
                if y_data == '学历':
                    for j in dgree_x:
                        y_show_num.append(len([i for i in dgrees_l if i ==j]))
                        x_list = dgree_x
                elif y_data == '薪资':
                    for j in xinzi_x:
                        y_show_num.append(len([i for i in xinzi_l if i ==j]))
                        x_list = xinzi_x
                elif y_data == '工作经验':
                    for j in worktime_x:
                        y_show_num.append(len([i for i in worktime_l if i ==j]))
                        x_list = worktime_x
                elif y_data == '工作地点':
                    for j in address_x:
                        y_show_num.append(len([i for i in address_l if i ==j]))
                        x_list = address_x
                else:
                    y_show_num=[]
                    x_list = []

                datas_show = {'name':y_data,'data':y_show_num}
                data_s = {}
                data_s['data'] = datas_show
                data_s['figure_data'] = data['figure_data']
                data_s['y_data'] = data['y_data']
                data_s['x_list'] = x_list
                return json.dumps({'code': 200, 'data_s': data_s})
            except:
                return json.dumps({'code': 500, 'message': u'无满足条件数据，展示错误！'})
        elif data['figure_data'] =='饼形图':
            try:
                # 处理数据
                bossjobs_c = Bossjob.query.filter(Bossjob.jobname.like('%' + jobname + '%'), Bossjob.status == '0',
                                                  Bossjob.releasetime >= data_start,
                                                  Bossjob.releasetime <= data_end).all()

                lagoujobs_c = Lagoujob.query.filter(Lagoujob.jobname.like('%' + jobname + '%'), Lagoujob.status == '0',
                                                    Lagoujob.releasetime >= data_start,
                                                    Lagoujob.releasetime <= data_end).all()
                zhilianjobs_c = Zhilianjob.query.filter(Zhilianjob.jobname.like('%' + jobname + '%'),
                                                        Zhilianjob.status == '0', Zhilianjob.releasetime >= data_start,
                                                        Zhilianjob.releasetime <= data_end).all()
                if y_data == '学历':
                    boss_c = [i.degree for i in bossjobs_c]
                    lagou_c = [i.degree for i in lagoujobs_c]
                    zhilian_c = [i.degree for i in zhilianjobs_c]

                elif y_data == '薪资':
                    boss_c = [i.money for i in bossjobs_c]
                    lagou_c = [i.money for i in lagoujobs_c]
                    zhilian_c = [i.money for i in zhilianjobs_c]
                elif y_data == '工作经验':
                    boss_c = [i.worktime for i in bossjobs_c]
                    lagou_c = [i.worktime for i in lagoujobs_c]
                    zhilian_c = [i.worktime for i in zhilianjobs_c]
                elif y_data == '工作地点':
                    boss_c = [i.address for i in bossjobs_c]
                    lagou_c = [i.address for i in lagoujobs_c]
                    zhilian_c = [i.address for i in zhilianjobs_c]
                else:
                    boss_c = []
                    lagou_c = []
                    zhilian_c = []
                zhilian_n = len(zhilian_c)
                lagou_n = len(lagou_c)
                boss_n = len(boss_c)
                zhilian_data_l = list(set(zhilian_c))
                lagou_data_l = list(set(lagou_c))
                boss_data_l = list(set(boss_c))
                sum_c = lagou_n + boss_n + zhilian_n  #float('%.2f' % a)
                lagou_data = [float('%.2f'  % (lagou_c.count(i)/lagou_n*float(lagou_n/sum_c*100))) for i in lagou_data_l]
                boss_data = [float('%.2f'  % (boss_c.count(i)/boss_n*float(boss_n/sum_c*100))) for i in boss_data_l]
                zhilian_data = [float('%.2f'  % (zhilian_c.count(i)/zhilian_n*float(zhilian_n/sum_c*100))) for i in zhilian_data_l]
                data_s = {}
                data_s['lagou'] = {'sum':float('%.2f'  % (lagou_n/sum_c*100)),'data':lagou_data,'data_l':lagou_data_l}
                data_s['boss'] = {'sum':float('%.2f'  % (boss_n/sum_c*100)),'data':boss_data,'data_l':boss_data_l}
                data_s['zhilian'] = {'sum':float('%.2f'  % (zhilian_n/sum_c*100)),'data':zhilian_data,'data_l':zhilian_data_l}
                data_s['figure_data'] = data['figure_data']
                data_s['y_data'] = y_data
                return json.dumps({'code': 200, 'data_s': data_s})
            except:
                return json.dumps({'code': 500, 'message': u'无满足条件数据，展示错误！'})
        elif data['figure_data'] == '柱状图':
            try:
                time_range = []
                for i in range(-1,12):
                    newtime = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(days=i*30)), '%Y-%m-01')
                    time_range.append(newtime)
                time_ranges = time_range[::-1]
                b_c = []
                l_c = []
                z_c = []
                for i in range(len(time_ranges)-1):
                    bossjobs = Bossjob.query.filter(Bossjob.jobname.like('%'+jobname+'%'),Bossjob.status == '0', Bossjob.releasetime >= time_ranges[i],Bossjob.releasetime<=time_ranges[i+1]).count()
                    lagoujobs = Lagoujob.query.filter(Lagoujob.jobname.like('%'+jobname+'%'),Lagoujob.status == '0', Lagoujob.releasetime >= time_ranges[i],Lagoujob.releasetime<=time_ranges[i+1]).count()
                    zhilianjobs = Zhilianjob.query.filter(Zhilianjob.jobname.like('%'+jobname+'%'),Zhilianjob.status == '0', Zhilianjob.releasetime >= time_ranges[i],Zhilianjob.releasetime<=time_ranges[i+1]).count()
                    b_c.append(bossjobs)
                    l_c.append(lagoujobs)
                    z_c.append(zhilianjobs)

                data_s = {}
                data_s['month']= [i[:-3] for i in time_ranges[:12]]
                print(data_s['month'])
                data_s['figure_data'] = data['figure_data']
                data_s['data'] = {'boss':b_c,'lagou':l_c,'zhilian':z_c}
                return json.dumps({'code': 200, 'data_s': data_s})
            except:
                return json.dumps({'code': 500, 'message': u'无满足条件数据，展示错误！'})
        elif data['figure_data'] == '词云图':
            try:
                bossjobs = Bossjob.query.filter(Bossjob.jobname.like('%' + jobname + '%'), Bossjob.status == '0',
                                                Bossjob.releasetime >=data_start,
                                                Bossjob.releasetime <= data_end).all()
                lagoujobs = Lagoujob.query.filter(Lagoujob.jobname.like('%' + jobname + '%'), Lagoujob.status == '0',
                                                  Lagoujob.releasetime >= data_start,
                                                  Lagoujob.releasetime <= data_end).all()
                zhilianjobs = Zhilianjob.query.filter(Zhilianjob.jobname.like('%' + jobname + '%'),
                                                      Zhilianjob.status == '0',
                                                      Zhilianjob.releasetime >= data_start,
                                                      Bossjob.releasetime <= data_end).all()
                if data['y_data'] == '学历':
                    boss_jobs = [i.degree for i in bossjobs]
                    lagou_jobs = [i.degree for i in lagoujobs]
                    zhilian_jobs = [i.degree for i in zhilianjobs]
                elif data['y_data'] == '薪资':
                    boss_jobs = [i.money for i in bossjobs]
                    lagou_jobs = [i.money for i in lagoujobs]
                    zhilian_jobs = [i.money for i in zhilianjobs]
                elif data['y_data'] == '工作经验':
                    boss_jobs = [i.worktime for i in bossjobs]
                    lagou_jobs = [i.worktime for i in lagoujobs]
                    zhilian_jobs = [i.worktime for i in zhilianjobs]
                elif data['y_data'] == '工作地点':
                    boss_jobs = [i.address for i in bossjobs]
                    lagou_jobs = [i.address for i in lagoujobs]
                    zhilian_jobs = [i.address for i in zhilianjobs]
                elif data['y_data'] == '职位名称':
                    boss_jobs = [i.jobname for i in bossjobs]
                    lagou_jobs = [i.jobname for i in lagoujobs]
                    zhilian_jobs = [i.jobname for i in zhilianjobs]
                else:
                    boss_jobs = []
                    lagou_jobs = []
                    zhilian_jobs = []
                data_ciyun = boss_jobs+lagou_jobs+zhilian_jobs
                data_ciyun_all = ' '.join(data_ciyun)
                data_s = {}
                data_s['figure_data'] = data['figure_data']
                data_s['data'] = str(data_ciyun_all)
                return json.dumps({'code': 200, 'data_s': data_s})
            except:
                return json.dumps({'code': 500, 'message': u'无满足条件数据，展示错误！'})
        elif data['figure_data'] == '分布图':
            try:

                bossjobs = Bossjob.query.filter(Bossjob.jobname.like('%' + jobname + '%'), Bossjob.status == '0',
                                                Bossjob.releasetime >= data_start,
                                                Bossjob.releasetime <= data_end).all()
                lagoujobs = Lagoujob.query.filter(Lagoujob.jobname.like('%' + jobname + '%'),
                                                  Lagoujob.status == '0',
                                                  Lagoujob.releasetime >= data_start,
                                                  Lagoujob.releasetime <= data_end).all()
                zhilianjobs = Zhilianjob.query.filter(Zhilianjob.jobname.like('%' + jobname + '%'),
                                                      Zhilianjob.status == '0',
                                                      Zhilianjob.releasetime >= data_start,
                                                      Bossjob.releasetime <= data_end).all()
                boss_jobs = [i.address for i in bossjobs]
                lagou_jobs = [i.address for i in lagoujobs]
                zhilian_jobs = [i.address for i in zhilianjobs]
                data_address = boss_jobs+lagou_jobs+zhilian_jobs
                sum_all = len(data_address)
                data_address_s = list(set(data_address))
                data_all = []
                for i in data_address_s:
                    data_all.append({'name':i ,'value':data_address.count(i)})
                data_s = {}
                data_s['figure_data'] = data['figure_data']
                # data_s['data'] =[  {'name': "常德", 'value': 152},{'name': "保定", 'value': 153}]
                data_s['data'] =data_all
                data_s['sum_all'] = sum_all
                return json.dumps({'code': 200, 'data_s': data_s})
            except:
                return json.dumps({'code': 500, 'message': u'无满足条件数据，展示错误！'})
        else:
            return json.dumps({'code': 500, 'message': u'无满足条件数据，展示错误！'})


@showdata.route('/show_index_web_num',methods=["GET","POST"])
@auth.require_login
def show_index_web_num():
    if request.method == 'GET':
        times = []
        boss = []
        lagou =[]
        zhilian = []
        for i in range(8):
            newtime = datetime.datetime.strftime((datetime.datetime.now() - datetime.timedelta(days=i)), '%Y-%m-%d')
            times.append(newtime)
        times = times[::-1]
        for d in range(len(times)-1):
            boss_count = Bossjob.query.filter(Bossjob.status == '0',Bossjob.releasetime >= times[d], Bossjob.releasetime <= times[d+1]).count()
            lagou_count = Lagoujob.query.filter(Lagoujob.status == '0',Lagoujob.releasetime >= times[d], Lagoujob.releasetime <= times[d+1]).count()
            zhilian_count = Zhilianjob.query.filter(Zhilianjob.status == '0',Zhilianjob.releasetime >= times[d], Zhilianjob.releasetime <= times[d+1]).count()
            boss.append(boss_count)
            lagou.append(lagou_count)
            zhilian.append(zhilian_count)
        return json.dumps({'times':times[:7],'boss': boss, 'zhilian': zhilian, 'lagou': lagou})

