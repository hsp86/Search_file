#-*- coding: utf-8 -*-

# 指定数据库文件名
dbfile = "dir.db"

# 指定webpytemplate目录
temp_dir = r'template/'

# 设置是否支持utf-8外的其它编码：
# 设置为True则考虑gb2312编码，其实就是将非utf-8当做gb2312编码；
# 设置为False则所有文件都当做utf-8编码，这样效率较高，
# 但是这样gb2312编码文件时乱码，且其中的中文无法被搜索到
other_encoding = False # True

# 指定返回的搜索结果的多少：
# span_before指定搜索字符之前返回多少个字符；
# span_after指定搜索字符之后返回多少个字符。
# span_before和span_after较小时返回数据更小，占用流量较小
span_before = 30
span_after = 40
