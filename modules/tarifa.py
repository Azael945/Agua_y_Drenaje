# Módulo de Tarifa
from fastapi import APIRouter, status
from pydantic import BaseModel, Field

# Importación del módulo principal para acceder a la base de datos en memoria
import main

# Esquemas Pydantic para Tarifa
class TarifaBase(BaseModel):
    tarifa: float = Field(
        ..., 
        ge=0, 
        description="Valor de la tarifa por m3. Debe ser un valor no negativo (>= 0)."
    )


class TarifaResponse(BaseModel):
    indicador_exito: bool
    mensaje: str
    tarifa_actual: float


# Router de Tarifa
router = APIRouter(
    prefix="/v1/api/tarifa",
    tags=["Tarifa"]
)


# 1. Consultar la tarifa actual
@router.get(
    "",
    response_model=TarifaResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar la tarifa actual"
)
def consultar_tarifa():
    return {
        "indicador_exito": True,
        "mensaje": "Tarifa actual consultada correctamente.",
        "tarifa_actual": main.tarifa_actual
    }


# 2. Modificar la tarifa actual
@router.put(
    "",
    response_model=TarifaResponse,
    status_code=status.HTTP_200_OK,
    summary="Modificar la tarifa actual de agua"
)
def actualizar_tarifa(tarifa_data: TarifaBase):
    main.tarifa_actual = tarifa_data.tarifa
    return {
        "indicador_exito": True,
        "mensaje": "Tarifa actualizada correctamente.",
        "tarifa_actual": main.tarifa_actual
    }