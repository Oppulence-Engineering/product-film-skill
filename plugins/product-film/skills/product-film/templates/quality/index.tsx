import React from 'react';
import {Composition, registerRoot, useCurrentFrame, useVideoConfig} from 'remotion';
import {ActionRecipe, captionAt, ComparisonRecipe, formats, NarrationTrack, ReadabilityGuard, ResultRecipe, SceneFrame, TableRecipe, type Brand, type Format, type Narration} from '../recipes';

type Props = {format: Format; fps: number; fontFile: string; fault?: 'small' | 'clip' | 'overlap'; narration?: Narration};
const brand: Brand = {fontFamily: 'FilmProof', fontFile: 'font.ttf', background: '#f5f6f8', surface: '#e1e5ea', text: '#152c3c', muted: '#536777', accent: '#146450'};
const headings = ['Find the scenario', 'Read the full model', 'Compare on one scale', 'Show the observed result'];
const descriptions = ['The menu shows Base as the default.', 'All periods, values and units remain visible.', 'Both bars use the same 30-month scale.', 'The final state is explicit and stays on screen.'];

function Proof(props: Props) {
  const frame = useCurrentFrame();
  const {fps, width} = useVideoConfig();
  const seconds = frame / fps;
  const segment = (props.narration?.durationMs ?? 32000) / 4000;
  const index = Math.min(3, Math.floor(seconds / segment));
  const local = seconds - index * segment;
  const tokens = {...brand, fontFile: props.fontFile};
  const u = width / formats[props.format].playerWidth;
  const surface = {padding: 20 * u, background: tokens.surface, borderRadius: 8 * u, fontSize: 19 * u, lineHeight: 1.5};
  const menu = <div style={surface}><div data-readable>Scenarios</div><div style={{display: 'flex', justifyContent: 'space-between', gap: 8 * u, marginTop: 18 * u}}><span data-readable>Base</span><span data-readable>Default</span></div></div>;
  const fallback = local >= 2 ? descriptions[index] : 'Synthetic test data • authored explanation';
  const caption = props.narration ? captionAt(props.narration.captions, seconds * 1000) : fallback;
  return <>
    <SceneFrame brand={tokens} title={headings[index]} caption={caption}>
      <div style={props.fault === 'overlap' ? {position: 'absolute', top: '100%', width: '100%'} : props.fault === 'clip' ? {transform: 'translateX(90%)'} : {}}>
        {index === 0 && <ActionRecipe seconds={local} actionAt={2} target={{x: 12 * u, y: 16 * u}}
          before={<div style={surface}><span data-readable>Scenarios ▾</span></div>} after={menu}/>}
        {index === 1 && <TableRecipe brand={tokens} periods={['Oct 2026', 'Nov 2026', 'Dec 2026']} rows={[
          {label: 'Cash ($)', values: ['1,150,000', '1,100,000', '1,050,000']},
          {label: 'Burn ($/mo)', values: ['50,000', '50,000', '50,000']},
          {label: 'Runway (mo)', values: ['23', '22', '21']},
        ]} focus={2} seconds={local} actionAt={2}/>}
        {index === 2 && <ComparisonRecipe brand={tokens} values={[{label: 'Base', value: 23}, {label: 'Example', value: 21}]} unitLabel="months" maximum={30} seconds={local} actionAt={2}/>}
        {index === 3 && <ResultRecipe seconds={local} actionAt={2}
          before={<div style={surface}><div data-readable>Before</div><div data-readable>No selection</div></div>}
          after={<div style={surface}><div data-readable>After</div><div data-readable>Base selected</div></div>}/>}
        {props.fault === 'small' && <span data-readable style={{fontSize: 8}}>Unreadable defect</span>}
      </div>
    </SceneFrame>
    {props.narration && <NarrationTrack narration={props.narration}/>}
    <ReadabilityGuard brand={tokens} playerWidth={formats[props.format].playerWidth}/>
  </>;
}

registerRoot(() => <Composition id="QualityProof" component={Proof} width={1920} height={1080} fps={30} durationInFrames={960}
  defaultProps={{format: 'landscape', fps: 30, fontFile: 'font.ttf'}}
  calculateMetadata={({props}) => {
    if (!(props.format in formats) || ![30, 60].includes(props.fps)) throw new Error('Use landscape/square/portrait and 30/60 fps');
    const duration = props.narration?.durationMs ?? 32000;
    if (!Number.isFinite(duration) || duration < 24000) throw new Error('Proof needs at least 24 seconds for four readable scenes');
    return {...formats[props.format], fps: props.fps, durationInFrames: Math.round(duration / 1000 * props.fps)};
  }}/>);
