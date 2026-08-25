# 虚构简历（测试夹具，人物/公司/项目/链接均不存在）

祁南舟 ｜ 21 岁 ｜ Full-Stack AI Agent Developer ｜ 求职方向：AI Infra
GitHub: github.com/example-candidate-xyz

## 教育
北屿理工大学 软件工程 本科 2022.09 - 2026.06

## 实习经历

**寰宇科技 · Agent 平台组 · 研发实习生** ｜ 2025.06 - 2026.05

开源 Agent Harness 项目「潮汐」（GitHub 32k stars · 4.1k forks）

**我的职责**：作为项目 owner 核心作者之一，主导 1.0 到 2.0 的架构升级与迭代

**2.0 架构（Agent Teams Harness + Middleware Chain + Skill System + Context Engineering）**：

- **Agent Teams Harness**：1.0 为五节点固定流水线，2.0 改为单一 Lead Agent 统一决策；Sub-agent 并发规则组装，线程池分离，最多 3 并发 / 单任务超时 900s
- **Middleware Chain**：1.0 上下文压缩 / 沙箱 / 记忆逻辑散落各处，改一处要动多处；2.0 统一为 ThreadData → Uploads → Sandbox → DanglingToolCall → SubagentLimit → Clarification 链路，Agent 推理代码零改动
- **Skill System**：每个 Skill 是一个目录，内含 SKILL.md；system_prompt 只注入索引避免上下文爆炸；custom/ 下新增目录即可扩展
- **Context Engineering**：Write —— 中间结果写入文件系统，索引/规则每轮注入 system；Compress —— 超限调轻量 LLM 压缩历史 + 异步提炼持久化记忆，沙箱按 thread_id 隔离

**结果**：超 180k token 触发 Micro compact，超 250k 触发 LLM 兜底续跑；核心链路重构后维护成本显著下降

## 技能
Python / TypeScript / React / Node.js / Docker / LLM Agent / Prompt Engineering / RAG
