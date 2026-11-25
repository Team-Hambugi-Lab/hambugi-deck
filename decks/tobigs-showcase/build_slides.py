"""4조 발표회 최종 덱 (흰 배경, 정수 pt, 긴 하이픈 금지)."""
import re
import sys
from pathlib import Path

OUT = Path(sys.argv[1])

HEAD = """<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.min.css">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; word-break: keep-all; overflow-wrap: break-word; }
body { width: 720pt; height: 405pt; background: #FFFFFF; color: #1A1A1A;
  font-family: 'Pretendard', sans-serif; padding: 32pt 44pt; display: flex; flex-direction: column; }
.strip { display: flex; justify-content: space-between; align-items: center; }
.label { font-size: 10pt; font-weight: 600; letter-spacing: 0.14em; color: #888888; }
.num { font-family: 'Pretendard', sans-serif; font-weight: 800; letter-spacing: -0.02em; color: #1F3A6E; line-height: 1.4; padding-bottom: 2pt; }
.rule { width: 48pt; height: 2pt; background: #1F3A6E; margin: 10pt 0 0; }
h1 { font-size: 24pt; font-weight: 700; line-height: 1.3; letter-spacing: -0.02em; text-wrap: balance; }
h2 { font-size: 18pt; font-weight: 700; line-height: 1.4; }
h3 { font-size: 14pt; font-weight: 700; line-height: 1.4; text-wrap: balance; }
p, li { font-size: 12pt; line-height: 1.6; text-wrap: pretty; }
b { font-weight: 700; }
.muted { color: #888888; }
.red { color: #1F3A6E; }
.cap { font-size: 10pt; color: #888888; line-height: 1.5; }
.small { font-size: 11pt; line-height: 1.5; }
ul { list-style: none; }
.hair { border-top: 1pt solid #BBBBBB; }
.dark { border-top: 2pt solid #1A1A1A; }
.redtop { border-top: 2pt solid #1F3A6E; }
.chip { display: inline-block; background: #1F3A6E; color: #FFFFFF; padding: 3pt 8pt; border-radius: 2pt; }
.prog { position: absolute; left: 0; bottom: 0; height: 4pt; background: #1F3A6E; }
body { position: relative; }
img { display: block; object-fit: contain; }
table { border-collapse: collapse; width: 100%; }
td, th { font-size: 11pt; padding: 5pt 6pt; text-align: left; border-top: 1pt solid #BBBBBB; }
th { font-weight: 700; border-top: 2pt solid #1A1A1A; }
</style>
</head>
"""

S = []


def strip(label):
    """상단 라벨 띠. 번호는 추가 순서로 자동 부여."""
    return (f'<div class="strip"><p class="label chip" style="color:#FFFFFF;">{label}</p>'
            f'<p class="label">{len(S) + 1:02d} / {{TOTAL}}</p></div>')


def raw(html):
    """완성된 슬라이드 HTML 추가."""
    S.append(HEAD + html)


def page(label, title, body, sub="", title_size=None):
    """일반 콘텐츠 슬라이드."""
    sub_html = f'<p class="muted" style="font-size:12pt; margin-top:4pt;">{sub}</p>' if sub else ""
    h1_attr = f' style="font-size:{title_size}pt;"' if title_size else ''
    raw(f'<body>{strip(label)}'
        f'<div style="margin-top:14pt;"><h1{h1_attr}>{title}</h1>{sub_html}<div class="rule"></div></div>'
        f'<div style="flex:1; display:flex; flex-direction:column; justify-content:center;">'
        f'{body}</div></body></html>')


def divider(num, title, sub, weeks):
    """섹션 디바이더."""
    raw(f'''<body style="justify-content:space-between;">{strip("SECTION " + num)}
<div style="display:flex; align-items:flex-end; gap:28pt;">
  <p class="num" style="font-size:120pt; line-height:1.4;">{num}</p>
  <div style="padding-bottom:22pt;"><p class="label red">{weeks}</p>
  <h1 style="font-size:40pt; margin-top:6pt;">{title}</h1>
  <p class="muted" style="font-size:14pt; margin-top:6pt;">{sub}</p></div>
</div>
<div style="height:8pt; background:#1F3A6E;"></div></body></html>''')


