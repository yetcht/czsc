# -*- coding: utf-8 -*-
"""
author: zengbin93
email: zeng_bin8888@163.com
create_dt: 2022/4/29 12:06
describe: 请描述文件用途
"""
from czsc.data.jq import *
from czsc import CzscAdvancedTrader
from czsc.objects import PositionLong, PositionShort
from examples import tactics


def trader_tactic_snapshot(symbol, tactic: dict, end_dt=None, file_html=None, fq=True, max_count=1000):
    """使用聚宽的数据对任意标的、任意时刻的状态进行策略快照

    :param symbol: 交易标的
    :param tactic: 择时交易策略
    :param end_dt: 结束时间，精确到分钟
    :param file_html: 结果文件
    :param fq: 是否复权
    :param max_count: 最大K线数量
    :return: trader
    """
    base_freq = tactic['base_freq']
    freqs = tactic['freqs']
    get_signals = tactic['get_signals']

    long_states_pos = tactic.get('long_states_pos', None)
    long_events = tactic.get('long_events', None)
    long_min_interval = tactic.get('long_min_interval', None)

    short_states_pos = tactic.get('short_states_pos', None)
    short_events = tactic.get('short_events', None)
    short_min_interval = tactic.get('short_min_interval', None)

    if not end_dt:
        end_dt = datetime.now().strftime(dt_fmt)

    if long_states_pos:
        long_pos = PositionLong(symbol, T0=False,
                                long_min_interval=long_min_interval,
                                hold_long_a=long_states_pos['hold_long_a'],
                                hold_long_b=long_states_pos['hold_long_b'],
                                hold_long_c=long_states_pos['hold_long_c'])
    else:
        long_pos = None

    if short_states_pos:
        short_pos = PositionShort(symbol, T0=False,
                                  short_min_interval=short_min_interval,
                                  hold_short_a=short_states_pos['hold_short_a'],
                                  hold_short_b=short_states_pos['hold_short_b'],
                                  hold_short_c=short_states_pos['hold_short_c'])
    else:
        short_pos = None

    bg, data = get_init_bg(symbol, end_dt, base_freq=base_freq, freqs=freqs, max_count=max_count, fq=fq)
    trader = CzscAdvancedTrader(bg, get_signals, long_events, long_pos, short_events, short_pos,
                                signals_n=tactic.get('signals_n', 0))
    for bar in data:
        trader.update(bar)

    if file_html:
        trader.take_snapshot(file_html)
        print(f'saved into {file_html}')
    else:
        trader.open_in_browser()
    return trader


if __name__ == '__main__':
    ct = trader_tactic_snapshot("000001.XSHG", end_dt="20070427 15:15", tactic=tactics.trader_strategy_example())

