
from appjuavaal2.pycode.connPOO import Conn

conn = Conn()



#Extension postgis
conn.cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'postgis'")
extension_exist = conn.cursor.fetchone()
# Si la extensión no existe, crearla
if not extension_exist:
    conn.cursor.execute("CREATE EXTENSION postgis")
    print('extension postgis has been created')
else:
    print('extension postgis already exists')



#Schema JR
print("creando schema d")
conn.cursor.execute("""
    DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.schemata WHERE schema_name = 'd') THEN
                CREATE SCHEMA d;
            END IF;
    END $$;
""")




#Table demo
print("creando tabla demo")
conn.cursor.execute("""
    DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'd' AND table_name = 'demo') THEN
                CREATE TABLE d.demo (
                    gid serial primary key,
                    descripcion varchar
                    );
            END IF;
    END $$;
""")



#Table people
print("creando tabla people")
conn.cursor.execute("""
    DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'd' AND table_name = 'people') THEN
                CREATE TABLE d.people (
                    dni integer primary key,
                    nombre varchar,
                    apellido varchar,
                    profesion varchar,
                    ciudad varchar
                    );
            END IF;
    END $$;
""")


#Table parks
print("creando tabla parks")
conn.cursor.execute("""
    DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'd' AND table_name = 'parks') THEN
                CREATE TABLE d.parks (
                    gid serial primary key,
                    nombre varchar,
                    descripcion varchar,
                    Xcoord double precision,
                    Ycoord double precision,
                    geom geometry(POINT, 25830)
                    );
            END IF;
    END $$;
""")


#Table streets
print("creando tabla streets")
conn.cursor.execute("""
    DO $$
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'd' AND table_name = 'streets') THEN
                CREATE TABLE d.streets (
                    gid serial primary key,
                    nombre varchar,
                    tipo varchar,
                    ncarril integer,
                    longitud double precision,
                    geom geometry(LINESTRING, 25830)
                    );
            END IF;
    END $$;
""")


conn.conn.commit()

print("finalizado")  