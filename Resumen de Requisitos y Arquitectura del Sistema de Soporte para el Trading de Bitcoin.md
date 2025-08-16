
# Resumen de Requisitos y Arquitectura del Sistema de Soporte para el Trading de Bitcoin

## Visión General
El objetivo principal es crear un Sistema de Soporte a la Decisión (DSS) autónomo para el trading de Bitcoin, consolidando análisis multidimensional en un tablero web único. El sistema debe generar una recomendación diaria (Comprar/Vender/No Operar) y un informe detallado a las 09:00 ART.

## Alcance del Proyecto
*   **Producto Principal:** Un tablero de control web estático, de bajo mantenimiento y alta disponibilidad.
*   **Backend/Pipeline de Datos:** Un sistema automatizado de ingesta, procesamiento y almacenamiento de datos.
*   **Motor de Decisión:** Scripts con lógica predefinida para generar señales y la decisión diaria.
*   **Sistema de Alertas:** Notificaciones en tiempo real (Telegram/Discord) basadas en condiciones críticas del mercado.
*   **NO incluido en el MVP:** Ejecución de trades, gestión de portafolio en vivo, autenticación de usuarios.

## Arquitectura de la Solución y Stack Tecnológico
La arquitectura está optimizada para bajo costo, escalabilidad y evitar el vendor lock-in.

**Flujo de Datos:**
APIs Externas → Ingesta (Python) → Orquestación (n8n) → Almacenamiento (S3-compatible) → Lógica de Decisión (Python) → Frontend (React/Next.js)

**Componentes Clave:**
*   **Orquestación:** n8n (self-hosted) para flujos de trabajo (CRON, triggers).
*   **Scripts/Lógica:** Python 3.10+ (Pandas, Pydantic, Requests, CCXT, Boto3).
*   **Almacenamiento:** Cloudflare R2 / Backblaze B2 (alternativas a AWS S3 con costos de transferencia bajos/nulos, ideal para servir JSON al frontend).
*   **Frontend:** Next.js (Static Export) para un sitio 100% estático, rápido y seguro.
*   **Hosting Frontend:** Vercel / Cloudflare Pages (optimizadas para Next.js con CDN global y despliegue continuo).
*   **Alertas:** Telegram / Discord (vía n8n).
*   **Backtesting:** Python (local) usando datos históricos en formato Parquet.

## Fuentes de Datos y APIs
Se priorizan APIs robustas, gratuitas y con límites de tasa razonables:
*   **Técnico:** Binance API (klines, openInterest).
*   **Derivados:** Coinglass API (funding, liquidation/map).
*   **On-Chain:** Glassnode API (SOPR, MVRV, flujos) - datos con 24h de latencia.
*   **Macro:** St. Louis FRED API (DXY, Tasas), yfinance (SPY, QQQ, GLD).
*   **Noticias:** RSS Feeds (Coindesk, The Block).
*   **Redes:** PRAW (Reddit API).

## Diseño del Dashboard: UI, Widgets y KPIs
El diseño será denso en información pero claro, priorizando la 


"escaneabilidad" para la toma de decisiones a las 09:00 ART.

**Layout:** Un grid de 3 columnas:
*   **Columna Izquierda:** Contexto (Macro y Narrativa).
*   **Columna Central:** Acción del Precio (Técnico).
*   **Columna Derecha:** Flujos de Mercado (Derivados y On-Chain).

**Widgets y KPIs Clave:**
*   **Macro Snapshot:** DXY, S&P500 Futures, Oro (mini-gráficos de línea 24h).
*   **Calendario Económico:** Próximos 3 eventos con nivel de impacto.
*   **Feed de Narrativas:** Top 5 posts de r/Bitcoin + titulares de RSS curados.
*   **Gráfico Principal:** Gráfico de BTC/USD (4H) con EMAs 21/50/200, S/R.
*   **Indicadores de Momentum:** Gauges para RSI y MACD en TF 1D y 4H.
*   **Volatilidad:** Gráfico de línea simple para ATR (14D) y HV (30D).
*   **Perfil de Volumen (VPVR):** Barras horizontales sobre el gráfico principal.
*   **Métricas de Derivados:** Tabla con Funding Rate, OI Agregado, P/C Ratio.
*   **Mapa de Liquidaciones:** Gráfico de barras mostrando pools de liquidez.
*   **Métricas On-Chain Clave:** Tabla con SOPR, MVRV Z-Score, Flujo Neto a Exchanges.
*   **Panel de Decisión (Header):** [COMPRAR / VENDER / NEUTRAL] + Precio actual + Cambio 24h.

## Plan de Desarrollo e Implementación por Fases

*   **Fase 1: Pipeline de Datos (Backend Core) - 3 semanas:**
    *   Configurar Infraestructura (R2/B2, n8n en VPS).
    *   Desarrollar Scripts de Ingesta (Python) para cada fuente de datos (JSON/Parquet en bucket).
    *   Crear Workflows de Orquestación en n8n (CRON, llama scripts de ingesta).
    *   **Entregable:** Bucket S3 poblado de forma confiable y automática con datos crudos.

*   **Fase 2: Motor de Lógica y Señales (El Cerebro) - 2 semanas:**
    *   Desarrollar Script de Procesamiento (`process_signals.py`) para leer datos crudos.
    *   Implementar Lógica: Calcular indicadores derivados, normalizar datos, llenar "Tabla de Señales".
    *   Implementar Motor de Decisión: Generar `salida_diaria.json` con la recomendación.
    *   Integrar en n8n al final del workflow principal.
    *   **Entregable:** Archivo `salida_diaria.json` generado y actualizado automáticamente en el bucket.

