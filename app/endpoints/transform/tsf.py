import pandas as pd
from db.db_setup import db

database = db()

def tsf_datos_piloto(json):
    df = pd.DataFrame(pd.json_normalize(json))

    df = df[['driver_number','country_code','first_name','last_name','full_name','broadcast_name','name_acronym','team_name']]

    df.rename(columns={'driver_number':'num_piloto','country_code':'codigo_pais','first_name':'nombre_piloto','last_name':'apellido_piloto','full_name':'nombre_completo_piloto',
                       'broadcast_name':'nombre_transmision_piloto', 'name_acronym':'acronimo', 'team_name':'equipo_piloto'})
    
    df.to_sql(name='informacion_pilotos', con=database.engine, if_exists='replace', index=False)
    return True

