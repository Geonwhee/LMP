"""채점 진입점 (GitHub Actions 에서 실행).

정답과 채점 로직은 암호화된 bundle.enc 안에 있어 공개 저장소에서 볼 수 없다.
학생 PR 에서 가져온 파일은 '데이터'로만 읽고 절대 실행하지 않는다.

사용: python .github/grader/run.py <제출폴더> <출력폴더>
  제출폴더: submission.enc, submission_info.json, changed.txt (PR 에서 바뀐 파일 목록)
"""
import io
import json
import os
import sys
import tempfile
import zipfile
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, ROOT)
from envelope import decrypt
from answer_spec import FILES, MAX_BYTES

ALLOWED = {"submission/submission.enc", "submission_info.json"}
MARK = "<!--LMP-GRADE "


def clean(s, n):
    return "".join(ch for ch in str(s)[:n] if ch not in "|<>`\r\n")


def safe_zip(blob):
    out = {}
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        for info in z.infolist():
            if info.filename in FILES or info.filename == "meta.json":
                if info.file_size > MAX_BYTES:
                    raise ValueError(f"{info.filename} 이(가) 너무 큽니다")
                out[info.filename] = z.read(info)
    return out


def write(out_dir, body):
    open(os.path.join(out_dir, "comment.md"), "w", encoding="utf-8").write(body)


def main(sub_dir, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    key = os.environ["GRADER_PRIVATE_KEY"].encode()
    sha = clean(os.environ.get("HEAD_SHA", ""), 40)
    info = {}
    try:
        info = json.load(open(os.path.join(sub_dir, "submission_info.json"), encoding="utf-8"))
    except Exception:
        pass
    name, model = clean(info.get("name", "?"), 30), clean(info.get("model_name", "?"), 40)

    changed = set()
    p = os.path.join(sub_dir, "changed.txt")
    if os.path.exists(p):
        changed = {line.strip() for line in open(p, encoding="utf-8") if line.strip()}
    extra = sorted(changed - ALLOWED)
    if extra:
        write(out_dir,
              "## ⚠️ 채점하지 않았습니다\n\n"
              "PR 에 제출 파일 2개 외의 파일이 들어 있습니다. fork 는 **공개 저장소**라서 다른 학생이 볼 수 있습니다.\n\n"
              + "\n".join(f"- `{clean(f, 120)}`" for f in extra[:20])
              + "\n\n`submission/submission.enc` 와 `submission_info.json` 만 남기고 나머지 변경을 되돌린 뒤 다시 push 하세요.")
        return

    with tempfile.TemporaryDirectory() as tmp:
        bundle = decrypt(open(os.path.join(os.path.dirname(__file__), "bundle.enc"), "rb").read(), key)
        zipfile.ZipFile(io.BytesIO(bundle)).extractall(tmp)
        sys.path.insert(0, tmp)
        import grade_core

        enc = os.path.join(sub_dir, "submission.enc")
        if not os.path.exists(enc) or os.path.getsize(enc) == 0:
            write(out_dir, "## ❌ 채점 실패\n\n`submission/submission.enc` 가 없습니다. `python tools/submit.py` 로 만드세요.")
            return
        try:
            files = safe_zip(decrypt(open(enc, "rb").read(), key))
        except Exception:
            write(out_dir, "## ❌ 채점 실패\n\n`submission.enc` 를 열 수 없습니다. `python tools/submit.py` 로 다시 만드세요.")
            return
        res, msgs = grade_core.grade(files, ROOT)

    res.update(name=name, model=model, sha=sha, at=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    rows = "\n".join(f"| {t} | {res[t]:.1f} / {pt} | " + "<br>".join(msgs[t]) + " |"
                     for t, pt in grade_core.POINTS.items())
    body = (f"## 📊 자동 채점 결과: **{res['total']:.1f} / 100**\n\n"
            f"제출자 **{name}** · 모델 `{model}` · commit `{sha[:7]}`\n\n"
            f"| 과제 | 점수 | 내용 |\n|---|---|---|\n{rows}\n\n"
            f"정답 값은 공개되지 않습니다. 고친 뒤 같은 PR 에 다시 push 하면 자동으로 재채점됩니다.\n\n"
            f"{MARK}{json.dumps(res, ensure_ascii=False)}-->")
    write(out_dir, body)
    json.dump(res, open(os.path.join(out_dir, "result.json"), "w", encoding="utf-8"), ensure_ascii=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
