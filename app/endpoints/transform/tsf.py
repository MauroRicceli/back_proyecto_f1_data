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

async def tsf_info_grandes_premios_año(json):
    df = pd.DataFrame(pd.json_normalize(json))

    df['date_start'] = pd.to_datetime(df['date_start'], yearfirst=True).dt.tz_localize(None)

    df = df.drop(columns=['gmt_offset','country_key','country_code'])

    df = df.rename(columns={'meeting_key':'id_gp','meeting_code':'acronimo_pais' ,'meeting_name':'nombre_gran_premio','meeting_official_name':'nombre_completo_gp','circuit_key':'id_circuito','circuit_short_name':'nombre_circuito', 'country_name':'nombre_pais','location':'ubicacion_circuito','year':'año', 'date_start':'fecha_hora_inicio'})

    meetings = df['id_gp']

    return {'dataframe' : df,
            'meetings' : meetings}

async def tsf_resultados_grandes_premios(json):
    df = pd.DataFrame(pd.json_normalize(json))

    df = df.rename(columns={'position':'posicion', 'driver_number':'num_piloto','number_of_laps':'vueltas','duration':'duracion_segs','gap_to_leader':'dif_lider','meeting_key':'id_gp','session_key':'id_sesion','points':'puntos'})
    df = df.explode(['duracion_segs','dif_lider'])

    df['posicion'] = pd.to_numeric(df['posicion'], errors='coerce').astype('Int64') #Int64 permite NaN
    df['duracion_segs'] = pd.to_numeric(df['duracion_segs'], errors='coerce')
    df['vueltas'] = pd.to_numeric(df['vueltas'], errors='coerce', downcast='integer').astype('Int64')
    df['dif_lider'] = pd.to_numeric(df['dif_lider'], errors='coerce')
    df['puntos'] = pd.to_numeric(df['puntos'], errors='coerce').astype('Int64')

    print(df.dtypes)

    return True

