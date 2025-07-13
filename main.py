import uvicorn
from app.connection_info.datos_conexion import datosAPI

myIp = datosAPI()

#IP Y PUERTOS LOCALES. SE OBTIENEN DE UN ARCHIVO NO PUSHEADO EN EL REPO.

if __name__ == "__main__":
    config = uvicorn.run("app.api.api:app", host=myIp.ip, port=int(myIp.puerto), log_level="info",reload=True)