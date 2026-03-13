# 前言

用 python 实现一套企业级别的 sdk，侧重于数据等后端处理相关服务，不涉及 UI 相关内容，其模块包括配置管理、自动重试、数据库连接、s3 存储等，具体如下

**基础层**：配置管理、环境管理、安全、日志、错误码&异常类型、时间类型处理
**网络层**：grpc、http、tcp、自动重试
**数据层**：数据库连接、s3 存储、 Mock 内存数据、消息队列、本地文件 IO
**业务层**：

文档
CI/CD

| 模块            | 功能                                        | 描述     |
| --------------- | ------------------------------------------- | -------- |
| alisa-env       | .env 支持                                   |          |
| alisa-config    | 保存读取 json 配置                          |          |
| alisa-storage   | s3、本地存储                                |          |
| alisa-data      | 提供数据库连接、redis 连接、消息中间件连接  |          |
| alisa-network   | 提供 grpc、http、tcp 、websocket 客户端支持 |          |
| alisa-time      | 处理时间格式                                |          |
| alisa-exception | 定义错误码、异常类型                        |          |
| alisa-log       | 处理日志                                    |          |
| alisa-security  | 提供身份验证、授权、加密                    | 暂未实现 |
| alisa-mock      | 提供假数据                                  | 暂未实现 |

# 实验环境

- uv
- python 3.12
- make

## 目标

- 模块隔离
- 层次分明
- 开箱即用
