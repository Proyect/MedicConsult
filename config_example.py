# Configuración de ejemplo para variables de entorno
# Copia este archivo como .env en la raíz del proyecto

# Configuración de la aplicación
DEBUG=True
SECRET_KEY=django-insecure-xcs3#ae6j+&o&0!#85r_$$p)v=zhoc@s2^$c$ls-5c159&#$b!
ALLOWED_HOSTS=localhost,127.0.0.1

# Configuración de base de datos
# Para desarrollo local (SQLite)
USE_POSTGRES=False

# Para producción con PostgreSQL (Docker)
# USE_POSTGRES=True
# DB_NAME=medic_db
# DB_USER=medic_user
# DB_PASSWORD=medic_password
# DB_HOST=db
# DB_PORT=5432
