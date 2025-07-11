from fastapi import APIRouter, HTTPException, Request
from app.endpoints.routers.router_interaccion_api_externa import obtener_datos_grandes_premios_año, obtener_resultados_gran_premio
from app.endpoints.transform.tsf import tsf_info_grandes_premios_año, tsf_resultados_grandes_premios
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

        json_completo = []

        for id in ret['meetings']:
            json_completo.extend(obtener_resultados_gran_premio(id))
            await asyncio.sleep(0.5) #LA API EXTERNA PUEDE DAR ERROR TOO MANY REQUEST SINO.

        await tsf_resultados_grandes_premios(json_completo)

        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error inesperado {e}')