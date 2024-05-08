from . import connPOO

def checkIntersection(layerName, geometryWkt, epsg):
    conn = connPOO.Conn()
    cursor = conn.cursor
    q=f'select gid from {layerName} where st_intersects(geom, st_geometryfromtext(%s,%s))'
    cursor.execute(q,[geometryWkt,epsg])
    r=cursor.fetchall()  #() si no hay nada, none
                        #((1,),(2,), ...)
    if r is None:
        return False

    if len(r) > 0:
        return True
    else:
        return False

