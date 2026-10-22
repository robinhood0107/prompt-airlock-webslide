# 중간 발표 애니메이션(manim). 렌더(720p):
#   manim -qm --format=mp4 scenes.py CompareFlow PipelineSample SafetyChecks DemoReplay
# 각 장면은 슬라이드 문장과 같은 말을 쓴다(7번 다른 점, 9번 가명 과정, 10번 실수와 고장, 12번 시연).
import json
from pathlib import Path

from manim import *

FONT = "Malgun Gothic"
ACCENT = "#2456a6"
LINE = "#d7dce2"
INK = "#171717"
MUTED = "#60666f"
RED = "#b3261e"
config.background_color = WHITE


def label(text, size=22, color=INK):
    return Text(text, font=FONT, font_size=size, color=color)


def box(text, w=2.2, size=20, color=INK):
    t = label(text, size, color)
    r = RoundedRectangle(width=max(w, t.width + 0.4), height=0.75, corner_radius=0.06, color=LINE, stroke_width=2)
    return VGroup(r, t)


def row(names, w, buff):
    return VGroup(*[box(n, w=w, size=18) for n in names]).arrange(RIGHT, buff=buff)


def arrows(group):
    return VGroup(*[Arrow(group[i].get_right(), group[i + 1].get_left(), buff=0.04, stroke_width=2,
                          max_tip_length_to_length_ratio=0.25, color=MUTED) for i in range(len(group) - 1)])


class CompareFlow(Scene):
    """7번 장: 기존 도구와 다른 점 다섯 가지."""

    def construct(self):
        self.add(label("기존 도구와 다른 점", 32).to_edge(UP, buff=0.4))
        top = row(["기관 앱", "중간 서버", "Presidio 가리기", "외부 LLM", "가명 되돌림"], 1.9, 0.35).scale(0.85).shift(UP * 1.4)
        bot = row(["기관 앱", "기밀 확인", "개인정보 찾기", "가명 바꾸기", "남은 정보 확인", "외부 LLM", "답 검사", "되돌리기"],
                  1.3, 0.22).scale(0.78).shift(DOWN * 0.3)
        t1 = label("LiteLLM + Presidio", 20, MUTED).next_to(top, UP, buff=0.15).align_to(top, LEFT)
        t2 = label("Prompt Airlock", 20, ACCENT).next_to(bot, UP, buff=0.15).align_to(bot, LEFT)
        self.play(FadeIn(t1), LaggedStart(*[FadeIn(b) for b in top], lag_ratio=0.15), Create(arrows(top)), run_time=2)
        self.play(FadeIn(t2), LaggedStart(*[FadeIn(b) for b in bot], lag_ratio=0.1), Create(arrows(bot)), run_time=2.5)
        points = [
            (2, "한국 개인정보 형식이 처음부터 들어 있습니다"),
            (3, "가명 짝은 따로 떨어진 보관 프로그램(Vault)에 둡니다"),
            (4, "검사 도구가 고장 나면 보내지 않습니다"),
            (6, "받은 답을 다시 검사한 뒤 되돌립니다"),
            (1, "기밀 문서는 밖으로 보내지 않습니다"),
        ]
        caption = None
        for index, text in points:
            new = label(text, 24, ACCENT).to_edge(DOWN, buff=0.9)
            if caption is not None:
                self.play(FadeOut(caption), run_time=0.3)
            self.play(bot[index][0].animate.set_stroke(ACCENT, width=4), FadeIn(new), run_time=0.6)
            caption = new
            self.wait(1.6)
        self.wait(1)


class PipelineSample(Scene):
    """9번 장: 가명이 오가는 과정."""

    def construct(self):
        self.add(label("가명이 오가는 과정", 32).to_edge(UP, buff=0.4))
        q = label("김민준 주무관에게 010-2345-6789 로 알려 주세요", 24).shift(UP * 2)
        self.play(Write(q), run_time=1.5)
        vault = box("Vault (기관 안)", w=3.4, size=20).shift(RIGHT * 4.2 + DOWN * 0.2)
        pairs = VGroup(label("⟦PERSON_PYZH…⟧ = 김민준", 16, MUTED),
                       label("⟦KOREAN_PHONE_N84Q…⟧ = 010-2345-6789", 16, MUTED)).arrange(DOWN, aligned_edge=LEFT)
        pairs.next_to(vault, DOWN, buff=0.2)
        sent = label("⟦PERSON_PYZHWD8MSY⟧ 주무관에게 ⟦KOREAN_PHONE_N84Q9DY2F5⟧ 로 …", 20, ACCENT).shift(UP * 0.6 + LEFT * 1.2)
        s_note = label("외부 LLM 으로 나가는 질문: 가명만 들어 있음", 18, MUTED).next_to(sent, UP, buff=0.15)
        self.play(FadeIn(vault), run_time=0.6)
        self.play(TransformFromCopy(q, sent), FadeIn(s_note), FadeIn(pairs), run_time=1.6)
        self.wait(1.5)
        back = label("답: 김민준 주무관에게 010-2345-6789 로 …", 22).shift(DOWN * 1.6 + LEFT * 1.2)
        b_note = label("답이 오면 이번 질문의 가명만 원래 값으로", 18, MUTED).next_to(back, UP, buff=0.15)
        self.play(TransformFromCopy(sent, back), FadeIn(b_note), run_time=1.6)
        self.wait(1.2)
        gone = label("질문이 끝나면 짝을 지웁니다", 20, RED).next_to(vault, DOWN, buff=0.25)
        self.play(FadeOut(pairs), FadeIn(gone), run_time=0.8)
        self.wait(1)
        warn1 = label("가명이 한 글자라도 바뀌어 오면 되돌리지 않습니다", 22, RED).to_edge(DOWN, buff=0.9)
        self.play(FadeIn(warn1))
        self.wait(1.8)
        warn2 = label("답의 링크 안에 가명이 있으면 답 전체를 막습니다", 22, RED).to_edge(DOWN, buff=0.9)
        self.play(FadeOut(warn1), run_time=0.3)
        self.play(FadeIn(warn2))
        self.wait(2)


