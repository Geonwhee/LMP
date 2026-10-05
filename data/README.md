# 과제 데이터

저장소를 Fork → Clone 하면 이 폴더가 함께 내려옵니다. 따로 다운로드할 파일은 없습니다.
(보기만 할 때는 GitHub 의 **Code → Download ZIP** 도 가능하지만, 제출하려면 Fork 가 필요합니다.)

| 파일 | 쓰는 과제 | 내용 |
|---|---|---|
| `../cases/case118_pglib.py` | 1 ~ 5 | IEEE 118-bus 계통 (PyPower 형식). `from cases import case118_pglib` |
| `../cases/case3_lecture.py` | 강의 예제 | 강의 3-bus (LMP 20 · 50 · 80) |
| `scenarios.csv` | 2 · 4 | 시나리오 S1~S4: `load_scale` (부하 배율), `gen_out_bus` (정지할 발전기 버스), `branch_out_id` (정지할 선로 번호) |
| `profile_24h.csv` | 3 · 5 | 24시간: `load_scale` (모든 버스 부하 배율), `W1_cf`~`W3_cf` (풍력 이용률 0~1) |
| `wind_farms.csv` | 3 · 5 | 풍력단지 3곳: `bus`, `capacity_mw` (설비용량), `cost` ($/MWh) |
| `raw/pglib_opf_case118_ieee.m` | 참고 | 원본 MATPOWER 형식 파일 (PGLib-OPF v23.07). `case118_pglib.py` 는 이것을 변환한 것 |

- 빈 칸은 '해당 없음' 입니다 (예: S1 은 정지 설비 없음).
- `branch_out_id` · `branch_id` 는 `ppc["branch"]` 의 **행 번호 (1부터)** 입니다.
- 풍력 · 부하 프로파일은 교육용 합성 데이터입니다.

출처: IEEE PES Power Grid Library - OPF (https://github.com/power-grid-lib/pglib-opf), CC BY 4.0.