def cols(items, gap=20, top="dark"):
    """괘선 컬럼: (라벨, 제목, 본문)."""
    cells = ''.join(
        f'<div class="{top}" style="padding-top:8pt;"><p class="label red">{k}</p>'
        f'<h3 style="margin-top:4pt;">{h}</h3><p class="small" style="margin-top:4pt;">{b}</p></div>'
        for k, h, b in items)
    return (f'<div style="display:grid; grid-template-columns:repeat({len(items)},1fr); '
            f'gap:{gap}pt;">{cells}</div>')


def stat(value, unit, cap, size=40):
    """큰 숫자 + 캡션."""
    return (f'<div class="dark" style="padding-top:6pt;"><p class="num" style="font-size:{size}pt;">'
            f'{value}<span style="font-size:14pt;">{unit}</span></p><p class="cap">{cap}</p></div>')


def table(head, rows, widths=None):
    """간단 표."""
    cg = ''.join(f'<col style="width:{w}">' for w in widths) if widths else ''
    th = ''.join(f'<th><p class="small"><b>{h}</b></p></th>' for h in head)
    tr = ''.join('<tr>' + ''.join(f'<td><p class="small">{c}</p></td>' for c in r) + '</tr>'
                 for r in rows)
    return f'<table><colgroup>{cg}</colgroup><tr>{th}</tr>{tr}</table>'


def bullets(items, pad=6):
    """괘선 불릿."""
    return '<ul>' + ''.join(
        f'<li class="hair" style="padding:{pad}pt 0;">{t}</li>' for t in items) + '</ul>'


def steps(items, last_accent=True):
    """가로 단계 흐름: (라벨, 본문)."""
    n = len(items)
    cells = ''.join(
        f'<div class="{"redtop" if last_accent and i == n - 1 else "dark"}" style="padding-top:8pt;">'
        f'<p class="label red">{i + 1:02d} {a}</p><p class="small" style="margin-top:4pt;">{b}</p></div>'
        for i, (a, b) in enumerate(items))
    return f'<div style="display:grid; grid-template-columns:repeat({n},1fr); gap:10pt;">{cells}</div>'


def two(left, right, ratio="1fr 1fr", gap=28):
    """2단 레이아웃."""
    return (f'<div style="display:grid; grid-template-columns:{ratio}; gap:{gap}pt; align-items:start;">'
            f'<div>{left}</div><div>{right}</div></div>')


# ================= 도입 =================
raw('''<body style="justify-content:space-between;">
<div class="strip"><p class="label">TOBIGS 26기 심화세션 결과 발표회</p><p class="label">4조 · DATA ENGINEERING</p></div>
<div><h1 style="font-size:52pt;">투빅스 심화세션 발표회</h1>
<p class="num red" style="font-size:24pt; margin-top:6pt;">Team Hambugi</p>
<div class="rule" style="margin:14pt 0;"></div>
<p style="font-size:14pt;">데이터 엔지니어링을 배우고, 바로 공모전에 써 본 8주</p></div>
<div class="strip hair" style="padding-top:10pt;"><p class="cap">김태은 · 이정연 · 진재언</p>
<p class="cap">01 / {TOTAL}</p></div></body></html>''')

page("도입 · TEAM", "팀 햄부기", two(cols([
    ("김태은", "파이프라인 · 검증", "DE 개론 발표, 공고 파이프라인, 비자부기 서비스, 빅콘 데이터 전수 검증과 지표 재설계"),
    ("이정연", "모델링 · 분석 · 설계", "저장 · 모델링 발표, HWPX 원문 파싱, 빅콘 활동 신호와 위험 특징 사전, 외부 검증"),
    ("진재언", "구조화 · 공간 · 지수", "오케스트레이션 발표, 공통 스키마 v2와 Supabase 적재, SK 데이터 통합, SGIS 고립 위험 지수"),
], gap=14), '<img src="./assets/team_logo.png" alt="Team Hambugi 로고" style="width:100%; height:170pt;">',
    ratio="3fr 1fr", gap=20), sub="팀명의 부기는 거북이에서 따왔다. 햄은 보시는 대로")

