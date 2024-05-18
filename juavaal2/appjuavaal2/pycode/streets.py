'''
Created on 7 mar. 2024
@author: vagrant
'''
#from dbconnection import Conn 
from .connPOO import Conn
from .geometryChecks import checkIntersection


class Streets():
    conn:Conn
    
    #Constructor
    def __init__(self, conn:Conn):
        self.conn = conn
      
    #User methods  
    def insert(self, data:dict) -> dict:
        #data to insert
        nombre = data['nombre']
        tipo = data['tipo']
        ncarril = data['ncarril']
        geometryWKT = data['geom']



        #Check geometry
        r = checkIntersection('d.streets', geometryWKT, 25830)
        if r:
            return {'Ok':False, 'Message': 'La calle intersecta con otra', 'Data':[]}
        

        #Insertion
        query = """
                INSERT INTO d.streets (nombre, tipo, ncarril, longitud, geom)
                VALUES (%s, %s, %s, st_length(st_geometryfromtext(%s,25830)), st_geometryfromtext(%s,25830))
                RETURNING gid"""
        
        self.conn.cursor.execute(query, [nombre, tipo, ncarril, geometryWKT, geometryWKT])
        self.conn.conn.commit()

        #List of gid inserted
        gid = self.conn.cursor.fetchall()[0][0]
        return {'Ok':True, 'Message': f'Carretera insertada. gid: {gid}', 'Data':[{'gid':gid}]}
        
            
    
    def update(self, data:dict) -> dict:
        """Update a Streets based in the gid"""
        #Row and data to update
        gid = data['gid']
        nombre = data['nombre']
        tipo = data['tipo']
        ncarril = data['ncarril']
        geometryWKT = data['geom']
        
        #Check geometry
        r = checkIntersection('d.streets', geometryWKT, 25830)
        if r:
            return {'Ok':False, 'Message': 'La calle intersecta con otra', 'Data':[]}
        
        #Update
        query = """
                UPDATE d.streets
                SET (nombre, tipo, ncarril, longitud, geom) = (%s, %s, %s, st_length(st_geometryfromtext(%s,25830)), st_geometryfromtext(%s,25830))
                WHERE gid = %s
                """

        self.conn.cursor.execute(query, [nombre, tipo, ncarril, geometryWKT, geometryWKT, gid])
        self.conn.conn.commit()
        
        #Number of rows updated
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'Ok':False, 'Message': 'Carreteras actualizadas: 0', 'Data':[]}
        elif n==1:
            return {'Ok':True, 'Message': f'Carretera actualizada. Filas afectadas : {n}', 'Data':[{'numOfRowsAffected':n}]}
        elif n > 1:
            return {'Ok':False, 'Message': f'Demasiadas carreteras actualizadas. Filas afectadas : {n}', 'Data':[{'numOfRowsAffected':n}]}
        
    
    def delete(self, gid:int) -> dict:
        """Deletes a Streets based in the gid"""
        #Delete
        query = """
                DELETE FROM d.streets
                WHERE gid = %s
                """
        self.conn.cursor.execute(query, [gid])
        self.conn.conn.commit()
        
        #Number of rows deleted
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'Ok':False, 'Message': 'Cero carreteras borradas', 'Data':[]}
        elif n == 1:
            return {'Ok':True, 'Message': f'Carretera borrada. Filas afectadas : {n}', 'Data':[{'numOfRowsAffected':n}]}
        elif n > 1:
            return {'Ok':False, 'Message': f'Demasiadas carreteras borradas. Filas afectadas : {n}', 'Data':[{'numOfRowsAffected':n}]}
        

    def select(self, gid=None) -> dict:
        """select by gid as dictionary"""
        if gid:
            query = """
                    SELECT array_to_json(array_agg(registros)) FROM (
                        SELECT gid, nombre, tipo, ncarril, longitud, st_astext(geom) as geometry_text, st_asgeojson(geom) as geometry_json 
                        FROM d.streets
                        WHERE gid = %s) AS registros
                    """
            self.conn.cursor.execute(query, [gid])
            #Output
            l = self.conn.cursor.fetchall()
            r = l[0][0]
            if r is None:
                return {'Ok':False, 'Message': 'Carreteras seleccionadas: 0', 'Data':[]}
            else:
                n = len(r)
                return {'Ok':True, 'Message': f'Carreteras seleccionadas: {n}', 'Data':r} 
        
        if gid is None:
            """Select all records as dictionary"""
            query = """
                    SELECT array_to_json(array_agg(registros)) FROM (
                        SELECT gid, nombre, tipo, ncarril, longitud, st_astext(geom) as geometry_text, st_asgeojson(geom) as geometry_json
                        FROM d.streets
                        ) AS registros
                    """
            self.conn.cursor.execute(query)
            #Output
            l = self.conn.cursor.fetchall()
            r = l[0][0]
            if r is None:
                return {'Ok':False, 'Message': 'Carreteras seleccionadas: 0', 'Data':[]}
            else:
                n = len(r)
                return {'Ok':True, 'Message': f'Carreteras seleccionadas: {n}', 'Data':r}
        

