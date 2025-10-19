#!/bin/bash

# 部署脚本 - FastAPI TodoApp
# 使用方法: ./deploy.sh [环境] [镜像标签]

set -e

# 默认值
ENVIRONMENT=${1:-production}
IMAGE_TAG=${2:-latest}
APP_NAME="todoapp"
REGISTRY="your-registry.com"  # 替换为你的容器注册表

echo "🚀 开始部署 $APP_NAME..."
echo "环境: $ENVIRONMENT"
echo "镜像标签: $IMAGE_TAG"

# 构建镜像
echo "📦 构建 Docker 镜像..."
docker build -t $APP_NAME:$IMAGE_TAG .

# 标记镜像
echo "🏷️  标记镜像..."
docker tag $APP_NAME:$IMAGE_TAG $REGISTRY/$APP_NAME:$IMAGE_TAG

# 推送镜像
echo "📤 推送镜像到注册表..."
docker push $REGISTRY/$APP_NAME:$IMAGE_TAG

# 部署到云平台 (示例: Kubernetes)
echo "☁️  部署到云平台..."
kubectl set image deployment/$APP_NAME $APP_NAME=$REGISTRY/$APP_NAME:$IMAGE_TAG

# 等待部署完成
echo "⏳ 等待部署完成..."
kubectl rollout status deployment/$APP_NAME

echo "✅ 部署完成!"
echo "🌐 应用访问地址: https://your-domain.com"
