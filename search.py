#-*- coding: utf-8 -*-

import threading
import webpy_main,wx_main

if __name__ == '__main__':
    webpy_thread = threading.Thread(target=webpy_main.webpy_run,args=('webpy start\n',))
    wx_thread = threading.Thread(target=wx_main.wx_run,args=('wx start\n',))
    webpy_thread.start()
    wx_thread.start()

