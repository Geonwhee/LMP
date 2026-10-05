"""강의 3-bus 예제 (모든 선로 리액턴스 동일)

  버스1: 발전기 G1  20 $/MWh, 최대 300 MW   (slack)
  버스2: 발전기 G2  50 $/MWh, 최대 300 MW
  버스3: 부하 300 MW
  선로 1-3 만 열용량 160 MW, 나머지는 500 MW

강의 결과: G1 = 180 MW, G2 = 120 MW, LMP = [20, 50, 80] $/MWh
"""
from numpy import array


def case3_lecture():
    ppc = {"version": "2"}
    ppc["baseMVA"] = 100.0

    # bus_i type Pd Qd Gs Bs area Vm Va baseKV zone Vmax Vmin
    ppc["bus"] = array([
        [1, 3,   0, 0, 0, 0, 1, 1, 0, 230, 1, 1.1, 0.9],
        [2, 2,   0, 0, 0, 0, 1, 1, 0, 230, 1, 1.1, 0.9],
        [3, 1, 300, 0, 0, 0, 1, 1, 0, 230, 1, 1.1, 0.9],
    ])

    # bus Pg Qg Qmax Qmin Vg mBase status Pmax Pmin (+ 11 zero columns)
    ppc["gen"] = array([
        [1, 0, 0, 300, -300, 1, 100, 1, 300, 0] + [0] * 11,
        [2, 0, 0, 300, -300, 1, 100, 1, 300, 0] + [0] * 11,
    ])

    # fbus tbus r x b rateA rateB rateC ratio angle status angmin angmax
    ppc["branch"] = array([
        [1, 2, 0, 0.1, 0, 500, 500, 500, 0, 0, 1, -360, 360],
        [1, 3, 0, 0.1, 0, 160, 160, 160, 0, 0, 1, -360, 360],
        [2, 3, 0, 0.1, 0, 500, 500, 500, 0, 0, 1, -360, 360],
    ])

    # model startup shutdown n c1 c0   (선형 비용: 20 P, 50 P)
    ppc["gencost"] = array([
        [2, 0, 0, 2, 20, 0],
        [2, 0, 0, 2, 50, 0],
    ])
    return ppc
