import sys
import os
cwd = os.getcwd()
sys.path.append('src')

from og_mysql.wrapper import DatabaseWrapper
from og_log import LOG

class MyDatabase(DatabaseWrapper):

    TABLE_JOB_SUMMARY = 'TABLE0'

    DatabaseWrapper.TABLES[TABLE_JOB_SUMMARY] = (
        "CREATE TABLE `"+TABLE_JOB_SUMMARY+"` ("
        "  `name` char(64) NOT NULL,"    
        "  `target` char(64) NOT NULL,"    
        "  `comment` varchar(256) DEFAULT NULL,"    
        "  PRIMARY KEY (`name`)"
        ") ENGINE=InnoDB")



if __name__ == "__main__":

    LOG.start()

    db = MyDatabase(('172.16.2.3',43306),'testdb','testuser','testuser')
    LOG.info("Connected to database : "+str(db.is_connected()))

    l = db.show_tables()
    LOG.info(db.show_tables())

    db.drop_table(l[0])
    LOG.info(db.show_tables())





