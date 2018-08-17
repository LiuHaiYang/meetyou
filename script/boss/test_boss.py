# encoding:utf-8
import requests,re,urllib.request
from lxml import etree
import xlwt
from bs4 import BeautifulSoup
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

    def get_proxy(self,aip):
        """构建格式化的单个proxies"""
        proxy_ip = 'http://' + aip
        proxy_ips = 'https://' + aip
        proxy = {'https': proxy_ips, 'http': proxy_ip}
        return proxy

    def get_ip_list(self):
        """ 从代理网站上获取代理"""
        headers = self.headers
        url = 'http://www.xicidaili.com/wt'
        ip_list = []
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.text, 'lxml')
        ul_list = soup.find_all('tr', limit=20)
        for i in range(2, len(ul_list)):
            line = ul_list[i].find_all('td')
            ip = line[1].text
            port = line[2].text
            address = ip + ':' + port
            ip_list.append(address)
        for ip in ip_list:
                try:
                    proxy_host = "https://" + ip
                    proxy_temp = {"https": proxy_host}
                    res = urllib.urlopen(url, proxies=proxy_temp).read()
                except Exception as e:
                    ip_list.remove(ip)
                    continue
        return ip_list

    def get_source(self, url):
        aips =self.get_ip_list()
        for i in aips:
            proxies = self.get_proxy(i)
            try:
                html = requests.get(url,headers=self.headers,proxies=proxies)
                print('IP 可用')
                html.encoding = 'utf-8'
                break
            except:
                print('IP 不可用')
        return etree.HTML(html.text)
    def run(self):
        print('RUN')
        for url in self.url_list:
            html = self.get_source(url)
            num_list = []
            for j in range(1,31):
                num_list.append(html.xpath("//*[@id='main']/div/div[2]/ul/li["+str(j)+"]/div/div[1]/h3/a//@href"))

            print('get data')
            self.get_data_info(num_list)
            for each in range(20):
                time.sleep(1)
    def get_data_info(self,num_list):
        for each in range(1, 15):
            time.sleep(1)
        for i in num_list:
            try:
                url_info = 'https://www.zhipin.com/{}'.format(i[0])

                html_info = self.get_source(url_info)
                platform = 'boss'
                job_status = 0
                job_label = ''
                company_leavl = html_info.xpath('//*[@id="main"]/div[1]/div/div/div[3]/p[1]/text()[1]')
                company_type = html_info.xpath('//*[@id="main"]/div[1]/div/div/div[3]/p[1]/a/text()')
                job_name = html_info.xpath("//*[@id='main']/div[1]/div/div/div[2]/div[2]/h1/text()")
                put_time =  datetime.datetime.strftime((datetime.datetime.now()),'%Y-%m-%d %H:%M:%S')
                company_desc = html_info.xpath('//*[@id="main"]/div[3]/div/div[2]/div[3]/div[2]/div/text()')
                company_name = html_info.xpath("//*[@id='main']/div[1]/div/div/div[3]/h3/a/text()")
                money = html_info.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[2]/span/text()')
                city = html_info.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()[1]')
                worktime = html_info.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()[2]')
                degree = html_info.xpath('//*[@id="main"]/div[1]/div/div/div[2]/p/text()[3]')
                youhuo = ''
                zhize_all = html_info.xpath('//*[@id="main"]/div[3]/div/div[2]/div[3]/div[1]/div/text()')
                format_time = html_info.xpath('//*[@id="main"]/div[1]/div/div/div[2]/div[1]/span/text()')
                jobdesc = ''
                fabu_time = str(format_time[0])[3:]+":00"
                if len(city) ==0:
                    city=''
                else:
                    if  '：' in str(city):
                        citys=str(city[0]).split('：')
                        city = citys[1]
                    else:
                        city = ''
                if len(degree) ==0:
                    degree=''
                else:
                    if  '：' in str(degree):
                        degrees=str(degree[0]).split('：')
                        degree = degrees[1]
                    else:
                        degree = ''
                if len(money) ==0:
                    money=''
                else:
                    money=money[0]
                if len(worktime) == 0:
                    worktime = ''
                else:
                    if  '：' in str(worktime):
                        worktimes=str(worktime[0]).split('：')
                        worktime = worktimes[1]
                    else:
                        degree = ''
                # print(zhize_all)
                for i in range(1,len(zhize_all)):
                    if  '职位需求' in zhize_all[i] or '资格' in zhize_all[i] or '要求' in zhize_all[i]  or '职位描述​：' in zhize_all[i] or  '任职要求：' in zhize_all[i]:
                        zz_data = str(''.join(zhize_all[:i]))
                        yaoqiu_data = str(''.join(zhize_all[i:]))
                        break
                    else:
                        zz_data = str(''.join(zhize_all))
                        yaoqiu_data = ''

                #保存到数据库
                # platform, companyname, companytype, companylevel, jobname, releasetime, date, \
                # address, requirements, worddata, welfare, degree, money, worktime, jobdesc, companydesc, status, label):
                boss_info = Bossjob(platform, company_name[0], company_type[0],company_leavl[0], job_name[0],fabu_time , put_time, \
                city, yaoqiu_data, zz_data.strip(), youhuo, degree, money, worktime, jobdesc, company_desc[0],job_status,job_label)
                db.session.add(boss_info)
                db.session.commit()
                db.create_all()
                print('boss insert ok!')
            except:
                print('boss error 下一个url!')
if __name__ == '__main__':
# def get_boss_data():
    url_list = []
    for i in range(1,50):
        url ='https://www.zhipin.com/c101010100/?page={}'.format(i)
        url_list.append(url)
    spider = LaGoSpider(url_list)
    spider.run()
