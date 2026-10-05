# 노드별 전기 가격(LMP) 과제: 3-bus → IEEE 118

PyPower 로 송전망을 고려한 전기 가격(LMP)을 계산하고, 송전 혼잡 · 재생에너지 · PTDF 까지 분석합니다.
제출하면 GitHub Actions 가 자동 채점하고 리더보드에 반영합니다.

> **다른 학생은 내 답을 볼 수 없습니다.** 답은 `tools/submit.py` 가 채점 서버 전용 공개키로 암호화한
> `submission/submission.enc` 로만 올라갑니다. 대신 **풀이 코드와 `answers/` 폴더는 절대 push 하지 마세요** (fork 는 공개 저장소).

---

## 1. 환경 구축 (지난 수업과 같음)

| 단계 | 할 일 |
|---|---|
| 1 | 강의자 저장소 https://github.com/Tsukuyomi1252/LMP 를 **Fork** → `C:\LMP` 로 **Clone** |
| 2 | `conda env create -f environment.yml` (수 분 소요) → `conda activate lmp` |
| 3 | `python check_environment.py` → 모두 **[성공]** |
| 4 | `python examples/lecture_3bus.py` → 강의 3-bus 결과 (LMP = 20, 50, 80) 확인 |

conda 를 쓰지 않는다면 2단계 대신 `pip install -r requirements.txt` (Python 3.11 권장).
PyPower 는 MATPOWER 를 Python 으로 옮긴 패키지라 MATLAB 은 필요 없습니다.

**최적화 솔버는 따로 설치하지 않아도 됩니다.** `rundcopf` 는 PyPower 내장 솔버(PIPS)로 풀고, 직접 정식화하려면 SciPy 에 들어 있는 무료 HiGHS (`scipy.optimize.linprog`) 를 쓰면 됩니다 → `examples/lecture_3bus_linprog.py`. Gurobi 같은 상용 솔버는 필요 없습니다.

**MATLAB + MATPOWER 로 계산하고 싶다면 (선택)** → [matlab/README.md](matlab/README.md). 답안 형식과 제출 방법은 같고, 제출 도구 때문에 위 Python 환경도 필요합니다.

과제 데이터는 Clone 할 때 함께 내려옵니다 → [data/README.md](data/README.md)

막히면 에러 메시지를 그대로 AI(Claude Code · Codex)에게 붙여넣으세요.

## 2. 폴더 구성

```
cases/case3_lecture.py     강의 3-bus 예제
cases/case118_pglib.py     IEEE 118 (PGLib 버전: 선로 열용량 한계 포함)   ← 과제는 이것만 사용
data/scenarios.csv         과제 2 · 4 시나리오
data/profile_24h.csv       과제 3 · 5 시간별 부하 배율과 풍력 이용률
data/wind_farms.csv        과제 3 · 5 풍력단지 (버스, 용량, 비용)
data/raw/                  원본 MATPOWER 형식 파일 (참고용)
examples/lecture_3bus.py   PyPower 사용 예시
examples/lecture_3bus_linprog.py  무료 솔버(HiGHS)로 DC-OPF 직접 풀기
matlab/                    (선택) MATLAB · MATPOWER 예제
tools/validate_answers.py  답안 형식 검사
tools/submit.py            답안 암호화 → submission/submission.enc
work/                      ← 직접 만들어 풀이 코드를 두는 곳 (git 에 올라가지 않음)
answers/                   ← 답안 CSV 를 두는 곳 (git 에 올라가지 않음)
```

불러오기: `from cases import case118_pglib` → `ppc = case118_pglib()`

> PyPower 기본 `case118` 은 모든 선로 한계가 9900 MW 라서 혼잡이 생기지 않습니다. **반드시 `case118_pglib` 를 쓰세요.**

## 3. 과제 (총 100점)

공통 규칙
- 모든 계산은 **DC-OPF** (`rundcopf`) 기준, 버스 · 선로 번호는 1부터.
- `branch_id` = `ppc["branch"]` 의 **행 번호 (1~186)**. 같은 두 버스를 잇는 병렬 선로가 있어서 버스 번호 대신 이것을 씁니다.
- **혼잡 선로** = 쉐도우 프라이스 `MU_SF + MU_ST > 1e-4` 인 선로.

### 과제 1. 노드별 가격 LMP (15점)
기준 상태(`case118_pglib` 그대로)의 118개 버스 LMP.
- `answers/task1_lmp.csv` : `bus, lmp`

### 과제 2. 송전 혼잡 예측 (20점)
`data/scenarios.csv` 의 S1~S4 각각에 대해
- `ed` : **송전 제약을 무시한** 경제급전(모든 선로 `RATE_A = 0`, PyPower 에서 0 은 '한계 없음')의 조류가 **원래 한계를 넘는** 선로 = 예측
- `opf` : 원래 한계로 DC-OPF 를 풀었을 때의 **혼잡 선로** = 실제

