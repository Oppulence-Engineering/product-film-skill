# Final render, verification and delivery

Select the render profile using [the Remotion quality extension](remotion-quality.md). The original supersampled pipeline below remains available. For a linear Remotion tutorial, use the direct profile in this file; the Screen Studio reference applies to exports made in that app. Neither technical profile replaces visual review.

This pipeline is for Remotion films that use the master/loop contract below. For Screen Studio exports and linear demos, use [screen-studio.md](screen-studio.md#export-and-inspect-the-actual-file); do not apply fixed background or seamless-loop assertions to ordinary footage.

## Pipeline (`scripts/render.ts`)

1. **Master.** 240 fps, PNG frames, H.264 at CRF 8, `yuv444p`, muted: `--props '{"fps":240}' --image-format png --pixel-format yuv444p --crf 8 --muted`.
2. **Audio.** Once, at 60 fps: `--codec wav`.
3. **Motion blur.** ffmpeg `tmix=frames=4` averages each group of 4 subframes, and `select='not(mod(n+1\,4))'` keeps one, giving 60 fps. Convert color once: `scale=in_range=tv:out_range=tv:in_color_matrix=bt601:out_color_matrix=bt709`, then ProRes 4444 as the intermediate.
4. **Deliverables.**
   - a muted H.264 loop for the landing page (CRF 20, `yuv420p`, BT.709 tags, `+faststart`)
   - the same with music (AAC 256k)
   - a VP9 WebM
   - `poster.jpg` from the headline (not frame 0, which is empty)
   - a loop-seam sheet (the last 8 and first 8 frames, played twice)
5. Delete the master and the intermediate. Print the file sizes.

A full-frame render at 240 fps takes about 10 minutes for 50 s on a laptop. Run it in the background and review other things meanwhile.

## Verify before sending (`scripts/verify.py`)

```bash
uv run --with numpy --with imageio-ffmpeg python3 scripts/verify.py out/<film> --duration 52.8 --bg 10,10,10 --probe 9.4:944,800
```

It checks, for every deliverable:
- the duration
- decoded frame 0 at the center: expect the background ±2 (#0a0a0a comes back as 9 or 10)
- the last frame against frame 0: only encoder noise (a few hundred pixels off by a few values)
- optional probes (time:x,y) to check an accent color or a surface

If the background comes back lighter (#171717 for #0a0a0a), the color range was read wrong. Fix the `scale` filter above; never "fix" the tokens.

## Deliver

- Keep each version: `cp` the deliverables into `out/<film>/vN/` before the next render.
- Send the files (with music for review, the muted loop for the page, WebM, poster) with a two-line caption of what changed.
- Report: durations, sizes, the checks you ran.
- Do not commit or publish unless asked.

## Direct UI render profile

For a linear UI walkthrough, start with the intended delivery fps (usually 30 or 60), full delivery dimensions, and no whole-frame temporal blur. Reuse the workspace's pinned Remotion version and render wrapper when it supports these settings. Verify flags against that installed version rather than upgrading the app to match a web example.

This example uses the kit's `fps` input prop. It requires `calculateMetadata` to resolve both fps and `durationInFrames = round(durationSeconds * fps)`. Substitute the actual entry, composition, complete input props, and a new versioned output directory. A bare CLI fps override without retiming the composition can change duration and cut timing. For fixed-fps compositions, retain their resolved metadata instead of passing an ignored prop.

```bash
npx --no-install remotion render src/index.ts MyFilm out/my-film/v2/demo.mp4 \
  --props '{"fps":30}' --codec h264 --image-format png \
  --crf 18 --pixel-format yuv420p --color-space bt709 \
  --x264-preset slow --hardware-acceleration disable
```

CRF 18 is a starting point, not a quality verdict. Check file size and thin text in the encoded file, then tune to the destination. Use `--muted` only for a silent deliverable. A separate half-size render can check pacing; it cannot approve final text sharpness. `--frames` can render a short proof sequence at the selected fps. See the official [CLI options](https://www.remotion.dev/docs/cli/render). Honor local command wrappers such as RTK.

This direct export explicitly selects BT.709. Do not apply the older pipeline's assumed BT.601-to-BT.709 conversion again. Probe actual color metadata and decoded brand pixels. If motion blur is useful, compare the same moving label with and without it and keep reading holds sharp; newer Remotion motion-blur APIs need a version/renderer compatibility check.

For either profile, probe the finished video/audio streams and fully decode with ffmpeg. Compare duration to the resolved composition, not a requested number the renderer may have ignored. Inspect opening, action, result, and ending at target display size, then play the complete file. Use `scripts/verify.py` only when its background-at-center and seamless-loop assumptions apply, passing the real `--fps` and `--size`. It is not a general linear-film quality gate. Record any playback or audio review that could not be completed.

Preserve source captures, input props, editable compositions, and previous exports. Keep each new render in its own version directory. Generate only requested formats and choose a poster with a readable product result; a loop or blank opening is not mandatory for a linear film.
