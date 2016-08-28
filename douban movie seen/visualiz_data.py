# -*- coding: utf-8 -*-

import pymysql # 导入pymysql驱动
import numpy
import matplotlib.pyplot as mpl
import  matplotlib

'''
从数据库中读取数据，使用 matplotlib 可视化影片分类数据。
'''




# 连接数据库, douban_movie 之前就创建好了的
conn = pymysql.connect(user='root', password='123456', database='douban_movie', charset='utf8')
# 获取游标 
cursor = conn.cursor()

cursor.execute('select * from movie')
# fetcahall访问游标数据
result = cursor.fetchall()

print(type(result))

print(result)

category = []
num = []

for row in result:
    category.append(row[0])
    num.append(row[1])

# print(category)
# print(num)

# 解决中文显示问题
matplotlib.rcParams['font.sans-serif'] = ['SimHei'] #指定默认字体
matplotlib.rcParams['axes.unicode_minus'] = False #解决保存图像是负号'-'显示为方块的问题  


x_pos = numpy.arange(len(category))    # 定义x轴坐标数
mpl.bar(x_pos, num, align='center', alpha=0.4)  # alpha图表的填充不透明度(0~1)之间
mpl.xticks(x_pos, category, rotation='45') # 在x轴上做分类名的标记
    
for num, x_pos in zip(num, x_pos):
#     # 分类个数在图中显示的位置，就是那些数字在柱状图尾部显示的数字
    mpl.text(x_pos, num, num, horizontalalignment='center', verticalalignment='center', weight='bold')  
mpl.xlim(+28.0, -1.0) # 可视化范围，相当于规定y轴范围
mpl.title('我看过的电影'.encode('utf-8').decode('utf-8'))   # 图表的标题
mpl.xlabel('电影分类')     # 图表x轴的标记
mpl.subplots_adjust(bottom = 0.15) 
mpl.ylabel('分类出现次数')  # 图表y轴的标记
mpl.savefig('movie_seen.png')   # 保存图片