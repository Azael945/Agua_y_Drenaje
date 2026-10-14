# Módulo de Reportes
from datetime import date
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel, Field

# Importación del módulo principal para acceder a la base de datos en memoria
import main

# Esquemas de Pydantic para Reportes
class ClienteReporteInfo(BaseModel):
    id_cliente: int
    nombre_cliente: str
    direccion: str


class ReporteItem(BaseModel):
    id_consumo: int
    cliente: ClienteReporteInfo
    consumo_agua: float
    fecha_registro: date
    tarifa: float = Field(description="Tarifa actual aplicada al consumo")
    total_pagar: float = Field(description="Calculado como: consumo_agua * tarifa_actual")


class ReporteResponse(BaseModel):
    indicador_exito: bool
    total_registros: int
    tarifa_aplicada: float
    reporte: List[ReporteItem]

# Router de Reportes
router = APIRouter(
    prefix="/v1/api/reportes",
    tags=["Reportes de Consumo"]
)

# 1. Obtener reporte de consumos para clientes activos
@router.get(
    "/consumos",
    response_model=ReporteResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener reporte de consumos para clientes activos"
)
def obtener_reporte_consumos(
    fecha_registro: Optional[date] = Query(
        None, 
        description="Filtrar por fecha específica de registro (Formato: YYYY-MM-DD)"
    )
):
    clientes_activos = {
        c["id_cliente"]: c 
        for c in main.clientes_db 
        if c.get("active", False)
    }

    reporte_items = []

    for consumo in main.consumos_db:
        id_cliente = consumo["id_cliente"]

        if id_cliente not in clientes_activos:
            continue

        if fecha_registro and consumo["fecha_registro"] != fecha_registro:
            continue

        cliente_info = clientes_activos[id_cliente]
        total_pagar = round(consumo["consumo_agua"] * main.tarifa_actual, 2)

        item = {
            "id_consumo": consumo["id_consumo"],
            "cliente": {
                "id_cliente": cliente_info["id_cliente"],
                "nombre_cliente": cliente_info["nombre_cliente"],
                "direccion": cliente_info["direccion"]
            },
            "consumo_agua": consumo["consumo_agua"],
            "fecha_registro": consumo["fecha_registro"],
            "tarifa": main.tarifa_actual,
            "total_pagar": total_pagar
        }

        reporte_items.append(item)

    if fecha_registro and len(reporte_items) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontraron registros de consumo para la fecha {fecha_registro}."
        )

    return {
        "indicador_exito": True,
        "total_registros": len(reporte_items),
        "tarifa_aplicada": main.tarifa_actual,
        "reporte": reporte_items
    }