import React, {useLayoutEffect, type CSSProperties, type ReactNode} from 'react';
import {AbsoluteFill, Audio, cancelRender, continueRender, delayRender, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {cursorAt, UserCursor} from './kit/cursor';

export const formats = {
  landscape: {width: 1920, height: 1080, playerWidth: 640},
  square: {width: 1080, height: 1080, playerWidth: 480},
  portrait: {width: 1080, height: 1920, playerWidth: 360},
} as const;
export type Format = keyof typeof formats;
export type Brand = {fontFamily: string; fontFile: string; background: string; surface: string; text: string; muted: string; accent: string};
export type Caption = {startMs: number; endMs: number; text: string};
export type Narration = {durationMs: number; audio: string; captions: Caption[]};

/** Copy the product's tokens into Brand; the examples are synthetic explanations. */
export function SceneFrame({brand, title, caption, children, controlsPx = 48}: {
  brand: Brand; title: string; caption?: string; children: ReactNode; controlsPx?: number;
}) {
  const {width, height} = useVideoConfig();
  const portrait = height > width;
  const playerWidth = portrait ? 360 : width === height ? 480 : 640;
  const unit = width / playerWidth;
  return <AbsoluteFill data-film-root style={{background: brand.background, color: brand.text, fontFamily: brand.fontFamily, fontSynthesis: 'none', padding: 24 * unit, paddingBottom: (controlsPx + 16) * unit}}>
    <div data-readable="heading" style={{fontSize: 28 * unit, lineHeight: 1.12, maxWidth: '100%'}}>{title}</div>
    <div data-content style={{position: 'relative', flex: 1, marginTop: 20 * unit, marginBottom: 16 * unit, display: 'flex', flexDirection: 'column', justifyContent: 'center'}}>{children}</div>
    <div data-caption style={{minHeight: 54 * unit, fontSize: 18 * unit, lineHeight: 1.35, color: brand.muted}}>
      {caption && <span data-readable="caption">{caption}</span>}
    </div>
  </AbsoluteFill>;
}

export function NarrationTrack({narration}: {narration: Narration}) {
  return <Audio src={staticFile(narration.audio)}/>;
}

export function captionAt(captions: Caption[], milliseconds: number) {
  return captions.find(c => milliseconds >= c.startMs && milliseconds < c.endMs)?.text;
}

/** Pair with source-matched button/menu children. Target is in local scene pixels. */
export function ActionRecipe({seconds, actionAt, target, before, after}: {
  seconds: number; actionAt: number; target: {x: number; y: number}; before: ReactNode; after: ReactNode;
}) {
  const cursor = cursorAt(seconds, [
    {t: 0, x: target.x + 100, y: target.y + 100},
    {t: actionAt, ...target, click: true},
  ], (x, y) => ({x, y}));
  const zoom = interpolate(seconds, [Math.max(0, actionAt - 0.8), Math.max(0.01, actionAt - 0.4)], [0.96, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{position: 'relative', width: '100%', transform: `scale(${zoom})`, transformOrigin: 'center center'}}>
    {seconds < actionAt ? before : after}
    <div data-cursor><UserCursor {...cursor}/></div>
  </div>;
}

/** Keep labels and units visible; portrait stacks periods instead of cropping columns. */
export function TableRecipe({brand, periods, rows, focus, seconds, actionAt}: {
  brand: Brand; periods: string[]; rows: {label: string; values: string[]}[]; focus: number; seconds: number; actionAt: number;
}) {
  const {width, height} = useVideoConfig();
  const portrait = height > width;
  const unit = width / (portrait ? 360 : width === height ? 480 : 640);
  if (rows.some(r => r.values.length !== periods.length)) throw new Error('Each table row needs one value per period');
  const cell: CSSProperties = {padding: 9 * unit, borderBottom: `1px solid ${brand.muted}30`, textAlign: 'right'};
  return <div style={{fontSize: 17 * unit, lineHeight: 1.4}}>
    {portrait ? periods.map((period, column) => <div key={period} style={{marginBottom: 12 * unit}}>
      <div data-readable style={{color: brand.muted, marginBottom: 5 * unit}}>{period}</div>
      {rows.map((row, index) => <div key={row.label} style={{display: 'flex', justifyContent: 'space-between', gap: 10 * unit, padding: 3 * unit, color: seconds >= actionAt && index === focus ? brand.accent : brand.text}}>
        <span data-readable>{row.label}</span><span data-readable>{row.values[column]}</span>
      </div>)}
    </div>) : <table style={{borderCollapse: 'collapse', width: '100%'}}>
      <thead><tr><th style={cell}/>{periods.map(p => <th key={p} style={cell}><span data-readable>{p}</span></th>)}</tr></thead>
      <tbody>{rows.map((row, index) => <tr key={row.label} style={{color: seconds >= actionAt && index === focus ? brand.accent : brand.text}}>
        <td style={{...cell, textAlign: 'left'}}><span data-readable>{row.label}</span></td>
        {row.values.map((value, i) => <td key={i} style={cell}><span data-readable>{value}</span></td>)}
      </tr>)}</tbody>
    </table>}
  </div>;
}

/** An explanatory comparison with a shared scale and explicit values/units. */
export function ComparisonRecipe({brand, values, unitLabel, maximum, seconds, actionAt}: {
  brand: Brand; values: {label: string; value: number}[]; unitLabel: string; maximum: number; seconds: number; actionAt: number;
}) {
  if (!(maximum > 0) || values.some(v => !Number.isFinite(v.value) || v.value < 0 || v.value > maximum)) throw new Error('Comparison values must fit the declared scale');
  const {width, height} = useVideoConfig();
  const unit = width / (height > width ? 360 : width === height ? 480 : 640);
  const reveal = interpolate(seconds, [actionAt, actionAt + 0.35], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <div style={{fontSize: 19 * unit}}>
    {values.map((v, i) => <div key={v.label} style={{marginBottom: 24 * unit}}>
      <div style={{display: 'flex', justifyContent: 'space-between', gap: 10 * unit, marginBottom: 8 * unit}}>
        <span data-readable>{v.label}</span><span data-readable>{v.value} {unitLabel}</span>
      </div>
      <div style={{height: 18 * unit, background: brand.surface}}><div style={{height: '100%', width: `${100 * v.value / maximum * (i === 0 ? 1 : reveal)}%`, background: i === 0 ? brand.muted : brand.accent}}/></div>
    </div>)}
    <div data-readable style={{fontSize: 16 * unit, color: brand.muted}}>Scale: 0–{maximum} {unitLabel}</div>
  </div>;
}

export function ResultRecipe({before, after, seconds, actionAt}: {before: ReactNode; after: ReactNode; seconds: number; actionAt: number}) {
  const {width, height} = useVideoConfig();
  return <div style={{display: 'grid', gridTemplateColumns: height >= width ? '1fr' : '1fr 1fr', gap: 40}}>
    {before}<div style={{opacity: seconds >= actionAt ? 1 : 0}}>{after}</div>
  </div>;
}

/** QA observes the laid-out DOM after the exact font loads. It does not grade art direction. */
export function ReadabilityGuard({brand, playerWidth, controlsPx = 48, minimumTextPx = 16}: {
  brand: Brand; playerWidth: number; controlsPx?: number; minimumTextPx?: number;
}) {
  const frame = useCurrentFrame();
  const {width, height} = useVideoConfig();
  useLayoutEffect(() => {
    const handle = delayRender('font and layout audit');
    let active = true;
    const check = async () => {
      if (![...document.fonts].some(f => f.family === brand.fontFamily && f.status === 'loaded')) {
        const font = await new FontFace(brand.fontFamily, `url(${staticFile(brand.fontFile)})`).load().catch(() => {throw new Error(`FONT_LOAD: ${brand.fontFile}`);});
        document.fonts.add(font);
      }
      await document.fonts.ready;
      if (!active) return;
      const root = document.querySelector('[data-film-root]')!;
      const box = root.getBoundingClientRect();
      const scale = width / box.width;
      const visibleBottom = height - controlsPx * width / playerWidth;
      const issues: string[] = [];
      const caption = document.querySelector('[data-caption]')!.getBoundingClientRect();
      const content = document.querySelector('[data-content]')!.getBoundingClientRect();
      for (const el of document.querySelectorAll<HTMLElement>('[data-readable]')) {
        if (!el.textContent?.trim() || el.closest('[style*="opacity: 0"]')) continue;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        const name = el.textContent.slice(0, 70);
        const pixels = parseFloat(style.fontSize) * playerWidth / width;
        if (pixels < minimumTextPx) issues.push(`SMALL_TEXT: ${name} (${pixels.toFixed(1)}px)`);
        if ((rect.bottom - box.top) * scale > visibleBottom || (rect.left - box.left) * scale < -1 || (rect.right - box.left) * scale > width + 1 || (rect.top - box.top) * scale < -1) issues.push(`CLIPPED: ${name}`);
        if (el.scrollWidth > el.clientWidth + 1 && el.clientWidth > 0) issues.push(`OVERFLOW: ${name}`);
        if (el.closest('[data-content]') && (rect.top < content.top - 1 || rect.bottom > content.bottom + 1 || rect.left < content.left - 1 || rect.right > content.right + 1)) issues.push(`CONTENT_CLIPPED: ${name}`);
        if (el.closest('[data-content]') && rect.bottom > caption.top && rect.top < caption.bottom && rect.right > caption.left && rect.left < caption.right) issues.push(`CAPTION_OVERLAP: ${name}`);
      }
      if (issues.length) throw new Error(issues.join('\n'));
      console.info(`FILM_QA:${JSON.stringify({frame, width, height, minimumTextPx, playerWidth})}`);
      continueRender(handle);
    };
    check().catch(cancelRender);
    return () => {active = false; continueRender(handle);};
  }, [frame, brand.fontFamily, brand.fontFile, width, height, playerWidth, controlsPx, minimumTextPx]);
  return null;
}
