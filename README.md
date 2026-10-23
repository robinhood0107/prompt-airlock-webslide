# Prompt Airlock · 프로젝트 진행보고

월별 진행상황과 발표 슬라이드를 공개하는 정적 웹사이트입니다. 실제 Prompt Airlock 프로그램 소스 저장소와 분리해 관리합니다.

## 자료 목록

| 자료 | 주소 | 파일 |
|---|---|---|
| 진행보고 목록 | https://robinhood0107.github.io/prompt-airlock-webslide/ | `index.html` |
| 10월 진행보고 | https://robinhood0107.github.io/prompt-airlock-webslide/2026-10/ | `2026-10/` |
| 중간 발표 슬라이드(11장) | https://robinhood0107.github.io/prompt-airlock-webslide/middle-presentation/ | `middle-presentation/index.html` |
| 중간 발표 대본(약 8분 30초) | https://robinhood0107.github.io/prompt-airlock-webslide/middle-presentation/script.md | `middle-presentation/script.md` |

## 파일 구성

```text
index.html                      진행보고 목록
assets/airlock.svg              아이콘
2026-10/                        10월 진행보고(index.html, style.css, script.js)
middle-presentation/
  index.html                    중간 발표 슬라이드 11장
  style.css, script.js          슬라이드 모양과 넘기기
  script.md                     발표 대본(장별 말할 내용, 시간, 예상 질문, 시연 준비)
  media/                        슬라이드에 넣은 영상(mp4, webm)과 첫 화면 이미지(png)
  animations/
    scenes.py                   manim 애니메이션 원본
    demo-run.json               시연 영상에 쓴 실제 실행 기록
    requirements.txt            manim 판
tools/check-assets.mjs          슬라이드가 참조하는 파일이 모두 커밋됐는지 확인
```

## 중간 발표 영상

| 슬라이드 | 영상 | 길이 | 내용 |
|---|---|---|---|
| 7 기존 도구와 다른 점 | `CompareFlow.mp4` | 17.5초 | 두 처리 흐름과 차이 5가지 |
| 9 가명이 오가는 과정 | `PipelineSample.mp4` | 15.6초 | 가명으로 보내고 되돌리기, Vault 보관과 삭제 |
| 10 실수와 고장에도 새지 않게 | `SafetyChecks.mp4` | 17초 | 검사를 건너뛸 수 없는 구조, 고장 시 거절 |
| 12 시연 | `DemoReplay.mp4` | 32.4초 | 게이트웨이를 실제로 실행해 보낸 질문 6개의 기록 |

모두 720p 입니다. H.264 MP4와 VP9 WebM을 함께 제공하며, 브라우저가 지원하는 형식을 선택합니다. 다시 만들 때는 `middle-presentation/animations` 에서 다음을 실행하고, 결과(`media/videos/scenes/720p30/*.mp4`)를 `middle-presentation/media/` 로 복사합니다.

```bash
manim -qm --format=mp4 scenes.py CompareFlow PipelineSample SafetyChecks DemoReplay
```

MP4를 다시 만들면 WebM도 다음과 같이 갱신합니다.

```bash
for name in CompareFlow PipelineSample SafetyChecks DemoReplay; do
  ffmpeg -i "middle-presentation/media/$name.mp4" -an -c:v libvpx-vp9 -crf 32 -b:v 0 -pix_fmt yuv420p -row-mt 1 "middle-presentation/media/$name.webm"
done
```

manim 은 저장소 밖 가상환경(`.venv`, 커밋하지 않음)에 `requirements.txt` 판으로 설치합니다.

## 커밋 전 확인

```bash
node tools/check-assets.mjs
```

- 슬라이드가 참조하는 영상·이미지·스크립트가 하나라도 커밋에서 빠지면 실패합니다.
- 제외 규칙은 루트에만 걸리게 씁니다(`/media/`). `media/` 로 쓰면 `middle-presentation/media/` 까지 빠집니다.
- merge 뒤에는 Pages 주소에서 영상이 실제로 열리는지 확인합니다.

## 영상 재생 확인

로컬 서버를 실행합니다.

```bash
python3 -m http.server 8765 --bind 127.0.0.1
```

`gstack-browse-safe`가 PATH에 등록된 WSL 환경에서 다음을 실행합니다. 일반 설정과 ‘동작 줄이기’ 설정 모두 검사하며, 각 검사 후 결과가 `passed`인지 확인합니다. `running`이면 끝날 때까지 결과 조회를 반복합니다. 검사에는 영상 4개의 표시·실제 재생, 직접 열기 링크, 영상 조작 키가 슬라이드를 넘기지 않는지 확인하는 과정이 포함됩니다.

```bash
B=gstack-browse-safe
"$B" goto http://127.0.0.1:8765/middle-presentation/
"$B" cdp Emulation.setEmulatedMedia '{"features":[{"name":"prefers-reduced-motion","value":"no-preference"}]}'
"$B" eval tools/check-videos.js
# 검사 완료 후 결과를 확인합니다.
"$B" js 'JSON.stringify(window.__videoCheck)'
"$B" cdp Emulation.setEmulatedMedia '{"features":[{"name":"prefers-reduced-motion","value":"reduce"}]}'
"$B" eval tools/check-videos.js
"$B" js 'JSON.stringify(window.__videoCheck)'
"$B" stop
"$B" check
```

배포 후에는 `goto` 주소를 공개 Pages 주소로 바꿔 같은 검사를 실행합니다. 파일 존재 검사만으로는 CSS에 가려진 영상이나 재생 실패를 확인할 수 없습니다.

## 슬라이드 조작

좌우 화살표 키, Space, 화면의 이동 버튼, 마우스 휠 또는 가로 스와이프를 사용합니다. 운영체제의 애니메이션 줄이기 설정과 관계없이 영상과 재생 버튼을 표시합니다. 영상에 포커스가 있으면 Space와 방향키를 슬라이드 이동에 사용하지 않습니다. 각 영상 아래의 “영상 직접 열기” 링크로 영상 파일을 별도 탭에서 열 수도 있습니다.

## 다음 자료 추가

월별 디렉터리(예: `2026-11/`)를 만들고 정적 슬라이드 파일을 넣은 뒤, 루트 `index.html` 목록에 상대경로 링크를 추가합니다. 공개 자료에는 개인정보를 넣지 않습니다.

## GitHub Pages 설정

Settings → Pages → Build and deployment → Deploy from a branch → `main` / `(root)` → Save.
