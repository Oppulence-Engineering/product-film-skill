# Remotion: direction, product fidelity, and visual quality

Read this before writing or revising a Remotion story. It refines the earlier beat-driven defaults without removing the original workflow. Use it for authored motion and recorded UI inside Remotion; native Screen Studio controls remain in [screen-studio.md](screen-studio.md).

## Start from the actual weak export

When a user says the videos are poor, inspect the referenced files before prescribing effects. Resolve the exact version from the product's source or manifest, then inspect the delivered CDN file. Record its URL/path, retrieval date, duration, dimensions, fps, and audio presence. Compare the opening, action, result, transitions, and ending with source footage and cue data when available. A dated filename or green pipeline does not prove which bytes viewers receive.

Write a short defect list: timestamp → visible problem → viewer cost → smallest correction. Separate observations from suspected causes. Sample representative dense, sparse, and changing views in a batch; do not report the whole catalog reviewed. A skill audit does not itself authorize product edits, replacement uploads, or invented footage.

## Choose the story before the look

- Write one viewer question and one observable answer. A short demo should usually follow one workflow. The earlier 3–6-feature shape is an option for a feature reel, not a quota. Tutorials retain the steps required to teach the task.
- Open on a useful product state or a clear visual promise. Let the brand be present immediately without an obligatory logo reveal. Use a blank first frame only when an approved loop design needs it.
- For each shot, record its source component/capture, focal target, action, result, caption, and reading time. Opening a menu proves access to that menu, not a completed comparison, automation, or financial result.
- Match the closing proof to the claim. A headline about comparing scenarios needs a visible comparison; a generic model grid or Reports header does not demonstrate that outcome. If evidence is absent, narrow the words or obtain the required footage within the authorized scope.
- Preserve names, units, dates, and fixture values across shots. Frame-driven twins copy actual component structure and states. Distinguish a designed explanation from a captured product outcome.

## Set one coherent visual direction

Use the product's fonts, spacing, surfaces, icons, and motion language. Record the typography hierarchy, alignment, safe areas, framing, caption placement, and primary transition family in `BRAND.md`. Translate references into specific decisions; do not import another brand's identity. If direction is unclear, compare two treatments of the same hero frame, then carry one direction through the film.

Design three real style frames: orientation, action detail, and outcome. Use actual content, resolved fonts, and final aspect ratio. A wireframe cannot approve typography or capture sharpness. If the user already delegated direction or approved a reference, proceed within it and show frames without repeating the interview.

- Give each frame one dominant subject. Use a wide view to orient, a detail view to explain, and a result view to prove. Change framing because the subject changes; three copies of a centered dashboard are not distinct compositions.
- Keep the important object, label, value, units, and relevant comparison in view. A crop may exclude unrelated UI, but should not cut a required formula, graph axis, menu, or status. Include context margins and inspect the whole camera move, not only its end box.
- Remove irrelevant recording overlays and notifications during capture. If an upgrade prompt or changelog dominates the lesson's subject, choose a better crop or retake. Do not erase product state to imply an unavailable feature worked.
- Distinguish film heading, instructional caption, and product text. Avoid a persistent title that repeats the caption and competes with the UI. Reserve a stable caption area when needed, clear of the action and player controls.
- Measure type after all scaling and cropping. A 28 px label in a 1920-wide export appears about 9 px in a 640-wide embed. Name the text viewers must read and inspect it at the expected player width. Enlarge that subject or simplify the shot before shrinking everything. Secondary context can stay small when it is not the lesson.
- Load exact font families, weights, and styles before measuring. Check real copy and long labels for wrapping; avoid synthetic bold and fallback fonts. Remotion's [local font loader](https://www.remotion.dev/docs/fonts-api/load-font) waits for fonts before rendering. Prefer local assets and respect their licenses.

## Pace attention, action, and reading

Plan **orient → act → settle → read**. The hold starts after the target, caption, and camera are readable. Starting points for a short UI demo are a 0.2–0.5 s state transition and a 2–4 s result hold; dense tables, unfamiliar terms, or narration need longer. Tune by playing the sequence at normal speed, not by enforcing one duration everywhere.

