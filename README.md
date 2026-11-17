# hambugi-deck

Team Hambugi 발표 덱 모음입니다. 슬라이드를 HTML로 만들고 PDF로 내보냅니다.

## 덱 목록

| 덱 | 내용 | 바로 보기 |
|---|---|---|
| `decks/tobigs-showcase/` | 투빅스 26기 심화세션 발표회 (51장) | [PDF](decks/tobigs-showcase/tobigs-showcase.pdf) |

## 보는 방법

### 1. PDF로 보기 (설치 필요 없음)

위 표의 PDF 링크를 누르면 GitHub에서 바로 볼 수 있습니다. 내려받으려면 PDF 화면 오른쪽 위의 다운로드 버튼을 누르세요.

### 2. 브라우저에서 슬라이드로 보기

레포를 받은 뒤 `viewer.html`을 브라우저로 엽니다. 인터넷 연결이 필요합니다(폰트를 웹에서 불러옵니다).

```bash
git clone https://github.com/Team-Hambugi-Lab/hambugi-deck.git
cd hambugi-deck
open decks/tobigs-showcase/viewer.html      # Windows는 파일을 더블클릭
```

## 고치는 방법

슬라이드 내용은 `decks/tobigs-showcase/build_slides.py` 한 파일에 들어 있습니다. `slide-*.html`은 이 스크립트가 만들어내는 결과물이라 직접 고치면 다음 생성 때 덮어써집니다.

### 준비

- Python 3.10 이상
- [slides-grab](https://www.npmjs.com/package/slides-grab): `npm install -g slides-grab`

### 순서

```bash
# 1. build_slides.py에서 문구를 고친다

# 2. 슬라이드 HTML 다시 생성
python3 decks/tobigs-showcase/build_slides.py decks/tobigs-showcase

# 3. 레이아웃 검증 (글자 잘림, 화면 밖으로 넘침 확인)
slides-grab validate --slides-dir decks/tobigs-showcase

# 4. 미리보기와 PDF 갱신
slides-grab build-viewer --slides-dir decks/tobigs-showcase
slides-grab pdf --slides-dir decks/tobigs-showcase --output decks/tobigs-showcase/tobigs-showcase.pdf
```

고친 뒤에는 `build_slides.py`, `slide-*.html`, `viewer.html`, PDF를 함께 커밋합니다.

### PPTX로 내보내기

```bash
slides-grab convert --slides-dir decks/tobigs-showcase --output tobigs-showcase.pptx
```

slides-grab의 PPTX 변환은 실험 기능이라 레이아웃이 깨질 수 있습니다. 최종본은 PDF를 기준으로 합니다. `*.pptx`는 `.gitignore`에 들어 있어 커밋되지 않습니다.

## 폴더 구조

```
decks/<deck-name>/
├── build_slides.py     # 슬라이드 내용과 디자인 (여기를 고친다)
├── slide-outline.md    # 슬라이드 구성 개요
├── slide-01.html ...   # 생성된 슬라이드
├── viewer.html         # 브라우저 미리보기
├── <deck-name>.pdf     # 내보낸 PDF
└── assets/             # 지도, 그래프, 화면 캡처, 사진
```

## 작성 규칙

- 흰 배경, 포인트 컬러는 남색(`#1F3A6E`), 폰트는 Pretendard
- 글씨 크기는 정수 pt만 사용
- 긴 하이픈과 화살표 문자는 쓰지 않습니다. 넣으면 `build_slides.py`가 생성을 멈춥니다.
- Public 레포입니다. 원본 데이터와 개인정보는 올리지 않습니다.
