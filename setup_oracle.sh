#!/bin/bash

# Configuration
REPO_URL="https://github.com/Many3102w/Surchaing-manga.git"
PROJECT_DIR="/home/ubuntu/Surchaing-manga"
APP_NAME="moda_gomez"
USER="ubuntu"
DB_NAME="surchaing_db"
DB_USER="surchaing_user"
DB_PASS="CambiarEstaPasswordSegura123" # User should change this

echo "🚀 Iniciando Instalación para Oracle Cloud (Ubuntu)..."

# 1. Update System
sudo apt update && sudo apt upgrade -y

# 2. Install Dependencies
echo "📦 Instalando dependencias..."
sudo apt install -y python3-pip python3-venv python3-dev libpq-dev postgresql postgresql-contrib nginx curl git

# 3. Setup PostgreSQL
echo "🗄️ Configurando Base de Datos..."
sudo -u postgres psql -c "CREATE DATABASE $DB_NAME;"
sudo -u postgres psql -c "CREATE USER $DB_USER WITH PASSWORD '$DB_PASS';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET client_encoding TO 'utf8';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';"
sudo -u postgres psql -c "ALTER ROLE $DB_USER SET timezone TO 'UTC';"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;"

# 4. Clone/Update Code
if [ -d "$PROJECT_DIR" ]; then
    echo "🔄 Actualizando código..."
    cd $PROJECT_DIR
    git pull
else
    echo "⬇️ Clonando repositorio..."
    git clone $REPO_URL $PROJECT_DIR
    cd $PROJECT_DIR
fi

# 5. Setup Python Virtualenv
echo "🐍 Configurando Python..."
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# 6. Create .env file
echo "⚙️ Configurando variables de entorno..."
cat > .env <<EOF
DEBUG=False
SECRET_KEY=$(openssl rand -base64 32)
ALLOWED_HOSTS=$(curl -s ifconfig.me),localhost,127.0.0.1
DATABASE_URL=postgres://$DB_USER:$DB_PASS@localhost/$DB_NAME
GEMINI_API_KEY=CAMBIAR_POR_TU_API_KEY  # CAMBIAR ESTO
EOF

# 7. Migrate and Collect Static
echo "🏗️ Ejecutando migraciones..."
python manage.py migrate
python manage.py collectstatic --noinput

# 8. Setup Gunicorn Systemd Service
echo "🤖 Configurando servicio Systemd (Gunicorn)..."
sudo bash -c "cat > /etc/systemd/system/gunicorn.service <<EOF
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$PROJECT_DIR
ExecStart=$PROJECT_DIR/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:$PROJECT_DIR/$APP_NAME.sock webcomic.wsgi:application

[Install]
WantedBy=multi-user.target
EOF"

sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# 9. Setup Nginx
echo "🌍 Configurando Nginx..."
sudo bash -c "cat > /etc/nginx/sites-available/$APP_NAME <<EOF
server {
    listen 80;
    server_name $(curl -s ifconfig.me);

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root $PROJECT_DIR;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:$PROJECT_DIR/$APP_NAME.sock;
    }
}
EOF"

sudo ln -s /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled
sudo rm /etc/nginx/sites-enabled/default
sudo nginx -t && sudo systemctl restart nginx

# 10. Open Firewall (Oracle Specific)
echo "🔥 Abriendo Firewall..."
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 80 -j ACCEPT
sudo iptables -I INPUT 6 -m state --state NEW -p tcp --dport 443 -j ACCEPT
sudo netfilter-persistent save

echo "✅ ¡Instalación Completa!"
echo "Tu sitio debería estar visible en: http://$(curl -s ifconfig.me)"
echo "⚠️  IMPORTANTE: Edita el archivo .env para poner tu GEMINI_API_KEY real."
