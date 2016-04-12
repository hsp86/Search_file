# Search_file
实现通过关键字搜索文件内容

主要想用于快速查找之前做的笔记，所以建立此工程。

选择使用python实现，分为控制设置界面和web界面；分别用wxPython和webpy实现。
设置界面用于设置可搜索文件夹功能；web界面主要用于搜索，有全面的搜索功能。


需要安装的python库：
>Python 2.7.10
>wxPython3.0-3.0.2.0-py27
>webpy 0.37
>chardet-2.3.0
>py2exe-0.6.9（可选）

windows系统安装py2exe后可在dos下进入本工程目录运行：
python get_exe.py py2exe

即可生成exe文件，之后可用 .\exe\dist\search.exe运行

运行时可指定端口号，如下指定为80端口，否则默认端口为8080端口：
python search.py 80
