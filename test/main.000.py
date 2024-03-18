import sys
import os
cwd = os.getcwd()
sys.path.append('src')

from og_mysql.wrapper import DatabaseWrapper
from og_log import LOG


if __name__ == "__main__":

    LOG.start()

    db = DatabaseWrapper(('172.16.2.3',43306),'testdb','testuser','testuser')
    LOG.info("Connected to database : "+str(db.is_connected()))
    LOG.info("Disconnect : "+str(db.disconnect())) 
    LOG.info("Connected to database : "+str(db.is_connected()))
    LOG.info("Reconnect : "+str(db.reconnect()))
    LOG.info("Connected to database : "+str(db.is_connected()))

