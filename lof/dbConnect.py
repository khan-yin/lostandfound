# -*- coding: utf-8 -*-

"""have a nice day.

@author: Khan
@contact:  
@time: 2020/12/23 23:32
@file: dbConnect.py
@desc:  
"""

import pymysql

user = "root"
password = "12345678"
database = 'lof'


# sql="SELECT VERSION()"

def dbConnect(user, password, database, sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", user, password, database)

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute()  方法执行 SQL 查询
    cursor.execute(sql)

    # 使用 fetchone() 方法获取单条数据.
    data = cursor.fetchone()

    print("Database version : %s " % data)

    # 关闭数据库连接
    db.close()


# dbConnect(user,password,database,sql)


def dbUpdate(user, password, database, sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", user, password, database)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # SQL 插入语句
    try:
        # 执行sql语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
    except:
        # 如果发生错误则回滚
        db.rollback()
    # 关闭数据库连接
    db.close()


def dbQuery(user, password, database, sql):
    # 打开数据库连接
    db = pymysql.connect("localhost", user, password, database)
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    try:
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        print(len(results))
        # db.commit()
        return results
    except Exception as e:
        # db.rollback()
        print(e)
        print("Error: unable to fetch data")
    # 关闭数据库连接
    db.close()


# class GETLOST(APIView):
#

def devide(photo):
    if photo is None:
        return []
    m = photo.split(';')
    print(m)
    com = []
    for i in range(len(m)):
        com.append(str(m[i]))
    print(com)
    return com


def getMsgsql(page, status):
    sql = "SELECT * FROM event WHERE status='%s' ORDER BY id DESC" % status
    result = dbQuery(user, password, database, sql)
    lenth = len(result)
    print(lenth)
    # print(len(result))
    page = 1
    # print(page)
    # print(lenth)
    comments = []
    if page * 5 > lenth:
        res = result[(page - 1) * 5:lenth]
    else:
        res = result[(page - 1) * 5:page * 5]
    # print(res)
    for one in res:
        com = {}
        com['id'] = one[0]
        # openid
        com['truename'] = one[2]
        com['text'] = one[3]
        com['photo'] = devide(one[4])
        com['time'] = one[5]
        com['phoneNumber'] = one[6]
        com['qqNumber'] = one[7]
        com['status'] = one[8]

        com['type'] = one[9]
        # iscard
        com['avatarURL'] = one[11]
        # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
        comments.append(com)
    print(comments)
    return comments
    # res = Response(comments)
    # print(type(res))
    # return Response(comments)


# getlostsql(1)

def getMyinfo(page, openid, info):
    # print(openid)
    if info == "find":
        sql = "select * from event where openid= '%s' and status in('1','2') order by id DESC " % openid
    elif info == "lost":
        sql = "select * from event where openid= '%s' and status in('3','4') order by id DESC " % openid
    # MYLOST.lenth = len(MYLOST.result)
    # print(MYLOST.result)
    result = dbQuery(user, password, database, sql)
    lenth = len(result)
    print(lenth)
    comments = []
    if page * 5 > lenth:
        res = result[(page - 1) * 5:lenth]
    else:
        res = result[(page - 1) * 5:page * 5]
    print("res:", res)
    for one in res:
        com = {}
        com['id'] = one[0]
        com['truename'] = one[2]
        com['text'] = one[3]
        com['photo'] = devide(one[4])
        com['time'] = one[5]
        com['phoneNumber'] = one[6]
        com['qqNumber'] = one[7]
        com['status'] = one[8]
        com['type'] = one[9]
        com['avatarURL'] = one[11]
        com['count'] = len(result)
        # print(one.id,one.name,one.message,one.date,one.time,one.emotion)
        comments.append(com)
    return comments
