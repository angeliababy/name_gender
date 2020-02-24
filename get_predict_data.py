#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pymysql
import re

mysqlDict1 = {
    'host': '***',
    'port': ***,
    'user': '***',
    'passwd': '***',
    'db': '***',
    'charset': '***'
    }


def getMysqlConn(mysqlDict):
    conn = pymysql.connect(host = mysqlDict.get('host'),
                           port = mysqlDict.get('port'),
                           user = mysqlDict.get('user'),
                           passwd = mysqlDict.get('passwd'),
                           db = mysqlDict.get('db'),
                           charset = mysqlDict.get('charset')
                           )
    return conn

def getData(sql, connection):
    connection.ping(reconnect=True)
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
        connection.commit()
    finally:
        connection.close()

def getdatafromDB():

    sql = "select distinct id,nick_name,member_gender from tnaot_news_bz.member where member_gender in (0) and member_type != 3 and member_type != 10;"
    print(sql)
    conn = getMysqlConn(mysqlDict1)
    data = getData(sql, conn)

    return data


if __name__=="__main__":

    data = getdatafromDB()

    output = open('user_gender_predict.txt', 'w', encoding='utf-8')
    output.write('id' + ',' + 'gender' + ',' + 'lang' + ',' + 'name' + '\n')

    for i in data:
        # print(i[1])
        if i[1] == None:
            continue
        member_id = str(i[0])
        nick_name = i[1].strip()
        member_gender = str(i[2])

        lang_re = re.compile(r'[^\u4e00-\u9FBF\u1780-\u17ffa-zA-Z ]', re.S)
        nick_name_new = re.sub(lang_re, '', nick_name)

        # nick_name = re.sub("[.!//_,$&%^*()<>+\"'?@#-|:~{}\n]+|[——！\\\\，。=？、：“”‘’《》【】￥……（）]+", "", nick_name.strip())

        if len(nick_name_new) > 1 and len(re.findall('ID', nick_name_new)) == 0:
            if re.match("^[A-Za-z ]+$", nick_name):
                output.write(member_id + ',' + member_gender + ',' + '0' + ',' + nick_name_new + '\n')
            elif re.match("^[\u4e00-\u9FBF ]+$", nick_name):
                output.write(member_id + ',' + member_gender + ',' + '1' + ',' + nick_name_new + '\n')
            elif re.match("^[\u1780-\u17ff ]+$", nick_name):
                output.write(member_id + ',' + member_gender + ',' + '2' + ',' + nick_name_new + '\n')


