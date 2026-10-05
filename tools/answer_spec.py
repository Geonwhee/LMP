"""제출 파일 목록과 형식. validate_answers.py 와 submit.py 가 함께 사용한다."""

# 파일 이름: (필수 열, 기대 행 수 또는 None)
FILES = {
    "task1_lmp.csv":         (["bus", "lmp"], 118),
    "task2_congestion.csv":  (["scenario", "method", "branch_id"], None),
    "task3_lmp_24h.csv":     (["hour", "bus", "lmp"], 24 * 118),
    "task3_wind_24h.csv":    (["hour", "farm", "dispatch_mw", "curtail_mw"], 24 * 3),
    "task3_bus_daily.csv":   (["bus", "energy_mwh", "payment"], 118),
    "task4_ptdf.csv":        (["branch_id"] + [str(b) for b in range(1, 119)], 186),
    "task4_mu.csv":          (["branch_id", "mu"], None),
    "task4_lmp_decomp.csv":  (["bus", "energy", "congestion", "lmp"], 118),
    "task5_upgrade.csv":     (["branch_id"], None),
}
MAX_BYTES = 2_000_000
