# 중간 발표 애니메이션(manim). 렌더: manim -qh --format=mp4 scenes.py PipelineSample FailClosed CompareFlow Typestate DemoReplay
from manim import *

FONT = "Malgun Gothic"
ACCENT = "#2456a6"
LINE = "#d7dce2"
INK = "#171717"
RED = "#b3261e"
config.background_color = WHITE


def box(text, color=INK, w=3.2):
    t = Text(text, font=FONT, font_size=24, color=color)
    r = RoundedRectangle(width=max(w, t.width + 0.5), height=0.9, corner_radius=0.08, color=LINE, stroke_width=2)
    return VGroup(r, t)


class PipelineSample(Scene):
    """시연 장면 3: 원문 → token 으로 나가고 → 답에서 복원."""

    def construct(self):
        title = Text("가명으로 나가고, 원래 값으로 돌아온다", font=FONT, font_size=34, color=INK).to_edge(UP)
        self.play(FadeIn(title))
        q = Text("김민준 주무관에게 010-2345-6789 로 알려 주세요", font=FONT, font_size=26, color=INK).shift(UP * 1.6)
        self.play(Write(q))
        steps = VGroup(box("탐지"), box("Vault 가명"), box("잔여 검사")).arrange(RIGHT, buff=0.6).shift(UP * 0.1)
        self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.3))
        sent = Text("⟦PERSON_PYZHWD8MSY⟧ 주무관에게 ⟦KOREAN_PHONE_N84Q9DY2F5⟧ 로 ...", font=FONT, font_size=22,
                    color=ACCENT).shift(DOWN * 1.3)
        label = Text("provider 로 나간 내용", font=FONT, font_size=18, color=GRAY).next_to(sent, UP, buff=0.15)
        self.play(TransformFromCopy(q, sent), FadeIn(label))
        self.wait(1)
        back = Text("답: 김민준 주무관에게 010-2345-6789 로 ...", font=FONT, font_size=24, color=INK).shift(DOWN * 2.6)
        self.play(TransformFromCopy(sent, back))
        note = Text("같은 요청 범위에서 정확히 같은 token 만 복원", font=FONT, font_size=18, color=GRAY).next_to(back, DOWN, buff=0.15)
        self.play(FadeIn(note))
        self.wait(2)


class FailClosed(Scene):
    """어느 단계든 실패하면 provider 호출 0."""

    def construct(self):
        title = Text("실패하면 막는다 (fail closed)", font=FONT, font_size=34, color=INK).to_edge(UP)
        self.play(FadeIn(title))
        names = ["등급", "탐지", "정책", "Vault", "잔여 검사", "provider"]
        chain = VGroup(*[box(n, w=1.7) for n in names]).arrange(RIGHT, buff=0.35).scale(0.9)
        self.play(LaggedStart(*[FadeIn(b) for b in chain], lag_ratio=0.15))
        dot = Dot(color=ACCENT, radius=0.12).next_to(chain[0], LEFT)
        self.play(FadeIn(dot))
        for i, why in [(1, "NER 장애"), (3, "Vault 장애"), (4, "원문이 남음")]:
            self.play(dot.animate.move_to(chain[i].get_center() + UP * 0.8), run_time=0.8)
            x = Cross(chain[i], stroke_color=RED, stroke_width=6)
            msg = Text(f"{why} → 거절, provider 호출 0", font=FONT, font_size=22, color=RED).shift(DOWN * 1.5)
            self.play(Create(x), FadeIn(msg))
            self.wait(0.8)
            self.play(FadeOut(x), FadeOut(msg), dot.animate.next_to(chain[0], LEFT), run_time=0.5)
        self.play(dot.animate.move_to(chain[5].get_center() + UP * 0.8), run_time=1.5)
        ok = Text("모두 통과한 VerifiedPrompt 만 provider 로", font=FONT, font_size=24, color=ACCENT).shift(DOWN * 1.5)
        self.play(FadeIn(ok))
        self.wait(2)


class CompareFlow(Scene):
    """LiteLLM + Presidio 가드레일 흐름과 Prompt Airlock 흐름 비교."""

    def construct(self):
        title = Text("같은 문제, 다른 위치의 통제", font=FONT, font_size=34, color=INK).to_edge(UP)
        self.play(FadeIn(title))
        top = VGroup(*[box(t, w=2.3) for t in ["앱", "프록시", "Presidio 마스킹", "LLM", "되돌림"]]).arrange(RIGHT, buff=0.3).scale(0.85).shift(UP * 1.2)
        bot = VGroup(*[box(t, w=1.6) for t in ["앱", "등급", "탐지", "Vault", "잔여 검사", "LLM", "응답 검사"]]).arrange(RIGHT, buff=0.22).scale(0.8).shift(DOWN * 1.2)
        l1 = Text("LiteLLM + Presidio 가드레일", font=FONT, font_size=20, color=GRAY).next_to(top, UP, buff=0.2)
        l2 = Text("Prompt Airlock", font=FONT, font_size=20, color=ACCENT).next_to(bot, UP, buff=0.2)
        self.play(FadeIn(l1), LaggedStart(*[FadeIn(b) for b in top], lag_ratio=0.15))
        self.play(FadeIn(l2), LaggedStart(*[FadeIn(b) for b in bot], lag_ratio=0.12))
        for i in (1, 2, 3, 4, 6):
            self.play(bot[i][0].animate.set_stroke(ACCENT, width=4), run_time=0.35)
        note = Text("단계마다 실패하면 거절 · 응답도 다시 검사", font=FONT, font_size=22, color=ACCENT).to_edge(DOWN)
        self.play(FadeIn(note))
        self.wait(2)


