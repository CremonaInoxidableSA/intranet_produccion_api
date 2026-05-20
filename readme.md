python -m venv venv
    #Si sale error de permisos en la ejecución de scripts:
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
pip install --upgrade -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8007 --reload

# BLOQUEO POR MYSQL
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

# ORDEN DE INICIO
1. API BDD
2. API DATOS
3. FRONT