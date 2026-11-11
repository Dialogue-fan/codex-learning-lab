"""用真实运行结果重演“实现了结果但漏掉约束”的纠偏过程。"""
import importlib.util
from pathlib import Path
from score_fix import positive_score

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('buggy_score',ROOT/'labs/bugs/buggy_score.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def partial_fix(values):
    values.sort()
    return sum(value for value in values if value > 0)

def main():
    for name, function in [('练习原始实现',module.positive_score),('教学中的不完整修复',partial_fix),('参考修复',positive_score)]:
        values=[3,-2,5]
        original=values.copy()
        score=function(values)
        print(f'{name}：得分={score}；输入保留={values == original}')
    for values in ([],[-3,-1],[0],[3,-2,5]):
        original=values.copy()
        result=positive_score(values)
        assert result == sum(x for x in original if x>0)
        assert values == original
    print('参考修复：四组边界与输入不变检查通过。')

if __name__ == '__main__':
    main()
