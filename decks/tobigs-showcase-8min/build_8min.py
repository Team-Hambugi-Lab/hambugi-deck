"""투빅스 심화세션 발표회 8분판 (15장). 도입 · 방법 · 결과 · 마무리 구조.

사용법: python3 decks/tobigs-showcase-8min/build_8min.py decks/tobigs-showcase-8min
"""
import sys
from pathlib import Path

# ponytail: 디자인 헬퍼는 전체판 스크립트의 도입부를 그대로 실행해 공유한다. 덱이 더 늘면 모듈로 분리.
_full = Path(__file__).resolve().parent.parent / "tobigs-showcase" / "build_slides.py"
exec(_full.read_text(encoding="utf-8").split("# ================= 도입")[0])  # noqa: S102

# ================= 도입 (1분) =================
raw('''<body style="justify-content:space-between;">
<div class="strip"><p class="label">TOBIGS 26기 심화세션 결과 발표회</p><p class="label">4조</p></div>
<div><h1 style="font-size:52pt;">투빅스 심화세션 발표회</h1>
<p class="num red" style="font-size:24pt; margin-top:6pt;">Team Hambugi</p>
<div class="rule" style="margin:14pt 0;"></div>
<p style="font-size:14pt;">데이터 엔지니어링을 배우고, 바로 공모전에 써 본 8주</p></div>
<div class="strip hair" style="padding-top:10pt;"><p class="cap">김태은 · 이정연 · 진재언</p>
<p class="cap">01 / {TOTAL}</p></div></body></html>''')

page("도입 · TEAM", "팀 햄부기", two(cols([
    ("김태은", "파이프라인 · 검증", "공고 파이프라인, 비자부기 서비스, 빅콘 데이터 전수 검증과 지표 재설계"),
    ("이정연", "모델링 · 분석 · 설계", "HWPX 원문 파싱, 미래에셋 RAG, 빅콘 활동 신호와 위험 특징 사전"),
    ("진재언", "구조화 · 공간 · 지수", "F-2-R 공고 구조화, 공통 스키마 v2, SK 데이터 통합, SGIS 위험 지수"),
], gap=14), '<img src="./assets/team_logo.png" alt="Team Hambugi 로고" style="width:100%; height:170pt;">',
    ratio="3fr 1fr", gap=20), sub="데이터 엔지니어링 트랙. 팀명의 부기는 거북이에서 따왔다")

page("도입 · OVERVIEW", "8주, 공모전 셋", cols([
    ("1주차", "데이터 엔지니어링 학습", "개론 · 저장과 모델링 · 오케스트레이션을 셋이 나눠 발표"),
    ("2~3주차", "ICT융합 공모전 · 비자부기", "충북 외국인 주민 비자 준비 서비스. 공공 문서를 서비스 데이터로"),
    ("4주차", "미래에셋 AI 페스티벌", "금융 문서 RAG를 파싱부터 검증까지 직접 구현"),
    ("5~8주차", "빅콘테스트", "통신 · 카드 데이터로 사회적 고립 위험 지역을 찾는 AI 에이전트"),
], gap=14), sub="배운 개념을 매주 실제 데이터에 바로 적용했다")

# ================= 방법 (2~3분) =================
page("방법 · DE", "배운 개념이 바로 공모전에 쓰였다", table(
    ["배운 개념", "어디에 썼나"],
    [["정규화 · 공통 스키마", "비자 4종이 함께 쓰는 요건 · 절차 · 쿼터 테이블"],
     ["원본 보존", "PDF 변환본 대신 HWPX 원문을 직접 파싱"],
     ["멱등성 · 증분 적재", "반복 실행해도 중복 없는 적재, 실패하면 전체 롤백"],
     ["데이터 품질", "빅콘 제공 데이터 20개 파일 전수 검증"]], ["32%", "68%"]))

