python -m venv venv
    #Si sale error de permisos en la ejecución de scripts:
    Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
pip install --upgrade -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8200

# BLOQUEO POR MYSQL
GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' WITH GRANT OPTION;
FLUSH PRIVILEGES;

# ORDEN DE INICIO
1. API BDD
2. API DATOS
3. FRONT

# RUNNEO DE CONTENEDOR DESDE 0
# 1. Clonar/copiar el proyecto y crear el .env con las credenciales reales
# 2.
docker build -t produccion-cremona_bdd .
# 3.
docker run -d \
  --name produccion-cremona_bdd \
  --network=host \
  --env-file .env \
  --restart unless-stopped \
  produccion-cremona_bdd

# NUEVO USUARIO MYSQL
CREATE USER 'root'@'192.168.20.150' IDENTIFIED BY 'echo32415';
GRANT ALL PRIVILEGES ON *.* TO 'root'@'192.168.20.150' WITH GRANT OPTION;
FLUSH PRIVILEGES;