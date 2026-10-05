"""환경 점검: 패키지 설치, 3-bus 강의 예제, IEEE 118 계통, 과제 데이터를 차례로 확인한다.

실행:  python check_environment.py
"""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)
ok = True


def report(passed, msg):
    global ok
    ok &= passed
    print(("[성공] " if passed else "[실패] ") + msg)


try:
    import numpy, scipy, pandas, matplotlib, pypower, cryptography  # noqa: F401
    report(True, f"패키지 설치 (Python {sys.version.split()[0]}, numpy {numpy.__version__}, PYPOWER)")
except Exception as e:
    report(False, f"패키지 설치: {e}  →  conda env create -f environment.yml")
    sys.exit(1)

from pypower.api import ppoption, rundcopf
from pypower.idx_bus import LAM_P
from cases import case3_lecture, case118_pglib

opt = ppoption(VERBOSE=0, OUT_ALL=0)
r = rundcopf(case3_lecture(), opt)
lmp = [round(float(x), 2) for x in r["bus"][:, LAM_P]]
report(r["success"] and lmp == [20.0, 50.0, 80.0], f"3-bus 강의 예제 LMP = {lmp}  (기대값 [20.0, 50.0, 80.0])")

c = case118_pglib()
r = rundcopf(c, opt)
report(r["success"] and c["bus"].shape[0] == 118 and c["branch"].shape[0] == 186,
       f"IEEE 118 계통 (버스 {c['bus'].shape[0]}, 발전기 {c['gen'].shape[0]}, 선로 {c['branch'].shape[0]}) DC-OPF 수렴")

for f in ["scenarios.csv", "profile_24h.csv", "wind_farms.csv"]:
    report(os.path.exists(os.path.join(ROOT, "data", f)), f"data/{f}")

print("\n모든 점검 통과! 과제를 시작하세요." if ok else "\n실패한 항목을 AI 에게 에러 메시지와 함께 물어보세요.")
sys.exit(0 if ok else 1)
