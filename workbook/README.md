# 作业与进度

复制 templates/submission.md 到本目录，例如 01-task.md。选择题与作业都可以在 Codex 聊天里完成；本地工具负责记录，不会自动审阅语义。

提交例：

```bash
python3 tools/coach.py submit 01 --evidence workbook/01-task.md
python3 tools/coach.py feedback 01 --rubric 2,2,2,1,1 --note "已检查实际证据和本课要求"
```

分数顺序：目标、上下文、执行、验证、迁移。仅当本课具体要求都满足时记录通过，否则先补练。feedback 的分数是人工/导师输入，不能当作程序认证。重交作业会清除旧反馈，避免修改作业后仍沿用旧通过记录。

workbook 中个人作业和 .learning 进度不纳入 Git；若要同步，检查内容后明确选择提交，避免把私人记录或密钥上传。
