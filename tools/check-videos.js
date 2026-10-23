// gstack-browse-safe로 페이지를 연 뒤 eval tools/check-videos.js로 실행한다.
// 결과는 js 'JSON.stringify(window.__videoCheck)'로 확인한다.
(() => {
  const results = [];
  const check = (condition, message) => {
    if (!condition) throw new Error(message);
  };
  window.__videoCheck = { status: 'running' };
  const run = async () => {
    const videos = [...document.querySelectorAll('video.clip')];
    check(videos.length > 0, '검사할 영상이 없습니다.');
    while (!document.querySelector('#previous').disabled) document.querySelector('#previous').click();
    for (const video of videos) {
      while (video.closest('.slide').hidden && !document.querySelector('#next').disabled) document.querySelector('#next').click();
      check(!video.closest('.slide').hidden, '영상 슬라이드로 이동하지 못했습니다.');
      const { width, height } = video.getBoundingClientRect();
      check(getComputedStyle(video).display !== 'none' && width > 0 && height > 0, `${video.currentSrc}: 영상이 숨겨졌습니다.`);
      check(video.controls, `${video.currentSrc}: 재생 버튼이 없습니다.`);
      check([...video.parentElement.querySelectorAll('a')].some(link => link.href === (video.currentSrc || video.querySelector('source').src)), `${video.currentSrc}: 직접 여는 링크가 없습니다.`);
      const counter = document.querySelector('#slide-counter').textContent;
      video.focus();
      for (const key of [' ', 'ArrowLeft', 'ArrowRight']) {
        const event = new KeyboardEvent('keydown', { key, bubbles: true, cancelable: true });
        video.dispatchEvent(event);
        check(!event.defaultPrevented && document.querySelector('#slide-counter').textContent === counter, `${video.currentSrc}: 영상 조작 키가 슬라이드를 넘깁니다.`);
      }
      let timeout;
      try {
        await Promise.race([
          (async () => {
            await video.play();
            await new Promise(resolve => setTimeout(resolve, 350));
            check(!video.error && video.readyState >= 2 && video.currentTime > 0 && video.videoWidth > 0, `${video.currentSrc}: 영상을 재생하지 못했습니다.`);
          })(),
          new Promise((_, reject) => { timeout = setTimeout(() => reject(new Error(`${video.currentSrc}: 재생 시간 초과`)), 10000); }),
        ]);
      } finally {
        clearTimeout(timeout);
        video.pause();
        video.currentTime = 0;
      }
      results.push({ src: video.currentSrc, width: video.videoWidth, height: video.videoHeight, duration: video.duration });
    }
    return { status: 'passed', reducedMotion: matchMedia('(prefers-reduced-motion: reduce)').matches, results };
  };
  run().then(result => { window.__videoCheck = result; }, error => {
    window.__videoCheck = { status: 'failed', error: error.message, results };
  });
  return '영상 검사 시작';
})();
