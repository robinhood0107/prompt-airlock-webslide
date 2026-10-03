# Prompt Airlock · 프로젝트 진행보고

월별 개발 진행상황과 발표 슬라이드를 공개하는 정적 웹사이트입니다. 실제 Prompt Airlock 프로그램 소스 저장소와 분리해 관리합니다.

- 진행보고 아카이브: https://robinhood0107.github.io/prompt-airlock-webslide/
- 10월 제출용 슬라이드: https://robinhood0107.github.io/prompt-airlock-webslide/2026-10/

## 파일 구성

```text
index.html
assets/airlock.svg
2026-10/
  index.html
  style.css
  script.js
```

프레임워크, 별도 빌드, 외부 폰트, CDN, JavaScript 라이브러리가 필요하지 않습니다. 정적 서버로 저장소를 열어 미리 확인할 수 있습니다.

## 슬라이드 조작

좌우 화살표 키, Space, 화면의 이동 버튼, 마우스 휠 또는 가로 스와이프를 사용합니다. 첫 슬라이드와 마지막 슬라이드에서는 더 이상 이동하지 않습니다. 운영체제의 애니메이션 줄이기 설정을 따릅니다.

## 다음 월 자료 추가

`2026-11/`처럼 월별 디렉터리를 만들고 정적 슬라이드 파일을 넣습니다. 루트 `index.html`의 목록에 해당 디렉터리로 이동하는 상대경로 링크를 추가합니다. 공개 자료에는 개인정보를 포함하지 않습니다.

## GitHub Pages 설정

Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save.

10월 자료에는 9월 조사 및 설계 결과와 앞으로의 구현·평가 계획을 담았습니다. 11월 말 개발 완료는 목표 일정입니다.
