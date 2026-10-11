# Screen Studio: record, edit, export

For a repeatable check of fresh permission, source, resolution, export and idle observations before a take, use [capture readiness](production-capabilities.md#capture-readiness-and-observed-transitions). A readiness result is separate from the observed recording/edit/export states below.

Use the native macOS app for actual product recordings and `.screenstudio` edits. Use this workflow without the Remotion engine, 240 fps master, music grid, or seamless-loop checks unless the brief specifically needs them.

## Prepare the job

Reuse the brief and existing project. Resolve only missing choices: product/feature, source project or new recording, audience, duration, aspect ratio, narration, and destination. For a short demo with no further constraints, propose 30–45 seconds, 16:9, 1080p, 30 fps, and screen-only capture. Longer tutorials keep the requested length and reading time. Record the decisions in [templates/screen-studio-demo.md](../templates/screen-studio-demo.md), or reuse the product's existing manifest.

For Eigenn, Conduitt, and Cadense staging, first read [staging-demos.md](staging-demos.md). Write a small shot list with starting screen, action, observed result, hold time, and narration/caption. Keep read-aloud words separate from operator cues. Speaker Notes are a recording aid, not a narration track or proof that captions were exported.

Use an available native-computer tool for Screen Studio and the existing signed-in browser for the product. In Codex, use `cua_repl` when available; read its current API documentation before acting. Select Screen Studio by name or observed bundle ID (`com.timpler.screenstudio` on the verified Mac). Inspect live accessibility controls or screenshots, then re-observe after each meaningful action. Menus, shortcuts, and timeline positions vary by version and focus; never replay saved coordinates or blindly toggle a global recording shortcut.

After a tool timeout, inspect the current app/dialog before retrying the action. A blank window or unreachable file picker does not prove import, save, or export. If controls remain unavailable, preserve the pending work and report the precise automation limit; do not force-quit the app or restart a take that may still be active.

Try recoverable native UI paths before a manual handoff. If only a blank background window is exposed, inspect Window → Window for Start Recording or the named project. If a file picker times out in accessibility, inspect its screenshot; when the picker is confirmed open, its Go to Folder control can select an exact known local path. If editor actions remain inert, verify that no recording/export is active and every open project is saved, then try a normal Quit and relaunch. Preserve any unsaved-work prompt. Reopen the exact saved copy and verify its timeline before continuing. This recovered editing and export in a local Screen Studio 3.4.11 test; it is not proof that a fresh recording works.

Check that Screen Studio is installed, the intended capture source is available, required permissions already work, and local export is available. Record the app version when visible. If the app, license, OS permission, browser session, or UI control is unavailable, identify the blocker and preserve work. Do not promise a headless Screen Studio CLI, fabricate a `.screenstudio` package, or patch undocumented project internals. A manual handoff includes the exact source and next visible control; it is not completed automation.

## Record a new take

1. Prepare an isolated staging window or capture area with approved demo data. Keep unrelated tabs, notifications, password managers, and private fields out of frame. Use a consistent viewport and browser zoom. Prefer an area/window over the whole display, and verify the selected region visually.
2. Inspect the recording setup and its inherited settings. For screen-only capture, explicitly disable camera, microphone, and system audio; enable only tracks the brief requests. Do not change global defaults or grant new OS/privacy access silently. For narration, verify the chosen mic with a short take before a long tutorial.
3. Open the recording setup using the visible menu/control. Start with the observed Record control, then verify that capture is active before performing the journey. Leave a short head handle, perform the rehearsed actions, pause long enough to read the result, and leave a tail handle. Confirm the stop control before starting so a missing menu-bar icon cannot trap the take.
4. Stop through the visible recording control or a shortcut verified in the current settings. Verify that the editor opened with a non-empty timeline and playable frames. Returning to Start Recording alone does not prove that footage exists.
5. Save immediately to a unique local `.screenstudio` path using the app's File menu. Verify the saved path and project on disk. Use `product-feature-YYYYMMDD-take01.screenstudio`, then increment take/version names. Keep raw takes; do not choose Delete in a save/discard dialog to escape a failed attempt.
6. If interrupted, inspect any unfinished/recovered recording and save it before another attempt. If the app reports no unfinished recordings, report the missing take honestly. Do not keep issuing Record/Stop commands without a new observable state.

Screen Studio documents [recording setup](https://screen.studio/guide/new-recording), [start/stop behavior](https://screen.studio/guide/starting-finishing-the-recording), and [project saving](https://screen.studio/guide/saving-your-project). Use the installed UI as the authority for available controls.

## Diagnose fresh-recording automation

Source selection and capture start are separate steps. The official [single-window guide](https://screen.studio/guide/recording-single-window) supports right-clicking **Window** and choosing the exact target from its list. The installed Record → Record window menu is another entry point. Verify the selected app, dimensions, and target content, then use the separate **Start recording** control beside the selection. Require the [elapsed-time recording widget](https://screen.studio/guide/managing-recording-in-progress) or another explicit active-capture indicator before performing the demo. A picker disappearing or a shortcut returning successfully is not that indicator.

The same guide requires **Display** mode for full-screen apps. Prefer a normal, isolated window when unrelated desktop content must stay out of frame. A missing window is not evidence of denied permission: inspect its full-screen state, current desktop/display, and the live source list. Never select the first available window or silently fall back to the first display.

Inspect existing Screen Studio entries in System Settings → Privacy & Security → **Screen & System Audio Recording** and **Accessibility**, following the vendor's [permission guide](https://screen.studio/guide/setting-up-permissions). Do not reset or regrant permissions merely because automation cannot see the picker. In a local 3.4.11 test, both permissions were enabled while native control still lost access to the floating picker. A later source list changed from Code alone to Chrome and other apps; the precise focus/desktop cause was not established. Reconnect stale automation state and re-observe the named target. Stop blind retries when the tool loses the selected overlay or reports a capture error; preserve any take and distinguish an automation observation failure from a Screen Studio recorder failure.

An update-renewal prompt can obscure the controls. Inspect its actual options and retain the usable installed version when renewal is outside the brief. An update entitlement warning alone does not prove that recording is disabled. Do not purchase a renewal as an assumed fix.

### Community automation adapters: research, not a verified fallback

The community [screenstudio-cli](https://github.com/ShawnPana/screenstudio-cli) and [screenstudio-agent fork](https://github.com/HyperfocuSam/screenstudio-agent) use Electron remote debugging, internal React state, and AppleScript helpers. They are not a documented Screen Studio CLI/API. Do not install, run, or enable debugging by following a repository README alone; use them only when the user authorizes that control method and the active tool rules permit it. Enabling a local debugging port gives local processes control of Screen Studio; verify loopback-only binding and close the port after the job.

Source review of screenstudio-agent commit `b72de176e05db2652cb54ef04283bdb76eff8ed9` found an MIT license and useful saved-project checks, but no proof of compatibility with the tested 3.4.11 installation. Its start wait uses page-count stability plus a delay, not confirmed recorded frames, and display selection can fall back to the first display. Do not trust its success text, guessed display indices, or an ambiguous window match. For an authorized trial, pin the reviewed revision, isolate a synthetic named window, require a unique target, preserve existing projects, and independently verify a new playable recording and its duration. Do not use cancel/discard or force-quit to recover a failed trial. A source review is not a passed automation test.

## Edit a saved project or imported clip

Open the exact requested project through File → Open project or an observed recent-project entry. Check its name, source content, duration, and media availability before editing. A recent filename alone is not proof of a recording.

Preserve the original before the first edit: use Save As to a new version and verify the new active path. If unavailable, save/close and copy the complete project package to a new path, then open the copy. Never overwrite another take, modify a live package behind the app, or delete raw assets. Reopen the saved edited version to confirm that changes persist.

If the only source is an MP4, use the app's [Create project from video](https://screen.studio/guide/creating-project-from-existing-video) command. Imported video has no original mouse/camera capture metadata; do not promise editable cursor tracks or click-driven auto-zoom. Use manual framing/zooms instead.

| Edit | Operation and verification |
|---|---|
| Trim and remove mistakes | Drag clip edges for head/tail trims. Split at observed timeline times and remove only the unwanted segment in the versioned copy. Play across each cut; preserve the action/result relationship. See [trimming](https://screen.studio/guide/trimming). |
| Speed and pauses | Select the intended clip/segment, inspect its speed control, and shorten dead time without losing readable results. Avoid speeding narration. Recheck total duration and subtitle timing after changes. |
| Zooms | Inspect auto-generated zoom blocks; adjust start/end and intensity or remove distracting ones. Add manual zooms for a result away from a click. Preview entry, hold, and exit; do not clip labels. See [zoom editing](https://screen.studio/guide/adding-editing-zooms). |
| Crop and aspect ratio | Crop source chrome separately from setting the output canvas ratio. Make a separate 9:16/1:1 version and reframe each shot; a center crop may hide the important action. Verify export dimensions. |
| Cursor and layout | Inspect cursor size, smoothing, click effects, background, padding, and corner radius. Match the product's brand and avoid inherited settings from another film. Ensure the cursor does not cover the result. |
| Narration, music, captions | Inspect available audio tracks, volume, and captions in the installed version. Use only requested audio and licensed music. Correct names, amounts, and timing after the picture edit. If no speech track exists, supply the caption/narration script; Speaker Notes do not synthesize speech. Use a separate editor/Remotion only when needed and within the brief. |
| Masks and highlights | Prefer safe fixtures or a retake. If a mask is needed, follow it through scrolling, zooms, cuts, and the entire export. A visual mask does not sanitize the source project, which retains original recordings. Do not share raw projects containing private data. |

Save a new local version after substantial changes. Keep the edit list in source timestamps and record the resulting output timing, especially for trims and speed changes. Do not infer exact cuts from pixels on a zoomed timeline; use the displayed time and playback to verify them.

For an automation smoke test, use a short synthetic clip with a visible timecode and a known duration, saved outside the repository. Import it, save an original project, use Save As for an edit copy, and test an aspect change, clip speed, manual zoom, save/reopen, and local export. In the tested version, the clip context menu exposes Set speed. A 12-second source at 2× should produce about 6 seconds; verify the actual file. Compare original file hashes before and after. This tests the import/edit/export path only; keep fresh recording, trim, narration, captions, and other unexercised operations separate in the results.

## Export and inspect the actual file

1. In the editor, select Export and inspect format, output size, frame rate, quality, and audio. Use MP4 for normal demos, GIF only when requested. Match the brief; do not upscale to invent detail. See [export controls](https://screen.studio/guide/exporting-the-video).
2. Choose **Export to File**, with a new versioned destination such as `out/<film>/v1/demo.mp4`. Do not choose a shareable link or cloud upload unless the user requested that destination. Export the edited canvas, not an extracted raw source track.
3. Observe export completion, resolve the exact output path, and confirm the file is non-empty. If blocked by licensing or a permission prompt, retain the saved project and report export as blocked; do not purchase or activate anything without authorization.
4. Probe and fully decode the export with available ffmpeg tools. These commands inspect an existing file; substitute its exact path and honor local command wrappers such as RTK:

   ```bash
   ffprobe -v error -show_entries format=duration,size:stream=codec_type,codec_name,width,height,avg_frame_rate,color_range,color_space -of json "out/<film>/v1/demo.mp4"
   ffmpeg -v error -xerror -i "out/<film>/v1/demo.mp4" -map 0:v:0 -map '0:a?' -f null -
   ```

   Compare duration, dimensions, frame rate, and audio presence with the brief. Require a video stream and no decode failure. Do not invent missing tools or treat these commands alone as a visual/audio review. If ffprobe is unavailable, inspect the file with ffmpeg/player metadata and record any unverified fields.

   When system ffmpeg is absent but this skill's `uv` toolchain is available, use the existing imageio-ffmpeg dependency for decoding:

   ```bash
   uv run --with imageio-ffmpeg python -c 'import imageio_ffmpeg, subprocess, sys; subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-xerror", "-i", sys.argv[1], "-map", "0:v:0", "-map", "0:a?", "-f", "null", "-"], check=True)' "out/<film>/v1/demo.mp4"
   ```

   This supplies ffmpeg, not ffprobe, and proves decode only; inspect metadata and playback separately.
5. Play the complete exported file in an available player. Inspect the opening, every cut/zoom, result, and ending at delivery size; listen if sound is part of the brief. Check readability, pointer coverage, dropped/black frames, leaked data, crop, captions, audio sync, and truthful outcomes. If playback/audio inspection is unavailable, state the review limit instead of marking that stage passed.
6. For a poster, extract a readable result frame from the final export with ffmpeg or the player's frame export. Avoid an empty opening. Deliver the MP4, editable project path, poster, narration/caption files if used, and capture/edit log. Keep raw media local unless sharing is explicitly authorized.

`scripts/verify.py` assumes a constant-background seamless loop. Do not run it on a linear Screen Studio demo and treat its background/seam failures as export defects. For a requested loop, inspect the last-to-first transition; use that verifier only if the film satisfies its documented background/size/fps contract. Screen Studio color metadata is not assumed to match the Remotion master pipeline.

## Hybrid handoff

Use Screen Studio's verified edited MP4 as immutable footage in the existing video workspace. Retain the source `.screenstudio` project and record the export path/version, route, capture time, fixture, and observed outcome. Use the workspace's installed Remotion video component and its actual frame rate; calculate clip boundaries from the edited export rather than raw take time. Avoid applying a second cursor or camera zoom over an already framed recording. Verify captions, audio, dimensions, and trims again after composition. Keep recordings distinguishable from component-based illustrations; simulated UI is not staging evidence.

## Completion states

A shot list is **planned**; an active recording indicator is **recording**; a saved playable `.screenstudio` project is **captured**; persisted timeline changes are **edited**; a completed non-empty media file is **exported**; matching metadata, full decode, and complete playback review make it **verified**. Report the last state actually evidenced, per take and per product. Never label a setup window, preview, or saved project as a delivered video.


## Follow-up: isolated fresh-recording trial passed on 3.4.11

On 2026-10-11, an explicitly authorized trial of the pinned community fork above captured a new synthetic TextEdit window, saved and reopened the project, and exported an MP4 on Screen Studio **3.4.11-3961**. This updates the earlier source-review status for this narrow trial. The unmodified fork and unattended browser/staging capture are still unverified.

The trial exposed three separate automation issues. Native control lost the floating source picker; AppleScript launched from the agent shell reported denied assistive access; and the fork's cached Record window `onClick` callback did nothing in this installed version. Calling the currently observed menu action's `action.input.execute()` opened the picker. A helper executed in a dedicated Terminal window, which already had Accessibility access, found the synthetic target after moving to its desktop. A single sequence on that desktop then completed launch, selection, recording, and stop. These observations establish a working combination, not one proven cause for every earlier failure. No OS permission, app binary, license, or project internals were changed.

For another authorized adapter trial:

1. Preserve all open projects and verify no active recording/export before a normal quit/relaunch. Pin and inspect the adapter, use a compatible local Node runtime, and keep dependencies local. Do not assume the shell's default Node works; the trial required an explicit installed Node 22 path because another local Node executable could not load its library.
2. Put the uniquely named synthetic target and picker on the same desktop. Inspect the live app, title, dimensions, and content. Require exactly one matching overlay; stop on zero or multiple matches. Do not use the fork's first-display fallback. The successful patch restricted lookup to the one known TextEdit fixture and is not a general browser-window resolver.
3. When a version-specific callback is inert, inspect the current menu action before adapting the local checkout. Refresh cached callbacks after relaunch. Treat internal React paths as unsupported and version-dependent, not a stable API. Do not substitute a trusted helper host unless that control method is authorized; this test reused Terminal's existing access without granting new permissions.
4. Require an independently observed active timer, then stop normally and require a newly saved non-empty project. Preserve the original package, reopen an export copy, and inspect actual media. The successful trial observed a 0:12 timer and a reopened 13.09-second timeline; CLI start success alone was not accepted.
5. Export through the observed editor controls to a new local filename. If the native Save panel shows the correct path but Save stays disabled, try its visible **show more options** disclosure, then recheck the path and enabled Save control. This recovered the tested export dialog; it is not a universal fix.
6. After export finishes and the project is saved, quit normally and independently check that the temporary loopback debugging listener is gone. The trial verified `127.0.0.1:9222` while active and no listener after quit. Do not leave debugging enabled as a default.

Evidence: the raw take was 13.09 seconds, H.264, 2094×1446, approximately 60 fps, with no audio. The actual Screen Studio export was 13.07 seconds, H.264, 1468×1080 at 30 fps, 958,618 bytes, with no audio. Both passed full decoding. Export frames at 1, 6, and 12 seconds showed the intended synthetic window. All 58 original package file hashes stayed unchanged. Complete player playback of this fresh export was not confirmed; QuickTime's Open dialog remained unavailable to native control. Keep that review stage partial. This trial does not verify narration, dynamic browser interactions, staging recordings, or general unattended operation.
