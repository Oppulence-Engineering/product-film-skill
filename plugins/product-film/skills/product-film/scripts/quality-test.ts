import {mkdirSync, readFileSync, writeFileSync} from 'node:fs';
import {join, relative, resolve} from 'node:path';
import {spawnSync} from 'node:child_process';
import {bundle} from '@remotion/bundler';
import {openBrowser, renderMedia, renderStill, selectComposition} from '@remotion/renderer';

/** Run from a video workspace after copying templates/quality, recipes and kit into src.
 * bun scripts/quality-test.ts out/new-version [--narration public/narration/narration.json]
 * Uses public/font.ttf. Does not overwrite outputs or change the workspace's dependencies.
 */
const args = process.argv.slice(2);
const directory = args.shift();
if (!directory || (args.length !== 0 && !(args.length === 2 && args[0] === '--narration'))) {
  throw new Error('Usage: bun scripts/quality-test.ts <new-output-dir> [--narration <manifest.json>]');
}
const root = resolve(import.meta.dirname, '..');
const out = resolve(directory);
const narration = args.length ? JSON.parse(readFileSync(resolve(args[1]), 'utf8')) : undefined;
mkdirSync(out, {recursive: false});
const runPython = (script: string, ...values: string[]) => {
  const result = spawnSync('uv', ['run', '--with', 'numpy', '--with', 'pillow', '--with', 'imageio-ffmpeg', 'python', join(root, 'scripts', script), ...values], {stdio: 'inherit'});
  if (result.error || result.status !== 0) throw result.error ?? new Error(`${script} exited ${result.status}`);
};
runPython('test-capabilities.py');
const serveUrl = await bundle({entryPoint: join(root, 'src/quality/index.tsx'), publicDir: join(root, 'public')});
const browser = await openBrowser('chrome');
const manifest: {renders: any[]; fpsPairs: string[][]; negativeCases: Record<string, string>} = {renders: [], fpsPairs: [], negativeCases: {}};
try {
  for (const [fault, expected] of [['small', 'SMALL_TEXT'], ['clip', 'CLIPPED'], ['overlap', 'CAPTION_OVERLAP'], ['font', 'FONT_LOAD']]) {
    const inputProps = {format: 'landscape', fps: 30, fault: fault === 'font' ? undefined : fault, fontFile: fault === 'font' ? 'deliberately-missing-font.ttf' : 'font.ttf'};
    const composition = await selectComposition({serveUrl, id: 'QualityProof', inputProps, puppeteerInstance: browser});
    let rejected = false;
    try {
      await renderStill({serveUrl, composition, inputProps, frame: 120, output: join(out, `broken-${fault}.png`), puppeteerInstance: browser, overwrite: false});
    } catch (error) {
      const message = String(error);
      if (!message.includes(expected)) throw error;
      manifest.negativeCases[fault] = message;
      rejected = true;
    }
    if (!rejected) throw new Error(`Broken ${fault} fixture unexpectedly passed`);
  }
  for (const [format, fps] of [['landscape', 30], ['square', 30], ['portrait', 30], ['landscape', 60]] as const) {
    const inputProps = {format, fps, fontFile: 'font.ttf', narration};
    const composition = await selectComposition({serveUrl, id: 'QualityProof', inputProps, puppeteerInstance: browser});
    const name = `${format}-${fps}`;
    const samples: {frame: number; still: string; decoded: string}[] = [];
    const segment = (narration?.durationMs ?? 32000) / 4000;
    let measured = 0;
    const onBrowserLog = (log: {text: string}) => {if (log.text.startsWith('FILM_QA:')) measured++;};
    for (let scene = 0; scene < 4; scene++) {
      for (const local of [0, 1.8, 2.2, segment - 0.1]) {
        const frame = Math.round((scene * segment + local) * 30) * (fps / 30);
        const still = `${name}-${frame}-source.png`;
        await renderStill({serveUrl, composition, inputProps, frame, output: join(out, still), puppeteerInstance: browser, overwrite: false, onBrowserLog});
        samples.push({frame, still, decoded: `${name}-${frame}-player.png`});
      }
    }
    if (measured < samples.length) throw new Error(`Missing DOM measurement evidence for ${name}`);
    console.log(`Rendering ${name} (${composition.durationInFrames} frames)`);
    await renderMedia({serveUrl, composition, inputProps, outputLocation: join(out, `${name}.mp4`), codec: 'h264',
      imageFormat: 'png', pixelFormat: 'yuv420p', colorSpace: 'bt709', crf: 18, x264Preset: 'medium',
      hardwareAcceleration: 'disable', concurrency: 4, overwrite: false, puppeteerInstance: browser, onBrowserLog});
    manifest.renders.push({file: `${name}.mp4`, width: composition.width, height: composition.height, fps,
      frames: composition.durationInFrames, playerWidth: format === 'portrait' ? 360 : format === 'square' ? 480 : 640,
      audio: Boolean(narration), audioReference: narration ? relative(out, join(root, 'public', narration.audio)) : undefined, measuredStills: measured, samples});
    writeFileSync(join(out, 'manifest.json'), JSON.stringify(manifest, null, 2));
  }
  const first = manifest.renders[0];
  const last = manifest.renders[3];
  manifest.fpsPairs = first.samples.map((s: any, index: number) => [s.decoded, last.samples[index].decoded]);
  writeFileSync(join(out, 'manifest.json'), JSON.stringify(manifest, null, 2));
} finally {
  await browser.close({silent: true});
}
runPython('check-media.py', join(out, 'manifest.json'));
const cards = manifest.renders.map(r => `<section><h2>${r.file}</h2><button type="button">Play ${r.file}</button><br><video controls preload="metadata" width="${r.playerWidth}" src="${r.file}"></video><p>Visual review: NOT_REVIEWED · Audio listening: NOT_REVIEWED</p><pre>Not played</pre></section>`).join('\n');
writeFileSync(join(out, 'review.html'), `<!doctype html><meta charset="utf-8"><title>Product film quality proof</title><style>body{font:16px system-ui;padding:24px;background:#eee}section{margin:24px 0}video{max-width:100%;background:#fff}pre{white-space:pre-wrap}button{margin:8px 0;padding:8px}</style><h1>Encoded proof: inspect all scenes at normal speed</h1><p>These are synthetic recipe demonstrations, not product recordings. Check controls shown/hidden, opening, action, result and ending. Technical PASS is not visual acceptance.</p>${cards}<script>
for (const section of document.querySelectorAll('section')) {
  const video = section.querySelector('video'), log = section.querySelector('pre');
  let events = [], baseline;
  section.querySelector('button').onclick = () => {
    baseline = video.getVideoPlaybackQuality(); events = [];
    video.currentTime = 0; video.playbackRate = 1;
    video.play().catch(error => {log.textContent = String(error);});
  };
  for (const name of ['playing', 'waiting', 'seeking', 'ended', 'error']) video.addEventListener(name, () => {
    const q = video.getVideoPlaybackQuality();
    events.push({event:name,time:video.currentTime,rate:video.playbackRate,frames:q.totalVideoFrames-(baseline?.totalVideoFrames||0),dropped:q.droppedVideoFrames-(baseline?.droppedVideoFrames||0),error:video.error?.message||null});
    log.textContent = JSON.stringify(events, null, 2);
  });
}
</script>`);
console.log(`Technical checks passed. Open ${join(out, 'review.html')} for complete playback review.`);
