Instrucciones para la ejecucion del proyecto

1.- Abre el PowerShell en la carpeta del proyecto 

2.- Crear el entorno vitual:    python -m venv venv

3.- Activar el entorno vitual:  venv\Scripts\activate

4.- Instalar dependencias:      pip install fastapi uvicorn pydantic

5.- Ejecutar el servidor:       uvicorn main:app --reload

6.- Ingresar en navegador web:  http://127.0.0.1:8000/docs
