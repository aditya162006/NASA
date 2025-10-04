# syntax=docker/dockerfile:1
FROM node:20-alpine AS build
WORKDIR /app
# Copy only the manifests first for better caching
COPY package.json pnpm-lock.yaml* ./
RUN corepack enable && corepack prepare pnpm@9.10.0 --activate
RUN pnpm install --frozen-lockfile || pnpm install
# Copy the rest of the source
COPY . .
RUN pnpm build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