weeks = [("W1", "DE 학습", "개론 · 저장과 모델링 · 오케스트레이션 분담 발표"),
         ("W2", "8/14 보고", "HWPX 파싱, 비자 공고 21건 구조화, 공통 스키마 v1"),
         ("W3", "8/28 제출", "공통 스키마 v2, 서비스 완성, ICT 공모전 제출"),
         ("W4", "돌아보기", "ICT 회고, 비자부기를 팀 실험 프로젝트로 전환"),
         ("W5", "빅콘 착수", "주제 확정, 제공 데이터 전수 검증"),
         ("W6", "9/20 ~ 10/8", "지표 재설계와 재현, 집계구 마스터"),
         ("W7", "10/13 ~", "지수, 활동 신호, 위험 특징 사전, 외부 검증"),
         ("W8", "10/26 제출", "에이전트 설계, 발표자료, 빅콘 제출")]
wk = ''.join(
    f'<div class="{"redtop" if i == 7 else "dark"}" style="padding-top:8pt;">'
    f'<p class="num {"red" if i == 7 else ""}" style="font-size:22pt;">{a}</p>'
    f'<p class="cap">{b}</p><p class="small" style="margin-top:6pt;">{c}</p></div>'
    for i, (a, b, c) in enumerate(weeks))
page("도입 · OVERVIEW", "8주를 한 장으로",
     f'<div style="display:grid; grid-template-columns:repeat(8,1fr); gap:9pt;">{wk}</div>'
     '<p class="cap" style="margin-top:20pt;">W1 데이터 엔지니어링 학습, W2~4 ICT융합 공모전 비자부기, W5~8 빅콘테스트</p>')

# ================= 01 DE 학습 =================
page("01 DE 학습 · WEEK 1", "세 명이 세 파트를 나눠 맡았다", cols([
    ("발표 A · 김태은", "개론 · 파이프라인 기초", "데이터 엔지니어와 분석가, ETL vs ELT, Lake · Warehouse · Mart, Batch vs Streaming"),
    ("발표 B · 이정연", "데이터 저장 · 모델링", "RDB vs NoSQL, OLTP vs OLAP, 정규화와 비정규화, 스타 · 스노우플레이크 스키마, 인덱스"),
    ("발표 C · 진재언", "오케스트레이션 · 운영", "Airflow와 DAG가 필요한 이유, 멱등성과 증분 적재, 데이터 품질 모니터링"),
], gap=22))

page("01 DE 학습 · MATERIALS", "실제로 만든 1주차 발표 자료", '''
<div style="display:grid; grid-template-columns:1.3fr 1.3fr 1fr; gap:12pt; align-items:start;">
  <div><img src="./assets/real/w1_taeeun_pipeline.png" alt="김태은 1주차 발표 데이터 파이프라인" style="width:100%; height:150pt; border:1pt solid #BBBBBB;">
  <p class="cap" style="margin-top:4pt;">김태은 · 데이터 파이프라인</p></div>
  <div><img src="./assets/real/w1_taeeun_etl.png" alt="김태은 1주차 발표 ETL vs ELT" style="width:100%; height:150pt; border:1pt solid #BBBBBB;">
  <p class="cap" style="margin-top:4pt;">김태은 · ETL vs ELT</p></div>
  <div><img src="./assets/real/w1_jaeun.png" alt="진재언 1주차 발표 오케스트레이션" style="width:100%; height:150pt; border:1pt solid #BBBBBB; object-fit:cover; object-position:top;">
  <p class="cap" style="margin-top:4pt;">진재언 · 오케스트레이션과 Dagster</p></div>
</div>
<p class="cap" style="margin-top:10pt;">이정연 파트(저장 · 모델링)는 Notion 문서로 정리해 발표</p>''')