- Beat alignment is a timing aid. It does not require a click, pulse, counter, or camera move on every beat. A deliberate reading hold is valid. Never add a zoom solely to defeat a freeze detector or maximum-scene-length rule.
- Where the project enforces timing limits, split content into meaningful steps while preserving reading time; do not weaken its gates just to pass.
- Move attention before or with the action, then settle the camera while the viewer reads. Avoid simultaneous camera travel, scrolling, word reveals, and count-ups. One motion should explain the change; subordinate motion should not compete.
- Use cuts for a new task or location, restrained camera moves for detail in the same context, and shared-element moves when the same object connects both views. Repeated actions on one target may keep their framing; do not automatically alternate wide/close to manufacture variety.
- Keep action and result continuous. Synchronize captions to what is visible, not just when an automation command was issued. Preserve a response interval and settled state; disclose compressed waits when they affect a performance claim.
- Anchor zooms to measured targets. Account for source resolution, letterboxing, crop, and container transforms once. Re-measure after layout changes and inspect viewport edges throughout the move. Enlarging an already scaled export cannot restore source detail.
- Keep text crisp during reading. Reserve bounce, word-by-word blur, long slides, and heavy camera movement for an approved purpose. Transitions should not consume the time needed to read their content.
- Silent films need sufficient visual explanation. Narrated films follow the actual voice track and pauses. Music and effects support events; do not add them automatically to an intentionally silent tutorial.

## Prove one sequence before rendering the batch

When improving this skill because its videos are poor, perform the render test as part of the skill change. Documentation validation and code review do not establish output quality. Keep the failing draft, corrective changes, final encoded proof, and test results. If rendering or playback is unavailable, label output quality unverified instead of accepting the change as visually proven.

Render a representative 6–12-second sequence with a difficult UI state, action, and result. Use a unique output version, intended fonts, framing, captions, and encoding profile. Inspect stills at the start, maximum movement, settled result, and handoff; play the encoded sequence at delivery size. Repair composition and timing before repeating the pattern across scenes or products.

Include both an interaction and dense content when the complaint concerns a tutorial catalog. A readable menu does not validate a table: inspect complete labels, periods, values, units, and formulas separately. Test the intended player with its controls visible as well as hidden, including the paused ending. Keep essential evidence outside that player's overlays; a generic fixed margin is not proof of clearance.

Use the original capture or a source-matched component detail when enlarging the delivery encode makes text soft. A frame-driven adaptation must retain the observed state and be identified as an authored explanation in the review, not a newly captured interaction. Check measurement overlays after fonts and styles are ready; confirm their coordinates against the actual rendered frame before placing a cursor.

Retain a before/after sample of the same moment when revising. For a new film, compare with the agreed reference and real source UI. Show a specific improvement: a complete target, readable result, correct timing, or clearer hierarchy. A larger file, higher fps, or more animation is not itself evidence of improvement.

| Gate | Evidence needed | Revise when |
|---|---|---|
| Product truth | Source state and matching visible result | A headline claims an outcome that never appears, or a twin invents behavior |
| Composition and type | Orientation/detail/result frames at target player size | Required labels are small, a key value is clipped, or irrelevant chrome dominates |
| Motion and pacing | Encoded action, settle, hold, and handoff at normal speed | The camera pumps without a new subject, captions lead the UI, or text has no calm read |
| Technical delivery | Metadata, full decode, fonts/assets, and color/sharpness checks | Assets are missing, audio is unintended, or duration/encoding is wrong |

Record `PASS`, `REVISE`, or `NOT_REVIEWED` per gate with timestamps and paths in the film prompt. A technical pass cannot override a visual defect. Contact sheets find composition problems; they do not prove playback, synchronization, or audio quality. After a fix, review the affected sequence and its neighbors; review the complete final export before calling the film verified.

For a batch, approve the representative treatment before bulk rendering. Review every final storyboard and unusual transition; the first successful file does not validate the rest. Keep each video's review state separate and report incomplete stages honestly.

## Encode for the content

Use [the direct UI render profile](render.md#direct-ui-render-profile) for most linear tutorials and crisp product walkthroughs. Keep the existing 240→60 fps pipeline for an authored film that benefits from its look. Test blur on moving details; never use it to hide poor capture quality. Higher resolution can help vector text on dense displays, but cannot reconstruct low-resolution footage. See Remotion's [quality guide](https://www.remotion.dev/docs/quality) and [motion-blur guide](https://www.remotion.dev/docs/motion-blur).

The loop verifier checks a particular duration/background/seam contract. It does not judge storytelling, reading time, framing, or claim evidence. A linear tutorial should end on its result or next step; it does not need to reset to a blank opening.
