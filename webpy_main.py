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
    for f in files:
        path_file = path + '/' + f
        if(os.path.isfile(path_file)):
            try:
                fid = open(path_file)
                file_str = fid.read().decode('utf-8') # 搜索前将读取的内容以utf-8解码
            except:
                print u"当前只支持utf-8的文件！"
                continue
            finally:
                fid.close()
            pattern = re.compile(search_text)
            s = pattern.search(file_str)
            if s != None:
                res_item = {}
                start_index = 0; # 判断是否超出文件首末
                end_index = len(file_str);
                if start_index < s.span()[0] - 10:
                    start_index = s.span()[0] - 10
                if end_index > s.span()[1] + 20:
                    end_index = s.span()[1]
                res_item[path_file] = file_str[start_index:end_index] # 截取搜索到的文本的前后10个字符
                # print res_item,start_index,end_index
                res.append(res_item)
    return res

# 将上面搜索到的结果转换为html返回
def trans2html(search_re):
    res = ""
    for item in search_re:
        for key in item: # 返回给网页的内容要以utf-8编码
            res = res +  '''
                <div class="result_item">
                    <div class="item_fname">''' + key.encode('utf-8') + '''</div>
                    <div class="item_fcontent">''' + item[key.encode('utf-8')] + '''</div>
                </div>
                '''
    return res

class search:
    def GET(self):
        get_data = web.input(search_text={},dir=[])
        get_str = get_data.search_text.decode('utf-8') # 从网页接收的内容以utf-8解码，在用于搜索
        print get_str
        re_html = ""
        for item in get_data.dir:
            re_html = re_html + trans2html(search_file(get_str,item.decode('utf-8')))
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
        if os.path.isfile(get_data.file_name):
            try:
                fid = open(get_data.file_name)
                file_str = fid.read()
            except:
                file_str = "文件打开失败！"
                print file_str
            finally:
                fid.close()
        else:
            return u"文件不存在！"
        return file_str

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
