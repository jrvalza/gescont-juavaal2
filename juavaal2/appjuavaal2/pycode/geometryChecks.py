from . import connPOO

def checkIntersection(layerName1, layerName2, geometryWkt, epsg):
    conn = connPOO.Conn()
    cursor = conn.cursor
    if layerName2 == 'd.parks':
        q=f"""SELECT l1.gid 
            FROM {layerName1} l1, {layerName2} l2 
            WHERE ST_Intersects(l1.geom, ST_Geometryfromtext(%s,%s))
            OR ST_Intersects(ST_Buffer(l2.geom,0.02), ST_Geometryfromtext(%s,%s))"""
        
    elif layerName2 == 'd.streets':
        q=f"""SELECT l1.gid
            FROM {layerName1} l1, {layerName2} l2
            WHERE ST_Intersects(ST_Buffer(l1.geom,0.02), ST_Buffer(ST_Geometryfromtext(%s,%s),0.02))
            OR ST_Intersects(l2.geom, ST_Buffer(ST_Geometryfromtext(%s,%s),0.02))"""
            
    cursor.execute(q,[geometryWkt,epsg,geometryWkt,epsg])
    r=cursor.fetchall()  #() si no hay nada, none
                        #((1,),(2,), ...)
    if r is None:
        return False

    if len(r) > 0:
        return True
    else:
        return False
    

def checkDistance(layerName1, layerName2, geometryWkt, epsg):
    conn = connPOO.Conn()
    cursor = conn.cursor

    total1 =None
    total2 =None

    #Comprobacion con layer 1
    q=f"""  SELECT gid
            FROM {layerName1}
            WHERE ST_DWithin(geom, ST_Geometryfromtext(%s,%s),50)
            OR gid NOT IN (SELECT gid 
                            FROM {layerName1}
                            WHERE ST_DWithin(geom, ST_Geometryfromtext(%s,%s),10000)
                            )
        """
    cursor.execute(q,[geometryWkt, epsg, geometryWkt, epsg])
    r=cursor.fetchall()#si no hay nada, none
                        #((1,),(2,), ...)
    if r:
        total1 = len(r)
    
    #Comprobación con layer 2
    q=f"""  SELECT gid
            FROM {layerName2}
            WHERE ST_DWithin(geom, ST_Geometryfromtext(%s,%s),50)
        """
    cursor.execute(q,[geometryWkt, epsg])
    r=cursor.fetchall()
        
    if r:
        total2 = len(r)

    if total1 is None and total2 is None:
        return False

    elif total1 is not None and total2 is None:
        if total1 > 0:
            return True

    elif total2 is not None and total1 is None:
        if total2 > 0:
            return True
    else:
        return False
    


#OR NOT ST_DWithin(l1.geom, ST_Geometryfromtext(%s,%s),1000)