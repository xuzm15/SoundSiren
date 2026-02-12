# SoundSiren

SoundSiren: Zero-Shot Neural Vocal Morphing

SoundSiren 是一款将日常语音（Speech）转化为高保真歌唱（Singing）的端到端合成系统。通过解耦声音的特征表征（Vocal Identity）与旋律属性，SoundSiren 允许用户仅凭极短的语音样本，即可跨越式地生成具备个人特征的任意歌曲。

## 核心特性
- Zero-Shot 身份提取：无需针对特定声音进行微调（Fine-tuning），通过少量日常对话音频即可提取声纹特征。
- 端到端全自动流水线：集成搜索、伴奏分离、音高修正与合成渲染。
- LLM 驱动的编排逻辑：利用 LLM 强大的理解能力，处理从歌曲搜索到情感建模的中间层逻辑。
- 极简式交互设计：将复杂的信号处理屏蔽在简单的 API 调用之下。

## 目录结构（初版）
- `src/soundsiren/` 核心逻辑
- `src/soundsiren/api/` API 入口
- `src/soundsiren/core/` Pipeline 与模块占位
- `web/` Web 控制台雏形
- `tests/` 测试占位

## 快速开始（占位）
```bash
# 系统依赖
brew install ffmpeg

# 一键准备（克隆 Seed-VC + 安装依赖）
./scripts/bootstrap.sh

# 如果 macOS + Python 3.13 遇到 SciPy 编译失败，建议安装 Python 3.11：
# brew install python@3.11
# SOUNDSIREN_PYTHON=python3.11 ./scripts/bootstrap.sh

# 启动 API
./scripts/run_demo.sh

# 发送请求（默认 demo 30 秒）
./scripts/request_demo.sh "Song Name or URL" /path/to/your_voice.wav

# 或使用本地歌曲文件（绕过下载限制）
./scripts/request_demo.sh /path/to/song.wav /path/to/your_voice.wav
```

## 配置
使用环境变量配置（示例）：
```bash
export SOUNDSIREN_WORKDIR=./runs
# 可选：外部声纹转换命令（Seed-VC）
export SOUNDSIREN_SEED_VC_DIR=/path/to/seed-vc
export SOUNDSIREN_VC_BACKEND=external
export SOUNDSIREN_VC_COMMAND="bash scripts/seed_vc_convert.sh --input $input --output $output --reference $reference"

# 可选：降噪（默认开启）
export SOUNDSIREN_DENOISE=1
export SOUNDSIREN_DENOISE_NF=-25

# 可选：yt-dlp cookies（用于 YouTube 下载）
export SOUNDSIREN_YTDLP_COOKIES=/path/to/youtube_cookies.txt
export SOUNDSIREN_YTDLP_COOKIES_FROM_BROWSER=edge
```

## 说明
- 当前实现包含下载、分离与混音流程，声纹转换通过外部命令接入。
- 未配置声纹转换时，系统会直接使用原曲人声做混音（仅用于流程跑通）。
- 歌曲名称查询会通过 `yt-dlp` 的搜索功能解析为来源链接，请确保具备相应内容的使用权限。
- 默认请求为 30 秒 demo（可通过 `demo_seconds` 表单字段调整）。
- 如果 YouTube 下载被限制，可改用本地歌曲文件路径作为 `song_query`。

## Seed-VC（零样本声纹转换）
1. 克隆 Seed-VC 仓库并安装依赖（请参考其 README）
2. 配置 `SOUNDSIREN_SEED_VC_DIR` 指向 seed-vc 目录
3. 通过 `SOUNDSIREN_VC_COMMAND` 启用转换脚本

## 重要提示
- 首次运行会从 Hugging Face 自动下载模型权重，请确保网络可用。
- 该流程会消耗 CPU/GPU 资源，完整歌曲可能耗时较长。
 - 若使用 YouTube 下载并遇到 “Sign in to confirm you’re not a bot”，请使用 cookies 文件：
   - `export SOUNDSIREN_YTDLP_COOKIES=/path/to/youtube_cookies.txt`

## 路线图
见 `ROADMAP.md`。

## 相关文档
- 设计草案：`DESIGN.md`
