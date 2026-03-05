#!/bin/bash

# 打包脚本 - 将项目打包成 tar.gz 文件

echo "=========================================="
echo "  公务员培训助手 - 项目打包"
echo "=========================================="
echo ""

PROJECT_DIR="/workspace/projects"
PACKAGE_NAME="civil-service-assistant"
OUTPUT_DIR="/tmp"

# 进入项目目录
cd $PROJECT_DIR

# 创建临时目录
TEMP_DIR="/tmp/${PACKAGE_NAME}-package"
rm -rf $TEMP_DIR
mkdir -p $TEMP_DIR

echo "正在打包项目文件..."

# 复制项目文件
cp -r src $TEMP_DIR/
cp -r config $TEMP_DIR/
cp -r assets $TEMP_DIR/
cp -r scripts $TEMP_DIR/
cp -r docs $TEMP_DIR/
cp requirements.txt $TEMP_DIR/
cp README.md $TEMP_DIR/
cp .gitignore $TEMP_DIR/
cp .coze $TEMP_DIR/ 2>/dev/null || true

# 打包
cd $TEMP_DIR
tar -czf ${OUTPUT_DIR}/${PACKAGE_NAME}.tar.gz .

# 移动到项目根目录
mv ${OUTPUT_DIR}/${PACKAGE_NAME}.tar.gz $PROJECT_DIR/

# 清理临时目录
rm -rf $TEMP_DIR

echo ""
echo "=========================================="
echo "✓ 打包完成！"
echo "=========================================="
echo ""
echo "打包文件：${PROJECT_DIR}/${PACKAGE_NAME}.tar.gz"
echo ""
echo "上传到服务器的命令："
echo "  scp ${PROJECT_DIR}/${PACKAGE_NAME}.tar.gz root@your_server_ip:/tmp/"
echo ""
echo "在服务器上解压："
echo "  mkdir -p /opt/civil-service-assistant"
echo "  cd /opt/civil-service-assistant"
echo "  tar -xzf /tmp/${PACKAGE_NAME}.tar.gz"
echo ""