page("01 DE 학습 · APPLY", "배운 개념이 바로 공모전에 쓰였다", table(
    ["배운 개념", "어디에 썼나"],
    [["정규화 · 공통 스키마", "비자 4종이 함께 쓰는 요건 · 절차 · 쿼터 테이블"],
     ["원본 보존", "PDF 변환본 대신 HWPX 원문을 직접 파싱"],
     ["멱등성 · 증분 적재", "반복 실행해도 중복 없는 적재, 실패하면 전체 롤백"],
     ["데이터 품질", "빅콘 제공 데이터 20개 파일 전수 검증"]], ["32%", "68%"]))

# ================= 02 비자부기 =================
page("02 비자부기 · WHAT", "충북 외국인 주민을 위한 다국어 AI 비자 준비 서비스", f'''
<div style="display:grid; grid-template-columns:1.9fr 1fr; gap:20pt; align-items:start;">
  <div><img src="./assets/visa_home.png" alt="비자부기 홈 화면" style="width:100%; height:200pt; border:1pt solid #BBBBBB;">
  <p class="cap" style="margin-top:6pt;">홈: 준비 현황과 현재 단계를 한눈에</p></div>
  <div><img src="./assets/visa_ocr.png" alt="비자부기 OCR 서류 점검 화면" style="width:100%; height:200pt; border:1pt solid #BBBBBB;">
  <p class="cap" style="margin-top:6pt;">서류: 신청서를 찍으면 누락 항목 점검</p></div>
</div>
<p class="small" style="margin-top:8pt;"><b>직접 써 보기</b>&nbsp; visa-bugi-web.vercel.app</p>''',
     sub="제13회 전국 ICT융합 공모전 · 디지털 시제품 부문 · 2026.08.28 제출")

frames = [("demo_8", "로그인"), ("demo_60", "온보딩"), ("demo_120", "챗봇")]
fr = ''.join(
    f'<div><img src="./assets/real/{f}.jpg" alt="비자부기 시연 영상 {c} 장면" style="width:100%; height:120pt; object-fit:cover;">'
    f'<p class="cap" style="margin-top:4pt;">{c}</p></div>' for f, c in frames)
page("02 비자부기 · DEMO", "시연 영상",
     f'<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:12pt;">{fr}</div>'
     '<div style="margin-top:16pt; background:#1F3A6E; padding:10pt 16pt;">'
     '<p style="color:#FFFFFF; font-size:14pt; font-weight:700;">이 화면에서 시연 영상을 재생합니다</p></div>',
     sub="로그인부터 온보딩, 서류 점검, 챗봇 상담까지")

page("02 비자부기 · SERVICE", "데이터에서 화면까지, 서비스로 연결했다", cols([
    ("BACKEND", "인증 · BFF", "아이디 · 비밀번호 인증, 브라우저가 Supabase에 직접 붙지 않도록 BFF로 이관, RLS 정비"),
    ("AI", "RAG 챗봇", "하이브리드 비자 상담 챗봇, OCR 서류 점검 결과와 연동, 다국어 응답"),
    ("UX", "온보딩 · 홈", "비자 4종 온보딩, 실제 잔여 인원 표시, 서류 준비 단계를 실데이터로"),
    ("INFRA", "지도 · 다국어", "카카오맵 기관 표시, next-intl 다국어 라우팅, 약관 · 개인정보처리방침"),
], gap=14), sub="구조화한 비자 데이터를 네 가지 기능으로 연결")

