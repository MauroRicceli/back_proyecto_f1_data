import sqlalchemy as al
from sqlalchemy.ext.declarative import declarative_base
from app.connection_info.datos_conexion import datosDB, datosDBCloud

datosDB = datosDBCloud()
base = declarative_base()

class datosPilotos(base):
        __tablename__ = 'informacion_pilotos'
        id_entry = al.Column(al.Integer(), primary_key=True, autoincrement=True)
        num_piloto = al.Column(al.Integer())
        codigo_pais = al.Column(al.String(3))
        nombre_piloto = al.Column(al.String(80))
        apellido_piloto = al.Column(al.String(120))
        nombre_completo_piloto = al.Column(al.String(380))
        nombre_transmision_piloto = al.Column(al.String(300))
        acronimo = al.Column(al.String(3))
        equipo_piloto = al.Column(al.String(380))

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
