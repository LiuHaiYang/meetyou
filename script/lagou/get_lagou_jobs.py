# encoding:utf-8
import requests,re,urllib.request
from lxml import etree
import xlwt
import time
from main import db
from models import Bossjob,Lagoujob,Zhilianjob
import json
import datetime
class LaGoSpider:
    def __init__(self,url_list):
        self.url_list = url_list
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}
        self.workbook = xlwt.Workbook()
        self.table = self.workbook.add_sheet('Sheet2',cell_overwrite_ok=True)

    def get_source(self, url):
        html = requests.get(url,headers=self.headers)
        html.encoding = 'utf-8'
        return etree.HTML(html.text)
    def run(self):
        for url in self.url_list:
            html = self.get_source(url)
            num_list = html.xpath("//*[@id='s_position_list']/ul/li//@data-positionid")
            # print(num_list)
            self.get_data_info(num_list)

            for each in range(1,30):
                time.sleep(1)
    def get_data_info(self,num_list):
        for i in num_list:
            for each in range(1, 15):
                time.sleep(1)
            try:
                url_info = 'https://www.lagou.com/jobs/{}.html'.format(i)
                html_info = self.get_source(url_info)
    # 发布平台 # 招聘公司 # 公司类型 # 公司级别 # 职位名称#  # 发布时间 拉取数据时间  # 地点  # 招聘要求
    # 工作职责 # 福利  # 学历 # 薪资 # 工作时间 # 职位描述 # 公司描述 # job 状态 # job 标签
                # #招聘的岗位名称：
                platform = '拉勾'
                job_status = 0
                job_label = ''
                company_leavl = html_info.xpath('//*[@id="job_company"]/dd/ul/li[2]/text()')
                company_type = html_info.xpath('//*[@id="job_company"]/dd/ul/li[1]/text()')
                job_name = html_info.xpath("/html/body/div[2]/div/div[1]/div/span/text()")
                put_time =  datetime.datetime.strftime((datetime.datetime.now()),'%Y-%m-%d %H:%M:%S')
                t_time =  datetime.datetime.strftime((datetime.datetime.now()),'%Y-%m-%d')
                company_desc = html_info.xpath('//*[@id="job_company"]/dd/ul/li[3]/text()')
                company_name = html_info.xpath("/html/body/div[2]/div/div[1]/div/div[1]/text()")
                money = html_info.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[1]/text()')
                city = html_info.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[2]/text()')
                worktime = html_info.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[3]/text()')
                degree = html_info.xpath('/html/body/div[2]/div/div[1]/dd/p[1]/span[4]/text()')
                youhuo = html_info.xpath('//*[@id="job_detail"]/dd[1]/p/text()')
                zhize_all = html_info.xpath('//*[@id="job_detail"]/dd[2]/div/p/text()')
                format_time = html_info.xpath('/html/body/div[2]/div/div[1]/dd/p[2]/text()')
                jobdesc = ''#''.join(zhize_all)
                for i in range(3,len(zhize_all)):
                    if len(zhize_all[i]) <=4 or '任职资格' in zhize_all[i] or '任职要求' in zhize_all[i]  or '详细任职要求' in zhize_all[i]:
                        zhize = ''.join(zhize_all[:i])
                        yaoqiu = ''.join(zhize_all[i:])
                        break
                    else:
                        zhize = ''.join(zhize_all)
                        yaoqiu = ''

                # print(company_leavl,company_type)
                # print(''.join(company_leavl).strip(),''.join(company_type).strip())
                # print(platform,job_status,job_label,''.join(company_leavl),''.join(company_type),put_time,fuli,
                #       ''.join(job_name),''.join(city),''.join(money),''.join(worktime),''.join(company_desc),''.join(company_name),''.join(degree),','.join(youhuo),zhize,yaoqiu,''.join(format_time))
                #保存到数据库
                fabu_time = str(t_time) + ' ' + str(''.join(format_time)).split(' ')[0][:-1]+str(':00')
                if '/' in ''.join(worktime)[:-2]:
                    worktimedata = ''.join(worktime)[:-2]
                else:
                    worktimedata = ''.join(worktime)[:-2]
                lagou_info = Lagoujob(platform, ''.join(company_name), ''.join(company_type).strip(), ''.join(company_leavl).strip(), ''.join(job_name),fabu_time , put_time, \
                ''.join(city)[1:-2], yaoqiu, zhize, youhuo, ''.join(degree)[:-2], ''.join(money), worktimedata, jobdesc, ''.join(company_desc).strip(),job_status,job_label)
                db.session.add(lagou_info)
                db.session.commit()
                db.create_all()
                print('lagou insert ok!')
            except:
                print('lagou error 下一个url!')

def get_lagou_data():
    url_list = []
    for i in range(1,30):
        url ='https://www.lagou.com/zhaopin/{}'.format(i)
        url_list.append(url)
    spider = LaGoSpider(url_list)
    spider.run()

# from email.MIMEMultipart import MIMEMultipart
# from email.mime.text import MIMEText
# import smtplib
# def send(email):
#     msg = MIMEMultipart.MIMEMultipart()
#     content = '''<html><body>        <h4>你好!</h4></body></html>'''
#     txt = MIMEText(content, 'html', 'utf-8')
#     msg.attach(txt)
#     msg["Accept-Language"] = "zh-CN"
#     msg["Accept-Charset"] = "ISO-8859-1,utf-8"
#
#     msg['from'] = 'soloerp@newborntown.com'
#     msg['subject'] = 'Test---'
#     mail_to = [email]   #收件人
#     msg['To'] = ';'.join(mail_to)
#     mail_from = "@Xxx.com"  #发件人
#     smtp = smtplib.SMTP()
#     smtp.connect('smtp.exmail.qq.com', '25')  #邮箱服务器  自己更改
#     smtp.login('XX@xx.com', 'passwd')
#     smtp.sendmail(mail_from, mail_to, msg.as_string())
#     smtp.quit()