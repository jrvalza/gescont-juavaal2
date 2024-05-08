'''
Created on 27 feb. 2024

@author: vagrant
'''
import psycopg2
from django.db import connection as conn

class Conn():
    conn=None
    cursor=None
    def __init__(self):
        self.conn=conn
        self.cursor=self.conn.cursor()
        
    def close(self):
        self.conn.close()
