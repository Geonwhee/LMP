"""answers/ 폴더의 제출 파일 형식을 검사한다 (정답 여부는 채점 서버에서 확인).

실행:  python tools/validate_answers.py
"""
import os
import sys

import pandas as pd

sys.path.insert(0, os.path.dirname(__file__))
from answer_spec import FILES, MAX_BYTES

ROOT = os.path.join(os.path.dirname(__file__), "..")
ANS = os.path.join(ROOT, "answers")


def check(verbose=True):
    ok = True
    for name, (cols, nrows) in FILES.items():
        path = os.path.join(ANS, name)
        if not os.path.exists(path):
            print(f"[없음] answers/{name}  (이 과제는 0점 처리)")
            continue
        if os.path.getsize(path) > MAX_BYTES:
            print(f"[실패] answers/{name}: 파일이 너무 큽니다"); ok = False; continue
        try:
            df = pd.read_csv(path)
        except Exception as e:
            print(f"[실패] answers/{name}: CSV 로 읽을 수 없음 ({e})"); ok = False; continue
        df.columns = [str(c).strip() for c in df.columns]
        miss = [c for c in cols if c not in df.columns]
        if miss:
            print(f"[실패] answers/{name}: 열 {miss[:5]} 이(가) 없습니다"); ok = False; continue
        if nrows is not None and len(df) != nrows:
            print(f"[실패] answers/{name}: {len(df)}행 (기대 {nrows}행)"); ok = False; continue
        if df[cols].isna().any().any():
            print(f"[실패] answers/{name}: 빈 값이 있습니다"); ok = False; continue
        if name == "task5_upgrade.csv" and len(df) > 3:
            print(f"[실패] answers/{name}: 선로는 최대 3개까지"); ok = False; continue
        if verbose:
            print(f"[성공] answers/{name}  ({len(df)}행)")
    return ok


if __name__ == "__main__":
    sys.exit(0 if check() else 1)
