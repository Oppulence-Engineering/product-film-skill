# Tested scenes, formats, narration, and capture readiness

Use this extension when building repeatable product walkthroughs or testing a skill change. It adds runnable helpers to the existing workflow. Keep the original render/loop helpers for their documented contract. No helper in this extension records a screen, publishes a video, or modifies an application.

## One-command render proof

In an isolated video workspace, use its existing, exactly matched `remotion`, `@remotion/bundler`, `@remotion/renderer` and React versions. Copy this skill's `scripts/` into `scripts/`, `templates/kit/` into `src/kit/`, `templates/recipes.tsx` into `src/recipes.tsx`, and `templates/quality/` into `src/quality/`. Put a licensed, locally available regular font at `public/font.ttf`. The synthetic fixture uses neutral test colors; real films must supply the product's own tokens and source-backed content.

Run from that workspace, using the host's required command wrapper if any:

```sh
bun scripts/quality-test.ts out/proof-v1
# Include the prepared voice track when testing narration:
bun scripts/quality-test.ts out/proof-voice-v1 --narration public/narration/narration.json
```

Create the parent `out/` directory first. The version directory must not exist. `uv` supplies the same numpy/imageio-ffmpeg dependencies used by the existing audio scripts, plus Pillow for decoded review images. This command does not install JavaScript dependencies or change application files.

The runner executes audio/capture helper tests, rejects four deliberately broken scenes (small text, clipped content, caption overlap, missing font), then renders four 32-second exports: landscape at 30/60 fps, square at 30 fps, and portrait at 30 fps. Narrated runs use the measured voice duration, split into four equal demonstration sections; prepare that test voice with those sections in mind. Real film cue boundaries follow its actual voice and observed actions, not this fixture's equal sections.

Each export has measured opening, approach, action and settled-result stills for all four scenes. `check-media.py` verifies dimensions, duration, fps, complete frame decoding, audio presence, non-silent/non-clipped audio when expected, fidelity to source stills, and matching 30/60 fps moments. It emits decoded PNGs at 640/480/360-pixel player widths and an HTML playback page. Its edge comparison catches substantial encode damage against a known source; it does not measure all forms of blur or certify text recognition.

The media check also rejects intentionally wrong fps, duration and audio contracts and a deliberately blurred encode. For these H.264/AAC fixtures, the container-duration check allows up to 60 ms of AAC packet padding; video length still requires the exact decoded frame count. Narrated runs also compare decoded audio with the prepared mix, report measured offset, and reject a shift over 60 ms or substantial signal changes. Review reports retain these rejected cases as evidence that the checks execute. Signal matching does not establish pronunciation or listening quality.

Open `review.html`, play every complete file at normal speed, inspect controls shown/hidden and paused endings, and listen to voiced exports. Record timestamped visual/audio decisions separately. Generated reports deliberately retain `NOT_REVIEWED` for those judgments. Deliberate reading holds are valid; this runner does not reject a stable result as a freeze. Preserve failed drafts and their logs.

For a project-specific test, adapt the fixture to its real components and hardest states; retain the negative cases and intended-size inspection. Do not claim that synthetic recipe output verifies live product behavior or a whole catalog.

## Four scene recipes and three layouts

`templates/recipes.tsx` supplies composable React patterns, using the existing cursor helper:

| Recipe | Use | Required evidence |
|---|---|---|
| `ActionRecipe` | Pointer approach, action, changed menu/control state, reading hold | Actual before/after components; measured target in local coordinates; observed result |
| `TableRecipe` | Dense values with row emphasis | Complete labels, periods and units; every row has one value per period |
| `ComparisonRecipe` | Explain two or more values on a shared scale | Source values and unit; explicit scale; distinguish explanation from a captured chart |
| `ResultRecipe` | Before/after evidence | The same subject and fixture; an observed final state; no invented success |

