# Módulo de Consumos
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

# Importación del módulo principal para acceder a la base de datos en memoria
import main

# Esquemas de Pydantic para Consumos (solo YYYY-MM-DD)
class ConsumoBase(BaseModel):
    id_cliente: int
    consumo_agua: float = Field(..., ge=0, description="Lectura del consumo de agua en m3. No puede ser negativa.")
    fecha_registro: Optional[date] = Field(
        default_factory=date.today,
        description="Fecha del registro (YYYY-MM-DD). Si se omite, toma la fecha de hoy."
    )


class ConsumoCreate(ConsumoBase):
    pass


class ConsumoUpdate(BaseModel):
    consumo_agua: Optional[float] = Field(None, ge=0)
    fecha_registro: Optional[date] = None


class ConsumoResponse(ConsumoBase):
    id_consumo: int

# Router de Consumo
router = APIRouter(
    prefix="/v1/api/consumos",
    tags=["Consumos de Agua"]
)

# Variable para autoincrementar el ID de consumo
consumo_id_counter: int = 1

# Busqueda de cliente por id_cliente
def buscar_cliente(id_cliente: int):
    for cliente in main.clientes_db:
        if cliente["id_cliente"] == id_cliente:
            return cliente
    return None

# 1. Registrar una nueva lectura de consumo
@router.post(
    "",
    response_model=ConsumoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar una nueva lectura de consumo"
)

def registrar_consumo(consumo_data: ConsumoCreate):
    global consumo_id_counter

    cliente = buscar_cliente(consumo_data.id_cliente)

    if not cliente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El cliente con id_cliente={consumo_data.id_cliente} no existe."
        )

    if not cliente["active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede registrar consumo: El cliente con id_cliente={consumo_data.id_cliente} está inactivo."
        )

    nuevo_consumo = {
        "id_consumo": consumo_id_counter,
        "id_cliente": consumo_data.id_cliente,
        "consumo_agua": consumo_data.consumo_agua,
        "fecha_registro": consumo_data.fecha_registro
    }

    main.consumos_db.append(nuevo_consumo)
    consumo_id_counter += 1

    return nuevo_consumo

# 2. Consultar todas las lecturas de consumo
@router.get(
    "",
    response_model=List[ConsumoResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar todas las lecturas de consumo"
)
def consultar_consumos():
    return main.consumos_db

# 3. Consultar lecturas de consumo por cliente
@router.put(
    "/{id_consumo}",
    response_model=ConsumoResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar una lectura de consumo existente"
)
def actualizar_consumo(id_consumo: int, consumo_data: ConsumoUpdate):
    consumo_encontrado = None
    for consumo in main.consumos_db:
        if consumo["id_consumo"] == id_consumo:
            consumo_encontrado = consumo
            break

    if not consumo_encontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"La lectura de consumo con id_consumo={id_consumo} no existe."
        )

    cliente = buscar_cliente(consumo_encontrado["id_cliente"])

    if not cliente or not cliente["active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede actualizar el consumo: El cliente asociado está inactivo o fue desactivado."
        )

    if consumo_data.consumo_agua is not None:
        consumo_encontrado["consumo_agua"] = consumo_data.consumo_agua
    if consumo_data.fecha_registro is not None:
        consumo_encontrado["fecha_registro"] = consumo_data.fecha_registro

    return consumo_encontrado