page("방법 · 비자부기", "공고 24건을 하나의 스키마로", f'''
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt;">
  {stat("24", "건", "구조화한 공식 공고 · 지침 · 서식", 36)}
  {stat("13", "개", "공통 스키마 테이블", 36)}
  {stat("1,101", "", "비자 4종 통합 레코드", 36)}
  {stat("407", "개", "자동 검증 테스트, CI 연결", 36)}
</div>
<div style="display:grid; grid-template-columns:1fr 1fr; gap:24pt; margin-top:20pt;">
  <p class="small"><b>PDF를 버리고 HWPX로</b>&nbsp; PDF로 바꾸면 강조된 숫자가 사라져서, ZIP 안의 XML을 직접 읽고 표 구조까지 보존했다</p>
  <p class="small"><b>이번 주 뼈저리게 깨달은 점</b>&nbsp; 비자별로 따로 만든 데이터는 결국 하나의 공통 스키마로 다시 합쳐야 했다</p>
</div>''')

page("방법 · 빅콘 데이터", "명세서를 믿지 않고 원본 20개를 다 열었다", f'''
<div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20pt;">
  {stat("2", "배", "12월 파일이 통째로 중복 배포. 모르고 쓰면 12월 수치 2배", 40)}
  {stat("5", "건 미만", "카드 결제 셀 삭제. 고령층 · 춘천처럼 희소한 집단이 사라진다", 40)}
  {stat("53.9", "배", "강남 유동인구가 거주인구의 최대 53.9배. 주민 신호가 묻힌다", 40)}
</div>
<p style="font-size:14pt; margin-top:22pt;">데이터가 우리가 찾으려는 사람들을 <b>먼저 지울 수 있다.</b></p>''',
     sub="SK텔레콤 유동인구 × 신한카드 결제, 강남구와 춘천시 2025년 7~12월")

page("방법 · 분석 단위", "동 평균은 동네 안의 차이를 가린다", f'''
<div style="display:grid; grid-template-columns:1fr 1.15fr; gap:24pt; align-items:center;">
  <img src="./assets/map_yeoksam.png" alt="역삼2동 집계구별 1인가구 비율 지도" style="width:100%; height:236pt;">
  <div><p class="label red">역삼2동 1인가구 비율</p>
  <p class="num" style="font-size:48pt;">36.5<span style="font-size:20pt;">%</span></p>
  <p class="cap">동 평균</p>
  {bullets(["주택가 덩어리 <b>66%</b> vs 아파트 단지 <b>8%</b>",
            "그래서 통계청이 공표하는 가장 작은 단위, <b>집계구 1,698곳</b>으로 본다"])}</div>
</div>''')

page("방법 · 구조", "두 개의 신호를 교차한다", cols([
    ("STEP 1 · 어디가 위험한가", "고립 위험 지수", "SGIS 6개 지표, 고령 독거 · 중장년 주거취약 두 테마"),
    ("STEP 2 · 누가 줄었나", "활동 저하 신호", "기대 유동 회귀의 잔차가 6개월 중 4개월 이상 -0.1 미만"),
    ("DICTIONARY", "위험 특징 사전", "실태조사 근거로 대화에서 확인할 24개 특징"),
    ("RESOURCE", "기관 태그", "복지 · 공공기관 17,925곳을 서비스 태그 16종으로"),
], gap=14) + '''
<div style="margin-top:20pt; background:#1F3A6E; padding:11pt 16pt;">
<p style="color:#FFFFFF; font-size:14pt; font-weight:700;">지역 유형으로 관찰하고, 대화로 판단하고, 기관으로 연결하는 AI 에이전트</p></div>''')

# ================= 결과 (2~3분) =================
page("결과 · 비자부기", "실제로 돌아가는 화면", f'''
<div style="display:grid; grid-template-columns:1.9fr 1fr; gap:20pt; align-items:start;">
  <div><img src="./assets/visa_home.png" alt="비자부기 홈 화면" style="width:100%; height:216pt; border:1pt solid #BBBBBB;">
  <p class="cap" style="margin-top:6pt;">홈: 준비 현황과 현재 단계를 한눈에</p></div>
  <div><img src="./assets/visa_ocr.png" alt="비자부기 OCR 서류 점검 화면" style="width:100%; height:216pt; border:1pt solid #BBBBBB;">
  <p class="cap" style="margin-top:6pt;">서류: 신청서를 찍으면 누락 항목 점검</p></div>
</div>
<p class="cap" style="margin-top:8pt;">시연 영상은 별도 파일로 제출</p>''')

