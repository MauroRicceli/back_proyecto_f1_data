from fastapi import APIRouter, HTTPException, Request


router_db = APIRouter(prefix="/db_interaction", tags=["db_management"])

#@router.post("/prueba",response_model = str)
#async def hola_mundo():
    #return "Hola mundo"

@router_db.post("/cargar_datos_db", response_model=bool, response_description="Devuelve TRUE no hubo problemas con la carga de los datos, con FALSE, lo contrario")
async def obtener_datos_api():
    response = True
    return response