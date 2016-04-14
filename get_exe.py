#coding:utf-8

from distutils.core import setup
import py2exe

# bundle_files有效值为：
#   3 (默认)不打包。
#   2 打包，但不打包Python解释器。
#   1 打包，包括Python解释器。
options = {"py2exe":{"compressed": 1, #压缩
                    "optimize": 2, 
                    "bundle_files": 3 #所有文件打包成一个exe文件 
                    }
            }

# setup(console=["search.py"],options=options,zipfile=None) # 64位系统不支持，所以不用
setup(console=["search.py"])

# 以下移动生成的文件
import shutil
import os

import config
temp_dir = config.temp_dir

dest_dir = r"./exe" # 生成exe文件要放入的目标目录
dest_build = dest_dir + r'/build'
dest_dist = dest_dir + r'/dist'

if os.path.isdir(dest_build): # 目标目录存在需要先删除，否则导致复制出错
    shutil.rmtree(dest_build)
if os.path.isdir(dest_dist):
    shutil.rmtree(dest_dist)

shutil.copytree(r'./build',dest_build)
shutil.copytree(r'./dist',dest_dist)
shutil.copytree(r'./' + temp_dir,dest_dist + r'/' + temp_dir)
shutil.copytree(r'./static',dest_dist + r'/static')

shutil.rmtree(r'./build')
shutil.rmtree(r'./dist')

# 最后运行dest_dist + r'/search.exe'即可

# console windows
# 然后按下面的方法运行:
# python get_exe.py py2exe