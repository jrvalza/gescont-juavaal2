'''
Created on 7 mar. 2024
@author: vagrant
'''
#from dbconnection import Conn 
from .connPOO import Conn

class People():
    conn:Conn
    
    #Constructor
    def __init__(self, conn:Conn):
        self.conn = conn
      
    #User methods  
    def insert(self, data:dict) -> dict:
        #data to insert
        dni = data['dni']
        nombre = data['nombre']
        apellido = data['apellido']
        profesion = data['profesion']
        ciudad = data['ciudad']        
        #Insertion
        query = """
                INSERT INTO d.people (dni, nombre, apellido, profesion, ciudad)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING dni"""
        
        try:
            self.conn.cursor.execute(query, [dni, nombre, apellido, profesion, ciudad])
            self.conn.conn.commit()
            dni = self.conn.cursor.fetchall()[0][0]

            if dni is not None:
                return {'Ok':True, 'Message': f'Persona insertada. DNI: {dni}', 'Data':[{'DNI':dni}]}
            
        except Exception as e:
            ms = str(e).split(':')[1].strip()
            return {'Ok':False, 'Message': ms}

            

    
    
    def update(self, data:dict) -> dict:
        """Update a People based in the dni"""
        #Row and data to update
        dni = data['dni']
        nombre = data['nombre']
        apellido = data['apellido']
        profesion = data['profesion']
        ciudad = data['ciudad'] 
        
        #Update
        query = """
                UPDATE d.people
                SET (nombre, apellido, profesion, ciudad) = (%s, %s, %s, %s)
                WHERE dni = %s
                """
        self.conn.cursor.execute(query, [nombre, apellido, profesion, ciudad, dni])
        self.conn.conn.commit()
        
        #Number of rows updated
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'Ok':False, 'Message': 'Personas actualizadas: 0', 'Data':[]}
        elif n==1:
            return {'Ok':True, 'Message': f'Persona actualizada. Filas afectadas : {n}', 'Data':[{'numOfRowsAffected':n}]}
        elif n > 1:
            return {'Ok':False, 'Message': f'Demasiadas personas actualizadas. Filas afectadas : {n}', 'Data':[{'numOfRowsAffected':n}]}
        
    
    
    def delete(self, dni:int) -> dict:
        """Delete a People based in the dni"""
        #Delete
        query = """
                DELETE FROM d.people
                WHERE dni = %s
                """
        self.conn.cursor.execute(query, [dni])
        self.conn.conn.commit()
        
        #Number of rows deleted
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'Ok':False, 'Message': 'Cero personas borradas', 'Data':[]}
        elif n == 1:
            return {'Ok':True, 'Message': f'Persona borrada. Filas afectadas : {n}', 'Data':[{'numOfRowsAffected':n}]}
        elif n > 1:
            return {'Ok':False, 'Message': f'Demasiadas personas borradas. Filas afectadas : {n}', 'Data':[{'numOfRowsAffected':n}]}


        
    def select(self, dni=None) -> dict:
        """select by dni as dictionary"""
        if dni:
            query = """
                    SELECT array_to_json(array_agg(registros)) FROM (
                        SELECT dni, nombre, apellido, profesion, ciudad 
                        FROM d.people
                        WHERE dni = %s) AS registros
                    """
            self.conn.cursor.execute(query, [dni])
            #Output
            l = self.conn.cursor.fetchall()
            r = l[0][0]
            if r is None:
                return {'Ok':False, 'Message': 'Personas seleccionadas: 0', 'Data':[]}
            else:
                n = len(r)
                return {'Ok':True, 'Message': f'Personas seleccionadas: {n}', 'Data':r} 
        
        if dni is None:
            """Select all records as dictionary"""
            query = """
                    SELECT array_to_json(array_agg(registros)) FROM (
                        SELECT dni, nombre, apellido, profesion, ciudad
                        FROM d.people
                        ) AS registros
                    """
            self.conn.cursor.execute(query)
            #Output
            l = self.conn.cursor.fetchall()
            r = l[0][0]
            if r is None:
                return {'Ok':False, 'Message': 'Personas seleccionadas: 0', 'Data':[]}
            else:
                n = len(r)
                return {'Ok':True, 'Message': f'Personas seleccionadas: {n}', 'Data':r}
        