page("결과 · 빅콘 지표", "만든 지표가 현실과 맞았다", f'''
<div style="display:grid; grid-template-columns:repeat(4,1fr); gap:16pt;">
  {stat("477", "곳", "지수 관찰 후보 집계구", 36)}
  {stat("461", "곳", "60대 이상 활동 저하 신호", 36)}
  {stat("+0.639", "", "지수 vs 서울시 관심집단 비율 (ρ)", 36)}
  {stat("-0.601", "", "신호율 vs 고령 1인가구 이동 횟수 (ρ)", 36)}
</div>
<p style="font-size:14pt; margin-top:22pt;">신호가 많은 동일수록 고령 1인가구가 <b>집에 오래 머물고 덜 움직였다.</b></p>
<p class="cap" style="margin-top:6pt;">강남 22개 동 외부 대조. 20~30대는 같은 방식이 맞지 않아 신호로 쓰지 않았다</p>''')

page("결과 · 빅콘 지도", "두 신호를 교차해 다섯 유형으로", f'''
<div style="display:grid; grid-template-columns:1.3fr 1fr; gap:22pt; align-items:center;">
  <img src="./assets/map_type.png" alt="지역 유형 분류 지도" style="width:100%; height:240pt;">
  <div>{table(["유형", "강남", "춘천", "합계"],
              [["<b class='red'>집중관찰</b>", "133", "24", "<b>157</b>"],
               ["잠재위험", "151", "120", "271"],
               ["활동저하", "157", "133", "290"],
               ["일반", "421", "232", "653"],
               ["확인필요", "236", "91", "327"]], ["40%", "20%", "20%", "20%"])}
  <p class="cap" style="margin-top:8pt;">집중관찰 = 지수 후보이면서 활동 신호도 나타난 곳</p></div>
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
page("결과 · 에이전트", "29세, 역삼1동, 1인가구",
     f'<div style="display:grid; grid-template-columns:repeat(5,1fr); gap:12pt;">{fl}</div>'
     '<p class="cap" style="margin-top:20pt;">합성 페르소나 예시. 위기 신호는 티어 계산 없이 109와 지정 담당자에게 바로 연결</p>',
     sub="한 사람의 사이클로 본 에이전트")

# ================= 마무리 (1분) =================
page("마무리 · 결과", "3전 3패, 그래도 남은 것", cols([
    ("ICT융합 공모전 · 탈락", "공고를 구조화하는 법", "공공 문서를 차수별 요건과 적용기간까지 데이터로 만든 경험"),
    ("미래에셋 AI 페스티벌 · 예선 탈락", "RAG는 검색과 검증", "품질은 생성 모델이 아니라 근거 검색과 답변 검증에서 갈렸다"),
    ("빅콘테스트 · 예선 탈락", "원본을 의심하는 습관", "명세서 대신 원본을 열고, 팀원 결과도 직접 재현했다"),
], gap=20))

page("마무리 · 한계와 계획", "아쉬운 점과 다음 단계", two(
    '<p class="label">LIMITS</p>'
    + bullets(["비자부기: 기능 구현에 집중해 사용자 효과를 실측하지 못했다",
               "빅콘: 에이전트는 설계와 합성 시나리오까지, 실제 구동은 못 했다",
               "빅콘: 20~30대 신호 실패, 강남은 유입 인구에 주민 신호가 묻힌다"], pad=7),
    '<p class="label red">NEXT</p>'
    + bullets(["비자부기를 팀 실험 프로젝트로 계속 디벨롭",
               "사용자 로그를 쌓아 이탈 분석",
               "운영 DB와 분석 DB를 나누는 구조로 확장"], pad=7)))

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
for f in OUT.glob("slide-*.html"):
    f.unlink()
for n, html in enumerate(S, start=1):
    html = html.replace("{TOTAL}", str(TOTAL))
    html = html.replace("</body>", f'<div class="prog" style="width:{n / TOTAL * 100:.0f}%;"></div></body>', 1)
    assert not re.search("[—–−―→]", html), f"slide {n}: 금지 문자"
    (OUT / f"slide-{n:02d}.html").write_text(html, encoding="utf-8")
print("ok", TOTAL)
