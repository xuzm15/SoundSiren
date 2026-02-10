# SoundSiren 设计草案（Vision Draft）

目标：将“日常语音 -> 高保真歌唱”的复杂神经渲染流水线抽象为极简接口，做到“输入即所得”。

## 1. 产品定义
- 一句话：SoundSiren 是一个 Zero-Shot 的语音转歌唱合成系统，只需极短的日常语音样本即可生成带有个人声纹的任意歌曲演唱。
- 受众：
  - 创作者：想用自己的声音快速生成歌唱 demo
  - AIGC 工具链开发者：需要高层接口与可编排的语音合成能力
  - 研究人员：关注高保真声纹迁移、歌唱韵律与情感建模

## 2. 核心承诺（产品级）
- Zero‑Shot 身份提取：无需微调，少量语音样本即可锁定声纹身份。
- 端到端自动化：搜索、分离、校音、合成、渲染一体化闭环。
- LLM 驱动编排：将“找歌 -> 分离 -> 风格/情感 -> 生成”流程抽象成可编排的语言层。
- 极简交互：复杂信号处理隐藏于简单 API/CLI。

## 3. 体验与交互（首版）
### 3.1 用户流程
1. 上传 3–30 秒日常语音（或多段短音频）
2. 输入歌曲名/链接 + 可选情感描述
3. 系统自动完成：搜索/伴奏分离/音高修正/合成渲染
4. 输出：完整演唱音频 + 可选多版本（情感/风格）

### 3.2 交互形态
- API（优先）：面向开发者与工具链接入
- Web 控制台（可选）：演示、试听与参数调优
- CLI（可选）：批处理/内部调试

## 4. 系统架构（高层）
```
Input Audio + Song Query
        |
   [Identity Encoder] ----> Vocal Identity
        |
    [LLM Orchestrator] -> tasks: search -> stem -> pitch -> render
        |
   [Singing Synthesizer]
        |
   Rendered Singing
```

### 4.1 模块拆解
- Identity Encoder: 从少量语音抽取声纹向量
- Song Retrieval: 搜索歌曲及歌词/音频源
- Source Separation: 人声/伴奏分离
- Pitch Alignment: 将人声音高与目标旋律对齐
- Singing Synthesizer: 生成歌唱人声
- Mixing/Rendering: 与伴奏混合，输出可发布音频

## 5. LLM 编排层（中枢逻辑）
LLM 负责：多源查询、意图解析、风格/情感建模、异常兜底与多版本策略。
- 输入：用户 query、可用资源、目标风格
- 输出：可执行任务图 + 质量评估建议

## 6. API 设计（初稿）
### 6.1 核心接口
`POST /v1/sing`
- input:
  - `voice_samples[]` (audio)
  - `song_query` (string)
  - `emotion` (optional, string)
  - `style` (optional, string)
  - `output_format` (optional)
- output:
  - `job_id`
  - `preview_url`

`GET /v1/jobs/{id}`
- output:
  - `status`
  - `result_urls[]`
  - `metadata` (pitch, alignment, style tags)

### 6.2 设计原则
- 默认合理：用户不填参数也能得到可用结果
- 失败可解释：返回清晰的错误与修复建议
- 低学习成本：仅暴露必要选项

## 7. 质量目标（MVP）
- 音色一致性：与样本声纹高度一致（主观评分优先）
- 旋律准确性：音高偏差低于指定阈值
- 合成自然度：无明显电子噪声、气声衰减可控
- 端到端延迟：单曲 1–3 分钟内完成

## 8. 风险与对策
- 版权来源：提供可替换的检索/上传入口
- 语音样本质量：通过质量评估提示用户补录
- 歌曲难度差异：提供多版本 fallback（简化旋律）

## 9. 后续里程碑（建议）
- M0：API 原型 + 基础流水线
- M1：Zero‑Shot 身份提取增强 + 歌唱自然度提升
- M2：LLM 编排优化 + 多版本质量评估
- M3：Web 控制台 + 多语言支持

---
下一步：确认该设计方向与术语边界（产品/系统/模型），再进入代码与仓库初始化。
