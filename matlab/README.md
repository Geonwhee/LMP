# (선택) MATLAB + MATPOWER 로 과제하기

기본은 PyPower(Python)이지만, MATLAB 에 익숙하다면 계산은 MATPOWER 로 해도 됩니다.
**답안 CSV 형식과 제출 방법은 같습니다.** 제출 도구(`tools/submit.py`)는 Python 이므로 저장소 README 의 환경 구축(conda)도 해 두어야 합니다.

## 1. 설치

1. MATLAB: 학교 학생 라이선스로 설치
2. MATPOWER: https://matpower.org/download/ 에서 내려받아 **한글 없는 경로**에 압축 해제 (예: `C:\matpower8.1`)
3. MATLAB 에서 그 폴더로 이동 → `install_matpower` 실행 → 경로 저장 선택
4. 점검
   ```matlab
   cd C:\LMP\matlab
   check_matpower      % 모두 [성공] 이면 준비 끝
   lecture_3bus        % 강의 3-bus: LMP = 20, 50, 80
   ```

## 2. 파일

| 파일 | 내용 |
|---|---|
| `case3_lecture.m` | 강의 3-bus 예제 |
| `lecture_3bus.m` | 3-bus DC-OPF 실행 · 결과 읽기 · CSV 저장 예시 |
| `check_matpower.m` | MATPOWER · 118 계통 · 제출용 Python 점검 |
| `../data/raw/pglib_opf_case118_ieee.m` | 과제 계통 (`loadcase('pglib_opf_case118_ieee')`, 경로 추가 필요) |

## 3. PyPower 와 다른 점

| | PyPower (Python) | MATPOWER (MATLAB) |
|---|---|---|
| 열 번호 | 0부터 (`LAM_P` = 13) | 1부터 (`LAM_P` = 14) → `define_constants` 로 이름 사용 |
| 118 계통 | `from cases import case118_pglib` | `addpath('..\data\raw'); mpc = loadcase('pglib_opf_case118_ieee');` |
| 실행 | `rundcopf(ppc, ppoption(VERBOSE=0, OUT_ALL=0))` | `rundcopf(mpc, mpoption('verbose', 0, 'out.all', 0))` |
| 결과 | `r['bus'][:, LAM_P]` | `r.bus(:, LAM_P)` |
| PTDF | `makePTDF(...)` (먼저 `ext2int`) | `makePTDF(ext2int(mpc))` |
| 총비용 | `totcost(...)` | `r.f` |
| CSV 저장 | `pandas.DataFrame.to_csv` | `writetable(table(...), 'answers\task1_lmp.csv')` |

- 열 이름은 저장소 README 의 형식과 **정확히 같아야** 합니다 (예: `bus,lmp`).
- `task4_ptdf.csv` 처럼 열 이름이 숫자(`1`~`118`)인 파일은 `fprintf` 로 머리줄을 직접 쓰는 것이 편합니다.
- 강의자가 같은 과제를 MATPOWER 8.1 로 풀어 채점기에 넣어 본 결과 100점 (PyPower 정답과 LMP 차이 < 1e-6).

## 4. 제출 (Python 사용자와 동일)

```
python tools/validate_answers.py
python tools/submit.py
git add submission/submission.enc submission_info.json
```
