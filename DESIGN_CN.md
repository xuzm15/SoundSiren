# SoundSiren 设计草案（Updated Vision）

目标：将“日常语音 -> 高保真歌唱”的复杂流水线抽象为极简接口，实现“输入即所得”。

> English version: `DESIGN.md`

---

## 1. 产品定义
- 一句话：SoundSiren 是一个 Zero‑Shot 的语音转歌唱系统，用极短语音样本即可生成带有个性声纹的歌唱。
- 受众：
  - 创作者：快速生成个人声线的歌唱 demo
  - AIGC 工具链开发者：需要高层接口与可编排的声线转换能力
  - 研究人员：关注高保真声纹迁移、旋律与情感建模

## 2. 核心承诺（产品级）
- Zero‑Shot 身份提取：无需微调，少量语音即可锁定声纹特征。
- 端到端自动化：搜索、分离、音高控制、合成、渲染一体化。
- LLM 编排（规划中）：从检索到情感/风格的中间层编排。
- 极简交互：复杂信号处理隐藏于简单 API/CLI。

## 3. 当前实现（MVP 已落地）
### 3.1 已实现能力
- 本地/检索歌曲输入（`song_query` 支持本地路径）
- 伴奏/人声分离（Demucs）
- 歌唱变声（Seed‑VC 外部调用）
- 混音渲染（FFmpeg）
- Demo 模式：默认 30 秒，加速验证效果
- 基础降噪：人声/伴奏/转换后人声轻量降噪

### 3.2 已知限制
- YouTube 下载可能触发验证码，需要 cookies
- 本机推理速度偏慢，完整歌曲耗时长
- Seed‑VC 输出仍可能出现“电音/颤音”，需参数调优

## 4. 体验与交互（首版）
1. 上传 3–30 秒日常语音
2. 输入歌曲名/链接（或本地文件）+ 可选情感描述
3. 系统执行：检索/分离/转换/混音
4. 输出：歌唱音频（demo/整曲）

交互形态：
- API（优先）
- CLI（优先）
- Web 控制台（演示用）

## 5. 系统架构（当前版）
```
Input Speech + Song Query
        |
   [Song Retrieval] -> (optional cookies)
        |
   [Source Separation (Demucs)]
        |
   [Seed-VC Conversion]
        |
   [Denoise + Mixdown]
        |
   Output Audio
```

## 6. API 设计（当前）
`POST /v1/sing`
- input:
  - `voice_samples[]` (audio)
  - `song_query` (string 或本地路径)
  - `demo_seconds` (optional, default=30)
  - `output_format` (optional)
- output:
  - `job_id`
  - `preview_url`
  - `output_path`

`GET /v1/jobs/{id}`
- output:
  - `status`
  - `result_urls[]`
  - `metadata`

## 7. 质量目标（MVP）
- 音色一致性：主观相似度可接受
- 旋律准确性：保留原唱旋律
- 合成自然度：减少电音/颤音
- Demo 时延：2–8 分钟（本机推理）

## 8. 风险与对策
- 版权来源：优先支持本地文件，下载时提示 cookies
- 样本质量：建议干净/近讲录音
- 推理时长：默认 demo 模式，整曲需更高算力

## 9. 后续里程碑
- M0：当前 MVP 已完成（demo pipeline）
- M1：音色相似度优化（F0 平滑 / 模型调参 / 去噪）
- M2：LLM 编排与多版本生成
- M3：Web 控制台与多语言支持

---
下一步：明确产品路线（Zero‑Shot 真实 SVS vs. SVC），再决定训练/推理体系升级。
