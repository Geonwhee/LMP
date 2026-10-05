"""강의 3-bus 예제를 PyPower 로 다시 계산해 본다.

실행:  python examples/lecture_3bus.py
기대 결과:  G1 = 180 MW, G2 = 120 MW, LMP = [20, 50, 80] $/MWh, 선로 1-3 만 혼잡
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pypower.api import ppoption, rundcopf
from pypower.idx_bus import BUS_I, LAM_P          # LAM_P = 13 (0부터 세는 열 번호)
from pypower.idx_gen import GEN_BUS, PG
from pypower.idx_brch import F_BUS, T_BUS, PF, RATE_A, MU_SF, MU_ST

from cases import case3_lecture

ppc = case3_lecture()
opt = ppoption(VERBOSE=0, OUT_ALL=0)      # 화면 출력 끄기
r = rundcopf(ppc, opt)                    # DC 최적조류 (DC-OPF)
print("수렴:", r["success"])

print("\n[발전기]")
for g in r["gen"]:
    print(f"  버스 {int(g[GEN_BUS])}: {g[PG]:7.1f} MW")

print("\n[노드별 가격 LMP]")
for b in r["bus"]:
    print(f"  버스 {int(b[BUS_I])}: {b[LAM_P]:6.2f} $/MWh")

print("\n[선로]")
for br in r["branch"]:
    mu = br[MU_SF] + br[MU_ST]            # 0 보다 크면 그 선로가 한계에 걸린(혼잡) 것
    print(f"  {int(br[F_BUS])}-{int(br[T_BUS])}: 조류 {br[PF]:7.1f} MW / 한계 {br[RATE_A]:5.0f} MW"
          f"   쉐도우 프라이스 μ = {mu:5.1f}")
