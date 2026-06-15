from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from config.config import settings

app = FastAPI(title="Servidor de mayusculas")

class PayloadInput(BaseModel):
    usuario: str
    contrasenia: str
    texto: str

@app.post("/procesar")
async def procesar_texto(pl_input: PayloadInput):

    if pl_input.usuario != settings.api_mayuscula_user or pl_input.contrasenia != settings.api_mayuscula_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas"
        )

    return pl_input.texto.upper()

