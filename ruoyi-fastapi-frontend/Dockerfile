# 构建阶段
FROM node:24-slim AS builder
WORKDIR /app

# 复制源代码
COPY . .

# 安装依赖
RUN npm install

# 执行docker构建命令（提高 Node 堆上限，避免 vite 构建 OOM）
ENV NODE_OPTIONS=--max-old-space-size=4096
RUN npm run build:docker

# 运行阶段
FROM nginx:latest
WORKDIR /usr/share/nginx/html

# 复制构建产物
COPY --from=builder /app/dist .

# 暴露端口
EXPOSE 80

# 启动nginx
CMD ["nginx", "-g", "daemon off;"]