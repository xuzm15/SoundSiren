# SoundSiren

SoundSiren: Zero-Shot Neural Vocal Morphing

中文 README。English version: `README.md`。

SoundSiren 是一款将日常语音转化为高保真歌唱的端到端系统。通过解耦声纹身份与旋律属性，支持用短语音样本进行零样本歌唱转换。

## 核心特性
- Zero-shot 身份提取
- 端到端流水线：搜索、分离、音高控制、合成、渲染
- LLM 编排逻辑（规划中）
- 极简 API 接口

## 目录结构
- `src/soundsiren/` 核心逻辑
- `src/soundsiren/api/` API 入口
- `src/soundsiren/core/` Pipeline 模块
- `web/` 控制台原型
- `tests/` 测试占位

## 快速开始
```bash
# 系统依赖
brew install ffmpeg

# 一键准备（克隆 Seed-VC + 安装依赖）
./scripts/bootstrap.sh

# 如果 macOS + Python 3.13 遇到 SciPy 编译失败，建议使用 Python 3.11
# brew install python@3.11
# SOUNDSIREN_PYTHON=python3.11 ./scripts/bootstrap.sh

# 启动 API
./scripts/run_demo.sh

# 发送请求（默认 30 秒 demo）
./scripts/request_demo.sh "Song Name or URL" /path/to/your_voice.wav

# 或使用本地歌曲文件（绕过下载限制）
./scripts/request_demo.sh /path/to/song.wav /path/to/your_voice.wav
```

## 配置
```bash
export SOUNDSIREN_WORKDIR=./runs
export SOUNDSIREN_SEED_VC_DIR=/path/to/seed-vc
export SOUNDSIREN_VC_BACKEND=external
export SOUNDSIREN_VC_COMMAND="bash scripts/seed_vc_convert.sh --input $input --output $output --reference $reference"

# 可选：降噪（默认开启）
export SOUNDSIREN_DENOISE=1
export SOUNDSIREN_DENOISE_NF=-25

# 可选：yt-dlp cookies
export SOUNDSIREN_YTDLP_COOKIES=/path/to/youtube_cookies.txt
export SOUNDSIREN_YTDLP_COOKIES_FROM_BROWSER=edge
```

## 说明
- 当前实现包含下载、分离与混音流程，声纹转换通过外部命令接入。
- 未配置声纹转换时，会直接混合原曲人声（仅用于流程跑通）。
- `song_query` 可使用本地音频路径绕过下载限制。
- 默认请求为 30 秒 demo，可用 `demo_seconds` 调整。

## Seed-VC
1. 克隆 Seed-VC 并安装依赖
2. 配置 `SOUNDSIREN_SEED_VC_DIR`
3. 设置 `SOUNDSIREN_VC_COMMAND`

## 重要提示
- 首次运行会从 Hugging Face 下载模型权重。
- 全曲转换计算量大。

## 路线图
见 `ROADMAP.md`。

## 文档
- 设计草案：`DESIGN.md`
