"""모든 PR 의 채점 코멘트(github-actions 봇이 단 것만)를 모아 리더보드 이슈 본문을 다시 만든다.

상태를 저장하지 않고 매번 처음부터 다시 만들기 때문에, 동시에 여러 번 실행돼도 결과가 꼬이지 않는다.
필요 환경변수: GH_TOKEN, GITHUB_REPOSITORY, LEADERBOARD_ISSUE
"""
import json
import os
import subprocess
import sys

REPO = os.environ["GITHUB_REPOSITORY"]
ISSUE = os.environ.get("LEADERBOARD_ISSUE", "").strip()
MARK = "<!--LMP-GRADE "
BOT = "github-actions[bot]"


def api(path):
    out = subprocess.run(["gh", "api", "--paginate", path], check=True, capture_output=True,
                         text=True, encoding="utf-8").stdout
    # --paginate 는 페이지마다 JSON 배열을 이어 붙여 출력한다
    items, dec, i = [], json.JSONDecoder(), 0
    while i < len(out):
        while i < len(out) and out[i].isspace():
            i += 1
        if i >= len(out):
            break
        obj, i = dec.raw_decode(out, i)
        items += obj if isinstance(obj, list) else [obj]
    return items


def collect():
    subs = []
    for pr in api(f"repos/{REPO}/pulls?state=all&per_page=100"):
        for c in api(f"repos/{REPO}/issues/{pr['number']}/comments?per_page=100"):
            if c["user"]["login"] != BOT or MARK not in c["body"]:
                continue
            try:
                r = json.loads(c["body"].split(MARK, 1)[1].rsplit("-->", 1)[0])
            except Exception:
                continue
            r.update(login=pr["user"]["login"], pr=pr["number"], at=c["created_at"])
            subs.append(r)
    return subs


def render(subs):
    best = {}
    for r in sorted(subs, key=lambda r: r["at"]):
        b = best.get(r["login"])
        if b is None or (r["total"], r["reduction"]) > (b["total"], b["reduction"]):
            best[r["login"]] = r
    rank = sorted(best.values(), key=lambda r: (-r["total"], -r["reduction"], r["at"]))
    t = lambda s: s[:16].replace("T", " ")
    lines = ["# 🏆 리더보드: 노드별 전기 가격 과제", "",
             "학생별 최고 점수 기준 · 동점이면 과제 5 (선로 증설) 비용 절감액이 큰 순서 · 채점 때마다 자동 갱신", "",
             "| 순위 | 이름 | 모델 | 총점 | T1 | T2 | T3 | T4 | T5 | 절감액 ($/일) | 제출 시각 (UTC) |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(rank, 1):
        lines.append(f"| {i} | {r['name']} | `{r['model']}` | **{r['total']:.1f}** | {r['T1']:.1f} | {r['T2']:.1f} | "
                     f"{r['T3']:.1f} | {r['T4']:.1f} | {r['T5']:.1f} | {r['reduction']:,.0f} | {t(r['at'])} |")
    lines += ["", "<details><summary>전체 제출 이력</summary>", "",
              "| 시각 (UTC) | 이름 | 모델 | 총점 | PR |", "|---|---|---|---|---|"]
    for r in sorted(subs, key=lambda r: r["at"], reverse=True):
        lines.append(f"| {t(r['at'])} | {r['name']} | `{r['model']}` | {r['total']:.1f} | #{r['pr']} |")
    lines.append("</details>")
    return "\n".join(lines), len(rank)


def main():
    if not ISSUE:
        sys.exit("LEADERBOARD_ISSUE 변수가 없습니다 (Settings → Secrets and variables → Actions → Variables)")
    subs = collect()
    body, n = render(subs)
    open("leaderboard.md", "w", encoding="utf-8").write(body)
    subprocess.run(["gh", "issue", "edit", ISSUE, "--repo", REPO, "--body-file", "leaderboard.md"], check=True)
    print(f"{n}명 · 제출 {len(subs)}건 반영")


if __name__ == "__main__":
    main()
