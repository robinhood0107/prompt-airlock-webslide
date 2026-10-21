# 중간 발표 애니메이션(manim). 렌더: manim -qm --format=mp4 scenes.py PipelineSample FailClosed
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
