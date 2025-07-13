from fastapi import APIRouter, HTTPException, Request
from app.endpoints.routers.router_interaccion_api_externa import obtener_datos_grandes_premios_año, obtener_resultados_gran_premio, obtener_parrilla_salida_gran_premio, obtener_datos_pilotos_gp
from app.endpoints.transform.tsf import tsf_info_grandes_premios_año, tsf_resultados_grandes_premios, tsf_parrilla_salida_grandes_premios, tsf_datos_piloto
import asyncio


router_db = APIRouter(prefix="/db_interaction", tags=["db_management"])

@router_db.post("/cargar_datos_db_informacion_completa_gp_año", response_description="Devuelve TRUE no hubo problemas con la carga de los datos, con FALSE, lo contrario")
async def cargar_datos_info_completa_gp_año(año : int):
    """
    Obtiene un año, toma todos los GP's de ese año (hasta la fecha actual) y luego toma todas las sesiones asociados a el.
    Luego une la información para facilitar su manejo en SQL y lo carga en la base de datos

    Parametros
    ---
        int año ->
            El año del que quieres obtener todos los GP's hasta la fecha.   

    Retorna
    ---
        Devuelve True si no hubo ningun problema en su carga

    Ejemplo
    ---
        >>> cargar_datos_info_completa_gp_año(2024)
        True
    """
    try:
        datos_año = obtener_datos_grandes_premios_año(año)
        ret = await tsf_info_grandes_premios_año(datos_año)

        json_completo_result = []
        json_completo_start = []
        json_completo_pilotos = []

        for id in ret['meetings']:
            json_completo_result.extend(obtener_resultados_gran_premio(id))
            await asyncio.sleep(0.5) #LA API EXTERNA PUEDE DAR ERROR TOO MANY REQUEST SINO.
            json_completo_start.extend(obtener_parrilla_salida_gran_premio(id))
            await asyncio.sleep(0.5)
            json_completo_pilotos.extend(obtener_datos_pilotos_gp(id))


        df_datos_piloto = await tsf_datos_piloto(json_completo_pilotos, ret['dataframe'])

        await tsf_resultados_grandes_premios(json_completo_result, ret['dataframe'], df_datos_piloto)
        await tsf_parrilla_salida_grandes_premios(json_completo_start, ret['dataframe'], df_datos_piloto)

        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error inesperado {e}')