# coding=utf-8
# -*- coding: utf-8 -*-
import MySQLdb as mdb
import web
import os
import sys
import json
urls = (
    '/img', 'UploadImage',
    '/hello','hello_1',
    '/query_req','query_req',
    '/piv','piv_register',
    '/img_back','back_img',
    '/deldata','deldata',
	'/nowa','nowa'
)

app = web.application(urls, globals())
count = 0


def float123(str1):
    return float(str1)
	
class nowa:
	def GET(self):
		return 'hello world'

class deldata:
    def GET(self):
        id1=int(web.input().id.encode("utf-8"))
        try:
            db = mdb.connect(host='104.129.180.80', port=3306, user='test', passwd='yang2900', db='piv', charset='utf8')
            print db
        except:
            print 'connect db error'
        cursor = db.cursor()
        sql2="delete from piv_usr where id='%d'"%(id1)
        print sql2
        try:
            cursor.execute(sql2)
            db.commit()
            
            return  'delete complete'        
           
        except:
            print "programme wrong"
        db.close()
        return "delete  OK! "


class piv_register:
    def POST(self):
        try:
            db = mdb.connect(host='104.129.180.80', port=3306, user='test', passwd='yang2900', db='piv', charset='utf8')
            print db
        except:
            print 'connect db error'
        try:
            usr_info=web.input()
            name=usr_info.name.encode("utf-8")
            pwd=usr_info.pwd.encode("utf-8")
            vip=int(usr_info.vip.encode("utf-8"))
        except:
            print 'Wrong input please input Integer!'
            return 'Wrong input please input Integer!'

        cursor = db.cursor()
        sql="insert into piv_usr(name,password,vip) values ('%s','%s','%d')" %(name,pwd,vip)
        sql2="select * from piv_usr where name='%s'"%(name)
        print sql2
        try:
            cursor.execute(sql)
            cursor.execute(sql2)
            db.commit()
            results = cursor.fetchall()
            print results
            for row in results:
                id = row[0]
                name = row[1]
                password = row[2]
                vip = row[3]
            print "id=%d,name=%s,password=%s,vip=%s" % (id,name.encode("utf-8"),password,vip)
        #     # data={"id":id,"name":name,"password":password,"vip":vip}
        #     # datajson.update(id)
            
        except:
            db.rollback()
            db.close()
        id=str(id)
        id='uin='+id
       
        return id

class UploadImage:
    def POST(self):
        # i = web.input()
        # a=i.a
        # print a
        # b=i.b
        # print b
        # return int(a)+int(b)
        # print(i)
        # d=i['attachment_file']
        # filename = 'pragramming.jpeg'
        # file1=open(filename,'w')
        # file1.write(d)
        # return 'programme ok'
        #!/usr/bin/python
        try:
            fin = open("/Users/leo/Downloads/IMG_6722.JPG")
            img = fin.read()
            fin.close()

        except IOError, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        try:
            conn = mdb.connect(host='104.129.180.80',port=3306,user='test',
            passwd='yang2900', db='piv')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Images SET Data='%s'" % \
            mdb.escape_string(img))
            conn.commit()
            cursor.close()
            conn.close()

        except mdb.Error, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        return 'programme ok'

        

class hello_1:
    def GET(self):
        name=web.input()
        try:
             bobi=name.bobi
             print bobi
            
        except :
            print 'no bobi string received'
        try:
            beichu=float123(name.beichu)
            print beichu
            chushu=float123(name.chushu)

            print chushu
            if float123(name.chushu)==0:
                return 'beichu cannot be zero'
        except:
            return 'you should input number'
        return beichu/chushu

class query_req:
   
    def GET(self):
        try:
            db = mdb.connect(host='127.0.0.1', port=3306, user='test', passwd='yang2900', db='piv', charset='utf8')
            print db
        except:
            print 'connect db error'
        cursor = db.cursor()
        sql2="select * from piv_usr"
        print sql2
        try:
            cursor.execute(sql2)
            db.commit()
            results = cursor.fetchall()
            datajson=[]
            for row in results:
                id = row[0]
                name = row[1]
                password = row[2]
                vip = row[3]
            # print "id=%d,name=%s,password=%s,vip=%s" % (id,name,password,vip)
                data={"id":id,"name":name,"password":password,"vip":vip}
                datajson.append(data)
            json_str=json.dumps(datajson)
            return  json_str          
           
        except:
            print "programme wrong"
        db.close()
    
       
        return "ok is good"

class back_img:
    def POST(self):
        try:
            conn = mdb.connect(host='104.129.180.80',user='test', 
            passwd='yang2900', db='piv')
            cursor = conn.cursor()
            cursor.execute("SELECT Data FROM Images where id=2")
            fout = open('image.png','wb')
            fout.write(cursor.fetchone()[0])
            fout.close()
            cursor.close()
            conn.close()

        except IOError, e:
            print "Error %d: %s" % (e.args[0],e.args[1])
            sys.exit(1)
        return 'programme ok!'



if __name__ == "__main__":
    app.run()
