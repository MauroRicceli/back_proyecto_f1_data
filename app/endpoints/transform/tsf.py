import pandas as pd
from app.db.db_setup import db

database = db()

async def tsf_datos_piloto(json, dataFrameGPs):
    df = pd.DataFrame(pd.json_normalize(json))

    df = df.rename(columns={'driver_number':'num_piloto','country_code':'codigo_pais','first_name':'nombre_piloto','last_name':'apellido_piloto','full_name':'nombre_completo_piloto',
                       'broadcast_name':'nombre_transmision_piloto', 'name_acronym':'acronimo', 'team_name':'equipo_piloto', 'meeting_key':'id_gp', 'session_key':'id_sesion', 'headshot_url':'url_imagen_piloto', 'team_colour':'color_equipo'})
    
    dataFrameGPs = dataFrameGPs[['nombre_gran_premio', 'anio', 'id_gp']]

    pilotosGP = pd.merge(df, dataFrameGPs, on='id_gp')

    pilotosGP.to_sql(name='informacion_pilotos_gp', con=database.engine, if_exists='replace', index=False)

    return pilotosGP

async def tsf_info_grandes_premios_año(json):
    df = pd.DataFrame(pd.json_normalize(json))

    df['date_start'] = pd.to_datetime(df['date_start'], yearfirst=True).dt.tz_localize(None)

    df = df.drop(columns=['gmt_offset','country_key','country_code'])

    df = df.rename(columns={'meeting_key':'id_gp','meeting_code':'acronimo_pais' ,'meeting_name':'nombre_gran_premio','meeting_official_name':'nombre_completo_gp','circuit_key':'id_circuito','circuit_short_name':'nombre_circuito', 'country_name':'nombre_pais','location':'ubicacion_circuito','year':'anio', 'date_start':'fecha_hora_inicio'})

    df.to_sql(name='grandes_premios', con=database.engine, if_exists='replace', index=False)

    meetings = df['id_gp']

    return {'dataframe' : df,
            'meetings' : meetings}

async def tsf_resultados_grandes_premios(json, dataFrameGPs, dataFramePilotos):
    df = pd.DataFrame(pd.json_normalize(json))

    df = df.rename(columns={'position':'posicion', 'driver_number':'num_piloto','number_of_laps':'vueltas','duration':'duracion_segs','gap_to_leader':'dif_lider','meeting_key':'id_gp','session_key':'id_sesion','points':'puntos_obtenidos'})
    df = df.explode(['duracion_segs','dif_lider'])

    df['posicion'] = pd.to_numeric(df['posicion'], errors='coerce').astype('Int64') #Int64 permite NaN
    df['duracion_segs'] = pd.to_numeric(df['duracion_segs'], errors='coerce')
    df['vueltas'] = pd.to_numeric(df['vueltas'], errors='coerce', downcast='integer').astype('Int64')
    df['dif_lider'] = pd.to_numeric(df['dif_lider'], errors='coerce')
    df['puntos_obtenidos'] = pd.to_numeric(df['puntos_obtenidos'], errors='coerce').astype('Int64')

    dataFrameGPs = dataFrameGPs[['id_gp','nombre_gran_premio', 'anio']]

    resultados_gp = pd.merge(df, dataFrameGPs, on='id_gp')

    dataFramePilotos = dataFramePilotos[['nombre_completo_piloto', 'equipo_piloto', 'id_gp', 'id_sesion', 'num_piloto']]

    resultados_gp = pd.merge(resultados_gp, dataFramePilotos, on=['id_gp','id_sesion','num_piloto'])

    resultados_gp.to_sql(name='resultados_gp', con=database.engine, if_exists='replace', index=True)

    return True

async def tsf_parrilla_salida_grandes_premios(json, dataFrameGPs, dataFramePilotos):
    df = pd.DataFrame(pd.json_normalize(json))

    df = df.rename(columns={'driver_number':'num_piloto','lap_duration':'tiempo_vuelta_quali','meeting_key':'id_gp','position':'posicion','session_key':'id_sesion'})

    dataFrameGPs = dataFrameGPs[['nombre_gran_premio', 'anio', 'id_gp']]

    parrilla_salida = pd.merge(df, dataFrameGPs, on='id_gp')

    dataFramePilotos = dataFramePilotos[['nombre_completo_piloto','equipo_piloto','id_gp','id_sesion','num_piloto']]

    parrilla_salida = pd.merge(parrilla_salida, dataFramePilotos, on=['id_gp','id_sesion','num_piloto'])

    parrilla_salida.to_sql(name='parrilla_salida_gp', con=database.engine, if_exists='replace', index=True)

    return True