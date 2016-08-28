#-*- coding: utf-8 -*-

import json
import pymysql # 导入pymysql驱动

'''
需要读取 static_type.py 保存得到的 static_movie.json 统计类型数据.

将数据存入mysql数据库 douban_movie 的 movie 表中.
        mysql> select * from movie;
        +------+------+
        | type | num  |
        +------+------+
        | 传记 |   32 |
        | 儿童 |    6 |
        .
        .
        | 运动 |    5 |
        | 音乐 |   13 |
        | 鬼怪 |    1 |
        +------+------+
'''

def saveDataIntoDb(temp_data):
    # 连接数据库, douban_movie 之前就创建好了的
    conn = pymysql.connect(user='root', password='123456', database='douban_movie', charset='utf8')
    # 获取游标 
    cursor = conn.cursor()

    cursor.execute("alter database douban_movie default character set utf8;")

    # # conn.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')

    # 创建 movie 表格
    cursor.execute('create table movie(type char(20) primary key, num int)')

    for name in temp_data.keys():
        # 插入数据到 movie 中，注意mysql的占位符是%s
        cursor.execute('insert into movie(type, num) values (%s, %s)', [name, temp_data[name]])
        print(cursor.rowcount)

    
    # 提交事务
    conn.commit()
    # 关闭游标
    cursor.close()


    # 重新获取游标
    # cursor = conn.cursor()
    # # 执行select查询，筛选id = 1的数据
    # cursor.execute('select * from user where id = %s', ['1'])
    # # fetcahall访问游标数据
    # values = cursor.fetchall()
    # print(values)
    # cursor.close()
    # conn.close()


if __name__ == '__main__':

    with open('static_movie.json', 'r') as f:
        a_dict = json.load(f)

    print(a_dict)

    saveDataIntoDb(a_dict)
