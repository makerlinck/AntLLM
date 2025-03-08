# AntLLM 🐜
 **智能图片管家** | **An Intelligent Image Organizer**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python Version](https://img.shields.io/badge/python-3.11-blue)
---

## 项目概述 📌 | Overview
基于 **🦜️🔗 LangChain ** 和 ** Deepdanbooru-tagger-mini ** 的智能图片管理系统，实现：
- 🖼️ 自动化图片归档分类
- 🏷️ 智能语义标签生成
- 🚀 即将支持 Eagle 媒体库集成

---

## 功能特性 ✨ | Features
| 当前功能 | 开发路线图 |
|----------|------------|
| ✅ 多格式图片支持（JPG/PNG/WebP） | 🔜 Eagle 软件集成 |
| ✅ 语义理解分类 | 🔜 高性能矢量检索数据库 |
| ✅ AI自动标签生成 | 🔜 主流创意软件插件开发 |
|  | 🔜 团队协作功能 |

---

## 快速开始 🚀 | Quick Start
### 环境准备 | Environment Preparation
```bash
# 安装依赖
$ pip install -r requirements.txt

# 启动Ollama服务
$ ollama serve
$ ollama pull qwen2.5:3b
$ wget https://github.com/KichangKim/DeepDanbooru/releases/download/v4-20200814-sgd-e30/deepdanbooru-v4-20200814-sgd-e30.zip
```
将deepdanbooru-v4-20200814-sgd-e30.zip解压后的内容放入./deepdanbooru_v4e30文件夹中。
### 基本使用 | Basic Usage
```bash

$ python ./bin/test_run_deepmini.py
#在第一次运行以后默认会在工作目录产生origin和output文件夹，origin文件夹为原始图片，output文件夹为自动分类后的图片。
# 将原始图片放入origin文件夹中，再次运行即可自动进行分类。
```


## 目录结构 🌳 | Directory Structure

```text
AntLLM/
├── bin/                  - 核心源代码
│   ├── deepmini          - deepmini模块 (Deepdanbooru 剪枝版，仅保留tagger核心功能;遵循MIT协议，源仓库地址: https://github.com/KichangKim/DeepDanbooru)
│   ├── file_manager/     - 文件路径管理操作模块
│   └── image_viewer.py   - 图片审查模块
├── .config/              - 配置文件
│   └── settings.yaml     - 应用配置
│
│
├── docs-n/               - 项目文档
├── requirements.txt      - Python依赖
└── README.md             - 项目说明
```

## 参与贡献 🤝 | Contribute
欢迎通过 Issue 提交建议或通过 PR 贡献代码：

- Fork 项目仓库
- 创建特性分支
- 提交修改
- 推送分支
- 发起 Pull Request

## 许可协议 📄 | License
本项目采用 MIT License

