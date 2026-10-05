"""answers/ 폴더를 암호화해 submission/submission.enc 를 만든다.

실행:  python tools/submit.py

  - 내 fork 는 공개 저장소라서 누구나 볼 수 있다. 그래서 답을 그대로 올리지 않고,
    채점 서버만 열 수 있는 공개키로 암호화한 submission.enc 만 올린다.
  - 학번은 암호화된 파일 안에만 들어가고, 공개되는 submission_info.json 에는 들어가지 않는다.
  - 이 스크립트는 파일만 만든다. commit · push 는 직접(또는 AI 에게 시켜서) 한다:
        git add submission/submission.enc submission_info.json
"""
import io
import json
import os
import sys
import zipfile
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(__file__))
from answer_spec import FILES
from envelope import encrypt
from validate_answers import check

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ANS = os.path.join(ROOT, "answers")
INFO = os.path.join(ROOT, "submission_info.json")
PRIVATE = os.path.join(ROOT, "student_private.json")   # 학번 (git 에 올라가지 않음)


def main():
    info = json.load(open(INFO, encoding="utf-8"))
    if not info.get("name") or info["name"].startswith("홍길동"):
        sys.exit("submission_info.json 의 name 을 본인 이름(또는 리더보드에 쓸 별명)으로 바꾸세요.")
    if not os.path.exists(PRIVATE):
        sid = input("학번을 입력하세요 (공개되지 않음): ").strip()
        json.dump({"student_id": sid}, open(PRIVATE, "w", encoding="utf-8"), ensure_ascii=False)
    sid = json.load(open(PRIVATE, encoding="utf-8"))["student_id"]

    print("== 형식 검사 ==")
    if not check():
        sys.exit("형식 오류를 고친 뒤 다시 실행하세요.")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for name in FILES:
            p = os.path.join(ANS, name)
            if os.path.exists(p):
                z.write(p, name)
        meta = dict(info, student_id=sid, created=datetime.now(timezone.utc).isoformat(timespec="seconds"))
        z.writestr("meta.json", json.dumps(meta, ensure_ascii=False))
    pub = open(os.path.join(ROOT, "tools", "grader_public_key.pem"), "rb").read()
    os.makedirs(os.path.join(ROOT, "submission"), exist_ok=True)
    out = os.path.join(ROOT, "submission", "submission.enc")
    open(out, "wb").write(encrypt(buf.getvalue(), pub))
    print(f"\n[완료] submission/submission.enc 생성 ({os.path.getsize(out):,} bytes)")
    print("다음 두 파일만 commit · push 하세요:\n  git add submission/submission.enc submission_info.json")


if __name__ == "__main__":
    main()
