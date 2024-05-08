
from appjuavaal2.pycode.connPOO import Conn
from appjuavaal2.pycode.parks import Parks
from appjuavaal2.pycode.streets import Streets
from appjuavaal2.pycode.people import People

conn = Conn()
print('Insertando')
conn.cursor.execute('insert into d.demo (descripcion) values (%s)',['Hola mundo'])

#Insert people
b = People(conn)
data1 = {'dni':100, 'nombre':'Marta', 'apellido':'Lazaro', 'profesion':'Fisioterapeuta', 'ciudad':'Valencia'}
data2 = {'dni':200, 'nombre':'Juan', 'apellido':'Ospina', 'profesion':'Dentinsta', 'ciudad':'Madrid'}
b.insert(data1)
b.insert(data2)

#Insert parks
b = Parks(conn)
data1 = {'nombre':'Bioparc', 'descripcion':'Zoologico de la ciudad de Valencia', 'geom': "POINT(724819 4373318)"}
data2 = {'nombre':'Turia', 'descripcion':'Parque urbano público situado en el antiguo cauce del río Turia de la ciudad de Valencia', 'geom': "POINT(726100 4375318)"}
b.insert(data1)
b.insert(data2)


#Insert streets
b = Streets(conn)
data1 = {'nombre':'Viver', 'tipo':'Calle', 'ncarril':1, 'geom': "LINESTRING(198231 263418,198213 268322)"}
data2 = {'nombre':'Primat Reig', 'tipo':'Avenida', 'ncarril':3, 'geom': "LINESTRING(198031 263018,198013 268022)"}
b.insert(data1)
b.insert(data2)


conn.conn.commit()
print('Finalizado')

