# Dashboard de Bitcoin - Sistema de Soporte para Trading

Un dashboard completo de Bitcoin que proporciona análisis en tiempo real, métricas del mercado, análisis de sentimiento y señales de trading para ayudar en la toma de decisiones de inversión.

## 🚀 Demo en Vivo

**URL del Dashboard:** https://8080-i6tll95kckhuifbsijv0u-761c290c.manusvm.computer

## 📋 Características Principales

### 📊 Visualización de Datos en Tiempo Real
- **Precio de Bitcoin**: Precio actual con cambios porcentuales en 24h
- **Capitalización de Mercado**: Valor total del mercado y dominancia de Bitcoin
- **Índice de Miedo y Codicia**: Indicador de sentimiento del mercado (0-100)

### 📈 Gráficos Interactivos
- **Gráfico de Precios BTC/USD**: Visualización de precios con múltiples marcos temporales (24h, 7d, 30d)
- **Gráficos de Área**: Evolución del precio con gradientes y animaciones
- **Estadísticas de Precio**: Máximo, mínimo y precio actual del período seleccionado

### 🎯 Métricas del Mercado
- **Open Interest**: Posiciones abiertas en derivados de Bitcoin
- **Funding Rates**: Tasas de financiamiento por exchange (Binance, Bybit, OKX, etc.)
- **Ratio Long/Short**: Distribución de posiciones largas vs cortas
- **Liquidaciones 24h**: Volumen de liquidaciones por hora
- **Dominancia del Mercado**: Distribución de capitalización (Bitcoin, Ethereum, Otros)

### 🧠 Análisis de Sentimiento
- **Índice de Miedo y Codicia**: Medidor radial con tendencia histórica
- **Sentimiento por Fuente**: Análisis de Reddit, Twitter, Noticias y Telegram
- **Métricas de Engagement**: Número de posts, cambios porcentuales y confianza
- **Resumen General**: Clasificación bullish/bearish con nivel de confianza

### ⚡ Señales de Trading
- **Señales Activas**: Monitoreo de señales BUY/SELL/HOLD en tiempo real
- **Indicadores Técnicos**: RSI, MACD, Bollinger Bands, Volumen
- **Historial de Señales**: Registro completo con P&L y tasa de acierto
- **Niveles de Confianza**: Clasificación de señales por fuerza (STRONG/MEDIUM/WEAK)
- **Alertas de Mercado**: Notificaciones para señales de alta confianza

### 📰 Noticias y Redes Sociales
- **Noticias Recientes**: Últimas noticias categorizadas por tipo y sentimiento
- **Posts de Redes Sociales**: Contenido de Reddit y Twitter con métricas de engagement
- **Trending Topics**: Hashtags y menciones más populares con cambios porcentuales

## 🛠️ Tecnologías Utilizadas

### Frontend
- **React 18**: Framework principal para la interfaz de usuario
- **Vite**: Herramienta de build y desarrollo rápido
- **Tailwind CSS**: Framework de CSS para diseño responsive
- **Recharts**: Librería de gráficos interactivos
- **Lucide React**: Iconos modernos y consistentes
- **shadcn/ui**: Componentes de UI reutilizables

### Backend (Scripts de Ingesta)
- **Python 3.11**: Lenguaje principal para scripts de datos
- **Requests**: Cliente HTTP para APIs
- **Pandas**: Manipulación y análisis de datos
- **PRAW**: Cliente de Reddit API
- **yfinance**: Datos financieros de Yahoo Finance
- **Boto3**: Cliente de AWS S3/Cloudflare R2

### APIs Integradas
- **Binance API**: Datos de precios y volumen en tiempo real
- **Coinglass API**: Métricas de derivados y liquidaciones
- **St. Louis FRED**: Datos macroeconómicos
- **Reddit API**: Análisis de sentimiento de comunidades crypto
- **RSS Feeds**: Noticias de fuentes especializadas

## 📁 Estructura del Proyecto

```
btc-dashboard/
├── btc-dashboard-frontend/          # Frontend React
│   ├── src/
│   │   ├── components/              # Componentes React
│   │   │   ├── Dashboard.jsx        # Componente principal
│   │   │   ├── PriceChart.jsx       # Gráfico de precios
│   │   │   ├── MarketMetrics.jsx    # Métricas del mercado
│   │   │   ├── SentimentAnalysis.jsx # Análisis de sentimiento
│   │   │   ├── TradingSignals.jsx   # Señales de trading
│   │   │   └── NewsAndSocial.jsx    # Noticias y redes sociales
│   │   ├── App.jsx                  # Aplicación principal
│   │   └── main.jsx                 # Punto de entrada
│   ├── dist/                        # Build de producción
│   └── package.json                 # Dependencias del frontend
├── btc-dashboard-backend/           # Scripts de backend
│   ├── scripts/                     # Scripts de ingesta de datos
│   │   ├── ingest_binance.py        # Datos de Binance
│   │   ├── ingest_coinglass.py      # Datos de Coinglass
│   │   ├── ingest_fred.py           # Datos de St. Louis FRED
│   │   ├── ingest_yfinance.py       # Datos de Yahoo Finance
│   │   ├── ingest_reddit.py         # Datos de Reddit
│   │   └── upload_to_r2.py          # Subida a Cloudflare R2
│   ├── config/                      # Configuración
│   ├── data/                        # Datos locales
│   └── requirements.txt             # Dependencias de Python
└── README.md                        # Documentación
```

