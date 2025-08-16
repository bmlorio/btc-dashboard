## Tareas Pendientes para el Dashboard de Bitcoin

### Fase 1: Análisis de documentos y planificación
- [x] Leer el documento principal del dashboard de Bitcoin.
- [x] Leer la guía de ejecución paso a paso del dashboard de Bitcoin.
- [x] Resumir los requisitos clave y la arquitectura del sistema.

### Fase 2: Búsqueda de APIs y datos de Bitcoin
- [x] Identificar las APIs necesarias para la ingesta de datos (Binance, Coinglass, Glassnode, St. Louis FRED, yfinance, RSS, Reddit).
- [x] Investigar la disponibilidad y los límites de uso de cada API, especialmente Coinglass y Glassnode para opciones gratuitas/bajo costo.

### Fase 3: Desarrollo del backend con APIs de datos
- [x] Configurar el entorno de desarrollo local (Python, venv, librerías).
- [x] Crear scripts de ingesta de datos para cada API.
- [x] Desarrollar el script para subir datos a Cloudflare R2.
- [ ] Desplegar los scripts en el VPS y configurar variables de entorno.
- [ ] Configurar n8n para orquestar la ingesta y subida de datos.

### Fase 4: Desarrollo del frontend del dashboard
- [x] Configurar el proyecto Next.js para exportación estática.
- [x] Desarrollar componentes React para cada widget del dashboard.
- [x] Conectar el frontend con los datos almacenados en Cloudflare R2.
- [ ] Configurar el despliegue automático en Vercel/Cloudflare Pages.

### Fase 5: Integración y pruebas del sistema completo
- [x] Implementar el motor de decisión en un script de Python.
- [x] Integrar el motor de decisión en el flujo de n8n.
- [x] Configurar alertas de mercado y monitoreo del pipeline en n8n.
- [x] Realizar pruebas exhaustivas de todo el sistema.

### Fase 6: Despliegue y entrega del dashboard
- [x] Preparar el código fuente para GitHub.
- [x] Exportar los workflows de n8n.
- [x] Generar la URL pública del dashboard.
- [x] Crear la documentación (README.md).
- [x] Entregar los resultados al usuario.

