import requests
import  bs4
import sqlite3
import pandas.io.sql as sql
result = {  "jobname": [],
            "area": [],
            "salary": [],
            "url": [],
            "cop": [],
            "edu":[]
          }
conn = sqlite3.connect('shenzhen_zhaopin.db')
cursor = conn.cursor()
#请提前新建数据库结构cursor.execute('create table zhaopin(id integer PRIMARY KEY AUTOINCREMENT,jobname text,area text,salary text,url text,cop text,edu text)')
for i in range(11):
    url = "https://www.liepin.com/zhaopin/?compkind=&dqs=050090&pubTime=&pageSize=40&salary=&compTag=&sortFlag=&compIds=&subIndustry=&jobKind=&industries=&compscale=&key=&siTag=1B2M2Y8AsgTpgAmY7PhCfg%7EfA9rXquZc5IkJpXC-Ycixw&d_sfrom=search_title&d_ckId=c16556e4cc914dee657cb1e26c5f809e&d_curPage=0&d_pageSize=40&d_headId=c16556e4cc914dee657cb1e26c5f809e" + str(i)
    print(url)
    headers = {'User-Agent' : 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)'}
    r = requests.get(url, params=None, headers=headers)
    html = bs4.BeautifulSoup(r.text, "html.parser")
    all_job = html.find("ul", class_="sojob-list").find_all("li")
    for date in all_job:
        name = date.find("a", target="_blank").text.strip()
        area = date.find("a", class_="area").text
        salary = date.find("span", class_="text-warning").text
        url = date.find("p", class_="company-name").find("a")["href"]
        cop = date.find("p", class_="company-name").text.strip()
        edu = date.find("span", class_="edu").text
        result["jobname"].append(name)
        result["area"].append(area)
        result["salary"].append(salary)
        result["url"].append(url)
        result["cop"].append(cop)
        result["edu"].append(edu)
        cursor.execute("insert into zhaopin (jobname,area,salary,url,cop,edu) values (?,?,?,?,?,?)",(name,area,salary,url,cop,edu))
table = sql.read_sql('select * from zhaopin', conn)
table.to_csv("shenzhen_zhaopin.csv", encoding="utf_8_sig")
conn.commit()
cursor.close()
conn.close()