발전기 고장은 해당 버스 발전기의 `GEN_STATUS = 0`, 선로 고장은 `BR_STATUS = 0`.
- `answers/task2_congestion.csv` : `scenario, method, branch_id` (선로 하나당 한 행, 해당 없으면 행 없음)

### 과제 3. 재생에너지와 시간대별 가격 (25점)
`data/profile_24h.csv` 의 24시간마다
- 모든 버스 부하 `Pd` × `load_scale`
- 풍력단지(`data/wind_farms.csv`)를 발전기로 추가: 버스 `bus`, `Pmax = 이용률 × capacity_mw`, `Pmin = 0`, 선형비용 `cost` $/MWh

제출
- `answers/task3_lmp_24h.csv` : `hour, bus, lmp` (2,832행)
- `answers/task3_wind_24h.csv` : `hour, farm, dispatch_mw, curtail_mw` (출력제한 = 가용량 − 실제 발전, 72행)
- `answers/task3_bus_daily.csv` : `bus, energy_mwh, payment` (하루 소비량 Σ Pd, 하루 지불액 Σ LMP × Pd)

### 과제 4. PTDF 와 LMP 분해 (25점)
- **PTDF** : 기준(slack) 버스 69, 버스 i 에 1 MW 주입하고 slack 에서 빼낼 때 선로 조류(from → to 가 +).
  B 행렬로 **직접 계산**하고 `pypower.makePTDF` 결과와 대조해 보세요.
  `answers/task4_ptdf.csv` : `branch_id, 1, 2, …, 118` (186행)
- **S2 (부하 115%)** 의 쉐도우 프라이스: 부호 있는 `μ = MU_SF − MU_ST`, |μ| > 1e-4 인 선로만.
  `answers/task4_mu.csv` : `branch_id, mu`
- **S2 LMP 분해** : `LMP_i = λ − Σ_k μ_k · PTDF_k,i`  (λ = slack 버스 LMP)
  `answers/task4_lmp_decomp.csv` : `bus, energy, congestion, lmp` (energy = λ, congestion = −Σ μ·PTDF)

### 과제 5. 선로 증설 리더보드 (15점)
과제 3 의 24시간 운영에서 **선로를 최대 3개** 골라 각각 `RATE_A` 를 **+100 MW** 늘립니다.
하루 총 발전비용을 가장 많이 줄이는 조합을 찾으세요.
- `answers/task5_upgrade.csv` : `branch_id` (1~3행)
- 점수 = 15 × (내 절감액 ÷ 강의자 기준 절감액), 최대 15점. 리더보드 동점은 절감액으로 순위.

## 4. 제출

```
python tools/validate_answers.py      # 형식 검사
python tools/submit.py                # 암호화 → submission/submission.enc (처음 한 번 학번 입력, 공개 안 됨)
git add submission/submission.enc submission_info.json
git commit -m "submit"
git push
```
1. `submission_info.json` 에 이름(리더보드 표시용)과 `model_name` 을 적습니다. 학번은 적지 않습니다.
2. 처음 한 번 **Pull Request** 를 만듭니다: 내 fork `main` → `Tsukuyomi1252/LMP` `main` (Merge 하지 않음).
3. 약 1분 뒤 PR 코멘트에 점수가 달리고, 리더보드(Issues 탭의 Leaderboard)가 갱신됩니다.
4. 이후에는 같은 PR 에 push 만 하면 다시 채점됩니다.

PR 에 **두 파일 외의 파일이 있으면 채점하지 않습니다** (풀이 공개 방지).

## 5. AI 에게 맡길 것, 내가 확인할 것

| AI 에게 | 반드시 직접 |
|---|---|
| PyPower 코드 작성 · 에러 해석 · 24시간 반복문 | 3-bus 결과가 강의 값(20, 50, 80)과 같은지 |
| CSV 형식 맞추기 · 그래프 · git 명령 | `case118_pglib` 를 썼는지 (`case118` 아님) |
| makePTDF 와 직접 계산 PTDF 비교 | LMP 분해 합이 실제 LMP 와 같은지 |
| | `answers/`, `work/` 를 push 하지 않았는지 |

프롬프트 예시
- "examples/lecture_3bus.py 를 work/task1.py 로 복사해서 case118_pglib 의 LMP 를 answers/task1_lmp.csv 로 저장해 줘."
- "data/scenarios.csv 의 S1~S4 마다 송전 제약을 뺀 경제급전 조류와 DC-OPF 혼잡 선로를 비교하는 표를 만들어 줘."
- "B 행렬로 PTDF 를 직접 계산해서 makePTDF 결과와 최대 오차를 출력해 줘. 오차가 크면 원인을 찾아 줘."
- "submission/submission.enc 와 submission_info.json 만 add, commit, push 해 줘."

---
데이터 출처: IEEE PES PGLib-OPF `pglib_opf_case118_ieee` (CC BY 4.0). 풍력 · 부하 프로파일은 교육용 합성 데이터.
