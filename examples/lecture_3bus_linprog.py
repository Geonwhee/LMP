"""강의 3-bus DC-OPF 를 무료 솔버로 직접 풀어 본다 (Gurobi 불필요).

SciPy 에 들어 있는 HiGHS (scipy.optimize.linprog) 로 선형계획 문제를 세우고,
쌍대변수(marginals)에서 λ, μ 를 읽어 LMP = λ − Σ μ·PTDF 를 계산한다.

실행:  python examples/lecture_3bus_linprog.py
기대 결과:  G1 = 180, G2 = 120, λ = 20, μ(1-3) = 90, LMP = [20, 50, 80]
"""
import numpy as np
from scipy.optimize import linprog

cost = np.array([20.0, 50.0])          # G1 (버스 1), G2 (버스 2)  $/MWh
pmax = np.array([300.0, 300.0])
load = np.array([0.0, 0.0, 300.0])     # 버스 1, 2, 3 부하 MW
F = np.array([500.0, 160.0, 500.0])    # 선로 1-2, 1-3, 2-3 한계 MW

# PTDF (slack = 버스 1, 선로 from→to 가 +) : 강의 슬라이드의 표
H = np.array([[0, -2/3, -1/3],
              [0, -1/3, -2/3],
              [0,  1/3, -1/3]])
Cg = np.array([[1, 0], [0, 1], [0, 0]])   # 발전기 → 버스

# 선로 조류 = H (Cg P − load)  →  −F ≤ 조류 ≤ F
A_ub = np.vstack([H @ Cg, -H @ Cg])
b_ub = np.concatenate([F + H @ load, F - H @ load])

res = linprog(cost, A_ub=A_ub, b_ub=b_ub,
              A_eq=np.ones((1, 2)), b_eq=[load.sum()],   # 수급 균형 (λ)
              bounds=list(zip([0, 0], pmax)), method="highs")
print("상태:", res.message)
print("발전:", res.x.round(2), " 총비용:", round(res.fun, 2))

lam = res.eqlin.marginals[0]                      # 수요 1 MW 증가 시 비용 증가 = λ
nl = len(F)
mu = -(res.ineqlin.marginals[:nl] - res.ineqlin.marginals[nl:])   # from→to 한계면 +, 반대면 −
lmp = lam - H.T @ mu
print("λ =", round(lam, 2), "  μ =", mu.round(2) + 0.0)
print("LMP =", lmp.round(2) + 0.0)
