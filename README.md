# Codex 高效沟通与游戏制作互动课

把想法变成可验证的结果，减少无关上下文和返工。中文、项目实操、逐课反馈。

课程整合官方 Bootcamp 101→实操→201→301、Academind 公开目录中的主题，以及沟通、上下文、交接和验证方法。加入游戏设计制作与功能观察复现两条主线。完整原创教案，不需要购买课程才能做练习；来源核对日期：2026-11-10。

## 立即开始

在连接本仓库的 Codex 会话中输入：

> 请按 TUTOR.md 带我学习。先问我的编程基础、使用入口和游戏引擎偏好，每次只带一课。让我先做，不直接替我交作业。根据证据验收，卡住时逐级提示。从第 00 课开始。

没有本地工具也能直接阅读课程，在聊天中提交答案。完整代码实操需要本地或云端开发环境；不必同时安装 CLI、IDE 和桌面端。

```bash
git clone https://github.com/Dialogue-fan/codex-learning-lab.git
cd codex-learning-lab
python3 tools/coach.py start
```

Windows 可将 `python3` 替换为 `py`。Python 建议 3.10+。选择题工具无需第三方包、不调用模型 API。`start` 会选择下一课并显示导师指令；`quiz` 支持交互作答；作业提交与反馈分开记录。

```bash
python3 tools/coach.py quiz 00
python3 tools/coach.py status
python3 tools/coach.py submit 00 --evidence workbook/00-profile.md
python3 tools/coach.py feedback 00 --rubric 2,2,2,1,1 --note "导师检查了命令记录，需补一次异常场景"
```

评分是学习者/导师提供的学习记录，工具不自动判断真实能力。反馈证据充分且总分至少 8、验证项非零才记录通过；可见 [评分规则](docs/assessment.md)。本地进度与作业默认不上传。

## 学习路线

| 课 | 内容 | 阶段 | 建议时长 |
| --- | --- | --- | --- |
| [00](lessons/00.md) | 诊断与环境 | 101 | 30 分钟 |
| [01](lessons/01.md) | 一次说清任务 | 101 | 45 分钟 |
| [02](lessons/02.md) | 上下文与短计划 | 101 | 45 分钟 |
| [03](lessons/03.md) | 游戏最小可玩版本 | 101 | 60 分钟 |
| [04](lessons/04.md) | 游戏设计与手感沟通 | 201 | 60 分钟 |
| [05](lessons/05.md) | 长期规则与会话衔接 | 201 | 45 分钟 |
| [06](lessons/06.md) | 用证据修 Bug 与验证 | 201 | 60 分钟 |
| [07](lessons/07.md) | Git、审查与恢复 | 201 | 45 分钟 |
| [08](lessons/08.md) | Skills、MCP 与可复用流程 | 301 | 60 分钟 |
| [09](lessons/09.md) | 功能逆向：观察与实验 | 201 | 60 分钟 |
| [10](lessons/10.md) | 功能逆向：独立实现与差异验证 | 201 | 75 分钟 |
| [11](lessons/11.md) | 省 token 的沟通实验 | 301 | 60 分钟 |
| [12](lessons/12.md) | Worktree、云端与稳定自动化 | 301 | 60 分钟 |
| [13](lessons/13.md) | 毕业项目与迁移 | 综合 | 90 分钟 |

全程约 13 小时，按个人基础分 2–4 周完成。优先路线 00→01→02→03→06→09→10→11；完整路线按课号进行。每课都有先答题、实践、验收、补练和迁移。

## 两条实战线

- **游戏制作**：[可玩起点](starter/game/README.md)→任务书→暂停→手感调参→修错→新增机制→验收。默认浏览器小游戏，支持 [Godot/Unity 分支](docs/engine-paths.md)。
- **功能逆向**：[观察流程](docs/reverse-workflow.md)→本地黑盒→假设→区分实验→独立实现→对照验证。可迁移到公开可观察的游戏或软件功能。

## 如何省时间和 token

[沟通速查](docs/communication.md) · [效率实验](docs/efficiency.md) · [提示模板](templates/task.md) · [交接模板](templates/handoff.md)

比较通过相同验收的总成本；不要仅按回复长短判断。并行不保证省 token，规则文件被读取时也占上下文，套餐额度和原始 token 不是同一指标。

## 导航

[TUTOR.md](TUTOR.md) · [前置操作](docs/prerequisites.md) · [来源和视频](sources/README.md) · [作业示例](workbook/README.md) · [项目规则](AGENTS.md)

## 仓库检查

```bash
python3 -m unittest discover -s tests -v
node --test starter/game/core.test.mjs
```

游戏手感和真实外部目标需单独实测。本仓库不承诺固定节省比例；以任务成功、耗时、纠偏轮次和实际可见用量判断效果。
