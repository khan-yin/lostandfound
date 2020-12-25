'''
author: feifei
date: 2020-12-24
file info: 更新数据库
'''

from pymysql import connect

pwd = "12345678"


def Update(**kwargs):
    '''

    :param kwargs:
        openid
        truename
        college
        cardNumber
        phoneNumber
        qqNumber
        email
    :return:
    '''

    conn = connect(host='localhost', user='root', password=pwd, port=3306, database='lof', charset='utf8')
    cursor = conn.cursor()

    try:
        count = cursor.execute("""select * from student where openid='%s';""" % kwargs.get('openid'))

        if count:
            temp = cursor.fetchone()
            # 默认不修改
            truename = temp[2]
            college = temp[3]
            cardNumber = temp[4]
            phoneNumber = temp[5]
            qqNumber = temp[6]
            email = temp[7]

            if kwargs.get('truename') != '' and truename != kwargs.get('truename'):
                truename = kwargs.get('truename')
            if kwargs.get('college') != '' and college != kwargs.get('college'):
                college = kwargs.get('college')
            if kwargs.get('cardNumber') != '' and cardNumber != kwargs.get('cardNumber'):
                cardNumber = kwargs.get('cardNumber')
            if kwargs.get('qqNumber') != '' and qqNumber != kwargs.get('qqNumber'):
                qqNumber = kwargs.get('qqNumber')
            if kwargs.get('phoneNumber') != '' and phoneNumber != kwargs.get('phoneNumber'):
                phoneNumber = kwargs.get('phoneNumber')
            if kwargs.get('email') != '' and email != kwargs.get('email'):
                email = kwargs.get('email')

            cursor.execute("""update student set truename='%s', college='%s', cardNumber='%s', 
            qqNumber='%s', phoneNumber='%s', email='%s' where openid = '%s';"""
                           % (truename, college, cardNumber, qqNumber, phoneNumber, email, kwargs.get('openid')))
            # 关闭游标
            cursor.close()
            conn.commit()

    except Exception as e:

        cursor.close()
        # 事务回滚
        conn.rollback()

    # 关闭数据库
    conn.close()

    #     return HttpResponse(json.dumps({'msg': '修改成功'}), status=200)
    # except Exception:
    # return HttpResponse(json.dumps({'msg': '修改失败'}), status=404)


# 查找student表中指定openid的行并返回字典型行数据
def Search_By_Openid(openid):
    conn = connect(host='localhost', user='root', password=pwd, port=3306, database='lof', charset='utf8')
    cursor = conn.cursor()
    count = cursor.execute("""select * from student where openid='%s';""" % openid)

    data = {}
    if count:
        temp = cursor.fetchone()
        data = {
            'truename': temp[2],
            'college': temp[3],
            'cardNumber': temp[4],
            'phoneNumber': temp[5],
            'qqNumber': temp[6],
            'email': temp[7]
        }

    return data


# 删除student指定id的数据
def Delete(id):
    conn = connect(host='localhost', user='root', port=3306, password=pwd, database='lof', charset='utf8')
    cursor = conn.cursor()

    try:
        count = cursor.execute("""select * from event where id='%s';""" % id)
        if count:
            cursor.execute("""delete from event where id = '%s'; """ % id)

        cursor.close()
        conn.commit()

    except Exception as e:
        cursor.close()
        conn.rollback()

    conn.close()


# 改变event表中指定id的status状态
def ChangeSta(id):
    conn = connect(host='localhost', user='root', port=3306, password=pwd, database='lof', charset='utf8')
    cursor = conn.cursor()

    try:
        count = cursor.execute("""select * from event where id='%s';""" % id)
        if count:
            # 获取原status，status为str型，先将status转化为int型
            status = int(cursor.fetchone()[8])
            status = str(status + 1)
            cursor.execute("""update event set status='%s' where id = '%s';""" % (status, id))

        cursor.close()
        conn.commit()

    except Exception as e:
        cursor.close()
        conn.rollback()

    conn.close()


# 查找student表中指定cardNumber的行并返回字典型行数据
def Search_By_CardNumber(cardNumber):
    conn = connect(host='localhost', user='root', port=3306, password=pwd, database='lof', charset='utf8')
    cursor = conn.cursor()

    try:
        count = cursor.execute("""select * from student where cardNumber='%s';""" % cardNumber)
        data = {}
        if count:
            temp = cursor.fetchone()
            data = {
                'truename': temp[2],
                'phoneNumber': temp[5],
                'qqNumber': temp[6],
                'email': temp[7]
            }
        cursor.close()
        conn.commit()
    except Exception as e:
        cursor.close()
        conn.rollback()
    finally:
        conn.close()
        return data


if __name__ == '__main__':
    # Update(openid='oTdQp43pZDf2ZEeLvESb8-6-nWbs', truename='尹可汗',college='武汉理工大学',
    #        cardNumber='666666', qqNumber='321321', phoneNumber='123123', email='321321@qq.com')
    #
    # print(Search('oTdQp43pZDf2ZEeLvESb8-6-nWbs'))
    Delete(7)
    ChangeSta(122)
    print(Search_By_CardNumber(333333))
