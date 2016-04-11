#-*- coding: utf-8 -*-
import web
import sys,os
import sqlite3
import re

import config
dbfile = config.dbfile
temp_dir = config.temp_dir

# reload(sys)#支持中文
# sys.setdefaultencoding('utf8')

urls = (
    '/','index',
    '/search','search',
    '/open_file','open_file'
    )

render = web.template.render(temp_dir)

config.search_list = [] # 保存所有要搜索的绝对路径，将search_list放到config模块，直接用全局变量则不对

# 重新加载目录，更新search_list
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

# 从指定目录（path）中所有文件中搜索内容（search_text）
def search_file(search_text,path):
    res = []
    files = os.listdir(path)
    pattern = re.compile(search_text)
    for f in files:
        file_str = ""
        res_item = {}
        path_file = path + '/' + f
        if(os.path.isfile(path_file)):
            try:
                fid = open(path_file)
                file_str = fid.read()#后面搜索字符不decode这里也不用.decode('utf-8') # 搜索前将读取的内容以utf-8解码
            except:
                print u"读取文件失败!",path_file
                continue
            finally:
                fid.close()
            s = pattern.search(file_str)
            if s != None:
                start_index = 0 # 判断是否超出文件首末
                end_index = len(file_str)
                if start_index < s.span()[0] - 10:
                    start_index = s.span()[0] - 10
                if end_index > s.span()[1] + 20:
                    end_index = s.span()[1] + 20
                res_item[path_file] = file_str[start_index:end_index] # 最多截取搜索到的文本的前10后20个字符
                print res_item,start_index,end_index,len(file_str)
                res.append(res_item)
    return res

# 将上面搜索到的结果转换为html返回
def trans2html(search_re):
    res = ""
    for item in search_re:
        for key in item: # 返回给网页的内容要以utf-8编码，但是item[key]加.encode('utf-8')反而出错；避免搜索结果中有html标签，所以替换<为&lt;等
            res = res +  '''
                <div class="result_item">
                    <div class="item_fname">''' + key.encode('utf-8').replace("<","&lt;").replace(">","&gt;") + '''</div>
                    <div class="item_fcontent">''' + item[key].replace("<","&lt;").replace(">","&gt;") + '''</div>
                </div>
                '''
    return res

class search:
    def GET(self):
        get_data = web.input(search_text={},dir=[])
        get_str = get_data.search_text # 搜索字符
        print get_str
        re_html = ""
        for item in get_data.dir:
            re_html = re_html + trans2html(search_file(get_str,item)) # 不用.decode('utf-8')也行
        if re_html == "":
            re_html = '''
                <div class="result_item">
                    <div class="item_fname">在所选目录中没有找到包含搜索文本的文件</div>
                    <div class="item_fcontent">没有搜索到搜索文本</div>
                </div>'''
        return re_html

class open_file:
    """实现打开文件，并返回文件内容"""
    def GET(self):
        get_data = web.input(file_name={})
        f_name = get_data.file_name.decode('utf-8') # 测试所得，要支持中文文件名必须decode（疑问：上面的目录即使有中文不用decode也行？）
        if os.path.isfile(f_name):
            try:
                fid = open(f_name)
                file_str = fid.read()
            except:
                file_str = "文件打开失败！"
                print file_str
            finally:
                fid.close()
        else:
            return u"文件不存在！"
        return file_str.replace("<","&lt;").replace(">","&gt;") # 转换html特殊字符

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
