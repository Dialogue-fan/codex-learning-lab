"""本地可审计教学黑盒；第09–10课观察阶段请只调用命令，不读源码。"""
import argparse
import json

def damage(attack, armor, critical=False):
    if not isinstance(attack, int) or not isinstance(armor, int) or attack < 0 or armor < 0:
        raise ValueError('attack/armor 需要非负整数')
    base = max(1, attack - armor)
    return base * (2 if critical else 1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--attack', type=int, required=True)
    parser.add_argument('--armor', type=int, required=True)
    parser.add_argument('--critical', action='store_true')
    args = parser.parse_args()
    try:
        print(json.dumps({'damage':damage(args.attack,args.armor,args.critical)}))
    except ValueError as exc:
        parser.error(str(exc))
