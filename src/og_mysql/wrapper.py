import mysql.connector
from og_log import LOG

def try_raise(fct):
    def inner(*args,**kwargs):
        try: return fct(*args,**kwargs)
        except Exception as e: raise Exception(fct.__name__ +" exception : "+str(e))
    return inner

class DatabaseWrapper():
    TABLES = {}
    
    def __init__(self,host,database,user,password):
        self.cnx = None
        if self.connect(host,database,user,password):
            LOG.debug("Connected to database "+str(host))
            self._init_database()

    @try_raise
    def _init_database(self):
        table_list = self.show_tables()
        cursor = self.cnx.cursor()
        for table_name in DatabaseWrapper.TABLES:
            if table_name not in table_list:
                LOG.info("Table "+table_name+" not found, creating")
                self.execute(DatabaseWrapper.TABLES[table_name],cursor)
        cursor.close()
        
    @try_raise
    def execute(self,query,cursor=None):
        result = None
        if isinstance(query,str):
            sql = query
            data = None
        else:
            if len(query) < 1 or len(query) > 2: raise Exception("Invalid query : "+str(query))
            sql = query[0]
            data = None if len(query) == 1 else query[1]
        tcursor = self.cnx.cursor() if cursor is None else cursor
        if data is not None:
            LOG.debug("Execute SQL : "+str(sql)+" : "+str(data))
            tcursor.execute(sql,data)
        else:
            LOG.debug("Execute SQL : "+str(sql))
            tcursor.execute(sql)
        if cursor is None:
            result = tcursor.fetchall()
            self.cnx.commit()
            tcursor.close()
        return result

    @try_raise
    def is_connected(self):
        return self.cnx is not None and self.cnx.is_connected()

    @try_raise
    def connect(self,host,database,user,password):
        LOG.debug("Connecting to database "+str(host))
        if self.cnx is None:
            self.host = host
            self.database = database
            self.user = user
            self.password = password
            self.cnx = mysql.connector.connect(user=self.user,
                                            password=self.password,
                                            host=self.host[0],
                                            database=self.database,
                                            port=self.host[1])
            return self.is_connected()
        else:
            if not self.cnx.is_connected():
                return self.reconnect()

    @try_raise
    def close(self):
        LOG.debug("Closing connection to database")
        if self.cnx is None: return True
        self.cnx.close()
        self.cnx = None
        return not self.is_connected()

    @try_raise
    def reconnect(self):
        LOG.debug("Reconnecting database")
        if self.cnx is None: return False
        self.cnx.reconnect()
        return self.is_connected()

    @try_raise
    def disconnect(self):
        LOG.debug("Disconnecting database")
        if self.cnx is None: return True
        self.cnx.disconnect()
        return not self.is_connected()

    @try_raise
    def show_tables(self):
        return [ i[0] for i in self.execute("SHOW TABLES")]
                            
    @try_raise
    def drop_table(self,name):
        self.execute("DROP TABLE "+name)

