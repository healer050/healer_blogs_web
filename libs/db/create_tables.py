#coding=utf-8
from libs.db.dbsession import engine
from models.admin_models import Base

#将创建好的类，映射到数据库的表中
def run():
    print '------------table_create_start-------------'
    Base.metadata.create_all(engine)
    print '------------table_create_end-------------'

if __name__ == "__main__":
    run()