class Typestate(Scene):
    """타입 상태 전이: VerifiedPrompt 만 provider 로."""

    def construct(self):
        title = Text("타입이 순서를 강제한다", font=FONT, font_size=34, color=INK).to_edge(UP)
        self.play(FadeIn(title))
        names = ["RawPrompt", "PolicyChecked", "Protected", "VerifiedPrompt"]
        states = VGroup(*[box(n, w=2.6) for n in names]).arrange(RIGHT, buff=0.6).scale(0.85)
        arrows = VGroup(*[Arrow(states[i].get_right(), states[i + 1].get_left(), buff=0.05, color=INK) for i in range(3)])
        self.play(LaggedStart(*[FadeIn(s) for s in states], lag_ratio=0.25), Create(arrows))
        prov = box("provider 요청", color=ACCENT, w=3).shift(DOWN * 2)
        ok = Arrow(states[3].get_bottom(), prov.get_top(), color=ACCENT)
        self.play(FadeIn(prov), GrowArrow(ok))
        bad = DashedLine(states[0].get_bottom(), prov.get_left(), color=RED)
        x = Text("컴파일 실패", font=FONT, font_size=22, color=RED).next_to(bad, DOWN, buff=0.1).shift(LEFT)
        self.play(Create(bad), FadeIn(x))
        self.wait(2)


class DemoReplay(Scene):
    """실제 실행 기록(demo-run.json: 게이트웨이 127.0.0.1:18443, mock provider 19443)을 장면별로 재생한다."""

    def construct(self):
        import json
        from pathlib import Path

        run = json.loads((Path(__file__).parent / "demo-run.json").read_text(encoding="utf-8"))
        head = Text("실제 실행 기록 재생 · 게이트웨이 https://localhost:18443", font=FONT, font_size=20, color=GRAY).to_edge(UP, buff=0.25)
        self.add(head)
        left_t = Text("기관 앱이 보낸 질문 → 받은 결과", font=FONT, font_size=18, color=ACCENT).move_to([-3.4, 2.9, 0])
        right_t = Text("provider 로 실제 나간 내용", font=FONT, font_size=18, color=ACCENT).move_to([3.4, 2.9, 0])
        divider = Line([0, 2.7, 0], [0, -3.5, 0], color=LINE)
        self.add(left_t, right_t, divider)
        for i, s in enumerate(run["scenes"], 1):
            title = Text(f"{i}. {s['name']}", font=FONT, font_size=30, color=INK).move_to([-3.4, 2.1, 0])
            q = Paragraph(*wrap(s["text"], 24), font=FONT, font_size=18, color=INK, line_spacing=0.8).move_to([-3.4, 0.9, 0])
            if s["status"] == 200:
                result = "200 · 답: " + s["response"]["choices"][0]["message"]["content"]
                color = ACCENT
            else:
                err = s["response"]["error"]
                extra = " " + ",".join(err.get("blocked_types", [])) if err.get("blocked_types") else ""
                result = f"{s['status']} · {err['code']}{extra}"
                color = RED
            r = Paragraph(*wrap(result, 24), font=FONT, font_size=18, color=color, line_spacing=0.8).move_to([-3.4, -1.4, 0])
            sent = "\n".join(wrap(s["egress"][0], 26)) if s["egress"] else "(나간 내용 없음 · provider 호출 0)"
            e = Paragraph(*sent.split("\n"), font=FONT, font_size=17, color=ACCENT if s["egress"] else GRAY, line_spacing=0.8).move_to([3.4, 0.4, 0])
            self.play(FadeIn(title), Write(q), run_time=1.2)
            self.play(FadeIn(e, shift=RIGHT * 0.3), run_time=0.8)
            self.play(FadeIn(r, shift=UP * 0.2), run_time=0.8)
            self.wait(2.2)
            self.play(FadeOut(VGroup(title, q, r, e)), run_time=0.4)


def wrap(text, width):
    lines, cur = [], ""
    for word in text.split(" "):
        if len(cur) + len(word) + 1 > width and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    if cur:
        lines.append(cur)
    return lines
