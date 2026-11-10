#!/usr/bin/env python3
"""Offline lesson navigator. Records feedback; does not certify mastery."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

def read_json(path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))

def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    temporary.replace(path)

def main(argv=None):
    p = argparse.ArgumentParser(description='Codex 中文互动教案（离线，无 API 消耗）')
    p.add_argument('--state-dir', type=Path, default=ROOT/'.learning', help='进度目录')
    sub = p.add_subparsers(dest='cmd', required=True)
    a = sub.add_parser('start'); a.add_argument('lesson', nargs='?')
    sub.add_parser('status')
    a = sub.add_parser('quiz'); a.add_argument('lesson'); a.add_argument('--answer')
    a = sub.add_parser('submit'); a.add_argument('lesson'); a.add_argument('--evidence', required=True, type=Path)
    a = sub.add_parser('feedback'); a.add_argument('lesson'); a.add_argument('--rubric', required=True); a.add_argument('--note', required=True)
    args = p.parse_args(argv)
    try:
        lessons = read_json(ROOT/'curriculum.json', [])
        state_path = args.state_dir/'progress.json'
        state = read_json(state_path, {})
        if args.cmd == 'status':
            for lesson in lessons:
                entry = state.get(lesson['id'], {})
                print(f"{lesson['id']} {lesson['title']}：{entry.get('status', '未提交')}；小测 {'通过' if entry.get('quiz_passed') else '未通过'}")
            return 0
        lesson_id = getattr(args, 'lesson', None)
        if not lesson_id:
            lesson_id = next((x['id'] for x in lessons if state.get(x['id'], {}).get('status') != '反馈通过'), lessons[-1]['id'])
        lesson = next((x for x in lessons if x['id'] == lesson_id), None)
        if not lesson:
            raise ValueError('无效课号，请使用 00–13。')
        if args.cmd == 'start':
            print((ROOT/lesson['path']).read_text(encoding='utf-8'))
            print(f'\n给 Codex：请按 TUTOR.md 带我做第 {lesson_id} 课。先等我回答，再提示；最后按证据验收。')
            return 0
        entry = state.setdefault(lesson_id, {})
        if args.cmd == 'quiz':
            print(lesson['question'])
            print('\n'.join(lesson['options']))
            answer = args.answer if args.answer is not None else input('你的选择 A/B/C：')
            answer = answer.strip().upper()
            if answer not in ('A','B','C'):
                raise ValueError('请输入 A、B 或 C。')
            entry['attempts'] = entry.get('attempts',0)+1
            entry['quiz_passed'] = answer == lesson['answer']
            print('概念检查通过；还需提交实操作业。' if entry['quiz_passed'] else '再想一下：'+lesson['hint'])
        elif args.cmd == 'submit':
            evidence = args.evidence.resolve()
            if not evidence.is_file() or not evidence.read_text(encoding='utf-8').strip():
                raise ValueError('证据文件必须存在且非空。')
            entry.update(evidence=str(evidence), digest=hashlib.sha256(evidence.read_bytes()).hexdigest(), status='待反馈')
            entry.pop('feedback', None)
            print('已记录提交，等待导师核验具体要求与实际证据。')
        elif args.cmd == 'feedback':
            if not entry.get('evidence'):
                raise ValueError('请先提交证据，再记录反馈。')
            evidence = Path(entry['evidence'])
            if not evidence.is_file() or hashlib.sha256(evidence.read_bytes()).hexdigest() != entry['digest']:
                raise ValueError('证据已变化或丢失，请重新提交。')
            scores = [int(x) for x in args.rubric.split(',')]
            if len(scores) != 5 or any(x not in (0,1,2) for x in scores):
                raise ValueError('需要五项 0–2 分，例如 2,2,2,1,1。')
            if not args.note.strip():
                raise ValueError('反馈不能为空。')
            passed = sum(scores) >= 8 and scores[3] > 0
            entry['feedback'] = {'scores':scores, 'note':args.note, 'total':sum(scores)}
            entry['status'] = '反馈通过' if passed else '需补练'
            print(f"{entry['status']}（{sum(scores)}/10）。人工/导师反馈记录，非自动能力认证；具体课要求仍需逐项核对。")
        entry['updated_at'] = datetime.now(timezone.utc).isoformat()
        save(state_path, state)
        return 0
    except (ValueError, OSError, UnicodeError, EOFError) as exc:
        print(f'无法完成：{exc}', file=sys.stderr)
        return 2

if __name__ == '__main__':
    sys.exit(main())