page("02 비자부기 · TROUBLESHOOTING 1", "공고 문장이 통째로 사라졌다", two(
    '<p class="label red">문제</p>'
    '<p class="small" style="margin-top:4pt;">E-7-4R 공고에서 제외대상 ⑤⑥ 항목이 추출 결과에서 통째로 빠졌다.</p>'
    '<p class="label red" style="margin-top:12pt;">원인</p>'
    '<p class="small" style="margin-top:4pt;">글자 중간에 고정폭 공백 태그가 끼면, 그 뒤 글자는 <b>.text</b>가 아니라 자식 태그의 <b>.tail</b>에 저장된다.</p>'
    '<p class="label red" style="margin-top:12pt;">해결</p>'
    '<p class="small" style="margin-top:4pt;"><b>itertext()</b>로 하위 텍스트를 순서대로 모아 복원. 추출 결과 21,594에서 22,319 bytes로.</p>',
    '<div style="background:#F3F5F8; padding:12pt; font-family:Menlo, monospace;">'
    '<p class="small" style="font-family:Menlo, monospace;">&lt;hp:t&gt;⑤&lt;hp:fwSpace/&gt; 대한민국의 이익이나...&lt;/hp:t&gt;</p>'
    '<p class="cap" style="margin-top:10pt;">before · run.text</p><p class="small" style="font-family:Menlo, monospace;">⑤</p>'
    '<p class="cap" style="margin-top:8pt;">after · "".join(run.itertext())</p>'
    '<p class="small" style="font-family:Menlo, monospace;">⑤ 대한민국의 이익이나 공공의 안전 등을...</p></div>'
    '<p class="cap" style="margin-top:8pt;">덤: 페이지 번호는 자동으로 채우지 않기로 했다. 틀린 값이 그럴듯하게 들어가는 것보다 비워두는 게 안전하다. (visa-data #7)</p>',
    ratio="1fr 1.15fr"))

page("02 비자부기 · TROUBLESHOOTING 2", "이번 주 일단 뼈저리게 깨달은 점: <span class=\"red\">공통 스키마</span>", two(
    '<p class="label">v1 · 5개 테이블</p>'
    '<p class="small" style="margin-top:4pt;">F-4-R 중심의 평면 구조라 F-2-R의 중첩 조건, E-7-4R의 점수제, 쿼터 세분화, 서류 대체 관계를 담을 수 없었다.</p>'
    '<p class="label red" style="margin-top:14pt;">v2 · 13개 테이블 (서비스 10 + 근거 · 이관 3)</p>'
    + bullets(["명세 문서를 먼저 확정하고 검증기부터 구현",
               "F-4-R, E-7-4R, F-2-R 순서로 이관",
               "검증을 통과한 레코드에만 UUID를 마지막에 발급"], pad=4),
    '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12pt;">'
    + stat("1,101", "", "통합 레코드", 30) + stat("684", "건", "원천 데이터 추적정보", 30)
    + stat("407", "개", "자동 검증 테스트", 30) + stat("+8,828", "", "PR #46 변경 줄 수", 30) + '</div>'
    '<p class="cap" style="margin-top:8pt;">visa-data #44, PR #46</p>'), title_size=22)

page("02 비자부기 · RESULT", "결과는 탈락. 주제가 흔했나...", '''
<div style="display:grid; grid-template-columns:1fr 1fr 0.7fr; gap:20pt; align-items:start;">
  <div><p class="label red">아쉬웠던 점</p>''' + bullets([
        "기능 구현에 집중해 탐색시간 단축, 서류 누락 감소 같은 <b>실측 자료</b>가 부족했다",
        "기능 범위가 넓어 핵심 강점이 분산됐다",
        "외국인 비자 해결이라는 주제가 흔했을 수 있다"], pad=6) + '''</div>
  <div><p class="label red">그래도 남은 것</p>''' + bullets([
        "공고를 차수별 요건과 적용기간까지 구조화한 경험",
        "처음 제대로 써 본 GitHub 이슈와 PR",
        "비자부기는 팀 실험 프로젝트로 계속"], pad=6) + '''</div>
  <div><img src="./assets/photos/visa_allnighter.jpg" alt="비자부기 밤샘 작업 날 팀 사진" style="width:100%; height:230pt; object-fit:cover;">
  <p class="cap" style="margin-top:4pt;">비자부기 밤샘 작업 날</p></div>
</div>''')

