"""本地对照；参考结果由子进程提供，学习者不必读取 oracle 源码。"""
import json
from pathlib import Path
import random
import subprocess
import sys
from replica import damage

def main():
    rng = random.Random(2026)
    cases = [(0,0,False),(12,5,False),(12,5,True),(2,20,True)]
    cases += [(rng.randint(0,100),rng.randint(0,100),bool(rng.getrandbits(1))) for _ in range(12)]
    failed = 0
    for attack, armor, critical in cases:
        cmd = [sys.executable,str(Path(__file__).with_name('oracle.py')),'--attack',str(attack),'--armor',str(armor)]
        if critical:
            cmd.append('--critical')
        expected = json.loads(subprocess.check_output(cmd,text=True))['damage']
        try:
            actual = damage(attack,armor,critical)
        except NotImplementedError:
            print('副本尚未实现，这是练习起点。请先完成观察规格，再填写 replica.py。')
            return 2
        ok = actual == expected
        failed += not ok
        print(f'{attack=}, {armor=}, {critical=}：参考={expected}，副本={actual}，'+('一致' if ok else '差异'))
    print(f'共 {len(cases)} 组，差异 {failed}。仍需补充你自己的保留用例，有限测试不证明全部行为等价。')
    return 1 if failed else 0

if __name__ == '__main__':
    sys.exit(main())
