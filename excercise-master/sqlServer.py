# -*- coding:utf-8 -*-
__author__ = 'IanChen'

import pymssql
#
# conn = pymssql.connect(host='39.108.1.170', port='3433', user='Python', password='pl,okmPL<OKM',
#                        database='PythonCenter',  autocommit=True,charset='utf8')

# cur = conn.cursor()
# if not cur:
#     raise Exception("数据库连接失败")
# #存储过程方式存储
# str='[dbo].[Python_Serivce_DSTaxApplyShenZhen_Add]'
# param=(100, 542, 3, 4, 5, '10024417000028987665', '《城建税、教育费附加、地方教育附加税（费）申报表》', '城市维护建设税', '0.00', '网络申报', '2017-10-18', '2017-07-01', '2017-09-30', 14)
# cur.callproc(str, param)
# conn.commit()
#
# cur.close()

#连接python_service
conn = pymssql.connect(host='39.108.1.170', port='3433', user='Python', password='pl,okmPL<OKM',
                       database='ACT18282900', autocommit=True,charset='utf8')
cur = conn.cursor()

sql3='[dbo].[Python_Serivce_Job_Error]'
# params = (18282900, pymssql.output(str,''))

params3=("1513", 4, 5, 1,'wancheng')
foo = cur.callproc(sql3, params3)
print(foo[-1])
conn.close()

#连接company service
# conn = pymssql.connect(host='39.108.1.170', port='3433', user='Python', password='pl,okmPL<OKM',
#                        database='CompanyCenter', autocommit=True,charset='utf8')
# cur = conn.cursor()
# sql = "[dbo].[Platform_Company_GetDBUrl]"
# params = (18282900, pymssql.output(str,''))
# foo = cur.callproc(sql, params)
# jdbc=foo[-1]
# print(jdbc)
# import re
# match=re.search(r'jdbc:sqlserver://(.*?):(\d+);database=(.*)',jdbc)
# print(match.group(1),match.group(2),match.group(3))
# conn.close()