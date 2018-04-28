# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class BossjobPipeline(object):
    def open_spider(self,spider):
        # 连接数据库
        host=spider.settings.get('MYSQL_HOST')
        port=spider.settings.get('MYSQL_PORT')
        db=spider.settings.get('MYSQL_DBNAME')
        user=spider.settings.get('MYSQL_USER')
        passwd=spider.settings.get('MYSQL_PASSWD')
        # 通过cursor执行增删查改
        self.conn=pymysql.connect(host=host,port=port,db=db,user=user,passwd=passwd,charset='utf8',use_unicode=False)
        self.cur = self.conn.cursor()

    def process_item(self, item, spider):
        self.insert(item)
        return item
    def insert(self,item):
        for i in range(0, len(item["jobTitle"])):
            jobTitle=item['jobTitle']
            jobSalary=item['jobSalary']
            jobCompany=item['jobCompany']
            jobPublish=item['jobPublish']
            sql = '''INSERT INTO job(jobTitle,jobSalary,jobCompany,jobPublish) VALUES(%s,%s,%s,%s)'''
        try:
            # 插入数据
            self.cur.execute(sql,(jobTitle,jobSalary,jobCompany,jobPublish))
        except Exception as error:
            return False
            # # 出现错误时打印错误日志
            # log(error)
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()
