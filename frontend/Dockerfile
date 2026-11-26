# Imagen base de Node.js
FROM node:22-alpine

WORKDIR /app

# Instala las dependencias de React primero para aprovechar la caché
COPY package.json package-lock.json ./
RUN npm ci

# Código del frontend
COPY . .

EXPOSE 5173

# --host 0.0.0.0 hace que Vite escuche en todas las redes del contenedor;
# sin esto el navegador del equipo no puede entrar y la página sale en blanco
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
