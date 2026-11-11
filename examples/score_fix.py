"""第06课作业后的参考解答：只统计正分，保留输入顺序。"""
def positive_score(values):
    return sum(value for value in values if value > 0)
