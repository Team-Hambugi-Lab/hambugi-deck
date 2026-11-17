"""tobigs-showcase 슬라이드 HTML 생성 v2 (흰 배경, 정수 pt, 긴 하이픈 금지)."""
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
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 720pt; height: 405pt; background: #FFFFFF; color: #1A1A1A;
  font-family: 'Pretendard', sans-serif; padding: 32pt 44pt; display: flex; flex-direction: column; }
.strip { display: flex; justify-content: space-between; align-items: center; }
.label { font-size: 10pt; font-weight: 600; letter-spacing: 0.14em; color: #888888; }
.num { font-family: 'Pretendard', sans-serif; font-weight: 800; letter-spacing: -0.02em; color: #1F3A6E; line-height: 1.4; padding-bottom: 2pt; }
.rule { width: 48pt; height: 2pt; background: #1F3A6E; margin: 10pt 0 0; }
h1 { font-size: 28pt; font-weight: 700; line-height: 1.3; letter-spacing: -0.02em; }
h2 { font-size: 20pt; font-weight: 700; line-height: 1.4; }
h3 { font-size: 16pt; font-weight: 700; line-height: 1.4; }
p, li { font-size: 14pt; line-height: 1.55; }
b { font-weight: 700; }
.muted { color: #888888; }
.red { color: #1F3A6E; }
.cap { font-size: 12pt; color: #888888; line-height: 1.5; }
.small { font-size: 12pt; line-height: 1.5; }
ul { list-style: none; }
.hair { border-top: 1pt solid #BBBBBB; }
.dark { border-top: 2pt solid #1A1A1A; }
.redtop { border-top: 2pt solid #1F3A6E; }
.chip { display: inline-block; background: #1F3A6E; color: #FFFFFF; padding: 3pt 8pt; border-radius: 2pt; }
.prog { position: absolute; left: 0; bottom: 0; height: 4pt; background: #1F3A6E; }
body { position: relative; }
img { display: block; object-fit: contain; }
table { border-collapse: collapse; width: 100%; }
td, th { font-size: 12pt; padding: 5pt 6pt; text-align: left; border-top: 1pt solid #BBBBBB; }
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


def page(label, title, body, sub=""):
    """일반 콘텐츠 슬라이드."""
    sub_html = f'<p class="muted" style="font-size:14pt; margin-top:4pt;">{sub}</p>' if sub else ""
    raw(f'<body>{strip(label)}'
        f'<div style="margin-top:14pt;"><h1>{title}</h1>{sub_html}<div class="rule"></div></div>'
        f'<div style="flex:1; display:flex; flex-direction:column; justify-content:center;">'
        f'{body}</div></body></html>')


def divider(num, title, sub, weeks):
    """섹션 디바이더."""
    raw(f'''<body style="justify-content:space-between;">{strip("SECTION " + num)}
<div style="display:flex; align-items:flex-end; gap:28pt;">
  <p class="num" style="font-size:120pt; line-height:1.4;">{num}</p>
  <div style="padding-bottom:22pt;"><p class="label red">{weeks}</p>
  <h1 style="font-size:40pt; margin-top:6pt;">{title}</h1>
  <p class="muted" style="font-size:16pt; margin-top:6pt;">{sub}</p></div>
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
            f'{value}<span style="font-size:16pt;">{unit}</span></p><p class="cap">{cap}</p></div>')


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
<div class="strip"><p class="label">TOBIGS 26기 심화세션 활동 공유</p><p class="label">DATA ENGINEERING TRACK</p></div>
<div><h1 style="font-size:52pt;">투빅스 심화세션 발표회</h1>
<p class="num red" style="font-size:24pt; margin-top:6pt;">Team Hambugi</p>
<div class="rule" style="margin:14pt 0;"></div>
<p style="font-size:16pt;">데이터 엔지니어링을 배우고, 바로 공모전에 써 본 기록</p></div>
<div class="strip hair" style="padding-top:10pt;"><p class="cap">김태은 · 이정연 · 진재언</p>
<p class="cap">01 / {TOTAL}</p></div></body></html>''')

page("TEAM", "팀 햄부기", cols([
    ("김태은", "파이프라인 · 검증", "DE 개론 발표, 비자 공통 스키마와 월별 공고 파이프라인, 비자부기 서비스, 빅콘 데이터 전수 검증과 지표 재설계, 기관 태그"),
    ("이정연", "모델링 · 분석 · 설계", "저장·모델링 발표, HWPX 원문 파싱, 미래에셋 RAG, 빅콘 주제와 에이전트 흐름, 지수 재현, 활동 신호, 위험 특징 사전"),
    ("진재언", "구조화 · 공간 · 지수", "오케스트레이션 발표, F-2-R 공고 구조화, 공통 스키마 v2와 Supabase 적재, SK 데이터 통합, SGIS 고립 위험 지수"),
], gap=22), sub="팀명의 부기는 거북이에서 따왔다")

toc = [("01", "데이터 엔지니어링 학습", "개념부터 나눠서 발표", "1주차"),
       ("02", "ICT 공모전 · 비자부기", "공공 문서를 서비스 데이터로", "2~3주차"),
       ("03", "돌아보기 · 미래에셋", "ICT 회고와 RAG 실전", "4주차"),
       ("04", "빅콘테스트 · 탐색과 검증", "주제를 정하고 데이터를 의심하기", "5~6주차"),
       ("05", "빅콘테스트 · 분석과 제출", "두 개의 신호와 하나의 에이전트", "7~8주차"),
       ("06", "회고", "숫자와 배운 점", "")]
rows = ''.join(
    f'<div class="hair" style="display:grid; grid-template-columns:44pt 1.3fr 1.3fr 64pt; '
    f'align-items:baseline; padding:5pt 0;"><p class="num red" style="font-size:18pt;">{a}</p>'
    f'<h3 style="font-size:15pt;">{b}</h3><p class="muted small">{c}</p><p class="cap" style="text-align:right;">{d}</p></div>'
    for a, b, c, d in toc)
page("CONTENTS", "목차", rows)

weeks = [("W1", "DE 학습", "개론, 저장·모델링, 오케스트레이션 분담 발표"),
         ("W2", "8/14 보고", "HWPX 파싱, F-2-R 공고 21건 구조화, 공통 스키마 v1"),
         ("W3", "8/28 제출", "공통 스키마 v2, 서비스 완성, ICT 제출"),
         ("W4", "돌아보기", "ICT 회고, 미래에셋 RAG 결과 분석"),
         ("W5", "빅콘 착수", "주제 확정, 데이터 검증, SK 지도 분석"),
         ("W6", "9/20 ~ 10/8", "데이터 전수 재검증, 지표 재설계와 재현"),
         ("W7", "10/13 ~", "지수, 활동 신호, 위험 특징 사전, 외부 검증"),
         ("W8", "10/26 제출", "에이전트 설계, 발표자료, 빅콘 제출")]
wk = ''.join(
    f'<div class="{"redtop" if i == 7 else "dark"}" style="padding-top:8pt;">'
    f'<p class="num {"red" if i == 7 else ""}" style="font-size:22pt;">{a}</p>'
    f'<p class="cap">{b}</p><p class="small" style="margin-top:6pt;">{c}</p></div>'
    for i, (a, b, c) in enumerate(weeks))
page("OVERVIEW", "8주를 한 장으로",
     f'<div style="display:grid; grid-template-columns:repeat(8,1fr); gap:9pt;">{wk}</div>'
     '<p class="cap" style="margin-top:20pt;">팀원 주차 보고서, 세션 기록, GitHub 이슈와 커밋을 바탕으로 정리</p>')

# ================= 01 DE 학습 =================
divider("01", "데이터 엔지니어링 학습", "개념부터 나눠서 발표", "WEEK 1")

page("01 DE 학습 · WEEK 1", "세 명이 세 파트를 나눠 맡았다", cols([
    ("발표 A · 김태은", "개론 · 파이프라인 기초", "데이터 엔지니어와 분석가, ETL vs ELT, Lake · Warehouse · Mart, Batch vs Streaming"),
    ("발표 B · 이정연", "데이터 저장 · 모델링", "RDB vs NoSQL, OLTP vs OLAP, 정규화와 비정규화, 스타 · 스노우플레이크 스키마, 인덱스"),
    ("발표 C · 진재언", "오케스트레이션 · 운영", "Airflow와 DAG가 필요한 이유, 멱등성과 증분 적재, 데이터 품질 모니터링"),
], gap=22))

page("01 DE 학습 · KEY CONCEPTS", "현업은 왜 이렇게 나눌까", two(
    table(["구분", "OLTP", "OLAP"],
          [["목적", "주문 · 결제 · 회원가입", "연도별 매출, 구매 패턴 분석"],
           ["쿼리", "짧고 잦은 읽기 · 쓰기", "대량 조회 · 집계"],
           ["설계", "정규화", "비정규화, 스타 스키마"],
           ["핵심", "ACID 트랜잭션", "조회 성능"]], ["20%", "40%", "40%"]),
    bullets(["<b>ETL vs ELT</b>&nbsp; 저장과 연산이 싸지면서 원본을 먼저 쌓고 나중에 변환하는 ELT가 부상",
             "<b>인덱스</b>&nbsp; B+ Tree로 O(N) 검색을 O(log N)으로. 대신 쓰기 비용이 늘어난다",
             "<b>스타 스키마</b>&nbsp; Fact 주변에 Dimension. JOIN이 적어 BI에 널리 쓰인다"], pad=7),
    ratio="1.1fr 1fr"))

page("01 DE 학습 · APPLY", "배운 개념이 바로 공모전에 쓰였다", table(
    ["배운 개념", "어디에 썼나"],
    [["정규화 · 공통 스키마", "비자 유형 여러 개가 공유하는 요건 · 절차 · 쿼터 테이블 설계"],
     ["원본 보존 · ELT", "PDF 변환본 대신 HWPX 원문을 직접 파싱"],
     ["멱등성 · 증분 적재", "반복 실행해도 중복 없는 적재, 실패하면 전체 롤백. 바뀐 공고만 검토 리포트로"],
     ["OLTP · OLAP 분리", "비자부기 운영 DB와 분석 DB를 나누는 구조 논의"],
     ["데이터 품질", "빅콘 제공 데이터 20개 파일 전수 검증"]], ["32%", "68%"]))

# ================= 02 ICT 비자부기 =================
divider("02", "ICT 공모전 · 비자부기", "공공 문서를 서비스 데이터로", "WEEK 2 ~ 3")

page("02 비자부기 · WHAT", "충북 외국인 주민을 위한 다국어 AI 행정지원", two(
    '<p style="font-size:16pt;">비자 요건, 제출서류, 공고 일정, 지원기관을<br><b>한곳에서</b> 확인하는 서비스</p>'
    '<p class="cap" style="margin-top:10pt;">제13회 전국 ICT융합 공모전 · 디지털 시제품 부문 · 2026.08.28 제출</p>'
    '<div style="display:grid; grid-template-columns:repeat(2,1fr); gap:12pt; margin-top:16pt;">'
    + stat("24", "건", "분석한 공식 공고 · 지침 · 서식", 36) + stat("4", "종", "지원 비자 F-2-R · E-7-4R · F-4-R · D-2", 36) + '</div>',
    bullets(["<b>챗봇</b>&nbsp; 요건 · 절차 · 서류 안내, 임금체불 · 산재 같은 위험상황은 전문기관으로",
             "<b>OCR</b>&nbsp; 신청서 작성 상태와 누락 가능성 점검",
             "<b>캘린더 · 체크리스트</b>&nbsp; 준비 과정 관리",
             "<b>기관 지도</b>&nbsp; 카카오맵으로 실제 기관 표시"], pad=7)))

page("02 비자부기 · F-2-R", "공고 21건을 서비스 데이터로", two(
    '<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10pt;">'
    + ''.join(stat(v, u, c, 24) for v, u, c in [("21", "건", "수집 문서"), ("10", "개", "공고 차수"), ("60", "건", "시 · 군별 쿼터"), ("67", "건", "세부 요건"),
                                                ("16", "건", "AND · OR 그룹"), ("45", "건", "제출서류"), ("6", "건", "변경이력"), ("3", "건", "수동 확인")])
    + '</div><p class="cap" style="margin-top:8pt;">2025년 8차 ~ 2026년 17차 공고와 붙임자료</p>',
    bullets(["<b>보존</b>&nbsp; 원문 위치와 문서별 SHA-256을 남겨 구조화 결과를 원본과 대조",
             "<b>정제</b>&nbsp; 지역명 · 금액 · 기간 · 날짜 표기 통일, 원문 오탈자는 원문을 고치지 않고 정규화",
             "<b>판단 보류</b>&nbsp; 자료만으로 확정할 수 없는 3건은 수동 검수로 남겼다",
             "<b>갱신</b>&nbsp; 새 공고가 나오면 같은 노트북을 다시 실행"], pad=6),
    ratio="1fr 1.3fr"), sub="진재언 · SQLite와 서비스용 CSV 9종")

page("02 비자부기 · SCHEMA v1", "비자 여러 개가 함께 쓰는 공통 스키마", two(
    table(["테이블", "역할"],
          [["visa_requirements", "비자 기본 정보"],
           ["visa_requirement_criteria", "개별 심사요건 (OR 조건 그룹 구조화)"],
           ["visa_process_stages", "신청 절차 단계"],
           ["visa_quota_status", "잔여 인원 로그"],
           ["change_history", "공고 회차 간 변경 이력"]], ["46%", "54%"]),
    '<p class="label red">첫 적용 · F-4-R 12차 공고</p>'
    '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12pt; margin-top:6pt;">'
    + stat("9", "건", "요건", 32) + stat("4", "단계", "절차", 32) + '</div>'
    '<p class="small" style="margin-top:14pt;">코드리뷰로 복합조건 구조화, 레코드 수명주기, 쿼터 상태(정원 있음 · 무제한 · 미확인)를 정리</p>',
    ratio="1.2fr 1fr"))

page("02 비자부기 · SCHEMA v2", "이번 주에 뼈저리게 깨달은 것: 공통 스키마", f'''
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt;">
  {stat("13", "개", "테이블 (서비스 10 + 근거 · 이관 3)", 32)}
  {stat("1,101", "", "공통 데이터 레코드", 32)}
  {stat("684", "건", "원천 데이터 추적정보 (원천문서 24건)", 32)}
  {stat("407", "개", "자동 검증 테스트, CI 연결", 32)}
</div>
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20pt; margin-top:20pt;">
  <p class="small"><b>통합</b>&nbsp; F-2-R · E-7-4R · F-4-R · D-2의 자격조건 111건, 단계별 서류 77건, 쿼터 61건</p>
  <p class="small"><b>적재</b>&nbsp; Supabase 마이그레이션과 importer. 반복 실행해도 중복 없고, 실패하면 전체 롤백</p>
  <p class="small"><b>검증</b>&nbsp; UUID, 외래키, 순환참조, 조건 논리, 쿼터 계산, 출처 연결을 자동 검사</p>
</div>''', sub="진재언 · 비자별로 따로 만든 데이터를 하나의 구조로")

page("02 비자부기 · PARSING", "PDF를 버리고 HWPX 원문으로 갔다", two(
    bullets(["<b>문제</b>&nbsp; PDF로 변환하면 강조 표시된 숫자(나이 · 연수 기준)가 사라졌다",
             "<b>구조</b>&nbsp; HWPX는 XML · 이미지 · 메타데이터를 묶은 ZIP. section0.xml에 본문",
             "<b>누락</b>&nbsp; .text만 읽으면 자식 태그 뒤 문장(.tail)이 빠진다. itertext()로 복원",
             "<b>표</b>&nbsp; tbl, tr, tc, t 순서로 따로 탐색해 행과 셀을 보존",
             "<b>재귀</b>&nbsp; 중첩 깊이가 달라도 같은 방식으로 문서 전체를 탐색"], pad=6),
    '<p class="label red">원문에서 데이터까지</p>'
    + bullets(["HWPX 원본", "ZIP 내부 접근", "XML 파싱 · 트리 탐색", "텍스트 · 표 추출", "공통 스키마로 정제 · 저장"], pad=5),
    ratio="1.5fr 1fr"))

page("02 비자부기 · PIPELINE", "매달 올라오는 공고를 자동으로 반영", steps([
    ("분류", "새 공고를 비자 유형별로 자동 분류"),
    ("추출", "HWPX에서 요건 · 절차 · 쿼터 추출"),
    ("비교", "기존 데이터와 차이 비교"),
    ("리포트", "변경 내용을 검토 리포트로 생성"),
    ("사람 검토", "DB는 자동 수정하지 않고 사람이 확인 후 반영"),
]) + '<p class="small" style="margin-top:20pt;">실제 F-4-R 공고문으로 정상 케이스와 변경 케이스 모두 전 구간 검증</p>'
   '<p class="cap" style="margin-top:4pt;">자격 판정은 AI가 임의로 하지 않고, 검수된 규칙과 공식기관 확인을 기준으로</p>')

page("02 비자부기 · SERVICE", "제출 수준까지 한 주에 끌어올렸다", cols([
    ("BACKEND", "인증 · BFF", "아이디 · 비밀번호 인증, 브라우저가 Supabase에 직접 붙지 않도록 BFF로 이관, RLS 정비"),
    ("AI", "RAG 챗봇", "하이브리드 비자 상담 챗봇 MVP, OCR 서류 점검 결과와 연동, 다국어 응답 개선"),
    ("UX", "온보딩 · 홈", "비자 4종 온보딩 퍼널, 실제 잔여 인원 표시, 서류 준비 단계를 실데이터로"),
    ("INFRA", "지도 · 다국어", "카카오맵 기관 표시, next-intl 다국어 라우팅, 약관 · 개인정보처리방침"),
], gap=14))

# ================= 03 미래에셋 =================
divider("03", "돌아보기 · 미래에셋", "ICT 회고와 RAG 실전", "WEEK 4")

page("03 돌아보기 · ICT", "결과는 탈락, 대신 남은 것", two(
    '<p class="label red">아쉬웠던 점</p>'
    + bullets(["기능 구현에 집중해 탐색시간 단축, 서류 누락 감소, OCR 정확도 같은 <b>실측 자료</b>가 부족했다",
               "기능 범위가 넓어 핵심 강점이 분산됐다",
               "외국인 비자 해결이라는 주제가 흔했을 수 있다"], pad=7),
    '<p class="label red">그 다음</p>'
    + bullets(["<b>9/13</b>&nbsp; 사업계획서 기준으로 탈락 원인 분석",
               "<b>9/20</b>&nbsp; 사업화 대신 팀 학습용 실험 프로젝트로 전환",
               "<b>재언</b>&nbsp; 사용자 로그를 쌓아 고객 이탈 분석 담당",
               "<b>남은 것</b>&nbsp; 공고 차수별 요건을 구조화한 경험, 처음 제대로 써 본 GitHub"], pad=7)))

page("03 미래에셋 · BUILD", "금융 AI 서비스의 전체 흐름을 직접 구현", steps([
    ("파싱", "금융 상품 문서 파싱"),
    ("인덱스", "검색 인덱스 구축"),
    ("라우팅", "질문 유형 분류"),
    ("생성", "근거 기반 답변 생성"),
    ("검증", "인용 번호 · 수치 근거 검증"),
]) + '<p style="font-size:16pt; margin-top:24pt;">심사 결과를 분석해 보니, 품질은 생성 모델이 아니라 <b>검색과 검증</b>에서 갈렸다.</p>')

page("03 미래에셋 · LESSONS", "어디서 틀렸고, 어떻게 고칠까", table(
    ["취약점", "무슨 일이 있었나", "개선 방향"],
    [["질문 분류 오류", "수수료 질문을 상품 추천으로 분류", "신뢰도가 낮으면 복수 경로 검토"],
     ["검색 근거 부족", "비교 대상 일부 문서만 검색된 채 답변", "문서가 다 모이지 않으면 추정 답변 금지"],
     ["문서 내용 혼입", "무관한 문장이 최종 답변에 포함", "검색 결과를 개별 검증 후 전달"],
     ["검증 범위 한계", "논리 모순, 월 · 연 환산 누락은 통과", "질문 충족 여부와 계산까지 검증"],
     ["외부 공격 노출", "/health, /openapi.json 노출", "허용 IP만 접근, 불필요 엔드포인트 차단"]],
    ["20%", "42%", "38%"]),
    sub="자연스러운 답변보다 정확한 근거와 안전한 실패가 중요하다")

# ================= 04 빅콘 탐색·검증 =================
divider("04", "빅콘테스트 · 탐색과 검증", "주제를 정하고 데이터를 의심하기", "WEEK 5 ~ 6")

ideas = [("감각부하 기상도", "환승역 시간대별 감각 부하 예측"),
         ("신경다양 아동 가족", "생활권 이용 장벽과 부담 낮은 코스"),
         ("디지털 취약계층", "대면 창구 공백 지역 스크리닝"),
         ("상권 문턱값", "중심지 이론 기반 최소 수요 산정"),
         ("식품사막", "생활 필수시설 접근 공백"),
         ("독거노인 매칭", "고령 1인가구끼리 연결")]
grid = ''.join(
    f'<div class="hair" style="padding:8pt 0;"><h3 style="font-size:14pt;">{a}</h3>'
    f'<p class="small muted">{b}</p></div>' for a, b in ideas)
page("04 빅콘 · EXPLORE", "데이터안심구역과 빅콘을 동시에 뒤졌다",
     f'<div style="display:grid; grid-template-columns:repeat(3,1fr); column-gap:22pt;">{grid}</div>'
     '<p class="cap" style="margin-top:14pt;">9/17 하루 아이데이션 후보. 데이터로 증명할 수 있는지부터 따졌다</p>',
     sub="안심구역은 수상작, 센터별 데이터, 방문 조건까지 정리")

page("04 빅콘 · DECISION", "사회적 고립 예방 · 대응 AI 에이전트", two(
    '<p class="label red">DECISION · 9/20</p>'
    '<p style="font-size:16pt; margin-top:6pt;">빅콘테스트 AI데이터활용 분야<br>SK텔레콤 유동인구 × 신한카드 결제</p>'
    '<p class="small" style="margin-top:12pt;">주제와 타겟을 먼저 정하지 않고, <b>EDA 결과를 보고 결정</b>하기로 했다.</p>'
    '<p class="cap" style="margin-top:8pt;">1차 서류 평가는 아이디어 창의성과 데이터 근거가 각 25점</p>',
    '<p class="label">에이전트 흐름 초안</p>'
    + bullets(["위험 신호 탐지", "위험 요인 분석", "복지자원 검색", "맞춤형 개입안 제안", "담당자 검토 · 사후 모니터링"], pad=5),
    ratio="1.2fr 1fr"))

page("04 빅콘 · WHY", "사회적 고립은 왜 먼저 찾아야 하나", f'''
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20pt;">
  {stat("13.6", "%", "서울 1인가구 중 도움을 청할 사람이 한 명도 없는 비율")}
  {stat("1.29", "배", "사회적 고립의 사망 위험. 외로움 1.26배, 독거 1.32배")}
  {stat("26.6", "%", "고독사 최초 발견자가 가족인 경우")}
</div>
<p style="font-size:16pt; margin-top:22pt;">고독은 감정, 고립은 상태. 고립은 스스로 드러나지 않으니 <b>먼저 찾아야</b> 한다.</p>
<p class="cap" style="margin-top:6pt;">박민진 · 김성아(2022), Holt-Lunstad et al.(2015), 보건복지부 고독사 실태조사</p>''',
     sub="도움이 필요할 때 기댈 사람이 없는 상태 (통계청 사회적 고립도)")

page("04 빅콘 · DATA", "무엇으로 고립을 볼 것인가", table(
    ["구분", "데이터", "기관", "쓰임"],
    [["대회 제공", "이동전화 유동인구 (성 · 연령 · 시간대 · 요일)", "SK텔레콤", "활동 신호"],
     ["대회 제공", "카드 결제 · 이용고객 (주제2)", "신한카드", "소비 맥락"],
     ["외부", "SGIS 집계구 통계 297개 항목", "통계청", "지역 노출"],
     ["외부", "시민생활 데이터 (관심집단 · 통신정보)", "서울시", "외부 검증"],
     ["외부", "고립 · 은둔 청년 실태조사, 노인실태조사", "복지부 · 서울시", "고립 특징"],
     ["외부", "복지 · 공공기관 17,925곳, 지원사업 60건", "공공데이터포털 등", "추천"]],
    ["14%", "44%", "22%", "20%"]))

page("04 빅콘 · VERIFY", "명세서를 믿지 않고 원본 20개를 다 열었다", table(
    ["발견", "내용", "영향"],
    [["12월 파일 중복", "시간대 · 요일 테이블 12월 레코드가 정확히 2배", "모르고 쓰면 12월 수치 2배"],
     ["비식별 하한 컷", "카드 결제건수 5건 미만 셀 삭제", "고령층 · 춘천 등 희소 집단이 체계적으로 누락"],
     ["업종 금액 편중", "결제금액 50.7%가 미분류 · 세금공과금", "금액 지표에서 두 업종 제외"],
     ["양자화 단위", "SK 값이 0.0254 단위로 양자화", "양수 셀 약 2,100만 개가 이 규칙"],
     ["강남 유입", "유동인구가 거주인구의 최대 53.9배", "SK만으로 강남 주민 고립 측정은 어려움"]],
    ["18%", "46%", "36%"]),
    sub="데이터가 찾으려는 대상을 먼저 지울 수 있다")

page("04 빅콘 · INDEX v0", "지표를 합치기 전에, 같은 걸 재는지부터", two(
    '<p class="label red">김태은 · 지표 재설계</p>'
    '<div style="display:flex; align-items:baseline; gap:14pt; margin-top:6pt;">'
    '<p class="num" style="font-size:40pt;">-4.219</p><p class="muted">에서</p>'
    '<p class="num red" style="font-size:40pt;">0.720</p></div>'
    '<p class="small" style="margin-top:6pt;">서울연구원 4축을 빌린 1차 지수는 Cronbach α가 음수. 지표들이 고립이 아니라 <b>구매력</b>을 재고 있었다. 정의, 예측, 검증 순서로 다시 설계했다.</p>',
    '<p class="label red">이정연 · 재현 검증</p>'
    '<div style="display:flex; align-items:baseline; gap:14pt; margin-top:6pt;">'
    '<p class="num" style="font-size:40pt;">0.185</p><p class="muted">vs</p>'
    '<p class="num red" style="font-size:40pt;">0.589</p></div>'
    '<p class="small" style="margin-top:6pt;">같은 지수를 보고서만 보고 재현했더니 α가 달랐다. 원인은 <b>주말비 변수의 부호 하나</b>. 가정을 문서로 맞추는 게 코드보다 먼저였다.</p>'))

page("04 빅콘 · WHERE", "왜 강남과 춘천만 줬을까", f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:32pt;">
  <div class="dark" style="padding-top:10pt;"><p class="num" style="font-size:32pt;">강남구</p>
  <p class="muted">대도시 · 1인가구 · 직장 밀집 · 데이터의 15.5%</p></div>
  <div class="dark" style="padding-top:10pt;"><p class="num" style="font-size:32pt;">춘천시</p>
  <p class="muted">중소도시 · 고령화 · 넓은 외곽 · 데이터의 84.5%</p></div>
</div>
<p style="font-size:18pt; margin-top:24pt;">정반대인 두 지역에서 <b>모두 통하는 지표</b>를 만들면 된다.</p>
<p class="cap" style="margin-top:8pt;">강남은 외지 유입이 커서 주민 신호가 희석된다는 점도 데이터를 열어본 뒤에야 알았다.</p>''')

page("04 빅콘 · MAP", "춘천은 조용히 바뀌고 있었다", two(
    '<p class="label red">좌표부터 검증</p>'
    '<p class="small" style="margin-top:4pt;">UTM-K(EPSG:5179)를 적용해 SGIS 경계와 겹쳐 보니 강남 15,249개, 춘천 82,818개 지점이 경계 안, 밖은 62개뿐.</p>'
    '<div style="display:grid; grid-template-columns:1fr 1fr; gap:12pt; margin-top:14pt;">'
    + stat("0.994", "", "강남 7월 vs 12월 격자 순위상관", 32) + stat("0.835", "", "춘천 7월 vs 12월 격자 순위상관", 32) + '</div>'
    '<p class="cap" style="margin-top:10pt;">60대 이상 유동 비율은 강남 18.5~19.1%, 춘천 24.0~25.3%로 안정적</p>',
    '<p class="label red">10월에서 11월, 춘천 감소 지역</p>'
    + table(["지역", "유동인구 변화"], [["서면", "-29.8%"], ["남면", "-28.6%"], ["동산면", "-23.7%"], ["신동면", "-21.1%"], ["신북읍", "-21.0%"]], ["60%", "40%"])
    + '<p class="cap" style="margin-top:8pt;">전체 합계는 약 2% 감소. 합계만 보면 놓치는 변화</p>'),
    sub="진재언 · 87,448개 공통 격자로 7~12월 비교")

page("04 빅콘 · UNIT", "분석 단위를 집계구로 맞췄다", f'''
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt;">
  {stat("1,698", "", "분석 대상 집계구 (강남 + 춘천)", 32)}
  {stat("297", "", "SGIS 집계구 통계 항목", 32)}
  {stat("184", "", "분석에 쓸 항목만 남긴 결과", 32)}
  {stat("0.1", "명", "50m 격자 유동 중앙값. 격자 그대로는 노이즈", 32)}
</div>
<p class="small" style="margin-top:20pt;">코드 앞자리를 잘라 묶던 방식을 실제 경계 공간조인으로 바꾸고, 월 · 집계구마다 43개 지표의 합계, 평균, 유효 격자 수, 결측률을 냈다.</p><p class="cap" style="margin-top:4pt;">outer join으로 생긴 NULL은 0으로 바꾸거나 행째 지우지 않고 그대로 두었다</p>''')

page("04 빅콘 · WORKFLOW", "일하는 방식을 먼저 정했다", cols([
    ("ISSUE", "이슈로 쪼갠다", "작업마다 이슈를 열고 담당자, 산출물, 드라이브 위치까지 본문에 적었다"),
    ("BRANCH", "설계 문서부터", "이슈 헬퍼가 붙여 준 브랜치에서 설계 문서를 먼저 쓰고 시작했다"),
    ("CI", "테스트를 분리", "실데이터 없는 CI에서 깨지던 테스트를 pytest 마커로 분리했다"),
    ("WIKI", "근거는 위키로", "고립 연구와 조례 자료를 레포 위키로 공유했다"),
], gap=14), sub="10/8 주제설명자료가 갱신되며 탐지부터 복지자원 추천까지가 요구사항이 됐다")

# ================= 05 빅콘 분석·제출 =================
divider("05", "빅콘테스트 · 분석과 제출", "두 개의 신호와 하나의 에이전트", "WEEK 7 ~ 8")

page("05 분석 · WHY 집계구", "동 평균은 동네 안의 차이를 가린다", f'''
<div style="display:grid; grid-template-columns:1fr 1.15fr; gap:24pt; align-items:center;">
  <img src="./assets/map_yeoksam.png" alt="역삼2동 집계구별 1인가구 비율 지도" style="width:100%; height:236pt;">
  <div><p class="label red">역삼2동 1인가구 비율</p>
  <p class="num" style="font-size:48pt;">36.5<span style="font-size:20pt;">%</span></p>
  <p class="cap">동 평균</p>
  {bullets(["주택가 덩어리 <b>66%</b> vs 아파트 단지 <b>8%</b>",
            "20~50%인 집계구에 사는 가구는 약 <b>5%</b>뿐",
            "그래서 통계청이 공표하는 가장 작은 단위, <b>집계구</b>로 본다"])}</div>
</div>''')

page("05 분석 · STRUCTURE", "두 개의 신호를 교차한다", cols([
    ("STEP 1 · 어디가 위험한가", "고립 위험 지수", "SGIS 지표로 지역의 노출을 점수화. 관찰 후보 477곳"),
    ("STEP 2 · 누가 줄었나", "활동 저하 신호", "기대보다 유동이 적은 상태가 반복되는 곳. 60대 이상 461곳"),
    ("DICTIONARY", "위험 특징 사전", "실태조사 근거로 대화에서 확인할 24개 특징"),
    ("RESOURCE", "기관 태그", "기관 17,925곳을 서비스 태그 16종으로 분류"),
], gap=16) + '''
<div style="margin-top:20pt; background:#1A1A1A; padding:11pt 16pt; display:flex; justify-content:space-between; align-items:center;">
<p style="color:#FFFFFF; font-size:16pt; font-weight:700;">지역 유형 × 개인 티어로 관찰하고 연결하는 AI 에이전트</p>
<p class="cap" style="color:#BBBBBB;">재언 · 정연 · 태은</p></div>''')

page("05 분석 · STEP 1", "고립 위험 지수: 두 테마, 여섯 지표", f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:28pt;">
  <div><p class="label red">THEME A · 고령 + 독거</p>
  {bullets(["독거 · 연령: 1인가구율 × 50세 이상 비율",
            "노후주거: 1989년 이전 주택 × 비아파트 비율",
            "고령 비중: 65세 이상 비율"], pad=5)}</div>
  <div><p class="label red">THEME B · 중장년 독거 + 주거취약</p>
  {bullets(["남성 · 독거: 50~64세 남성 × 1인가구율",
            "비주택 · 연령: 고시원 등 거처 × 50세 이상",
            "소형 · 비주거: 비주거용 건물 내 주택, 20㎡ 이하"], pad=5)}</div>
</div>
<p class="small" style="margin-top:18pt;">테마별 표준화 점수를 백분위로 바꾸고, 종합 점수 = (A 백분위 + B 백분위) ÷ 2 를 1~5등급으로 나눴다.</p>
<p class="cap" style="margin-top:4pt;">참고: America's Health Rankings Senior Report, CDC SVI, OECD 합성지수 지침, 복지부 중장년 남성 고독사 위험</p>''')

page("05 분석 · STEP 1", "두 테마의 상위 지역은 절반만 겹친다", f'''
<div style="display:grid; grid-template-columns:1.5fr 1fr; gap:24pt; align-items:center;">
  <img src="./assets/map_theme.png" alt="테마 A, B 상위 집계구 지도" style="width:100%; height:240pt;">
  <div>
  <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:8pt;">
    {stat("159", "", "A만 상위", 28)}{stat("156", "", "중복", 28)}{stat("159", "", "B만 상위", 28)}
  </div>
  <p class="small" style="margin-top:16pt;">종합 등급만 쓰면 한쪽 테마의 높은 노출이 묻힌다. 종합 5등급에 더해 <b>한 테마라도 백분위 80 이상</b>인 곳을 관찰 후보로 넣었다.</p>
  <p class="num red" style="font-size:28pt; margin-top:10pt;">477<span style="font-size:14pt;"> 곳</span></p>
  <p class="cap">1,698개 집계구 중 관찰 후보</p></div>
</div>''')

page("05 분석 · STEP 2", "기대보다 덜 움직이는 동네를 찾는다", f'''
<div style="display:grid; grid-template-columns:1.25fr 1fr; gap:24pt; align-items:center;">
  <div><img src="./assets/chart_residual.png" alt="예시 집계구의 실제 대비 기대 유동 비율" style="width:100%; height:150pt;">
  <p class="cap" style="margin-top:6pt;">예시 집계구: 7·9·10·11월이 판정선 미만, 평균 로그 잔차 -0.108</p></div>
  <div>
  <p class="small"><b>기대 유동</b> = OLS(60대 이상 거주인구, 종사자 수, 다른 연령 유동, 월, 지역)</p>
  {bullets(["6개월 중 <b>4개월 이상</b> 로그 잔차 &lt; -0.1",
            "6개월 평균 로그 잔차 &lt; -0.1",
            "-0.1은 실제 유동이 기대보다 약 9.5% 적다는 뜻"], pad=5)}
  <p class="num red" style="font-size:28pt; margin-top:8pt;">461<span style="font-size:14pt;"> 곳</span></p>
  <p class="cap">60대 이상 활동 저하 신호 집계구</p></div>
</div>''')

page("05 분석 · VALIDATION", "만든 지표가 현실과 맞는가", f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:28pt;">
  <div><p class="label red">SGIS 지수 vs 서울시 관심집단 비율</p>
  {table(["지표", "순위상관 ρ"], [["테마 A 고령 · 독거", "+0.680"], ["테마 B 중장년 · 주거취약", "+0.633"], ["종합 점수", "+0.639"]], ["65%", "35%"])}
  <p class="cap" style="margin-top:6pt;">강남 22개 동 전체, 9개 대조 모두 양의 상관</p></div>
  <div><p class="label red">활동 신호율 vs 60대 이상 1인가구 통신정보</p>
  {table(["행동 지표", "평일 ρ", "휴일 ρ"], [["집 체류시간", "+0.509", "+0.438"], ["이동 횟수", "-0.601", "-0.493"]], ["50%", "25%", "25%"])}
  <p class="cap" style="margin-top:6pt;">신호가 많은 동일수록 집에 오래 머물고 덜 움직였다. 8개 대조 모두 예상 방향</p></div>
</div>
<p class="small" style="margin-top:16pt;">20~30대는 같은 방식이 맞지 않아 신호로 쓰지 않았다. 안 되는 것을 확인한 것도 결과였다.</p>''')

page("05 분석 · RESULT", "두 신호를 교차해 다섯 유형으로", f'''
<div style="display:grid; grid-template-columns:1.3fr 1fr; gap:22pt; align-items:center;">
  <img src="./assets/map_type.png" alt="지역 유형 분류 지도" style="width:100%; height:240pt;">
  <div>{table(["유형", "강남", "춘천", "합계"],
              [["<b class='red'>집중관찰</b>", "133", "24", "<b>157</b>"],
               ["잠재위험", "151", "120", "271"],
               ["활동저하", "157", "133", "290"],
               ["일반", "421", "232", "653"],
               ["확인필요", "236", "91", "327"]], ["40%", "20%", "20%", "20%"])}
  <p class="cap" style="margin-top:8pt;">집중관찰 = 지수 관찰 후보이면서 활동 신호도 나타난 곳. 판단이 보류된 곳은 지우지 않고 확인필요로 남겼다.</p></div>
</div>''')

page("05 분석 · DICTIONARY", "대화로 확인할 24개 위험 특징", f'''
<div style="display:grid; grid-template-columns:1.2fr 1fr; gap:28pt;">
  <div>{table(["범주", "특징 수", "대표 특징"],
              [["MIND 정신건강", "5", "우울 PHQ-9 10점 이상"],
               ["OUT 외출 · 활동", "2", "은둔 · 고립 1년 이상"],
               ["SOLO 독거", "2", "혼자 생활, 혼자 식사"],
               ["BODY 신체 · 일상", "5", "생활공간 관리 어려움"],
               ["REL 관계 단절", "7", "속마음 털어놓을 사람 없음"],
               ["ECON 경제", "2", "소득 활동 없음"],
               ["HOUSE 주거", "1", "고시원, 보증금 없는 월세"]], ["38%", "17%", "45%"])}</div>
  <div><p class="label red">정리 기준</p>
  {bullets(["고립 집단에서 많이 나타나는 특징만",
            "서울시 조사로 전체 청년보다 높은지 확인",
            "고립 판정에 쓴 문항은 근거에서 제외",
            "점수 없이 해당 여부만 본다"], pad=5)}
  <p class="cap" style="margin-top:8pt;">근거: 복지부 · 서울시 고립 · 은둔 청년 실태조사, 노인실태조사, 고독사 예방 기본계획</p></div>
</div>''')

page("05 에이전트 · LOGIC", "관찰하고, 판단하고, 연결한다", cols([
    ("1 OBSERVE", "관찰", "지역 유형으로 관찰 주기를 정하고 사용자의 변화를 계속 기록"),
    ("2 JUDGE", "판단", "대화 응답을 24개 특징에 매핑, 해당 범주 수로 티어 1~3"),
    ("3 CONNECT", "추천", "특징 × 기관 태그 44개 연결로 기관 17,925곳, 지원사업 60건 추천"),
    ("4 FOLLOW", "후속", "이용 결과를 확인하고 재분류. 공백은 지자체에 보고"),
], gap=16) + '''
<div style="margin-top:18pt; display:grid; grid-template-columns:1fr 1fr; gap:20pt;">
  <div class="redtop" style="padding-top:8pt;"><p class="small"><b class="red">위기는 사람이</b>&nbsp; 최근 2주 내 자살 · 자해 생각이나 시도가 나오면 티어 계산 없이 109와 지정 담당자에게 즉시 연결</p></div>
  <div class="hair" style="padding-top:8pt;"><p class="small"><b>개인을 판정하지 않는다</b>&nbsp; 지역 결과는 관찰 빈도만 바꾸고 개인 티어는 올리지 않는다</p></div>
</div>''')

flow = [("온보딩", "1년 넘게 거의 안 나갔어요", "OUT · ECON · HOUSE, 티어 2"),
        ("추천", "상담 해볼게요", "고립 전담기관 안내"),
        ("관찰", "요즘 잠을 잘 못 자요", "평소 상태 기록"),
        ("위기 감지", "사라지고 싶다는 생각이 들어요", "즉시 사람 연결"),
        ("후속", "센터에 두 번 다녀왔어요", "이용 확인 후 재분류")]
fl = ''.join(
    f'<div class="{"redtop" if i == 3 else "dark"}" style="padding-top:8pt;">'
    f'<p class="label {"red" if i == 3 else ""}">{a}</p><p class="small" style="margin-top:6pt;">"{b}"</p>'
    f'<p class="cap" style="margin-top:6pt;">{c}</p></div>' for i, (a, b, c) in enumerate(flow))
page("05 에이전트 · SCENARIO", "29세, 역삼1동, 1인가구",
     f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:12pt;">{fl}</div>'
     '<p class="cap" style="margin-top:20pt;">합성 페르소나 예시. 퇴사 후 1년 넘게 집에 있고, 생활비가 걱정이고, 속마음을 말할 사람이 없다.</p>',
     sub="한 사람의 사이클로 본 에이전트")

tl = [("10/20", "범주 확정 · 지수 v3", "발표자료 이슈 열고 제목 후보 회의"),
      ("10/22", "특징 24개 병합", "청년 21행 + 고령 12행 정리, 지수 외부 검증"),
      ("10/23", "발표 설계서", "슬라이드 설계를 마크다운으로 관리"),
      ("10/24", "기관 매핑 44개", "에이전트 설계로 핸드오프, PPT 초안"),
      ("10/25", "제출 코드 정리", "허술해 보이는 문서 정리, README"),
      ("10/26", "23:01 제출", "LLM 활용 문서와 합성 시나리오까지")]
t = ''.join(
    f'<div class="{"redtop" if i == 5 else "dark"}" style="padding-top:8pt;">'
    f'<p class="num {"red" if i == 5 else ""}" style="font-size:22pt;">{d}</p>'
    f'<h3 style="font-size:14pt; margin-top:4pt;">{h}</h3><p class="cap" style="margin-top:4pt;">{b}</p></div>'
    for i, (d, h, b) in enumerate(tl))
page("05 제출 · WEEK 8", "마지막 일주일",
     f'<div style="display:grid; grid-template-columns:repeat(6,1fr); gap:10pt;">{t}</div>',
     sub="흩어진 이슈를 하나의 흐름으로 묶은 일주일")

page("05 제출 · OUTPUT", "집계구 기반 사회적 고립 조기 탐지 및 지속 관리", f'''
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20pt;">
  {stat("23", "쪽", "결과보고서 (문제 정의, 분석 방법, 결과, 에이전트, 기대효과)", 40)}
  {stat("11", "편", "참고문헌", 40)}
  {stat("7", "종", "사용 데이터 (대회 제공 2 + 외부 5)", 40)}
</div>
<p style="font-size:16pt; margin-top:22pt;">지역의 신호를 복지 지원으로 연결하는 AI 에이전트</p>
<p class="cap" style="margin-top:4pt;">발표자료 PDF, 코드 · README · LLM 활용 문서를 담은 zip으로 제출</p>''')

# ================= 06 회고 =================
divider("06", "회고", "숫자와 배운 점", "RETRO")

page("06 회고 · NUMBERS", "숫자로 본 8주", f'''
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt;">
  {stat("8", "주", "심화세션")}
  {stat("3", "개", "참가한 공모전")}
  {stat("20", "개", "전수 검증한 제공 데이터 파일")}
  {stat("229", "개", "빅콘 레포 커밋")}
</div>
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt; margin-top:18pt;">
  {stat("1,101", "", "비자 공통 스키마 레코드")}
  {stat("407", "개", "비자 데이터 자동 검증 테스트")}
  {stat("1,698", "", "분석한 집계구")}
  {stat("17,925", "", "연결한 복지 · 공공기관")}
</div>''')

page("06 회고 · LEARNED", "8주 동안 배운 네 가지", f'''
<div style="display:grid; grid-template-columns:1fr 1fr; column-gap:28pt; row-gap:16pt;">
  <div class="dark" style="padding-top:8pt;"><h3>문서와 원본은 다르다</h3>
  <p class="small" style="margin-top:4pt;">PDF 변환본은 숫자를 잃었고, 데이터 명세서는 12월 중복을 말해 주지 않았다.</p></div>
  <div class="dark" style="padding-top:8pt;"><h3>작은 가정 하나가 결론을 바꾼다</h3>
  <p class="small" style="margin-top:4pt;">α 0.185와 0.589의 차이는 변수 부호 하나였다. 가정을 먼저 문서로 맞춘다.</p></div>
  <div class="dark" style="padding-top:8pt;"><h3>근거와 안전한 실패가 먼저다</h3>
  <p class="small" style="margin-top:4pt;">RAG의 품질은 생성이 아니라 검색과 검증에서 갈렸다.</p></div>
  <div class="dark" style="padding-top:8pt;"><h3>점수는 판정이 아니라 우선순위</h3>
  <p class="small" style="margin-top:4pt;">우리 데이터로 볼 수 있는 건 고립의 간접 신호뿐. "먼저 확인할 지역"으로 말한다.</p></div>
</div>''')

page("06 회고 · KPT", "계속할 것과 아쉬웠던 것", f'''
<div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:22pt;">
  <div><p class="label red">KEEP</p>
  {bullets(["원본을 전수 확인하고, 팀원 결과도 직접 재현하기",
            "정정한 사실과 데이터 규칙은 테스트로 고정하기",
            "결론을 확정과 잠정으로 나눠 공유하기"], pad=6)}</div>
  <div><p class="label">PROBLEM</p>
  {bullets(["검증에 시간이 쏠려 에이전트 설계가 늦었다",
            "작업이 큰 PR 하나로 몰려 리뷰가 부담됐다",
            "기능 구현에 집중해 사용자 효과를 실측하지 못했다"], pad=6)}</div>
  <div><p class="label red">TRY</p>
  {bullets(["재현 전에 원 코드와 단위 · 부호 · 필터부터 맞추기",
            "수치를 인용할 때 출처 데이터를 함께 적기",
            "작업은 작은 PR로 나눠 올리기"], pad=6)}</div>
</div>''', sub="세 명의 주차 보고서에서")

photos = ''.join(
    f'<img src="./assets/photos/photo-{i}.png" alt="팀 활동 사진 {i}" style="width:100%; height:114pt; object-fit:cover;">'
    for i in range(1, 5))
page("06 회고 · TOGETHER", "함께한 8주",
     f'<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:12pt;">{photos}</div>'
     '<p class="cap" style="margin-top:14pt;">함께 작업하던 날들</p>')

raw(f'''<body style="justify-content:space-between;">{strip("CLOSING")}
<div><h1 style="font-size:52pt;">감사합니다</h1><div class="rule" style="margin:14pt 0;"></div>
<p class="num" style="font-size:20pt;">Team Hambugi</p>
<p class="cap" style="margin-top:4pt;">김태은 · 이정연 · 진재언</p></div>
<div style="height:8pt; background:#1A1A1A;"></div></body></html>''')

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
