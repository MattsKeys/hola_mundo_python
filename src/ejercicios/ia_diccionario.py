from typing import TypedDict

# 1. Definimos primero la subestructura
class CollectionData(TypedDict):
    id_coleccion: int
    nombre_indice: str
    activo: bool

# 2. Definimos la estructura principal que anida a la anterior
class ConfigIA(TypedDict):
    modelo: str
    temperatura: float
    max_tokens: int
    tema: str
    consulta: str
    collection: CollectionData  # Subestructura anidada


def init_config_ia() -> ConfigIA:
    config_ia: ConfigIA = {
        "modelo": "",
        "temperatura": 0,
        "max_tokens": 0,
        "tema": "",
        "consulta": "",
        "collection": {
            "id_coleccion": 0,
            "nombre_indice": 0,
            "activo": False
        }

    }

}



configuracion_ia = {
    "modelo": "gpt-4o",
    "temperatura": 0.7,
    "max_tokens": 150
}