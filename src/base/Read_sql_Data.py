# encoding=utf-8
import pymysql
from src.base.URL_link import *
import base64


class Read_sql_Data(object):
    # def __init__(self):
    #     self.user = 'root'

    @classmethod
    def Conte(self, host,passwd, port, sql):
        # connectin = pymysql.Connect(host=host, database=database, user=self.user, password=passwd,
        #                             port=port, charset='utf8mb4')

        connectin = pymysql.Connect(host=host, user='root', password=passwd,
                                    port=port, charset='utf8mb4')

        print(sql)
        c = connectin.cursor()
        c.execute(sql)
        name = c.fetchall()  # 读取数据数据
        list1 = []
        for psl in name:
            list1.append(psl)
        # print(list1)
        return list1
        connectin.close()

# if __name__ == '__main__':
#     url=URL_link()
#     rsd = Read_sql_Data()
#     sql2 = "select id from rdp_system.r_user "
#     list1 = Read_sql_Data.Conte(url.HOST,url.PASSWD, url.PORT, sql2)