`SceneFrame` separates heading, subject, captions and player-control clearance. Portrait stacks table periods and before/after panels; landscape preserves side-by-side comparisons. `formats` defines 1920×1080, 1080×1080, and 1080×1920. These are separately composed layouts. Keep long labels/amounts in the test; reflow or divide the information when it fails, rather than shrinking below readable size.

`ReadabilityGuard` loads the declared font before inspecting marked `[data-readable]` text. Keep it mounted alongside `SceneFrame`, or use the project's own font-loading gate when running without the guard. It rejects text below 16 CSS pixels at the declared player width, off-frame text, content outside its region, overflow and caption collisions. Mark the text the viewer actually must read. For a real embed, pass its observed player width and control clearance; the fixture's 48-pixel controls are a test configuration, not a universal safe area. Camera transforms, overlapping siblings, cursor coverage and third-party player overlays still require decoded-frame and playback inspection.

## Narration and captions

Start with the actual recorded or authorized synthesized voice file. Correct product names, numbers and pronunciation before timing the film. Obtain word/phrase times from the transcription tool already available to the project; Remotion documents [transcription and caption utilities](https://www.remotion.dev/docs/captions/). Correct the transcript against the audio; never estimate subtitle timestamps from word count.

Create a JSON input with paths relative to that JSON:

```json
{
  "voice": "voice.wav",
  "music": "licensed-music.wav",
  "musicGainDb": -24,
  "duckDb": -12,
  "captions": [
    {"startMs": 500, "endMs": 3200, "text": "Open the scenario menu."},
    {"startMs": 4100, "endMs": 6800, "text": "Base is marked Default."}
  ]
}
```

Omit `music` for a voice-only film. Use a new output folder directly inside `public/`:

```sh
uv run --with numpy --with imageio-ffmpeg python scripts/prepare-narration.py narration-input.json public/narration
```

The helper reuses the existing audio decoder, validates ordered caption times against measured audio duration, lowers music around actual voice energy, preserves pauses, and leaves peak headroom. It rejects nested output folders so its public-relative audio path cannot silently point to the wrong file. It writes `audio.wav`, `captions.srt`, `narration.json` and `audio-checks.json`. This is peak control, not a claim of a particular integrated LUFS target. Listen for voice intelligibility, music pumping, clipped words, loop seams and correct pronunciation; adjust levels to the film and destination.

Mount `NarrationTrack` once in the composition. Use `captionAt(captions, frame / fps * 1000)` in the reserved caption area. Set duration from `durationMs` and the actual fps; place actions and holds against those measured cues. Add any closing silence to the voice timeline before preparation so narration, subtitles and film share one time origin. The JSON's audio path assumes its folder is directly inside `public/`; update that path when nesting assets. Recheck the final encode's sync and both burned-in and SRT captions after a picture edit. Plain captions are the default; word highlighting is optional.

## Capture readiness and observed transitions

Copy `templates/capture-observations.json` beside the capture log. Immediately before a take, use the current native UI to fill exact observations: installed app version, Screen Recording permission, Accessibility permission for the controlling host, unique named source and source identifier, source dimensions at the planned crop, available local export controls, and idle recorder state. Record tool/screenshot references in `evidence` and ISO timestamps with timezone. Unknown is not pass. The script checks these observations; it cannot inspect OS permission databases or infer permission from a successful shortcut.

```sh
python scripts/capture-preflight.py capture-observations.json --out readiness-v1.json
```

The checker rejects missing/stale observations (older than five minutes), ambiguous source matches, insufficient source size, active/unknown recorder state, existing output files and unwritable destinations. `READY_TO_ATTEMPT` means only that the supplied observations pass. Re-observe source and idle state immediately before the UI start action. Permissions, desktops and windows can change after a check.

Continue through the existing [Screen Studio workflow](screen-studio.md), verifying each state: selected source → active timer → saved playable project → completed local export → decode and full playback. After a timeout, inspect which state actually exists before doing anything else. Never repeat Start against an unknown state or restart an uncertain export. Refresh observations after a changed window, app relaunch or failed transition. Do not reset permissions, discard takes or enable unsupported adapters as an automatic repair.
