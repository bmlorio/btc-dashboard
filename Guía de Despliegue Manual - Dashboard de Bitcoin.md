# Guía de Despliegue Manual - Dashboard de Bitcoin

Esta guía te ayudará a desplegar manualmente tanto el frontend como el backend del Dashboard de Bitcoin.

## 📋 Prerrequisitos

- Node.js 18+ y npm
- Python 3.11+
- Git (opcional, pero recomendado)
- Cuenta en la plataforma de despliegue elegida

## 🚀 Despliegue del Frontend (Aplicación React)

### 1. Preparación del Proyecto

```bash
# Descomprimir el archivo
tar -xzf btc-dashboard-frontend.tar.gz
cd btc-dashboard-frontend

# Instalar dependencias
npm install

# Construir para producción
npm run build
```

Esto creará una carpeta `dist/` con todos los archivos estáticos listos para desplegar.

### 2. Opciones de Despliegue del Frontend

#### **Opción A: Vercel (Recomendado)**

```bash
# Instalar CLI de Vercel
npm install -g vercel

# Iniciar sesión
vercel login

# Desplegar desde el directorio del proyecto
vercel --prod
```

**Configuración automática:** Vercel detectará que es un proyecto Vite/React.

#### **Opción B: Netlify**

**Método 1 - Drag & Drop:**
1. Ve a [netlify.com](https://netlify.com)
2. Arrastra la carpeta `dist/` a la zona de despliegue
3. Tu sitio estará disponible inmediatamente

**Método 2 - Git Integration:**
1. Sube tu código a GitHub/GitLab
2. Conecta el repositorio en Netlify
3. Configuración de build:
   - **Build command:** `npm run build`
   - **Publish directory:** `dist`

#### **Opción C: GitHub Pages**

```bash
# Instalar gh-pages
npm install --save-dev gh-pages

# Agregar script al package.json
"scripts": {
  "deploy": "gh-pages -d dist"
}

# Desplegar
npm run deploy
```

#### **Opción D: Cloudflare Pages**

```bash
# Instalar Wrangler CLI
npm install -g wrangler

# Autenticarse
wrangler login

# Desplegar
wrangler pages deploy dist --project-name btc-dashboard
```

#### **Opción E: Servidor Web Tradicional**

Simplemente copia el contenido de la carpeta `dist/` a tu servidor web (Apache, Nginx, etc.).

**Configuración de Nginx:**
```nginx
server {
    listen 80;
    server_name tu-dominio.com;
    root /path/to/dist;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

## 🔧 Despliegue del Backend (Scripts de Python)

### 1. Preparación del Backend

```bash
# Descomprimir el archivo
tar -xzf btc-dashboard-backend.tar.gz
cd btc-dashboard-backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración de Variables de Entorno

Crea un archivo `.env` en el directorio raíz del backend:

```env
# APIs de Datos
BINANCE_API_KEY=tu_api_key_de_binance
BINANCE_SECRET_KEY=tu_secret_key_de_binance

# Reddit API
REDDIT_CLIENT_ID=tu_client_id_de_reddit
REDDIT_CLIENT_SECRET=tu_client_secret_de_reddit
REDDIT_USER_AGENT=tu_user_agent

# Cloudflare R2 (Almacenamiento)
CLOUDFLARE_R2_ACCESS_KEY=tu_access_key
CLOUDFLARE_R2_SECRET_KEY=tu_secret_key
CLOUDFLARE_R2_BUCKET=tu_bucket_name
CLOUDFLARE_R2_ENDPOINT=tu_endpoint_url

# St. Louis FRED API
FRED_API_KEY=tu_api_key_de_fred

# Coinglass API (opcional)
COINGLASS_API_KEY=tu_api_key_de_coinglass
```

### 3. Opciones de Despliegue del Backend

#### **Opción A: VPS/Servidor Dedicado**

```bash
# Transferir archivos al servidor
scp -r btc-dashboard-backend/ usuario@tu-servidor:/path/to/project/

# En el servidor, configurar crontab para ejecución automática
crontab -e

# Agregar estas líneas para ejecutar cada 15 minutos
*/15 * * * * cd /path/to/project && /path/to/project/venv/bin/python scripts/ingest_binance.py
*/15 * * * * cd /path/to/project && /path/to/project/venv/bin/python scripts/ingest_coinglass.py
*/30 * * * * cd /path/to/project && /path/to/project/venv/bin/python scripts/ingest_reddit.py
0 */6 * * * cd /path/to/project && /path/to/project/venv/bin/python scripts/ingest_fred.py
```

#### **Opción B: Heroku**

```bash
# Crear archivo Procfile
echo "worker: python scripts/run_all.py" > Procfile

# Crear requirements.txt si no existe
pip freeze > requirements.txt

# Desplegar a Heroku
heroku create tu-app-name
git add .
git commit -m "Deploy backend"
git push heroku main
```

#### **Opción C: AWS Lambda (Serverless)**

```bash
# Instalar Serverless Framework
npm install -g serverless

# Crear serverless.yml
cat > serverless.yml << EOF
service: btc-dashboard-backend
provider:
  name: aws
  runtime: python3.11
functions:
  ingestData:
    handler: handler.main
    events:
      - schedule: rate(15 minutes)
EOF

# Desplegar
serverless deploy
```

#### **Opción D: Google Cloud Functions**

```bash
# Desplegar función individual
gcloud functions deploy ingest-binance \
  --runtime python311 \
  --trigger-http \
  --entry-point main \
  --source scripts/
```

### 4. Script de Ejecución Automática

Crea un archivo `run_all.py` para ejecutar todos los scripts:

```python
#!/usr/bin/env python3
import subprocess
import sys
import os
from datetime import datetime

def run_script(script_name):
    try:
        print(f"[{datetime.now()}] Ejecutando {script_name}...")
        result = subprocess.run([sys.executable, f"scripts/{script_name}"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"[{datetime.now()}] ✅ {script_name} completado")
        else:
            print(f"[{datetime.now()}] ❌ Error en {script_name}: {result.stderr}")
    except Exception as e:
        print(f"[{datetime.now()}] ❌ Excepción en {script_name}: {e}")

if __name__ == "__main__":
    scripts = [
        "ingest_binance.py",
        "ingest_coinglass.py", 
        "ingest_fred.py",
        "ingest_yfinance.py",
        "ingest_reddit.py",
        "upload_to_r2.py"
    ]
    
    for script in scripts:
        run_script(script)
    
    print(f"[{datetime.now()}] 🏁 Todos los scripts completados")
```

## 🔗 Conectar Frontend con Backend

### 1. Actualizar URLs en el Frontend

En el archivo `src/config.js` (crear si no existe):

```javascript
export const API_CONFIG = {
  // URL base de tu API o bucket de datos
  BASE_URL: 'https://tu-bucket.r2.cloudflarestorage.com',
  
  // Endpoints de datos
  ENDPOINTS: {
    PRICE_DATA: '/price-data.json',
    MARKET_METRICS: '/market-metrics.json',
    SENTIMENT_DATA: '/sentiment-data.json',
    TRADING_SIGNALS: '/trading-signals.json',
    NEWS_DATA: '/news-data.json'
  }
};
```

### 2. Configurar CORS (si usas API directa)

Si expones el backend como API, asegúrate de configurar CORS:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app, origins=["https://tu-frontend-domain.com"])
```

## 📊 Monitoreo y Mantenimiento

### 1. Logs y Monitoreo

```bash
# Ver logs en tiempo real
tail -f /var/log/btc-dashboard.log

# Configurar logrotate
sudo nano /etc/logrotate.d/btc-dashboard
```

### 2. Backup de Datos

```bash
# Script de backup
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf backup_$DATE.tar.gz data/
aws s3 cp backup_$DATE.tar.gz s3://tu-bucket-backup/
```

### 3. Actualizaciones

```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt
npm update

# Reconstruir frontend
npm run build
```

## 🚨 Solución de Problemas

### Problemas Comunes del Frontend

1. **Error 404 en rutas:** Configura el servidor para servir `index.html` en todas las rutas
2. **CORS errors:** Verifica la configuración de CORS en el backend
3. **Build failures:** Verifica que todas las dependencias estén instaladas

### Problemas Comunes del Backend

1. **API rate limits:** Implementa delays entre llamadas
2. **Credenciales inválidas:** Verifica las variables de entorno
3. **Errores de conexión:** Implementa retry logic

## 📞 Soporte

Si encuentras problemas durante el despliegue:

1. Verifica que todas las dependencias estén instaladas
2. Revisa los logs de error
3. Confirma que las variables de entorno estén configuradas correctamente
4. Verifica que los puertos necesarios estén abiertos

---

**¡Tu Dashboard de Bitcoin estará listo para usar una vez completados estos pasos!** 🚀

