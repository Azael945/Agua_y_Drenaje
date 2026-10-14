from fastapi import FastAPI
from modules.clientes import router as clientes_router
from modules.consumo import router as consumos_router
from modules.reporte import router as reporte_router
from modules.tarifa import router as tarifa_router

# Inicialización de la aplicación FastAPI
app = FastAPI(
    title="API Agua y Drenaje",
    description="Sistema para administración de clientes, lecturas de consumo y tarifas.",
    version="1.0.0"
)

# Variables globales para almacenar datos en memoria
clientes_db = []
consumos_db = []
tarifa_actual = 0.50

# Incluir routers de los módulos
app.include_router(clientes_router)
app.include_router(consumos_router)
app.include_router(reporte_router)
app.include_router(tarifa_router)