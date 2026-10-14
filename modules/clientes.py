# Módulo de Clientes
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

# Importación del módulo principal para acceder a la base de datos en memoria
import main

# Esquemas de Pydantic para Clientes
class ClienteBase(BaseModel):
    nombre_cliente: str = Field(..., min_length=1, description="Nombre completo del cliente")
    direccion: str = Field(..., min_length=1, description="Dirección del domicilio")


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nombre_cliente: Optional[str] = Field(None, min_length=1)
    direccion: Optional[str] = Field(None, min_length=1)


class ClienteResponse(ClienteBase):
    id_cliente: int
    active: bool


class ClientesListResponse(BaseModel):
    indicador_exito: bool
    total_clientes: int
    clientes: List[ClienteResponse]


# Router de Clientes
router = APIRouter(
    prefix="/v1/api/clientes",
    tags=["Clientes"]
)

# Variable para autoincrementar el ID de cliente
cliente_id_counter: int = 1


# 1. Consultar todos los clientes
@router.get(
    "",
    response_model=ClientesListResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar todos los clientes"
)
def get_clientes():
    return {
        "indicador_exito": True,
        "total_clientes": len(main.clientes_db),
        "clientes": main.clientes_db
    }


# 2. Registrar un nuevo cliente
@router.post(
    "",
    response_model=ClienteResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo cliente"
)
def create_cliente(cliente_data: ClienteCreate):
    global cliente_id_counter

    nuevo_cliente = {
        "id_cliente": cliente_id_counter,
        "nombre_cliente": cliente_data.nombre_cliente,
        "direccion": cliente_data.direccion,
        "active": True  # Todo cliente se registra activo
    }

    main.clientes_db.append(nuevo_cliente)
    cliente_id_counter += 1

    return nuevo_cliente


# 3. Actualizar la información de un cliente
@router.put(
    "/{id_cliente}",
    response_model=ClienteResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar la información de un cliente"
)
def update_cliente(id_cliente: int, cliente_data: ClienteUpdate):
    for cliente in main.clientes_db:
        if cliente["id_cliente"] == id_cliente:
            if cliente_data.nombre_cliente is not None:
                cliente["nombre_cliente"] = cliente_data.nombre_cliente
            if cliente_data.direccion is not None:
                cliente["direccion"] = cliente_data.direccion
            return cliente

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El cliente con id_cliente={id_cliente} no existe."
    )


# 4. Desactivar un cliente (active = False)
@router.delete(
    "/{id_cliente}",
    status_code=status.HTTP_200_OK,
    summary="Desactivar cliente"
)
def deactivate_cliente(id_cliente: int):
    for cliente in main.clientes_db:
        if cliente["id_cliente"] == id_cliente:
            cliente["active"] = False  # Baja lógica
            return {
                "indicador_exito": True,
                "mensaje": f"Cliente con id_cliente={id_cliente} desactivado correctamente.",
                "cliente": cliente
            }

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"El cliente con id_cliente={id_cliente} no existe."
    )