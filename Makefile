# AI Assistant 项目主Makefile
# 用于管理backend和frontend的启动和开发

# 项目路径
PROJECT_ROOT := $(PWD)
BACKEND_DIR := $(PROJECT_ROOT)/backend
FRONTEND_DIR := $(PROJECT_ROOT)/frontend

# 默认目标
default: help

# 启动backend服务器
backend:
	@echo "启动Backend服务器..."
	cd $(BACKEND_DIR) && make run

# 启动frontend开发服务器
frontend:
	@echo "启动Frontend开发服务器..."
	cd $(FRONTEND_DIR) && pnpm dev

# 同时启动backend和frontend（使用后台进程）
start:
	@echo "同时启动Backend和Frontend..."
	@echo "启动Backend服务器（后台运行）..."
	cd $(BACKEND_DIR) && make run &
	@sleep 3
	@echo "启动Frontend开发服务器..."
	cd $(FRONTEND_DIR) && pnpm dev

# 安装所有依赖
install:
	@echo "安装Backend依赖..."
	cd $(BACKEND_DIR) && make install
	@echo "安装Frontend依赖..."
	cd $(FRONTEND_DIR) && pnpm i

# 构建项目
build:
	@echo "构建Frontend..."
	cd $(FRONTEND_DIR) && pnpm build

# 清理项目
clean:
	@echo "清理Backend缓存..."
	cd $(BACKEND_DIR) && make clean
	@echo "清理Frontend缓存..."
	cd $(FRONTEND_DIR) && rm -rf .next

# 格式化代码
format:
	@echo "格式化Backend代码..."
	cd $(BACKEND_DIR) && make format
	@echo "格式化Frontend代码..."
	cd $(FRONTEND_DIR) && npx prettier --write .

# 检查代码质量
check:
	@echo "检查Backend代码..."
	cd $(BACKEND_DIR) && make check
	@echo "检查Frontend代码..."
	cd $(FRONTEND_DIR) && pnpm lint

# 显示帮助信息
help:
	@echo "AI Assistant 项目 Makefile 命令:"
	@echo ""
	@echo "  启动命令:"
	@echo "    make backend        - 启动Backend服务器"
	@echo "    make frontend       - 启动Frontend开发服务器"
	@echo "    make start          - 同时启动Backend和Frontend"
	@echo ""
	@echo "  开发命令:"
	@echo "    make install        - 安装所有依赖"
	@echo "    make build          - 构建项目"
	@echo "    make clean          - 清理缓存文件"
	@echo "    make format         - 格式化代码"
	@echo "    make check          - 检查代码质量"
	@echo "    make help           - 显示此帮助信息"
	@echo ""
	@echo "  单独目录命令:"
	@echo "    cd backend && make help  - 查看Backend更多命令"
	@echo "    cd frontend && pnpm run   - 查看Frontend更多命令"

.PHONY: default backend frontend start install build clean format check help