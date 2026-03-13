# 变量定义，方便后续修改
PYTHON = uv run
BUILD = uv build

.PHONY: build test clean all

# 默认目标：直接输入 make 就会执行这个
all: build test

# 构建所有包
build:
	$(BUILD) --all-packages

# 运行测试脚本
test:
	$(PYTHON) alisa-test

# 清理构建产物
clean:
	@if exist dist rmdir /s /q dist
	@echo "🧹 Cleaned dist directory"

# 一键式：先构建再测试
rebuild-test: clean build test