*   **Fase 3: Desarrollo del Frontend (La Interfaz) - 4 semanas:**
    *   Setup del Proyecto Next.js para exportación estática.
    *   Construir Componentes de UI (React) para cada widget.
    *   Conectar Datos: Frontend hace fetch de `salida_diaria.json` y otros archivos desde R2/B2.
    *   Desplegar: Configurar despliegue automático en Vercel/Cloudflare Pages.
    *   **Entregable:** URL pública con el dashboard funcional y auto-actualizable.

*   **Fase 4: Sistema de Alertas y Monitoreo - 1 semana:**
    *   Crear Workflows de Alertas en n8n (ej: cada 5 min para Funding Rate).
    *   Implementar Monitoreo del Pipeline: Manejo de errores en workflow principal para notificar fallos.
    *   **Entregable:** Alertas proactivas y monitoreo de la salud del sistema.

## Modelo de Decisión Automatizado y Gestión de Riesgo
La lógica se implementa en `process_signals.py`.

**1. Ponderación de Señales:**
Se asigna un puntaje (-2 a +2) a cada señal con un peso específico (Bajo, Medio, Alto) para indicadores como Estructura (1D), RSI (1D), Funding Rate, Flujo Neto Exchanges, SOPR, y Contexto Macro.

**2. Cálculo del Score Final:**
`Score Total = Σ (Puntaje de Señal * Peso)`

**3. Reglas de Decisión:**
*   `Score Total >= 5` → COMPRAR
*   `Score Total <= -5` → VENDER
*   `EN OTRO CASO` → NEUTRAL

**4. Parámetros de Riesgo (para ejecución manual):**
*   **Stop Loss:** Calculado usando ATR (14).
*   **Take Profit:** Basado en S/R o extensiones de Fibonacci (R:R mínimo 1.5).
*   **Tamaño de Posición:** Calculado en base a Capital Total, Riesgo por Trade y Distancia al Stop Loss.

## Entregables Finales y Plantillas
*   Código Fuente (GitHub: Next.js frontend y scripts Python).
*   Workflows de n8n (archivos JSON exportables).
*   URL del Dashboard (enlace público).
*   Documentación (README.md).
*   Plantilla de Salida: `salida_diaria.json` con `timestamp_utc`, `decision_del_dia`, `score_total`, `resumen_ejecutivo`, `tabla_de_senales`, y `plan_de_trade_sugerido`.

## Guía de Ejecución Paso a Paso (Metodología)
*   **Construye local, despliega en la nube:** Desarrollar y probar localmente antes de desplegar.
*   **Git es tu red de seguridad:** Uso de Git para control de versiones y commits frecuentes.
*   **Un paso a la vez:** No avanzar hasta que el paso actual esté 100% funcional.

**Fase 0: Preparación del Campo de Batalla (Configuración Inicial):**
*   Preparar entorno local (MacBook: Homebrew, Python con pyenv, Node.js con nvm, VSC con extensiones, Git).
*   Preparar infraestructura Cloud (Hostinger VPS, Cloudflare R2: crear bucket público, obtener API keys; GitHub: crear repos `btc-dashboard-backend` y `btc-dashboard-frontend`).
*   Recolectar API Keys (Binance, Glassnode, St. Louis FRED, Reddit).

**Fase 1: Construir el Pipeline de Datos (Backend):**
*   Estructura del Proyecto Backend (clonar repo, entorno virtual, `requirements.txt`, `.gitignore`, carpeta `scripts/`).
*   Script de Ingesta #1: Binance (`ingest_binance.py`).
*   Script para Subir a R2 (`upload_to_r2.py`).
*   Repetir para todas las fuentes.
*   Desplegar scripts en VPS (git push, SSH, variables de entorno).
*   Orquestación con n8n (workflow CRON, `Execute Command` para scripts de ingesta y subida a R2).

**Fase 2: El Cerebro (Motor de Lógica):**
*   Desarrollo del Script de Procesamiento (`process_signals.py`) en Mac: descargar JSON de R2, cargar en Pandas, calcular indicadores, aplicar lógica de ponderación, generar `salida_diaria.json`.
*   Integración en n8n: subir `process_signals.py` a GitHub, actualizar repo en VPS, añadir nodo `Execute Command` en n8n para ejecutar `process_signals.py` y subir `salida_diaria.json` a R2.

**Fase 3: La Cara del Proyecto (Frontend):**
*   Estructura del Proyecto Frontend (clonar repo, `create-next-app`, limpiar código).
*   Conexión de Datos: Fetch de `salida_diaria.json` desde R2 en Next.js Server Component.
*   Construcción de Widgets (componentes React con TypeScript y Tailwind CSS, TradingView Lightweight Charts).
*   Despliegue con Vercel (importar repo, deploy).
*   Auto-actualización Diaria: Configurar Deploy Hook en Vercel y añadir nodo `HTTP Request` en n8n para activar reconstrucción del sitio.

**Fase 4: El Guardián (Alertas y Monitoreo):**
*   Alertas de Mercado en n8n: Nuevo workflow CRON (cada 15 min), HTTP Request a Coinglass, nodo IF para umbral, nodo Telegram para notificación.
*   Alertas de Fallo del Sistema: `Continue on Fail` en nodos de n8n, nodo IF al final para verificar errores, notificación a Telegram si falla el pipeline.

## Uso de Gemini Code Assist
La guía detalla cómo usar Gemini Code Assist en VS Code para cada fase del proyecto, proporcionando prompts específicos para generar código Python (scripts de ingesta, lógica de procesamiento) y componentes React (widgets, conexión de datos, gráficos), así como para depuración. Se enfatiza la importancia de ser específico, proporcionar contexto, refinar las respuestas y revisar el código generado.

