'''
Created on 7 mar. 2024
@author: vagrant
'''

#from dbconnection import Conn 
from .connPOO import Conn
from .geometryChecks import checkIntersection, checkDistance

class Parks():
    conn:Conn
    
    #Constructor
    def __init__(self, conn:Conn):
        self.conn = conn
      
    #User methods  
    def insert(self, data:dict) -> dict:
        #data to insert
        nombre = data['nombre']
        descripcion = data['descripcion']
        geometryWKT = data['geom']

        #Check geometry
        r = checkIntersection('d.parks', 'd.streets', geometryWKT, 25830)
        if r:
            return {'ok':False, 'message': 'El parque intersecta con otro o con una calle', 'data':[]}

        
        r = checkDistance('d.parks', 'd.streets', geometryWKT, 25830)
        if r:
            return {'ok':False, 'message': 'El parque esta muy cerca o demasiado lejos de otra entidad', 'data':[]}
    

        #Insertion
        query = """
                INSERT INTO d.parks (nombre, descripcion, xcoord, ycoord, geom)
                VALUES (%s, %s, st_x(st_geometryfromtext(%s,25830)), st_y(st_geometryfromtext(%s,25830)), st_geometryfromtext(%s,25830))
                RETURNING gid"""
        self.conn.cursor.execute(query, [nombre, descripcion, geometryWKT, geometryWKT, geometryWKT])
        self.conn.conn.commit()

        #List of gid inserted
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True, 'message': f'Parque insertado. gid: {gid}', 'data':[{'gid':gid}]}
    
    
    def update(self, data:dict) -> dict:
        """Update a Parks based in the gid"""
        #Row and data to update
        gid = data['gid']
        nombre = data['nombre']
        descripcion = data['descripcion']
        geometryWKT = data['geom']
        
        #Check geometry
        r = checkIntersection('d.parks', geometryWKT, 25830)
        if r:
            return {'ok':False, 'message': 'El parque intersecta con otro', 'data':[]}
        
        #Update
        query = """
                UPDATE d.parks
                SET (nombre, descripcion, xcoord, ycoord, geom) = (%s, %s, st_x(st_geometryfromtext(%s,25830)), st_y(st_geometryfromtext(%s,25830)), st_geometryfromtext(%s,25830))
                WHERE gid = %s
                """
        self.conn.cursor.execute(query, [nombre, descripcion, geometryWKT, geometryWKT, geometryWKT, gid])
        self.conn.conn.commit()
        
        #Number of rows updated
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False, 'message': 'Parques actualizados: 0', 'data':[]}
        elif n==1:
            return {'ok':True, 'message': f'Parque actualizado. Filas afectadas : {n}', 'data':[{'numOfRowsAffected':n, 'gid':gid}]}
        elif n > 1:
            return {'ok':False, 'message': f'Demasiados parques actualizados. Filas afectadas : {n}', 'data':[{'numOfRowsAffected':n}]}

    
    def delete(self, gid:int) -> dict:
        """Deletes a Parks based in the gid"""
        #Delete
        query = """
                DELETE FROM d.parks
                WHERE gid = %s
                """
        self.conn.cursor.execute(query, [gid])
        self.conn.conn.commit()
        
        #Number of rows deleted
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False, 'message': 'Cero parques borrados', 'data':[]}
        elif n == 1:
            return {'ok':True, 'message': f'Parque borrado. Filas afectadas : {n}', 'data':[{'numOfRowsAffected':n, 'gid':gid}]}
        elif n > 1:
            return {'ok':False, 'message': f'Demasiados parques borrados. Filas afectadas : {n}', 'data':[{'numOfRowsAffected':n}]}

        

    def select(self, gid=None) -> dict:
        """select by gid as dictionary"""
        if gid:
            query = """
                    SELECT array_to_json(array_agg(registros)) FROM (
                        SELECT gid, nombre, descripcion, st_x(geom) as xcoord, st_y(geom) as ycoord, st_asgeojson(geom) as geometry_json, st_astext(geom) as geometry_text
                        FROM d.parks
                        WHERE gid = %s) AS registros
                    """
            self.conn.cursor.execute(query, [gid])
            #Output
            l = self.conn.cursor.fetchall()
            r = l[0][0]
            if r is None:
                return {'ok':False, 'message': 'Parques seleccionados: 0', 'data':[]}
            else:
                n = len(r)
                return {'ok':True, 'message': f'Parques seleccionados: {n}', 'data':r} 
        
        if gid is None:
            """Select all records as dictionary"""
            query = """
                    SELECT array_to_json(array_agg(registros)) FROM (
                        SELECT gid, nombre, descripcion, st_x(geom) as xcoord, st_y(geom) as ycoord, st_asgeojson(geom) as geometry_json, st_astext(geom) as geometry_text
                        FROM d.parks
                        ) AS registros
                    """
            self.conn.cursor.execute(query)
            #Output
            l = self.conn.cursor.fetchall()
            r = l[0][0]
            if r is None:
                return {'ok':False, 'message': 'Parques seleccionados: 0', 'data':[]}
            else:
                n = len(r)
                return {'ok':True, 'message': f'Parques seleccionados: {n}', 'data':r}
        

