"""第 06 课故意保留的练习缺陷：统计正分且不能修改输入。"""
def positive_score(values):
    values.sort()
    return sum(values)