## 🚀 Instalación y Configuración

### Prerrequisitos
- Node.js 18+ y npm
- Python 3.11+
- Cuentas en APIs (Binance, Reddit, etc.)

### Frontend
```bash
cd btc-dashboard-frontend
npm install
npm run dev  # Desarrollo
npm run build  # Producción
```

### Backend
```bash
cd btc-dashboard-backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Variables de Entorno
Crear archivo `.env` en el directorio backend:
```env
BINANCE_API_KEY=tu_api_key
BINANCE_SECRET_KEY=tu_secret_key
REDDIT_CLIENT_ID=tu_client_id
REDDIT_CLIENT_SECRET=tu_client_secret
REDDIT_USER_AGENT=tu_user_agent
CLOUDFLARE_R2_ACCESS_KEY=tu_access_key
CLOUDFLARE_R2_SECRET_KEY=tu_secret_key
CLOUDFLARE_R2_BUCKET=tu_bucket
```

## 📊 Fuentes de Datos

### Datos de Precios y Mercado
- **Binance**: Precios en tiempo real, volumen, datos OHLCV
- **Coinglass**: Open interest, funding rates, liquidaciones
- **Yahoo Finance**: Datos de mercados tradicionales

### Análisis de Sentimiento
- **Reddit**: Posts de r/Bitcoin, r/CryptoCurrency
- **RSS Feeds**: Noticias de CoinDesk, CoinTelegraph
- **Análisis de Texto**: Procesamiento de sentimiento con NLP

### Indicadores Técnicos
- **RSI (14)**: Índice de Fuerza Relativa
- **MACD**: Convergencia/Divergencia de Medias Móviles
- **Bollinger Bands**: Bandas de volatilidad
- **Volumen**: Análisis de volumen de trading

## 🎨 Características de Diseño

### Tema Oscuro Profesional
- Gradientes púrpura y azul para el fondo
- Tarjetas con transparencia y blur effects
- Colores consistentes para diferentes tipos de datos

### Responsive Design
- Adaptable a desktop, tablet y móvil
- Grid layouts flexibles
- Componentes que se reorganizan según el tamaño de pantalla

### Interactividad
- Gráficos con tooltips informativos
- Navegación por pestañas
- Actualización automática cada 30 segundos
- Botón de actualización manual

## 📈 Métricas y KPIs

### Rendimiento del Sistema
- **Tasa de Acierto**: Porcentaje de señales exitosas
- **P&L Total**: Ganancia/pérdida acumulada
- **Confianza Promedio**: Nivel de confianza de señales activas
- **Tiempo de Respuesta**: Latencia de actualización de datos

### Métricas de Mercado
- **Volatilidad**: Medida de fluctuación de precios
- **Liquidez**: Volumen de trading disponible
- **Momentum**: Tendencia direccional del precio
- **Correlaciones**: Relación con otros activos

## 🔧 Configuración Avanzada

### Personalización de Alertas
- Configurar umbrales para señales de trading
- Personalizar fuentes de noticias
- Ajustar frecuencia de actualización

### Integración con APIs Adicionales
- Agregar nuevos exchanges
- Incorporar más fuentes de noticias
- Expandir análisis de redes sociales

## 📱 Uso del Dashboard

### Navegación Principal
1. **Resumen**: Vista general con métricas clave
2. **Gráficos**: Análisis técnico detallado
3. **Métricas**: Datos del mercado de derivados
4. **Sentimiento**: Análisis de redes sociales
5. **Señales**: Recomendaciones de trading

### Interpretación de Señales
- **Verde (BUY)**: Señal de compra
- **Rojo (SELL)**: Señal de venta
- **Amarillo (HOLD)**: Mantener posición
- **Fuerza**: STRONG > MEDIUM > WEAK

### Análisis de Sentimiento
- **0-25**: Miedo Extremo (Oportunidad de compra)
- **25-45**: Miedo (Precaución)
- **45-55**: Neutral
- **55-75**: Codicia (Precaución)
- **75-100**: Codicia Extrema (Considerar venta)

## 🤝 Contribuciones

Este proyecto está diseñado como un sistema completo de análisis de Bitcoin. Para contribuir:

1. Fork del repositorio
2. Crear rama para nueva funcionalidad
3. Implementar cambios con tests
4. Enviar pull request

## 📄 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## 📞 Soporte

Para soporte técnico o preguntas sobre el dashboard:
- Revisar la documentación
- Verificar logs de errores
- Contactar al equipo de desarrollo

---

**Desarrollado con ❤️ para la comunidad crypto**

