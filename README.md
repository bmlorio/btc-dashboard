BTC Dashboard

Repositorio monorepo para el dashboard de trading de Bitcoin.

Contenido
- `btc-dashboard-frontend/` - Aplicación frontend (Vite + React + Tailwind).
- `btc-dashboard-backend/` - Scripts y backend (Python).

Arrancar en local
1. Frontend
```bash
cd btc-dashboard-frontend
pnpm install
pnpm run dev
# o
npx vite --port 5173 --host 127.0.0.1
```
2. Backend (ejemplo)
```bash
cd btc-dashboard-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
# ejecutar scripts según necesidad
```

Buenas prácticas
- No subir `node_modules` ni archivos de configuración con credenciales.
- Usa `git` + PRs y protection rules en GitHub para merges a `main`.

Contacto
- Repo: https://github.com/bmlorio/btc-dashboard
