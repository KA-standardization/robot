# -*- coding:utf-8 -*-
import random

import pandas as pd


def foo(i):
    ids = [random.randint(21, 25) for _ in range(100)]
    actions = [random.randint(50, 2000) for _ in range(100)]
    dates = [
        f"2022-10-{random.randint(10, 17)} {random.randint(10, 23)}:{random.randint(10, 59)}:{random.randint(10, 59)}"
        for _ in range(100)]

    all_ = [{'r_num': ids[i], 'action': actions[i], 'time_set': dates[i]} for i in range(100)]

    df = pd.DataFrame(all_)
    df.to_excel(f'text{i}.xlsx', index=False)


for i in range(10):
    foo(i)
