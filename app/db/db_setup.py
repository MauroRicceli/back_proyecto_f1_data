import sqlalchemy as al
from sqlalchemy.ext.declarative import declarative_base
from app.connection_info.datos_conexion import datosDB, datosDBCloud

datosDB = datosDB()
base = declarative_base()

class datosPilotos(base):
        __tablename__ = 'informacion_pilotos_gp'
        id_entry = al.Column(al.Integer(), primary_key=True, autoincrement=True)
        num_piloto = al.Column(al.Integer())
        id_gp = al.Column(al.Integer())
        id_sesion = al.Column(al.Integer())
        nombre_gran_premio = al.Column(al.String(300))
        anio = al.Column(al.Integer())
        codigo_pais = al.Column(al.String(3))
        nombre_piloto = al.Column(al.String(80))
        apellido_piloto = al.Column(al.String(120))
        nombre_completo_piloto = al.Column(al.String(380))
        nombre_transmision_piloto = al.Column(al.String(300))
        acronimo = al.Column(al.String(3))
        equipo_piloto = al.Column(al.String(380))
        url_imagen_piloto = al.Column(al.String(1000))
        color_equipo = al.Column(al.String(15))

class resultadosGP(base):
      __tablename__ = 'resultados_gp'
      id_entry = al.Column(al.Integer(), primary_key=True, autoincrement=True)
      nombre_gran_premio = al.Column(al.String(300))
      anio = al.Column(al.Integer)
      posicion = al.Column(al.Integer())
      num_piloto = al.Column(al.Integer())
      nombre_piloto = al.Column(al.String(380))
      equipo_piloto = al.Column(al.String(380))
      vueltas = al.Column(al.Integer())
      dnf = al.Column(al.Boolean())
      dns = al.Column(al.Boolean())
      dsq = al.Column(al.Boolean())
      duracion_segs = al.Column(al.Float()) #MEJOR VUELTA EN PRACTICA O QUALI. TIEMPO TOTAL DE CARRERA EN CARRERAS O SPRINTS.
      dif_lider = al.Column(al.Float())
      id_gp = al.Column(al.Integer())
      id_sesion = al.Column(al.Integer())
      puntos_obtenidos = al.Column(al.Integer())

class parrilla_salida_gp(base):
      __tablename__ = 'parrilla_salida_gp'
      id_entry = al.Column(al.Integer(), primary_key=True, autoincrement=True)
      id_gp = al.Column(al.Integer())
      id_sesion = al.Column(al.Integer())
      nombre_gran_premio = al.Column(al.String(300))
      anio = al.Column(al.Integer)
      posicion = al.Column(al.Integer())
      num_piloto = al.Column(al.Integer())
      nombre_piloto = al.Column(al.String(380))
      equipo_piloto = al.Column(al.String(380))
      tiempo_vuelta_quali = al.Column(al.Float())

class grandes_premios(base):
      __tablename__ = 'grandes_premios'
      id_entry = al.Column(al.Integer(), primary_key=True, autoincrement=True)
      id_gp = al.Column(al.Integer(), unique=True)
      id_circuito = al.Column(al.Integer())
      nombre_circuito = al.Column(al.String(100))
      acronimo_pais = al.Column(al.String(3))
      ubicacion_circuito = al.Column(al.String(100))
      nombre_pais = al.Column(al.String(150))
      nombre_gran_premio = al.Column(al.String(300))
      nombre_completo_gp = al.Column(al.String(600))
      fecha_hora_inicio = al.Column(al.DateTime())
      año = al.Column(al.Integer())


class db():
    def __init__(self):
          self.engine = al.create_engine(f"mysql+pymysql://{datosDB.user}:{datosDB.password}@{datosDB.ip}:{datosDB.puerto}/{datosDB.db_name}?charset=utf8mb4",pool_recycle=3600,
                                         connect_args={
                                                "ssl": {"ssl_mode": "REQUIRED"}
                                         })
          self.connection = self.engine.connect()
          self.first_calls()

    def first_calls(self):
          base.metadata.create_all(self.engine)
