import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
COACH=ROOT/'tools/coach.py'

class CoachTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base=Path(self.temp.name)
        self.evidence=self.base/'answer.md'
        self.evidence.write_text('实际操作记录与验证证据',encoding='utf-8')
    def run_coach(self,*args):
        return subprocess.run([sys.executable,str(COACH),'--state-dir',str(self.base/'state'),*args],text=True,capture_output=True)
    def test_quiz_retry_and_no_auto_pass(self):
        self.assertEqual(self.run_coach('quiz','00','--answer','A').returncode,0)
        self.assertIn('再想一下',self.run_coach('quiz','00','--answer','A').stdout)
        self.assertIn('概念检查通过',self.run_coach('quiz','00','--answer','B').stdout)
        state=json.loads((self.base/'state/progress.json').read_text())
        self.assertTrue(state['00']['quiz_passed'])
        self.assertNotIn('status',state['00'])
    def test_evidence_and_feedback_gates(self):
        self.assertEqual(self.run_coach('feedback','00','--rubric','2,2,2,2,2','--note','ok').returncode,2)
        self.assertEqual(self.run_coach('submit','00','--evidence',str(self.base/'missing')).returncode,2)
        self.assertEqual(self.run_coach('submit','00','--evidence',str(self.evidence)).returncode,0)
        result=self.run_coach('feedback','00','--rubric','2,2,2,0,2','--note','验证缺失')
        self.assertIn('需补练',result.stdout)
        self.assertIn('反馈通过',self.run_coach('feedback','00','--rubric','2,2,2,1,1','--note','已逐项检查').stdout)
        self.evidence.write_text('changed',encoding='utf-8')
        self.assertEqual(self.run_coach('feedback','00','--rubric','2,2,2,2,2','--note','ok').returncode,2)
        self.run_coach('submit','00','--evidence',str(self.evidence))
        state=json.loads((self.base/'state/progress.json').read_text())
        self.assertEqual(state['00']['status'],'待反馈')
        self.assertNotIn('feedback',state['00'])
    def test_invalid_scores_and_lesson(self):
        self.assertEqual(self.run_coach('start','99').returncode,2)
        self.run_coach('submit','00','--evidence',str(self.evidence))
        self.assertEqual(self.run_coach('feedback','00','--rubric','2,2,2,3,1','--note','x').returncode,2)
    def test_start_chooses_first_unpassed(self):
        self.run_coach('submit','00','--evidence',str(self.evidence))
        self.run_coach('feedback','00','--rubric','2,2,2,2,2','--note','已核对')
        self.assertIn('第 01 课',self.run_coach('start').stdout)
    def test_curriculum_and_markdown_links(self):
        import re
        lessons=json.loads((ROOT/'curriculum.json').read_text())
        self.assertEqual(len(lessons),21)
        self.assertEqual([item['id'] for item in lessons], [f'{n:02d}' for n in range(21)])
        for item in lessons:
            self.assertTrue((ROOT/item['path']).is_file())
        for file in ROOT.rglob('*.md'):
            for target in re.findall(r'\]\(([^)]+)\)',file.read_text(encoding='utf-8')):
                if '://' not in target and not target.startswith('#'):
                    self.assertTrue((file.parent/target.split('#')[0]).exists(),f'{file}: {target}')
    def test_extension_lessons_are_navigable_and_quizzable(self):
        for lesson in json.loads((ROOT/'curriculum.json').read_text())[14:]:
            with self.subTest(lesson=lesson['id']):
                self.assertIn(lesson['title'], self.run_coach('start', lesson['id']).stdout)
                self.assertIn('概念检查通过', self.run_coach('quiz', lesson['id'], '--answer', lesson['answer']).stdout)
        self.assertIn('00–20', self.run_coach('start', '99').stderr)

    def test_oracle_invalid_input_and_repeatability(self):
        cmd=[sys.executable,str(ROOT/'labs/reverse/oracle.py'),'--attack','12','--armor','5']
        one=subprocess.check_output(cmd,text=True)
        self.assertEqual(one,subprocess.check_output(cmd,text=True))
        bad=subprocess.run(cmd[:-1]+['-1'],capture_output=True)
        self.assertNotEqual(bad.returncode,0)

if __name__=='__main__':
    unittest.main()
