import urllib.parse
import urllib.request
from fastapi import APIRouter, HTTPException, Request
import json, urllib


#ALL DATA RETRIEVED FROM OPENF1-ORG.

router_ext_api = APIRouter(prefix="/get_data", tags=["external_api_interaction"])

#@router.post("/prueba",response_model = str)
#async def hola_mundo():
    #return "Hola mundo"

@router_ext_api.get("/api_data_retrieve_car_data", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_datos_coche(numero_auto : str, id_meeting : str,id_sesion : str):
    """
    Obtienes la información de un coche específico, en un fin de semana de carreras y una sesión de él

    Parametros
    ----------

    numero_auto : str
        -> el numero asignado al piloto que quieres analizar
    id_meeting : str
        -> el id de la meeting (fin de semana) que quieras analizar. Para utilizar la última ingresar latest
    id_sesion : str
        -> el id de la sesión de ese fin de semana que quieras analizar. Para utilizar la última ingresar latest

    Retorna
    -------
    Devuelve un json con todos los datos de ese vehículo en esa sesión.

    Ejemplo
    -------
        >>> obtener_datos_coche(55, latest, latest)
        json
    """

    url = 'https://api.openf1.org/v1/car_data'
    parametros = {"driver_number" : numero_auto, "session_key":id_sesion, "meeting_key":id_meeting}
    try:
        response = urllib.request.urlopen(url= url+"?"+urllib.parse.urlencode(parametros))
        datos = response.read().decode('utf-8')
        return datos
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado {e}")
    

    
@router_ext_api.get("/api_data_retrieve_driver_data", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_datos_piloto(numero_auto : str):
    """
    Obtienes la información de un piloto específico en su última semana de carreras.

    Parametros
    ----------

    numero_auto : str
        -> el numero asignado al piloto que quieres analizar

    Retorna
    -------
    Devuelve un json con todos los datos de ese piloto

    Ejemplo
    -------
        >>> obtener_datos_piloto(43)
        json
    """

    url = 'https://api.openf1.org/v1/drivers'
    parametros = {"driver_number" : numero_auto, "session_key": "latest"}
    try:
        response = urllib.request.urlopen(url= url+"?"+urllib.parse.urlencode(parametros))
        datos = response.read().decode('utf-8')
        return datos
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado {e}")
    
@router_ext_api.get("/api_data_retrieve_driver_lap_data", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_datos_vueltas_piloto(numero_auto:str, id_meeting:str, id_sesion:str):
    """
    Obtienes la información de las vueltas de un coche específico, en un fin de semana de carreras y un sesión de él

    Parametros
    ----------

    numero_auto : str
        -> el numero asignado al piloto que quieres analizar
    id_meeting : str
        -> el id de la meeting (fin de semana) que quieras analizar. Para utilizar la última ingresar latest
    id_sesion : str
        -> el id de la sesión de ese fin de semana que quieras analizar. Para utilizar la última ingresar latest

    Retorna
    -------
    Devuelve un json con todos los datos de vueltas de ese vehículo en esa sesión.

    Ejemplo
    -------
        >>> obtener_datos_vueltas_piloto(43, latest, latest)
        json
    """

    url = "https://api.openf1.org/v1/laps"
    parametros = {'driver_number':numero_auto, 'meeting_key':id_meeting, 'session_key':id_sesion}
    try:
        response = urllib.request.urlopen(url=url+'?'+urllib.parse.urlencode(parametros))
        data = response.read().decode('utf-8')
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Se ha encontrado un error inesperado: {e}')
    

@router_ext_api.get("/api_data_retrieve_grand_prix_data", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_datos_gran_premio(id_meeting:str):
    """
    Obtienes la información del gran premio

    Parametros
    ----------

    id_meeting : str
        -> el id de la meeting (fin de semana) que quieras analizar. Para utilizar la última ingresar latest


    Retorna
    -------
    Devuelve un json con todos los datos de ese gran premio

    Ejemplo
    -------
        >>> obtener_datos_gran_premio(latest)
        json
    """

    url = "https://api.openf1.org/v1/meetings"
    parametros = {'meeting_key':id_meeting}
    try:
        response = urllib.request.urlopen(url=url+'?'+urllib.parse.urlencode(parametros))
        data = response.read().decode('utf-8')
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Se ha encontrado un error inesperado: {e}')
    
@router_ext_api.get("/api_data_retrieve_grand_prix_on_circuit_data", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_datos_gran_premio_circuito(nombre_circuito:str):
    """
    Obtienes la información de los grandes premios celebrados en este circuito

    Parametros
    ----------

    nombre_circuito : str
        -> el nombre del circuito que quieras obtener sus grandes premios registrados. (EN INGLES)


    Retorna
    -------
    Devuelve un json con todos los datos de esos grandes premios

    Ejemplo
    -------
        >>> obtener_datos_gran_premio_circuito('Singapore')
        json
    """

    url = "https://api.openf1.org/v1/meetings"
    parametros = {'circuit_short_name':nombre_circuito}
    try:
        response = urllib.request.urlopen(url=url+'?'+urllib.parse.urlencode(parametros))
        data = response.read().decode('utf-8')
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Se ha encontrado un error inesperado: {e}')
    
@router_ext_api.get("/api_data_retrieve_grand_prix_on_year_data", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_datos_grandes_premios_año(año:int):
    """
    Obtienes la información de los grandes premios celebrados en este año

    Parametros
    ----------

    año : str
        -> el año que quieras obtener todos sus grander premios


    Retorna
    -------
    Devuelve un json con todos los datos de esos grandes premios

    Ejemplo
    -------
        >>> obtener_datos_gran_premio_circuito('2025')
        json
    """

    url = "https://api.openf1.org/v1/meetings"
    parametros = {'year':año}
    try:
        response = urllib.request.urlopen(url=url+'?'+urllib.parse.urlencode(parametros))
        data = response.read().decode('utf-8')
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Se ha encontrado un error inesperado: {e}')
    


@router_ext_api.get("/api_data_retrieve_grand_prix_results", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_resultados_gran_premio(id_meeting : str):
    """
    Obtienes la información del resultado del gran premio

    Parametros
    ----------

    id_meeting : str
        -> el id del gran premio que quieras ver


    Retorna
    -------
    Devuelve un json con todos los datos de ese gran premio

    Ejemplo
    -------
        >>> obtener_resultados_gran_premio('latest')
        json
    """

    url = "https://api.openf1.org/v1/session_result"
    parametros = {'meeting_key':id_meeting}
    try:
        response = urllib.request.urlopen(url=url+'?'+urllib.parse.urlencode(parametros))
        data = response.read().decode('utf-8')
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Se ha encontrado un error inesperado: {e}')
    
@router_ext_api.get("/api_data_retrieve_grand_prix_starting_grid", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_parrilla_salida_gran_premio(id_meeting : str):
    """
    Obtienes la información de la parrilla del gran premio

    Parametros
    ----------

    id_meeting : str
        -> el id del gran premio que quieras ver


    Retorna
    -------
    Devuelve un json con todos los datos de ese gran premio

    Ejemplo
    -------
        >>> obtener_parrilla_salida_gran_premio('latest')
        json
    """

    url = "https://api.openf1.org/v1/starting_grid"
    parametros = {'meeting_key':id_meeting}
    try:
        response = urllib.request.urlopen(url=url+'?'+urllib.parse.urlencode(parametros))
        data = response.read().decode('utf-8')
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Se ha encontrado un error inesperado: {e}')
    

@router_ext_api.get("/api_data_retrieve_grand_prix_stints", response_description="Devuelve un JSON con la información si todo sale bien")
async def obtener_stints_gran_premio(id_meeting : str, numero_coche:str):
    """
    Obtienes la información de los stints de un coche en un gran premio

    Parametros
    ----------

    id_meeting : str
        -> el id del gran premio que quieras ver

    numero_coche : str
        -> el numero del coche/piloto que quieras ver


    Retorna
    -------
    Devuelve un json con todos los datos de los stints en ese gran premio

    Ejemplo
    -------
        >>> obtener_stints_gran_premio('latest')
        json
    """

    url = "https://api.openf1.org/v1/stints"
    parametros = {'meeting_key':id_meeting, 'driver_number' : numero_coche}
    try:
        response = urllib.request.urlopen(url=url+'?'+urllib.parse.urlencode(parametros))
        data = response.read().decode('utf-8')
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Se ha encontrado un error inesperado: {e}')
    

