#-*- coding: utf-8 -*-
import wx
import os
import sqlite3

import config
dbfile = config.dbfile

class myapp(wx.App):
    def __init__(self):
        wx.App.__init__(self)#必须调用父类的构造函数__init__
    def OnInit(self):#在程序开始的时候就会被自动调用
        self.frame = myframe()
        self.frame.Show()#显示
        self.SetTopWindow(self.frame)
        return True#必须要返回True才会继续执行，返回False则退出程序
    
    
class myframe(wx.Frame):#自建窗口类
    def __init__(self):
        self.dir_list = {} # 以父目录分组保存期子文件夹名
        self.check_list = {} # 以父目录分组保存checkbox（子文件夹名）引用
        self.search_list = [] # 保存被选中的绝对路径

        wx.Frame.__init__(self,None,-1,u"文本搜索设置---胡祀鹏设计制作",size = (550,450))

        # 整个界面大sizer
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        
        # 输入框，显示浏览的目录
        self.dir_text = wx.TextCtrl(self,-1,u'请选择目录')
        # 浏览按钮
        self.dir_button = wx.Button(self,-1,u'浏览')
        self.dir_button.Bind(wx.EVT_BUTTON,self.dir_button_click)

        # 数据操作按钮
        self.add_button = wx.Button(self,-1,u'添加')
        self.add_button.Bind(wx.EVT_BUTTON,self.add_button_click)
        self.save_button = wx.Button(self,-1,u'保存')
        self.save_button.Bind(wx.EVT_BUTTON,self.save_button_click)
        self.open_button = wx.Button(self,-1,u'打开')
        self.open_button.Bind(wx.EVT_BUTTON,self.open_button_click)
        self.clear_button = wx.Button(self,-1,u'清除')
        self.clear_button.Bind(wx.EVT_BUTTON,self.clear_button_click)

        # 浏览部分sizer
        sizer1 = wx.FlexGridSizer(rows = 1,cols = 2,hgap = 2,vgap = 0)
        sizer1.AddGrowableCol(0,5)
        sizer1.AddGrowableCol(1,1)
        sizer1.Add(self.dir_text,0,wx.EXPAND)
        sizer1.Add(self.dir_button,0,wx.EXPAND)

        # 数据操作部分sizer
        sizer2 = wx.FlexGridSizer(rows = 1,cols = 4,hgap = 0,vgap = 0)
        sizer2.AddGrowableCol(0,1)
        sizer2.AddGrowableCol(1,1)
        sizer2.AddGrowableCol(2,1)
        sizer2.AddGrowableCol(3,1)
        sizer2.Add(self.add_button,0,wx.EXPAND)
        sizer2.Add(self.save_button,0,wx.EXPAND)
        sizer2.Add(self.open_button,0,wx.EXPAND)
        sizer2.Add(self.clear_button,0,wx.EXPAND)

        # 显示添加目录的sizer
        self.add_sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加以上两个sizer
        self.sizer.Add(sizer1,0,wx.EXPAND | wx.ALL,10)
        self.sizer.Add(sizer2,0,wx.EXPAND | wx.ALL,10)
        self.sizer.Add(self.add_sizer,1,wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT,5)

        self.SetSizer(self.sizer)

    # 显示目录为checkbox
    def show_dir(self,path):
        self.check_list[path] = []
        check_parent =wx.CheckBox(self,-1,path)
        self.add_sizer.Add(check_parent)
        check_parent.Bind(wx.EVT_CHECKBOX,self.check_parent_click)
        dir_col = 5
        dir_len = len(self.dir_list[path])
        sizer1 = wx.FlexGridSizer(rows = (dir_len/dir_col+1),cols = dir_col,hgap = 3,vgap = 3)
        for d in self.dir_list[path]:
            temp = wx.CheckBox(self,-1,d,name = (path+'\\'+d))#通过name保存本项的绝对路径
            temp.Bind(wx.EVT_CHECKBOX,self.checkbox_click)
            sizer1.Add(temp,0,wx.EXPAND)
            self.check_list[path].append(temp)
        self.add_sizer.Add(sizer1, 1, wx.EXPAND | wx.ALL, 5)
        self.sizer.Fit(self)

    # 从指定目录中扫描其中子目录
    def refresh_dir(self,path):
        self.dir_list[path] = []
        files = os.listdir(path)
        add_dir = []
        for f in files:
            if(os.path.isdir(path + '/' + f)):
                # 排除隐藏文件夹，并添加
                if(f[0] != '.'):
                    self.dir_list[path].append(f)
        self.show_dir(path)

    # 浏览打开一个目录
    def dir_button_click(self,e):
        dir_dlg = wx.DirDialog(None,u'请选择一个目录',style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
        if dir_dlg.ShowModal() == wx.ID_OK:
            self.dir_text.SetValue(dir_dlg.GetPath())
            self.refresh_dir(self.dir_text.GetValue())
        dir_dlg.Destroy()

    # 检查指定checkbox是否被选中或取消选中来从self.search_list中添加或删除本项
    def check_append(self,item):
        item_name = item.GetName()
        if item.IsChecked():
            if not item_name in self.search_list:
                self.search_list.append(item.GetName())# 保存本项的绝对路径到self.search_list
                print "added path:",item.GetName()
        else:
            if item_name in self.search_list:
                self.search_list.remove(item.GetName())
                print "removed path:",item.GetName()

    # checkbox点击后触发，并添加或删除对应项，最后打印出当前选中的项
    def checkbox_click(self,e):
        this_check = e.GetEventObject()# 得到当前点击的checkbox
        self.check_append(this_check)
        print "self.search_list now is :"# 遍历显示当前self.search_list内容
        for item in self.search_list:
            print item

    # 父目录checkbox被选中时触发，添加或删除本父目录的所有项
    def check_parent_click(self,e):
        this_check = e.GetEventObject()
        this_path = this_check.GetLabelText()
        for item in self.check_list[this_path]:
            item.SetValue(this_check.IsChecked())
            self.check_append(item)

    # 添加，在原数据库中添加
    def add_button_click(self,e):
        conn = sqlite3.connect(dbfile)#连接到文件，连接到内存用(":memory:")
        cur = conn.cursor()#创建游标
        cur.execute('''
                create table if not exists dir_db
                (dir_name text)
            ''')# 不存在dir_db时即新建
        for item in self.search_list:
            cur.execute("select * from dir_db where dir_name = '" + item + "'")# 用str(item)且有中文时出错
            row = cur.fetchone()
            if row == None:# 没有在表里才插入
                cur.execute('insert into dir_db values(?)',(item,))
                print "add ",item
        conn.commit()
        conn.close()
        print "add end!"

    # 保存，将self.search_list中数据保存到数据库，原数据库中数据不要了
    def save_button_click(self,e):
        conn = sqlite3.connect(dbfile)#连接到文件，连接到内存用(":memory:")
        cur = conn.cursor()#创建游标
        cur.execute('''
                create table if not exists dir_db
                (dir_name text)
            ''')# 不存在dir_db时即新建
        cur.execute("delete from dir_db")# 保存时先删除
        for item in self.search_list:
            cur.execute('insert into dir_db values(?)',(item,))
            print "save ",item
        conn.commit()
        conn.close()
        print "save end!"

    # 打开，从数据库里读取到self.search_list
    def open_button_click(self,e):
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
            if not row_name in self.search_list:# 该项不在self.search_list中才加入self.search_list
                self.search_list.append(row_name)
                print "open ",row_name
            row = cur.fetchone()
        print "open over!"
        conn.commit()
        conn.close()

    # 清除，只清除self.search_list不会清除数据库，要清除数据要先“清除”后“保存”即可
    def clear_button_click(self,e):
        self.search_list = []
        print "clear over!save to clear db"


def wx_run(msg):
    print msg
    wx_app = myapp()
    wx_app.MainLoop()
    print 'wx bay!'
