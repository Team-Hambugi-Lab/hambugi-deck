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
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@1,600&display=swap">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { width: 720pt; height: 405pt; background: #FFFFFF; color: #1A1A1A;
  font-family: 'Pretendard', sans-serif; padding: 32pt 44pt; display: flex; flex-direction: column; }
.strip { display: flex; justify-content: space-between; align-items: center; }
.label { font-size: 10pt; font-weight: 600; letter-spacing: 0.14em; color: #888888; }
.num { font-family: 'Playfair Display', serif; font-style: italic; font-weight: 600; line-height: 1.4; padding-bottom: 2pt; }
.rule { width: 48pt; height: 2pt; background: #E63030; margin: 10pt 0 0; }
h1 { font-size: 28pt; font-weight: 700; line-height: 1.3; letter-spacing: -0.02em; }
h2 { font-size: 20pt; font-weight: 700; line-height: 1.4; }
h3 { font-size: 16pt; font-weight: 700; line-height: 1.4; }
p, li { font-size: 14pt; line-height: 1.55; }
b { font-weight: 700; }
.muted { color: #888888; }
.red { color: #E63030; }
.cap { font-size: 12pt; color: #888888; line-height: 1.5; }
.small { font-size: 12pt; line-height: 1.5; }
ul { list-style: none; }
.hair { border-top: 1pt solid #BBBBBB; }
.dark { border-top: 2pt solid #1A1A1A; }
.redtop { border-top: 2pt solid #E63030; }
img { display: block; object-fit: contain; }
table { border-collapse: collapse; width: 100%; }
td, th { font-size: 12pt; padding: 5pt 6pt; text-align: left; border-top: 1pt solid #BBBBBB; }
th { font-weight: 700; border-top: 2pt solid #1A1A1A; }
</style>
</head>
"""

S = {}


def strip(label, n):
    """상단 라벨 띠."""
    return (f'<div class="strip"><p class="label">{label}</p>'
            f'<p class="label">{n:02d} / {{TOTAL}}</p></div>')


def page(n, label, title, body, sub=""):
    """일반 콘텐츠 슬라이드."""
    sub_html = f'<p class="muted" style="font-size:14pt; margin-top:4pt;">{sub}</p>' if sub else ""
    S[n] = (HEAD + f'<body>{strip(label, n)}'
            f'<div style="margin-top:14pt;"><h1>{title}</h1>{sub_html}<div class="rule"></div></div>'
            f'<div style="flex:1; display:flex; flex-direction:column; justify-content:center;">'
            f'{body}</div></body></html>')


def divider(n, num, title, sub, weeks):
    """섹션 디바이더."""
    S[n] = (HEAD + f'''<body style="justify-content:space-between;">{strip("SECTION " + num, n)}
<div style="display:flex; align-items:flex-end; gap:28pt;">
  <p class="num" style="font-size:120pt; line-height:1.4;">{num}</p>
  <div style="padding-bottom:22pt;"><p class="label red">{weeks}</p>
  <h1 style="font-size:40pt; margin-top:6pt;">{title}</h1>
  <p class="muted" style="font-size:16pt; margin-top:6pt;">{sub}</p></div>
</div>
<div style="height:8pt; background:#1A1A1A;"></div></body></html>''')


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


# ---------- 도입 ----------
S[1] = HEAD + '''<body style="justify-content:space-between;">
<div class="strip"><p class="label">TOBIGS 심화세션 활동 공유</p><p class="label">2026.09.10 ~ 10.26</p></div>
<div><p class="num red" style="font-size:20pt;">Team Hambugi</p>
<h1 style="font-size:52pt; margin-top:6pt;">7주, 대회 셋,<br>제출 하나</h1>
<div class="rule" style="margin:14pt 0;"></div>
<p style="font-size:16pt;">사회적 고립 예방 AI 에이전트를 만들기까지의 기록</p></div>
<div class="strip hair" style="padding-top:10pt;"><p class="cap">김태은 · 이정연 · 진재언</p>
<p class="cap">01 / {TOTAL}</p></div></body></html>'''

page(2, "TEAM", "팀 햄부기", cols([
    ("김태은", "에이전트 · 기관", "복지·공공기관 수집과 태그 분류, 에이전트 설계와 사용자 흐름"),
    ("이정연", "신호 · 사전 · 검증", "활동 저하 신호, 위험 특징 사전, 외부 검증, 발표 설계와 제출 정리"),
    ("진재언", "지수 · 지도", "상권 통합과 QGIS 시각화, SGIS 고립 위험 지수 v1에서 v3.3까지"),
], gap=24), sub="팀명의 부기는 거북이에서 따왔다")

toc = [("01", "탐색", "무엇을 할 것인가", "1~2주차"),
       ("02", "데이터 이해", "강남과 춘천, 그리고 집계구", "3~5주차"),
       ("03", "분석", "두 개의 신호와 하나의 사전", "6주차"),
       ("04", "에이전트·제출", "결과를 서비스 흐름으로", "7주차"),
       ("05", "회고", "숫자와 배운 점", "")]
rows = ''.join(
    f'<div class="hair" style="display:grid; grid-template-columns:52pt 1fr 1.4fr 70pt; '
    f'align-items:baseline; padding:6pt 0;"><p class="num red" style="font-size:20pt;">{a}</p>'
    f'<h3>{b}</h3><p class="muted">{c}</p><p class="cap" style="text-align:right;">{d}</p></div>'
    for a, b, c, d in toc)
page(3, "CONTENTS", "목차", rows)

weeks = [("W1", "9/8", "안심구역 데이터 명세와 수상작 분석"),
         ("W2", "9/15", "주제 대량 발산, 빅콘 주제 확정"),
         ("W3", "9/22", "제공 데이터 EDA, 강남·춘천 해석"),
         ("W4", "9/29", "집계구 마스터, CI·로더 정비"),
         ("W5", "10/6", "요구사항 갱신, 방법론 위키"),
         ("W6", "10/13", "이슈 분할, 지수·신호·사전"),
         ("W7", "10/20", "통합, 발표자료, 10/26 제출")]
wk = ''.join(
    f'<div class="{"redtop" if i == 6 else "dark"}" style="padding-top:8pt;">'
    f'<p class="num {"red" if i == 6 else ""}" style="font-size:24pt;">{a}</p>'
    f'<p class="cap">{b}</p><p class="small" style="margin-top:6pt;">{c}</p></div>'
    for i, (a, b, c) in enumerate(weeks))
page(4, "OVERVIEW", "7주를 한 장으로",
     f'<div style="display:grid; grid-template-columns:repeat(7,1fr); gap:10pt;">{wk}</div>'
     '<p class="cap" style="margin-top:22pt;">주차는 월요일 기준. 세션 기록, GitHub 이슈 21개, 커밋 229개를 바탕으로 정리</p>')

# ---------- 01 탐색 ----------
divider(5, "01", "탐색", "무엇을 할 것인가", "WEEK 1 ~ 2")

page(6, "01 탐색 · WEEK 0", "출발점은 탈락이었다", f'''
<div style="display:grid; grid-template-columns:1fr 1.1fr; gap:32pt; align-items:center;">
  <div><p class="num" style="font-size:44pt;">ICT</p>
  <p style="font-size:16pt; margin-top:4pt;">8월 ICT융합 공모전에 낸<br><b>비자부기</b>가 탈락했다.</p>
  <p class="cap" style="margin-top:10pt;">심화세션은 이 회고에서 시작했다.</p></div>
  {bullets([
      '<b class="red num">9/13</b>&nbsp; 사업계획서 기준으로 탈락 원인을 분석',
      '<b class="red num">9/17</b>&nbsp; GitHub 조직을 Team-Hambugi로 새로 정비',
      '<b class="red num">9/20</b>&nbsp; 비자부기는 사업화 대신 팀 학습용 실험 프로젝트로',
      '<b class="red num">9/20</b>&nbsp; 운영 DB와 분석 DB를 나누는 구조를 공부하기로',
  ], pad=8)}
</div>''')

page(7, "01 탐색 · WEEK 1", "데이터안심구역부터 뜯어봤다", cols([
    ("RULE", "직접 가야 한다", "데이터는 센터 안에서만 분석 가능. 방문 일수가 정량 평가에 들어간다"),
    ("DATA", "센터마다 데이터가 다르다", "수도권 센터에서 받을 수 있는 데이터부터 다시 추렸다"),
    ("AWARD", "수상작은 결합한다", "역대 수상작은 대부분 여러 데이터를 결합해 하나의 처방까지 냈다"),
]), sub="데이터 명세, 참가 규정, 역대 수상작을 Notion에 정리")

ideas = [("감각부하 기상도", "환승역 시간대별 감각 부하 예측", "안심구역 데이터가 주인공이 되기 어려움"),
         ("신경다양 아동 가족", "생활권 이용 장벽과 부담 낮은 코스", "대상 아동 분포를 데이터로 찾기 어려움"),
         ("디지털 취약계층", "대면 창구 공백 지역 스크리닝", "발굴 결과를 검증할 방법이 약함"),
         ("상권 문턱값", "중심지 이론 기반 최소 수요 산정", "AI 요소가 약하고 기존 서비스와 겹침"),
         ("식품사막", "생활 필수시설 접근 공백", "국내 선행 연구가 이미 다수"),
         ("독거노인 매칭", "고령 1인가구끼리 연결", "빅콘 고립 주제로 이어짐")]
grid = ''.join(
    f'<div class="hair" style="padding:7pt 0;"><h3 style="font-size:14pt;">{a}</h3>'
    f'<p class="small">{b}</p><p class="cap">{c}</p></div>' for a, b, c in ideas)
page(8, "01 탐색 · 9/17", "하루 동안 주제를 쏟아냈다",
     f'<div style="display:grid; grid-template-columns:repeat(3,1fr); column-gap:22pt;">{grid}</div>',
     sub="떠오르면 바로 기획안으로 써 보고, 데이터로 증명할 수 있는지부터 따졌다")

page(9, "01 탐색 · 9/20", "사회적 고립 예방·대응 AI 에이전트", f'''
<div style="display:grid; grid-template-columns:1fr 1.2fr; gap:32pt;">
  <div><p class="label red">DECISION</p>
  <p style="font-size:16pt; margin-top:6pt;">빅콘테스트 AI데이터활용 분야<br>SK텔레콤 유동인구 × 신한카드 결제</p>
  <p class="cap" style="margin-top:10pt;">같은 날 레포와 가상환경을 세팅하고 첫 이슈를 셋이 함께 열었다.</p></div>
  <div><p class="label">주최 측 필수 포함 요소</p>
  {bullets(["<b>1</b>&nbsp; 데이터 기반 인사이트: 위험 신호, 특성, 영향 요인",
            "<b>2</b>&nbsp; AI 에이전트 설계: 탐지, 분석, 추천",
            "<b>3</b>&nbsp; 운영 흐름",
            "<b>4</b>&nbsp; 재현 가능한 설명: 판단 기준, 산출식, 추천 로직"])}</div>
</div>''')

page(10, "01 탐색 · WHY", "사회적 고립은 왜 먼저 찾아야 하나", f'''
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20pt;">
  {stat("13.6", "%", "서울 1인가구 중 도움을 청할 사람이 한 명도 없는 비율")}
  {stat("1.29", "배", "사회적 고립의 사망 위험. 외로움 1.26배, 독거 1.32배")}
  {stat("26.6", "%", "고독사 최초 발견자가 가족인 경우")}
</div>
<p style="font-size:16pt; margin-top:24pt;">고립은 스스로 드러나지 않는다. 신호를 기다리지 말고 <b>먼저 찾아야</b> 한다.</p>
<p class="cap" style="margin-top:6pt;">박민진·김성아(2022), Holt-Lunstad et al.(2015), 보건복지부 고독사 실태조사</p>''',
     sub="도움이 필요할 때 기댈 사람이 없는 상태 (통계청 사회적 고립도)")

# ---------- 02 데이터 이해 ----------
divider(11, "02", "데이터 이해", "강남과 춘천, 그리고 집계구", "WEEK 3 ~ 5")

page(12, "02 데이터 이해 · DATA", "무엇으로 고립을 볼 것인가", table(
    ["구분", "데이터", "기관", "쓰임"],
    [["대회 제공", "이동전화 유동인구 (성·연령·시간대·요일)", "SK텔레콤", "활동 신호"],
     ["대회 제공", "카드 결제·이용고객 (주제2)", "신한카드", "소비 맥락"],
     ["외부", "SGIS 집계구 통계 297개 항목", "통계청", "지역 노출"],
     ["외부", "시민생활 데이터 (관심집단·통신정보)", "서울시", "외부 검증"],
     ["외부", "고립·은둔 청년 실태조사, 노인실태조사", "복지부·서울시", "고립 특징"],
     ["외부", "복지·공공기관 17,925곳, 지원사업 60건", "공공데이터포털 등", "추천"]],
    ["14%", "44%", "22%", "20%"]))

page(13, "02 데이터 이해 · WEEK 3", "왜 강남과 춘천만 줬을까", f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:32pt;">
  <div class="dark" style="padding-top:10pt;"><p class="num" style="font-size:32pt;">Gangnam</p>
  <p class="muted">대도시 · 1인가구 · 직장 밀집 · 3.4 km</p></div>
  <div class="dark" style="padding-top:10pt;"><p class="num" style="font-size:32pt;">Chuncheon</p>
  <p class="muted">중소도시 · 고령화 · 넓은 외곽 · 15.4 km</p></div>
</div>
<p style="font-size:18pt; margin-top:24pt;">정반대인 두 지역에서 <b>모두 통하는 지표</b>를 만들면 된다.</p>
<p class="cap" style="margin-top:8pt;">EDA 중 춘천 일부 성·연령 집단에서 유동인구와 카드 결제가 함께 줄어든 것을 보고, 지역을 넓히기보다 두 지역을 깊게 보기로 했다.</p>''')

page(14, "02 데이터 이해 · WEEK 4", "분석 단위를 집계구로 맞췄다", f'''
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt;">
  {stat("1,698", "", "분석 대상 집계구 (강남 + 춘천)", 32)}
  {stat("297", "", "SGIS 집계구 통계 항목", 32)}
  {stat("184", "", "분석에 쓸 항목만 남긴 결과", 32)}
  {stat("6", "", "최종 위험 요인 지표", 32)}
</div>
<p class="small" style="margin-top:22pt;">인구 71 · 가구 8 · 주택 36 · 사업체 182개 항목을 집계구 마스터 테이블 하나로 결합하고, 결측과 no_record 처리 규칙을 팀 공통으로 정했다.</p>''')

page(15, "02 데이터 이해 · WEEK 5", "일하는 방식을 먼저 정했다", cols([
    ("ISSUE", "이슈로 쪼갠다", "작업 단위마다 이슈를 열고 담당자와 산출물, 드라이브 위치까지 본문에 적었다"),
    ("BRANCH", "봇이 브랜치를 판다", "이슈 헬퍼가 붙여 준 이름으로 브랜치를 만들고 설계 문서부터 썼다"),
    ("PR", "PR로 합친다", "CI에서 실데이터 테스트를 분리하고 squash 머지로 이력을 정리했다"),
    ("WIKI", "근거는 위키로", "고립 연구와 조례 자료를 레포 위키로 공유했다"),
], gap=16), sub="10/8 주최 측 주제설명자료가 갱신되며 탐지부터 복지자원 추천까지가 요구사항이 됐다")

# ---------- 03 분석 ----------
divider(16, "03", "분석", "두 개의 신호와 하나의 사전", "WEEK 6")

page(17, "03 분석 · WHY 집계구", "동 평균은 동네 안의 차이를 가린다", f'''
<div style="display:grid; grid-template-columns:1fr 1.15fr; gap:24pt; align-items:center;">
  <img src="./assets/map_yeoksam.png" alt="역삼2동 집계구별 1인가구 비율 지도" style="width:100%; height:236pt;">
  <div><p class="label red">역삼2동 1인가구 비율</p>
  <p class="num" style="font-size:48pt;">36.5<span style="font-size:20pt;">%</span></p>
  <p class="cap">동 평균</p>
  {bullets(["주택가 덩어리 <b>66%</b> vs 아파트 단지 <b>8%</b>",
            "20~50%인 집계구에 사는 가구는 약 <b>5%</b>뿐",
            "그래서 통계청이 공표하는 가장 작은 단위, <b>집계구</b>로 본다"])}</div>
</div>''')

page(18, "03 분석 · STRUCTURE", "두 개의 신호를 교차한다", cols([
    ("STEP 1 · 어디가 위험한가", "고립 위험 지수", "SGIS 지표로 지역의 노출을 점수화. 관찰 후보 477곳"),
    ("STEP 2 · 누가 줄었나", "활동 저하 신호", "기대보다 유동이 적은 상태가 반복되는 곳. 60대 이상 461곳"),
    ("DICTIONARY", "위험 특징 사전", "실태조사 근거로 대화에서 확인할 24개 특징"),
    ("RESOURCE", "기관 태그", "기관 17,925곳을 서비스 태그 16종으로 분류"),
], gap=16) + '''
<div style="margin-top:20pt; background:#1A1A1A; padding:11pt 16pt; display:flex; justify-content:space-between; align-items:center;">
<p style="color:#FFFFFF; font-size:16pt; font-weight:700;">지역 유형 × 개인 티어로 관찰하고 연결하는 AI 에이전트</p>
<p class="cap" style="color:#BBBBBB;">재언 · 정연 · 태은</p></div>''')

page(19, "03 분석 · STEP 1", "고립 위험 지수: 두 테마, 여섯 지표", f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:28pt;">
  <div><p class="label red">THEME A · 고령 + 독거</p>
  {bullets(["독거·연령: 1인가구율 × 50세 이상 비율",
            "노후주거: 1989년 이전 주택 × 비아파트 비율",
            "고령 비중: 65세 이상 비율"], pad=5)}</div>
  <div><p class="label red">THEME B · 중장년 독거 + 주거취약</p>
  {bullets(["남성·독거: 50~64세 남성 × 1인가구율",
            "비주택·연령: 고시원 등 거처 × 50세 이상",
            "소형·비주거: 비주거용 건물 내 주택, 20㎡ 이하"], pad=5)}</div>
</div>
<p class="small" style="margin-top:18pt;">테마별 표준화 점수를 백분위로 바꾸고, 종합 점수 = (A 백분위 + B 백분위) ÷ 2 를 1~5등급으로 나눴다.</p>
<p class="cap" style="margin-top:4pt;">참고: America's Health Rankings Senior Report, CDC SVI, OECD 합성지수 지침, 복지부 중장년 남성 고독사 위험</p>''')

page(20, "03 분석 · STEP 1", "두 테마의 상위 지역은 절반만 겹친다", f'''
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

page(21, "03 분석 · STEP 2", "기대보다 덜 움직이는 동네를 찾는다", f'''
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

page(22, "03 분석 · VALIDATION", "만든 지표가 현실과 맞는가", f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:28pt;">
  <div><p class="label red">SGIS 지수 vs 서울시 관심집단 비율</p>
  {table(["지표", "순위상관 ρ"], [["테마 A 고령·독거", "+0.680"], ["테마 B 중장년·주거취약", "+0.633"], ["종합 점수", "+0.639"]], ["65%", "35%"])}
  <p class="cap" style="margin-top:6pt;">강남 22개 동 전체, 9개 대조 모두 양의 상관</p></div>
  <div><p class="label red">활동 신호율 vs 60대 이상 1인가구 통신정보</p>
  {table(["행동 지표", "평일 ρ", "휴일 ρ"], [["집 체류시간", "+0.509", "+0.438"], ["이동 횟수", "-0.601", "-0.493"]], ["50%", "25%", "25%"])}
  <p class="cap" style="margin-top:6pt;">신호가 많은 동일수록 집에 오래 머물고 덜 움직였다. 8개 대조 모두 예상 방향</p></div>
</div>
<p class="small" style="margin-top:16pt;">20~30대는 같은 방식이 맞지 않아 신호로 쓰지 않았다. 안 되는 것을 확인한 것도 결과였다.</p>''')

page(23, "03 분석 · RESULT", "두 신호를 교차해 다섯 유형으로", f'''
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

page(24, "03 분석 · DICTIONARY", "대화로 확인할 24개 위험 특징", f'''
<div style="display:grid; grid-template-columns:1.2fr 1fr; gap:28pt;">
  <div>{table(["범주", "특징 수", "대표 특징"],
              [["MIND 정신건강", "5", "우울 PHQ-9 10점 이상"],
               ["OUT 외출·활동", "2", "은둔·고립 1년 이상"],
               ["SOLO 독거", "2", "혼자 생활, 혼자 식사"],
               ["BODY 신체·일상", "5", "생활공간 관리 어려움"],
               ["REL 관계 단절", "7", "속마음 털어놓을 사람 없음"],
               ["ECON 경제", "2", "소득 활동 없음"],
               ["HOUSE 주거", "1", "고시원, 보증금 없는 월세"]], ["38%", "17%", "45%"])}</div>
  <div><p class="label red">정리 기준</p>
  {bullets(["고립 집단에서 많이 나타나는 특징만",
            "서울시 조사로 전체 청년보다 높은지 확인",
            "고립 판정에 쓴 문항은 근거에서 제외",
            "점수 없이 해당 여부만 본다"], pad=5)}
  <p class="cap" style="margin-top:8pt;">근거: 복지부·서울시 고립·은둔 청년 실태조사, 노인실태조사, 고독사 예방 기본계획</p></div>
</div>''')

# ---------- 04 에이전트·제출 ----------
divider(25, "04", "에이전트·제출", "결과를 서비스 흐름으로", "WEEK 7")

page(26, "04 에이전트 · LOGIC", "관찰하고, 판단하고, 연결한다", cols([
    ("1 OBSERVE", "관찰", "지역 유형으로 관찰 주기를 정하고 사용자의 변화를 계속 기록"),
    ("2 JUDGE", "판단", "대화 응답을 24개 특징에 매핑, 해당 범주 수로 티어 1~3"),
    ("3 CONNECT", "추천", "특징 × 기관 태그 44개 연결로 기관 17,925곳, 지원사업 60건 추천"),
    ("4 FOLLOW", "후속", "이용 결과를 확인하고 재분류. 공백은 지자체에 보고"),
], gap=16) + '''
<div style="margin-top:18pt; display:grid; grid-template-columns:1fr 1fr; gap:20pt;">
  <div class="redtop" style="padding-top:8pt;"><p class="small"><b class="red">위기는 사람이</b>&nbsp; 최근 2주 내 자살·자해 생각이나 시도가 나오면 티어 계산 없이 109와 지정 담당자에게 즉시 연결</p></div>
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
page(27, "04 에이전트 · SCENARIO", "29세, 역삼1동, 1인가구",
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
page(28, "04 제출 · WEEK 7", "마지막 일주일",
     f'<div style="display:grid; grid-template-columns:repeat(6,1fr); gap:10pt;">{t}</div>',
     sub="흩어진 이슈를 하나의 흐름으로 묶은 일주일")

page(29, "04 제출 · OUTPUT", "집계구 기반 사회적 고립 조기 탐지 및 지속 관리", f'''
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20pt;">
  {stat("23", "쪽", "결과보고서 (문제 정의, 분석 방법, 결과, 에이전트, 기대효과)", 40)}
  {stat("11", "편", "참고문헌", 40)}
  {stat("7", "종", "사용 데이터 (대회 제공 2 + 외부 5)", 40)}
</div>
<p style="font-size:16pt; margin-top:22pt;">지역의 신호를 복지 지원으로 연결하는 AI 에이전트</p>
<p class="cap" style="margin-top:4pt;">발표자료 PDF, 코드·README·LLM 활용 문서를 담은 zip으로 제출</p>''')

# ---------- 05 회고 ----------
divider(30, "05", "회고", "숫자와 배운 점", "RETRO")

page(31, "05 회고 · NUMBERS", "숫자로 본 7주", f'''
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt;">
  {stat("7", "주", "9/10 ~ 10/26")}
  {stat("3", "개", "검토한 대회")}
  {stat("21", "개", "GitHub 이슈")}
  {stat("229", "개", "커밋")}
</div>
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt; margin-top:18pt;">
  {stat("1,698", "", "집계구")}
  {stat("17,925", "", "복지·공공기관")}
  {stat("24", "개", "위험 특징")}
  {stat("1", "번", "제출")}
</div>''')

page(32, "05 회고 · LESSONS", "잘한 것과 아쉬운 것", f'''
<div style="display:grid; grid-template-columns:1fr 1fr; gap:28pt;">
  <div><p class="label red">KEEP</p>
  {bullets(["이슈 단위로 쪼개 셋이 병렬로 움직였다",
            "결정과 근거를 이슈 코멘트와 문서에 남겼다",
            "Claude Code·Codex로 탐색과 문서 작업 속도를 냈다",
            "TODO 팀원 의견"], pad=6)}</div>
  <div><p class="label">PROBLEM</p>
  {bullets(["주제를 정하기까지 2주가 걸렸다",
            "지수 버전이 바뀔 때마다 하류 작업을 다시 돌렸다",
            "에이전트는 설계까지만, 실제 구동은 못 했다",
            "TODO 팀원 의견"], pad=6)}</div>
</div>''')

S[33] = HEAD + f'''<body style="justify-content:space-between;">{strip("CLOSING", 33)}
<div><h1 style="font-size:52pt;">감사합니다</h1><div class="rule" style="margin:14pt 0;"></div>
<p class="num" style="font-size:20pt;">Team Hambugi</p>
<p class="cap" style="margin-top:4pt;">김태은 · 이정연 · 진재언</p></div>
<div style="height:8pt; background:#1A1A1A;"></div></body></html>'''

TOTAL = len(S)
assert sorted(S) == list(range(1, TOTAL + 1)), "슬라이드 번호 누락"
BANNED = re.compile("[—–−―→]")  # 긴 하이픈, en dash, 마이너스, 화살표
for f in OUT.glob("slide-*.html"):
    f.unlink()
for n, html in S.items():
    html = html.replace("{TOTAL}", str(TOTAL))
    assert not BANNED.search(html), f"slide {n}: 금지 문자 {BANNED.findall(html)}"
    (OUT / f"slide-{n:02d}.html").write_text(html, encoding="utf-8")
print("ok", TOTAL)