# ================= 03 빅콘 =================
page("03 빅콘 · PROBLEM", "고립은 스스로 드러나지 않는다", f'''
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20pt;">
  {stat("13.6", "%", "서울 1인가구 중 도움을 청할 사람이 한 명도 없는 비율", 36)}
  {stat("1.29", "배", "사회적 고립의 사망 위험", 36)}
  {stat("26.6", "%", "고독사 최초 발견자가 가족인 경우", 36)}
</div>
<div style="margin-top:18pt; background:#1F3A6E; padding:11pt 16pt;">
<p style="color:#FFFFFF; font-size:14pt; font-weight:700;">통신 · 카드 데이터로 고립 위험 지역을 먼저 찾고, 복지로 연결할 수 있을까?</p></div>
<p class="cap" style="margin-top:6pt;">2026 빅콘테스트 AI데이터활용 분야 · SK텔레콤 유동인구 × 신한카드 결제 · 강남구와 춘천시</p>''',
     sub="도움이 필요할 때 기댈 사람이 없는 상태 (통계청 사회적 고립도)")

for key, label, title, cap in [
        ("bigcon_step1", "03 빅콘 · SOLUTION 1", "어디가 위험한가: 고립 위험 지수", "SGIS 6개 지표, 두 테마로 집계구 점수화. 관찰 후보 477곳, 외부 자료와 순위상관 0.639"),
        ("bigcon_step2", "03 빅콘 · SOLUTION 2", "누가 줄었나: 활동 저하 신호", "기대 유동보다 낮은 달이 6개월 중 4개월 이상. 60대 이상 461곳, 8개 대조 모두 예상 방향"),
        ("bigcon_agent", "03 빅콘 · SOLUTION 3", "관찰하고, 판단하고, 연결하는 에이전트", "위험 특징 24개로 판단, 복지 · 공공기관 17,925곳과 지원사업 60건으로 연결. 위기는 바로 사람에게")]:
    page(label, title,
         f'<img src="./assets/real/{key}.png" alt="빅콘 제출 발표자료 {title}" style="width:100%; height:236pt; border:1pt solid #BBBBBB;">'
         f'<p class="cap" style="margin-top:6pt;">{cap}</p>')

page("03 빅콘 · TROUBLESHOOTING", "상업지가 최고 위험으로 나왔다", two(
    '<p class="label red">v1 · 지도에 올려 보니</p>'
    '<div style="display:flex; align-items:baseline; gap:10pt; margin-top:4pt;">'
    '<p class="num" style="font-size:40pt;">109</p><p class="muted">/ 155</p></div>'
    '<p class="small">강남 5등급(최고 위험) 155곳 중 109곳이 테헤란로 같은 업무 · 상업지</p>'
    '<p class="label" style="margin-top:12pt;">원인</p>'
    + bullets(["1인가구 비율에 20~30대 직장인 오피스텔이 섞임",
               "주택이외 거처에 고시원뿐 아니라 오피스텔도 포함",
               "노후주택이 재건축 전 아파트와 오래된 상가를 구분 못 함"], pad=4),
    '<p class="label red">v2 · 고쳤더니 새 문제</p>'
    '<div style="display:flex; align-items:baseline; gap:10pt; margin-top:4pt;">'
    '<p class="num" style="font-size:40pt;">29,678</p><p class="muted">가구</p></div>'
    '<p class="small">업무지를 "판단 보류"로 빼자 보류가 291곳. 강남 1인가구 29,678가구가 사각지대가 됐다. 강남 5등급 전체의 두 배</p>'
    '<p class="cap" style="margin-top:10pt;">bigcontest #24 · 코멘트 19개, 가장 치열했던 이슈</p>'))

page("03 빅콘 · TROUBLESHOOTING", "보류를 쪼개고, 테마를 나눴다", two(
    table(["종사자 ÷ 거주자", "v3 처리"],
          [["1 이하", "주거형 · 등급 그대로"],
           ["1 ~ 5", "혼합형 · 등급 유지 + 혼합지 라벨"],
           ["5 초과", "보류 · 활동 신호로만 판단"]], ["40%", "60%"])
    + '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12pt; margin-top:14pt;">'
    + stat("291", "곳", "v2 보류", 30) + stat("약 70", "곳", "v3 보류", 30) + '</div>',
    '<img src="./assets/map_theme.png" alt="테마 A, B 상위 집계구 지도" style="width:100%; height:180pt;">'
    '<p class="small" style="margin-top:6pt;">고령 독거(A)와 중장년 주거취약(B) 테마를 분리하고 지역 안에서 백분위를 매겼다. 두 테마 상위 지역은 절반만 겹친다.</p>'
    '<p class="cap" style="margin-top:4pt;">v3.3 최종 지수 · 서울시 관심집단 비율과 순위상관 0.639</p>',
    ratio="1fr 1.2fr"))

