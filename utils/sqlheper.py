__author__ = "Administrator"

import pymysql

def get_list(sql,args):

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
    cursor.execute(sql,args)  # 执行SQL语句,班级信息
    result = cursor.fetchall()  # 获取数据传递给此变量
    cursor.close()  # 关闭光标对象
    conn.close()
    return result

def get_one(sql,args):

    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
    cursor.execute(sql,args)  # 执行SQL语句,班级信息
    result = cursor.fetchone()  # 获取数据传递给此变量
    cursor.close()  # 关闭光标对象
    conn.close()
    return result

def modify(sql,args):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='667596', db="data1",charset="utf8")  # 连接database
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)  # 得到一个可以执行SQL语句的光标对象
    cursor.execute(sql,args)  # 执行SQL语句,班级信息
    conn.commit()
    cursor.close()  # 关闭光标对象
    conn.close()