class SafetyChecks(Scene):
    """10번 장: 실수와 고장에도 새지 않게."""

    def construct(self):
        title = label("실수와 고장에도 새지 않게", 32).to_edge(UP, buff=0.4)
        self.add(title)
        steps = row(["원본 질문", "기밀 확인 끝", "가명 처리 끝", "검사 통과"], 2.4, 0.55).scale(0.9).shift(UP * 1.1)
        self.play(LaggedStart(*[FadeIn(s) for s in steps], lag_ratio=0.3), Create(arrows(steps)), run_time=2)
        out = box("외부 LLM 으로 보내기", w=3.2, size=20, color=ACCENT).shift(DOWN * 1.2 + RIGHT * 3.3)
        ok = Arrow(steps[3].get_bottom(), out.get_top(), color=ACCENT, buff=0.08)
        self.play(FadeIn(out), GrowArrow(ok), run_time=1)
        c1 = label("검사를 모두 거친 질문만 보낼 수 있습니다", 22, ACCENT).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(c1))
        self.wait(1.5)
        skip = DashedLine(steps[0].get_bottom(), out.get_left(), color=RED)
        c2 = label("검사를 빼먹은 코드는 프로그램이 아예 만들어지지 않습니다", 22, RED).to_edge(DOWN, buff=0.8)
        self.play(FadeOut(c1), run_time=0.3)
        self.play(Create(skip), FadeIn(c2), run_time=1)
        self.play(Create(Cross(skip, stroke_color=RED, stroke_width=5, scale_factor=0.2)))
        self.wait(1.8)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not title])
        cases = VGroup(box("개인정보 찾는 모델이 멈춤", w=4.6, size=20), box("가명 보관 프로그램이 멈춤", w=4.6, size=20),
                       box("가명으로 바꾼 뒤에도 개인정보가 남음", w=4.6, size=20)).arrange(DOWN, buff=0.35).shift(LEFT * 2.2)
        self.play(LaggedStart(*[FadeIn(c) for c in cases], lag_ratio=0.4), run_time=1.6)
        stop = VGroup(*[label("거절", 22, RED).next_to(c, RIGHT, buff=0.6) for c in cases])
        self.play(LaggedStart(*[FadeIn(s) for s in stop], lag_ratio=0.3))
        zero = label("세 경우 모두 외부 LLM 으로 한 번도 보내지 않습니다", 22, ACCENT).to_edge(DOWN, buff=0.8)
        self.play(FadeIn(zero))
        self.wait(2.5)


class DemoReplay(Scene):
    """12번 장: 실제 실행 기록(demo-run.json, 게이트웨이 127.0.0.1:18443, 시험용 provider 19443)을 재생한다."""

    def construct(self):
        run = json.loads((Path(__file__).parent / "demo-run.json").read_text(encoding="utf-8"))
        self.add(label("실제 실행 기록 재생", 20, MUTED).to_edge(UP, buff=0.25))
        self.add(label("보낸 질문과 받은 결과", 18, ACCENT).move_to([-3.4, 2.9, 0]),
                 label("외부 LLM 쪽이 실제로 받은 내용", 18, ACCENT).move_to([3.4, 2.9, 0]),
                 Line([0, 2.7, 0], [0, -3.5, 0], color=LINE))
        for i, s in enumerate(run["scenes"], 1):
            title = label(f"{i}. {s['name']}", 28).move_to([-3.4, 2.1, 0])
            q = Paragraph(*wrap(s["text"], 24), font=FONT, font_size=18, color=INK, line_spacing=0.8).move_to([-3.4, 0.9, 0])
            if s["status"] == 200:
                result, color = "통과 · 답: " + s["response"]["choices"][0]["message"]["content"], ACCENT
            else:
                err = s["response"]["error"]
                kinds = ", ".join(err.get("blocked_types", []))
                result, color = f"거절({s['status']}) · {err['code']}" + (f" · {kinds}" if kinds else ""), RED
            r = Paragraph(*wrap(result, 24), font=FONT, font_size=18, color=color, line_spacing=0.8).move_to([-3.4, -1.4, 0])
            sent = wrap(s["egress"][0], 26) if s["egress"] else ["(보낸 것 없음)"]
            e = Paragraph(*sent, font=FONT, font_size=17, color=ACCENT if s["egress"] else MUTED,
                          line_spacing=0.8).move_to([3.4, 0.4, 0])
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
