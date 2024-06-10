'''
Created on 7 mar. 2024
@author: vagrant
'''
#from dbconnection import Conn 
from .connPOO import Conn
from .geometryChecks import checkIntersection, checkDistance


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
        r = checkIntersection('d.streets', 'd.parks', geometryWKT, 25830)
        if r:
            return {'ok':False, 'message': 'La calle intersecta con otra calle o un parque', 'data':[]}
        
        r = checkDistance('d.streets', 'd.parks', geometryWKT, 25830)
        if r:
            return {'ok':False, 'message': 'La calle esta muy cerca o demasiado lejos de otra entidad', 'data':[]}
        

        #Insertion
        query = """
                INSERT INTO d.streets (nombre, tipo, ncarril, longitud, geom)
                VALUES (%s, %s, %s, st_length(st_geometryfromtext(%s,25830)), st_geometryfromtext(%s,25830))
                RETURNING gid"""
        
        self.conn.cursor.execute(query, [nombre, tipo, ncarril, geometryWKT, geometryWKT])
        self.conn.conn.commit()

        #List of gid inserted
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True, 'message': f'Carretera insertada. gid: {gid}', 'data':[{'gid':gid}]}
        
            
    
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
            return {'ok':False, 'message': 'La calle intersecta con otra', 'data':[]}
        
        r = checkDistance('d.streets', geometryWKT, 25830)
        if r:
            return {'ok':False, 'message': 'La calle esta muy cerca de otra o demasiado lejos', 'data':[]}
        
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
            return {'ok':False, 'message': 'Carreteras actualizadas: 0', 'data':[]}
        elif n==1:
            return {'ok':True, 'message': f'Carretera actualizada. Filas afectadas : {n}', 'data':[{'numOfRowsAffected':n, 'gid':gid}]}
        elif n > 1:
            return {'ok':False, 'message': f'Demasiadas carreteras actualizadas. Filas afectadas : {n}', 'data':[{'numOfRowsAffected':n}]}
        
    
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
            return {'ok':False, 'message': 'Cero carreteras borradas', 'data':[]}
        elif n == 1:
            return {'ok':True, 'message': f'Carretera borrada. Filas afectadas : {n}', 'data':[{'numOfRowsAffected':n, 'gid':gid}]}
        elif n > 1:
            return {'ok':False, 'message': f'Demasiadas carreteras borradas. Filas afectadas : {n}', 'data':[{'numOfRowsAffected':n}]}
        

    def select(self, gid=None) -> dict:
        """select by gid as dictionary"""
        if gid:
            query = """
                    SELECT array_to_json(array_agg(registros)) FROM (
                        SELECT gid, nombre, tipo, ncarril, longitud, st_astext(geom) as geometry_text, st_asgeojson(geom) as geometry_json, st_astext(geom) as geometry_text
                        FROM d.streets
                        WHERE gid = %s) AS registros
                    """
            self.conn.cursor.execute(query, [gid])
            #Output
            l = self.conn.cursor.fetchall()
            r = l[0][0]
            if r is None:
                return {'ok':False, 'message': 'Carreteras seleccionadas: 0', 'data':[]}
            else:
                n = len(r)
                return {'ok':True, 'message': f'Carreteras seleccionadas: {n}', 'data':r} 
        
        if gid is None:
            """Select all records as dictionary"""
            query = """
                    SELECT array_to_json(array_agg(registros)) FROM (
                        SELECT gid, nombre, tipo, ncarril, longitud, st_astext(geom) as geometry_text, st_asgeojson(geom) as geometry_json, st_astext(geom) as geometry_text
                        FROM d.streets
                        ) AS registros
                    """
            self.conn.cursor.execute(query)
            #Output
            l = self.conn.cursor.fetchall()
            r = l[0][0]
            if r is None:
                return {'ok':False, 'message': 'Carreteras seleccionadas: 0', 'data':[]}
            else:
                n = len(r)
                return {'ok':True, 'message': f'Carreteras seleccionadas: {n}', 'data':r}
        


    def select_xy(self, x, y) -> dict:
        """select by x,y click in map as dictionary"""
        
        #Intersect or within 1m
        query = """
                SELECT array_to_json(array_agg(registros)) FROM (
                    SELECT gid, nombre, tipo, ncarril, longitud, st_astext(geom) as geometry_text, st_asgeojson(geom) as geometry_json, st_astext(geom) as geometry_text
                    FROM d.streets
                    WHERE ST_Intersects(geom, ST_SetSRID(ST_Point(%s, %s),25830)) OR ST_DWithin(geom, ST_SetSRID(ST_Point(%s, %s),25830), %s))
                    AS registros
                """
        self.conn.cursor.execute(query, [x,y,x,y,50])
        
        #Output
        l = self.conn.cursor.fetchall()
        r = l[0][0]
        if r is None:
            return {'ok':False, 'message': 'Carreteras seleccionadas: 0', 'data':[]}
        else:
            n = len(r)
            return {'ok':True, 'message': f'Carreteras seleccionadas: {n}', 'data':r}