# ================= 마무리 =================
page("마무리 · RESULT", "2전 2패, 그래도 남은 것", cols([
    ("ICT융합 공모전 · 탈락", "공고를 구조화하는 법", "공공 문서를 차수별 요건과 적용기간까지 데이터로 만든 경험"),
    ("빅콘테스트 · 예선 탈락", "원본을 의심하는 습관", "명세서 대신 원본을 열고, 팀원 결과도 직접 재현했다"),
], gap=24) + '<p class="small muted" style="margin-top:20pt;">미래에셋 AI 페스티벌은 셋 다 각자 다른 팀으로 나갔고, 셋 다 예선에서 광탈했습니다.</p>')

page("마무리 · NEXT", "아쉬운 점과 다음 단계", two(
    '<p class="label">LIMITS</p>'
    + bullets(["비자부기: 사용자에게 실제로 도움이 됐는지 측정하지 못했다",
               "빅콘: 에이전트는 설계와 합성 시나리오까지, 실제 구동은 못 했다",
               "빅콘: 20~30대 신호 실패, 강남은 유입 인구에 주민 신호가 묻힌다"], pad=7),
    '<p class="label red">NEXT</p>'
    + bullets(["비자부기를 팀 실험 프로젝트로 계속 디벨롭",
               "사용자 로그를 쌓아 이탈 분석",
               "운영 DB와 분석 DB를 나누는 구조로 확장"], pad=7)))

page("마무리 · RETRO", "한 사람씩, 두 문장", cols([
    ("김태은", "적은 표본으로 단정하지 않기", "몇 개 확인해 보니 맞더라는 증명이 아니라는 걸 배웠다. 결과를 보고 정의를 끼워 맞추지 않는 게 핵심이었다."),
    ("이정연", "가정을 먼저 맞추기", "숫자가 비슷하다고 같은 방식으로 계산했다는 보장은 없다는 걸 배웠다. 분석 결과를 어떤 말로 전달하느냐도 분석의 일부였다."),
    ("진재언", "공통 스키마와 GitHub", "공통 스키마가 왜 중요한지 뼈저리게 깨달았다. GitHub를 제대로 써 본 건 처음인데 팀원들 덕분에 정말 많이 배웠다."),
], gap=20))

labels = ["1주차", "3주차", "4주차", "5주차", "9/17", "9/20", "6주차"]
photos = ''.join(
    f'<img src="./assets/photos/photo-{i}.jpg" alt="{lab} 팀 활동 사진" style="width:100%; height:84pt; object-fit:cover;">'
    for i, lab in enumerate(labels, 1))
raw(f'''<body>{strip("CLOSING")}
<div style="margin-top:14pt; display:flex; align-items:baseline; gap:16pt;"><h1 style="font-size:36pt;">감사합니다</h1>
<p class="num red" style="font-size:18pt;">Team Hambugi</p></div>
<div style="flex:1; display:flex; flex-direction:column; justify-content:center;">
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:8pt;">{photos}
<div style="display:flex; align-items:center; justify-content:center;"><p class="small muted">함께한 8주</p></div></div></div></body></html>''')

TOTAL = len(S)
BANNED = re.compile("[—–−―→]")  # 긴 하이픈, en dash, 마이너스, 화살표
for f in OUT.glob("slide-*.html"):
    f.unlink()
for n, html in enumerate(S, start=1):
    html = html.replace("{TOTAL}", str(TOTAL))
    html = html.replace("</body>", f'<div class="prog" style="width:{n / TOTAL * 100:.0f}%;"></div></body>', 1)
    assert not BANNED.search(html), f"slide {n}: 금지 문자 {BANNED.findall(html)}"
    (OUT / f"slide-{n:02d}.html").write_text(html, encoding="utf-8")
print("ok", TOTAL)
