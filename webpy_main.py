#-*- coding: utf-8 -*-
import web,sys
import sqlite3

import config
dbfile = config.dbfile
temp_dir = config.temp_dir

# reload(sys)#支持中文
# sys.setdefaultencoding('utf8')

urls = (
    '/','index',
    '/refresh_sl','refresh_sl',
    '/add/(.*)','add'#有（.*）则可以传递参数add中的na参数，而且URL中（/add/smt）的smt前的/不能省略，没有smt则na为空.
                     #即可以用正则表达式，如/(test1|test2)则匹配/test1和/test2，而且这里的test1或test2也会作为参数传入，如上na
    )

render = web.template.render(temp_dir)

config.search_list = [] # 保存所有要搜索的绝对路径，将search_list放到config模块，直接用全局变量则不对

def reload_db():
    config.search_list = [] # 刷新时删除之前目录
    conn = sqlite3.connect(dbfile)
    cur = conn.cursor()
    cur.execute('''
            create table if not exists dir_db
            (dir_name text)
        ''')# 防止下面查找出错，所以不存在dir_db时即新建
    cur.execute("select dir_name from dir_db")
    row = cur.fetchone()
    while row != None:
        row_name = row[0]# 注意是元组要取第一个元素
        config.search_list.append(row_name)
        row = cur.fetchone()
    conn.commit()
    conn.close()


class index:
    def GET(self):
        reload_db()
        load_dir = []
        for item in config.search_list:
            load_dir.append(item)
        return render.index(load_dir)

class refresh_sl:
    def GET(self):
        reload_db()
        r_str = "<div>"
        for item in config.search_list:
            r_str = r_str + item
        r_str = r_str + "</div>"
        return r_str

class add:
    def GET(self,na):#处理get方法
        return render.post(na)
    def POST(self,na):#处理post方法（method）
        print web.input()['name']#得到表单中的name = 'name'元素的值，也可以这样访问：web.input().name；或先i = web.input()再访问:i.name
        print web.data()#得到表单提交的所有值，返回形式如：title=title_name&name=add_name&age=24
        raise web.seeother('/')#转移到首页

def nf():
    return web.notfound("胡祀鹏 提示：Sorry, the page you were looking for was not found.")

def ine():
    return web.internalerror("胡祀鹏 提示：Bad, bad server. No donut for you.")

def webpy_run(msg):
    print msg
    webpy_app = web.application(urls,globals())
    webpy_app.notfound = nf#自定义未找到页面
    webpy_app.internalerror = ine#自定义 500 错误消息
    webpy_app.run()
    print 'webpy bay!'
