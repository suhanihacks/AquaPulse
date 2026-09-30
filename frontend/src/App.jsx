import React, { useEffect, useMemo, useRef, useState } from 'react';
import { MapContainer, TileLayer, CircleMarker, Polyline, Popup, useMap } from 'react-leaflet';

const API = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';
const links = [['BINDAL-UPPER','BINDAL-MID'],['BINDAL-MID','BINDAL-CONFLUENCE'],['BINDAL-CONFLUENCE','BINDAL-LOWER'],['RISPANA-MID','RISPANA-LOWER']];
const meta = { rain_runoff:['SCENARIO 01','high'], localized_discharge:['SCENARIO 02','medium'], rain_no_event:['SCENARIO 03','low'] };
const CITIES = {
  dehradun: { label:'Dehradun study area', short:'Dehradun', mode:'validated', center:[30.268,78.032], zoom:12.8 },
  gurugram: { label:'Gurugram preview', short:'Gurugram', mode:'preview', center:[28.4595,77.0266], zoom:11.8 }
};
const TABS = [['command','Command Center'],['memory','River Memory'],['hot','Hot Moments'],['verify','Verification'],['evidence','Evidence']];
const pretty = (v='') => v.toLowerCase().replaceAll('_',' ').replace(/\b\w/g,c=>c.toUpperCase());

function Fit({center,zoom}){ const m=useMap(); useEffect(()=>{m.setView(center,zoom,{animate:false});},[m,center,zoom]); return null; }
function MapResizer(){ const m=useMap(); useEffect(()=>{ const refresh=()=>m.invalidateSize({animate:false}); const id1=setTimeout(refresh,50); const id2=setTimeout(refresh,300); window.addEventListener('resize',refresh); const el=m.getContainer(); const ro=typeof ResizeObserver!=='undefined'?new ResizeObserver(refresh):null; if(ro) ro.observe(el); return ()=>{clearTimeout(id1);clearTimeout(id2);window.removeEventListener('resize',refresh);if(ro) ro.disconnect();}; },[m]); return null; }

class AppErrorBoundary extends React.Component {
  constructor(props){ super(props); this.state={hasError:false,error:null}; }
  static getDerivedStateFromError(error){ return {hasError:true,error}; }
  componentDidCatch(error,info){ console.error('AquaPulse UI error',error,info); }
  render(){
    if(this.state.hasError){
      return <div className="loading"><div className="brand"><span className="mark">≈</span><b>AquaPulse</b></div><p>That section could not be rendered safely.</p><small className="error-detail">The rest of AquaPulse is protected from this UI error.</small><button className="primary-btn" onClick={()=>this.setState({hasError:false,error:null})}>Try again</button></div>;
    }
    return this.props.children;
  }
}

export default function App(){
  const [scenario,setScenario]=useState('rain_runoff');
  const [scenarios,setScenarios]=useState([]);
  const [data,setData]=useState(null);
  const [segments,setSegments]=useState([]);
  const [tab,setTab]=useState('command');
  const [evidence,setEvidence]=useState(null);
  const [loading,setLoading]=useState(true);
  const [error,setError]=useState('');
  const [updated,setUpdated]=useState(null);
  const [demoMode,setDemoMode]=useState(false);
  const [notice,setNotice]=useState('');
  const [cityOpen,setCityOpen]=useState(false);
  const [city,setCity]=useState('dehradun');
  const [chatOpen,setChatOpen]=useState(false);
  const demoIndex=useRef(0);
  const requestId=useRef(0);
  const cityPickerRef=useRef(null);

  const load=async(id=scenario,full=false)=>{
    const currentRequest=++requestId.current;
    setLoading(true); setError('');
    try{
      const eventResponse=await fetch(`${API}/api/v1/intelligence/run?scenario=${encodeURIComponent(id)}`);
      if(!eventResponse.ok) throw new Error('Event API request failed');
      const d=await eventResponse.json();
      if(currentRequest!==requestId.current) return;
      setData(d); setScenario(id); setUpdated(new Date());
      if(full || !scenarios.length || !segments.length || !evidence){
        const responses=await Promise.all([
          fetch(`${API}/api/v1/intelligence/scenarios`),
          fetch(`${API}/api/v1/segments`),
          fetch(`${API}/api/v1/evidence/overview`)
        ]);
        if(responses.some(r=>!r.ok)) throw new Error('Supporting API request failed');
        const [s,g,ev]=await Promise.all(responses.map(r=>r.json()));
        if(currentRequest!==requestId.current) return;
        setScenarios(s.scenarios||[]); setSegments(g.segments||[]); setEvidence(ev);
      }
    }catch(e){
      if(currentRequest===requestId.current) setError('AquaPulse could not reach the local API. Start the backend on port 8000, then retry.');
    }finally{
      if(currentRequest===requestId.current) setLoading(false);
    }
  };

  useEffect(()=>{
    const hash=window.location.hash.replace('#','');
    if(['command','memory','hot','verify','evidence'].includes(hash)) setTab(hash);
    load('rain_runoff',true);
    const onHash=()=>{ const next=window.location.hash.replace('#',''); if(['command','memory','hot','verify','evidence'].includes(next)) setTab(next); };
    window.addEventListener('hashchange',onHash);
    return ()=>window.removeEventListener('hashchange',onHash);
  },[]);

  useEffect(()=>{
    if(!demoMode || scenarios.length<2) return;
    const timer=setInterval(()=>{
      demoIndex.current=(demoIndex.current+1)%scenarios.length;
      const next=scenarios[demoIndex.current]?.id;
      if(next) load(next);
    },6000);
    return ()=>clearInterval(timer);
  },[demoMode,scenarios]);

  useEffect(()=>{
    if(!cityOpen) return;
    const onPointerDown=(event)=>{ if(cityPickerRef.current && !cityPickerRef.current.contains(event.target)) setCityOpen(false); };
    const onKeyDown=(event)=>{ if(event.key==='Escape') setCityOpen(false); };
    document.addEventListener('pointerdown',onPointerDown);
    document.addEventListener('keydown',onKeyDown);
    return ()=>{document.removeEventListener('pointerdown',onPointerDown);document.removeEventListener('keydown',onKeyDown);};
  },[cityOpen]);

  const byId=useMemo(()=>Object.fromEntries(segments.map(s=>[s.id,s])),[segments]);
  const navigateTab=(id)=>{ setDemoMode(false); setNotice(''); setTab(id); window.location.hash=id; window.scrollTo({top:0,behavior:'smooth'}); };
  const selectCity=(id)=>{
    setCity(id); setCityOpen(false); setDemoMode(false); setChatOpen(false);
    setNotice(id==='dehradun'
      ? 'Dehradun is the current validated study area.'
      : 'Gurugram is available as a platform preview. Validated local freshwater datasets are not connected yet, so AquaPulse will not generate event intelligence for this city.');
    window.scrollTo({top:0,behavior:'smooth'});
  };
  const activeCity=CITIES[city]||CITIES.dehradun;
  const cityIsPreview=activeCity.mode==='preview';
  if(!data) return <div className="loading"><div className="brand"><span className="mark">≈</span><b>AquaPulse</b></div><p>{error||'Loading river intelligence…'}</p>{error&&<button className="primary-btn" onClick={()=>load('rain_runoff',true)}>Retry connection</button>}</div>;
  const e=data.event, m=meta[scenario]||meta.rain_runoff;
  const chooseScenario=(id)=>{ demoIndex.current=Math.max(0,scenarios.findIndex(s=>s.id===id)); load(id); };

  return <div className="app">
    <header>
      <div className="brand"><span className="mark">≈</span><div><b>AquaPulse</b><small>Freshwater Event Intelligence</small></div></div>
      <div className="header-right">
        <div className="city-picker" ref={cityPickerRef}>
          <button type="button" className="city-trigger" onClick={()=>setCityOpen(v=>!v)} aria-expanded={cityOpen} aria-haspopup="listbox" aria-label="Choose study area"><span className={`live-dot ${cityIsPreview?'preview-dot':''}`}/><span>{activeCity.label}</span><i className="city-chevron" aria-hidden="true"/></button>
          {cityOpen&&<div className="city-menu" role="listbox" aria-label="Choose study area">
            <button type="button" className={`city-option ${city==='dehradun'?'selected':''}`} onClick={()=>selectCity('dehradun')}><b>Dehradun</b><small>Validated prototype study area · Active intelligence</small></button>
            <button type="button" className={`city-option ${city==='gurugram'?'selected':''}`} onClick={()=>selectCity('gurugram')}><b>Gurugram (Gurgaon)</b><small>Platform preview · local datasets not connected</small></button>
          </div>}
        </div>
        <span className={`demo ${cityIsPreview?'preview-badge':''}`} title={cityIsPreview?'Gurugram is a preview city. No local event intelligence is generated until validated datasets are connected.':'The current event scenario is simulated for demonstration; contextual evidence remains labelled separately.'}>{cityIsPreview?'CITY PREVIEW · DATA NOT CONNECTED':'DEMO DATA · SIMULATED SIGNALS'}</span>
        <button type="button" className={`demo-toggle ${demoMode?'on':''}`} onClick={()=>{if(cityIsPreview){setNotice('Demo mode is available for the validated Dehradun study area only.');return;}setDemoMode(v=>!v);setNotice(demoMode?'Demo mode stopped':'Demo mode running — scenarios advance automatically')}}>{demoMode?'■ Stop demo':'▶ Run demo'}</button>
        <button type="button" className="refresh" title="Refresh the current intelligence view" onClick={()=>load()} disabled={loading||cityIsPreview}>{loading?'Updating…':cityIsPreview?'Preview mode':'↻ Refresh'}</button>
      </div>
    </header>
    <nav aria-label="AquaPulse sections">{TABS.map(([id,label])=><a href={`#${id}`} aria-current={tab===id?'page':undefined} className={tab===id?'active':''} onClick={()=>navigateTab(id)} key={id}>{label}</a>)}</nav>
    {notice&&<div className="demo-notice" onClick={()=>setNotice('')}>{notice}<span>×</span></div>}
    {loading&&<div className="updating-strip" aria-live="polite"><span/>Refreshing event intelligence from the prototype pipeline…</div>}
    <main>
      {cityIsPreview ? <CityPreview city={activeCity} onBack={()=>selectCity('dehradun')}/> : <>
        {tab==='command'&&<>
          <section className="hero"><div><p className="eyebrow">DEHRADUN · BINDAL / RISPANA · {m[0]}</p><h1>The river looks normal.<br/><em>Its memory disagrees.</em></h1><p className="lede">See the signal. Remember the pattern. Anticipate the next event.</p></div><div className={`hero-card ${m[1]}`}><span>EVENT CONFIDENCE</span><strong>{Math.round(e.confidence*100)}%</strong><small>{pretty(e.event_pattern)}</small><div className="hero-status">{e.potential_impact} potential impact · {e.evidence_quality} evidence quality</div></div></section>
          <section className="scenario-strip"><div><span className="eyebrow">DEMO SCENARIO</span><strong>Switch the event story</strong><small>High-frequency event signals are simulated for the prototype; CPCB and other contextual sources remain labelled by provenance.</small></div><div className="scenario-buttons">{scenarios.map(s=><button key={s.id} className={scenario===s.id?'selected':''} onClick={()=>chooseScenario(s.id)}>{s.name}</button>)}</div></section>
        </>}
        <div className="view-enter"><AppErrorBoundary key={tab}>{tab==='command'&&<Command data={data} segments={segments} scenario={scenario} refresh={()=>load()}/>} {tab==='memory'&&<Memory data={data}/>} {tab==='hot'&&<Hot data={data}/>} {tab==='verify'&&<Verify data={data} segments={byId}/>} {tab==='evidence'&&<Evidence evidence={evidence}/>}</AppErrorBoundary></div>
        <AquaPulseGuide data={data} evidence={evidence} open={chatOpen} onToggle={()=>setChatOpen(v=>!v)} />
      </>}
    </main>
    <footer><span>Observe → Detect → Remember → Predict → Prioritize → Verify → Learn</span><span>{updated?`Updated ${updated.toLocaleTimeString([], {hour:'2-digit',minute:'2-digit'})}`:'Provenance shown throughout'}</span></footer>
  </div>;
}

function CityPreview({city,onBack}){
  return <div className="city-preview">
    <div className="city-preview-copy">
      <p className="eyebrow">PLATFORM CITY PREVIEW</p>
      <h1>AquaPulse is ready to expand to {city.short}.</h1>
      <p>Gurugram is connected to the platform's city-selection layer, but its freshwater intelligence is intentionally not activated yet. AquaPulse will only generate event intelligence after validated local river, rainfall, environmental and historical datasets are connected.</p>
      <div className="city-preview-grid"><div><b>City</b><span>{city.short} · Haryana, India</span></div><div><b>Status</b><span>Preview only</span></div><div><b>Intelligence</b><span>Waiting for validated local data</span></div></div>
      <button className="primary-btn" type="button" onClick={onBack}>Return to Dehradun intelligence</button>
    </div>
    <div className="city-preview-map"><MapContainer center={city.center} zoom={city.zoom} scrollWheelZoom><MapResizer/><TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/><CircleMarker center={city.center} radius={10} pathOptions={{color:'#167c8a',fillColor:'#167c8a',fillOpacity:.2,weight:2}}><Popup><b>{city.short} preview</b><br/>Local AquaPulse datasets are not connected yet.</Popup></CircleMarker></MapContainer><div className="city-preview-map-label">{city.short} · geographic preview only</div></div>
  </div>;
}

function Command({data,segments,scenario,refresh}){
  const e=data.event,[reporting,setReporting]=useState(false),[sent,setSent]=useState(false),[reportError,setReportError]=useState(''),[lastReport,setLastReport]=useState(''),[custom,setCustom]=useState(''),mem=e.historical_matches?.[0]?.similarity||0;
  const send=async(cat)=>{setReporting(true);setReportError('');try{const r=await fetch(`${API}/api/v1/citizen-reports`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({segment_id:e.segment_id,category:cat,severity:.72,description:cat==='Other observation'?custom:'Prototype citizen observation'})});if(!r.ok)throw Error();setSent(true);setLastReport(cat);refresh();}catch(_){setSent(false);setReportError('Could not submit the observation. Check that the backend is running.')}finally{setReporting(false)}};
  return <>
    <section className="metrics"><Metric label="Event confidence" value={`${Math.round(e.confidence*100)}%`} hint="multi-signal evidence" tone={e.confidence>.8?'good':e.confidence>.55?'attention':'quiet'}/><Metric label="Potential impact" value={e.potential_impact} hint="not a health diagnosis"/><Metric label="Historical match" value={`${Math.round(mem*100)}%`} hint="River Memory"/><Metric label="Hot moment" value={`${Math.round(data.hot_moment*100)}%`} hint={data.hot_moment_window}/></section>
    <section className="grid"><div className="panel map-panel"><div className="panel-head"><div><h2>River intelligence map</h2><p>Event location, connected reaches and verification priorities</p></div><span className="chip">GEOSPATIAL DEMO</span></div><RiverMap segments={segments} targets={data.verification_targets} propagation={data.propagation} eventSegment={e.segment_id}/><div className="map-legend"><span><i className="legend-dot event"/>Current event</span><span><i className="legend-dot priority"/>Verification priority</span><span><i className="legend-line"/>Propagation path</span></div></div>
    <div className="stack"><div className="panel scenario-card"><div className="eyebrow">CURRENT EVENT · {scenario.toUpperCase()}</div><h2>{e.fingerprint.label}</h2><p>{e.fingerprint.description}</p><div className="fingerprint-score"><span>Fingerprint score</span><strong>{Math.round(e.fingerprint.score*100)}%</strong></div><div className="alternatives">{e.fingerprint.alternatives?.map(a=><span key={a.pattern}>{pretty(a.pattern)} · {Math.round(a.score*100)}%</span>)}</div></div>
    <Panel title="What the system sees" subtitle="Explainable evidence, not a black-box verdict"><ul className="evidence">{e.explanation.map((x,i)=><li key={i}>{x}</li>)}</ul></Panel>
    <div className="panel"><div className="panel-head compact"><div><h2>Evidence mix</h2><p>Each stream contributes independently.</p></div></div>{[['Rainfall signal','rainfall_signal'],['Water signal','water_quality_signal'],['Citizen signal','citizen_signal'],['Historical similarity','historical_similarity'],['Spatial coherence','spatial_coherence'],['Temporal coherence','temporal_coherence']].map(([l,k])=><Bar key={k} label={l} v={e.evidence[k]}/>)}</div>
    <div className="panel citizen"><div className="panel-head compact"><div><h2>Citizen observation</h2><p>Field reports add a human evidence stream.</p></div></div><div className="report-buttons">{['Unusual colour','Foam','Odour','Dead fish / insects','Oil sheen','Sewage smell','Floating waste','Algae / green water'].map(x=><button disabled={reporting} onClick={()=>send(x)} key={x}>{x}</button>)}</div><div className="custom-report"><input value={custom} onChange={e=>setCustom(e.target.value)} placeholder="Describe another observation…" aria-label="Describe another observation"/><button disabled={reporting||!custom.trim()} onClick={()=>send('Other observation')}>Report</button></div>{sent&&<div className="sent">✓ {lastReport} observation added. Intelligence refreshed.</div>}{reportError&&<div className="action-error">{reportError}</div>}</div></div></section><Timeline data={data}/><ReasoningPanel data={data}/><OneHealthPanel/></>;
}
function Timeline({data}){const e=data.event,steps=[['01','Observe',e.evidence.rainfall_signal>=.6?'Elevated rainfall signal enters the event window.':'Rainfall signal is limited.'],['02','Detect',e.evidence.water_quality_signal>=.45?'Environmental signal provides independent corroboration.':'No strong environmental corroboration yet.'],['03','Remember',e.historical_matches?.[0]?`Closest memory match: ${pretty(e.historical_matches[0].event_pattern)}.`:'No useful historical match.'],['04','Predict',data.propagation?.length?`${data.propagation.length} downstream candidates projected.`:'No downstream projection.'],['05','Prioritize',`${data.verification_targets?.length||0} locations ranked for human verification.`]];return <section className="timeline-panel"><div className="section-head"><div><p className="eyebrow">EVENT INTELLIGENCE LOOP</p><h2>From signal to field action</h2></div><span className="method-note">Rule-based prototype · explainable by design</span></div><div className="timeline">{steps.map(([n,t,x],i)=><div className="timeline-step" key={t}><div className="timeline-node">{n}</div><strong>{t}</strong><p>{x}</p>{i<4&&<i className="timeline-connector"/>}</div>)}</div></section>}
function ReasoningPanel({data}){const e=data.event;const signals=[['RAIN',e.evidence.rainfall_signal],['WATER',e.evidence.water_quality_signal],['CITIZEN',e.evidence.citizen_signal],['MEMORY',e.evidence.historical_similarity],['SPACE',e.evidence.spatial_coherence],['TIME',e.evidence.temporal_coherence]];return <section className="reasoning-panel"><div><p className="eyebrow">HOW AQUAPULSE REASONS</p><h2>Multiple weak signals become one explainable event hypothesis.</h2><p>Signals are fused with negative evidence and temporal/spatial checks. The output is a prioritization aid — not an autonomous pollution verdict.</p></div><div className="reasoning-flow"><div className="signal-row">{signals.map(([label,value])=><div className="signal-chip" key={label}><span>{label}</span><b>{Math.round(value*100)}%</b></div>)}</div><div className="reasoning-arrow">↓</div><div className="reasoning-result"><span>EVENT HYPOTHESIS</span><strong>{pretty(e.event_pattern)}</strong><small>{Math.round(e.confidence*100)}% confidence · {e.evidence_quality} evidence quality</small></div><div className="reasoning-arrow">↓</div><div className="reasoning-result priority"><span>FIELD ACTION</span><strong>Verification priority</strong><small>Human review remains the final decision step.</small></div></div></section>}
function OneHealthPanel(){return <section className="one-health"><div className="section-head"><div><p className="eyebrow">ONE HEALTH CONNECTION</p><h2>Why freshwater signals matter beyond the river.</h2></div><span className="method-note">Decision support · not a health diagnosis</span></div><div className="one-health-grid"><div><span>01</span><h3>Ecosystem health</h3><p>Surface environmental stress, recurrence and vulnerable reaches can be surfaced earlier for investigation and stewardship.</p></div><div><span>02</span><h3>Community awareness</h3><p>Citizen observations turn local experience into structured evidence without pretending every report is ground truth.</p></div><div><span>03</span><h3>Human & animal well-being</h3><p>Environmental risk signals can inform where qualified teams should verify conditions that may matter to communities and wildlife.</p></div></div></section>} 

function Metric({label,value,hint,tone=''}){return <div className={`metric ${tone}`}><span>{label}</span><strong>{value}</strong><small>{hint}</small></div>}
function Bar({label,v=0}){return <div className="bar"><div><span>{label}</span><b>{Math.round(v*100)}%</b></div><i><u style={{width:`${Math.max(0,Math.min(1,v))*100}%`}}/></i></div>}
function Panel({title,subtitle,children}){return <div className="panel"><div className="panel-head compact"><div><h2>{title}</h2>{subtitle&&<p>{subtitle}</p>}</div></div>{children}</div>}
function RiverMap({segments,targets,propagation,eventSegment}){const tm=Object.fromEntries((targets||[]).map(t=>[t.segment_id,t.priority])),sm=Object.fromEntries(segments.map(s=>[s.id,s]));return <div className="map"><MapContainer center={[30.268,78.032]} zoom={12.8} scrollWheelZoom><Fit center={[30.268,78.032]} zoom={12.8}/><MapResizer/><TileLayer attribution="&copy; OpenStreetMap contributors" url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>{links.map(([a,b])=>sm[a]&&sm[b]&&<Polyline key={a+b} positions={[[sm[a].lat,sm[a].lon],[sm[b].lat,sm[b].lon]]} pathOptions={{color:'#78a7a7',weight:3,opacity:.65,dashArray:'5 7'}}/>)}{(propagation||[]).map(p=>sm[p.segment_id]&&sm[eventSegment]&&<Polyline key={'p'+p.segment_id} positions={[[sm[eventSegment].lat,sm[eventSegment].lon],[sm[p.segment_id].lat,sm[p.segment_id].lon]]} pathOptions={{color:'#d99a35',weight:5,opacity:.75}}/>)}{segments.map(s=>{const p=tm[s.id]||0,ev=s.id===eventSegment,color=ev?'#d56550':p>.85?'#d56550':p?'#d99a35':'#167c8a';return <CircleMarker key={s.id} center={[s.lat,s.lon]} radius={ev?11:p?9:6} pathOptions={{color,fillColor:color,fillOpacity:.78,weight:ev?3:2}}><Popup><b>{s.name}</b><br/>{s.river}<br/>Vulnerability: {Math.round(s.vulnerability*100)}%{ev&&<><br/><br/><b>Current event location</b></>}{p>0&&<><br/><br/><b>Verification priority: {Math.round(p*100)}%</b></>}</Popup></CircleMarker>})}</MapContainer></div>}
function Memory({data}){const ms=data.event.historical_matches||[];return <div className="wide"><div className="section-title"><p className="eyebrow">RIVER MEMORY™</p><h2>What has the river seen before?</h2><p>Current features are compared with the prototype historical event library. Similarity is evidence for investigation, not proof of cause.</p></div><div className="memory-summary"><strong>{ms.length?Math.round(ms[0].similarity*100):0}%</strong><div><b>Closest historical resemblance</b><span>{ms[0]?pretty(ms[0].event_pattern):'No match'}</span></div></div><div className="cards">{ms.map((m,i)=><div className="memory-card" key={m.event_id}><span>#{i+1} MATCH · {m.event_id}</span><h3>{pretty(m.event_pattern)}</h3><strong>{Math.round(m.similarity*100)}%</strong><p>{m.segment_id} · cosine similarity across event features</p><div className="memory-line"><i style={{width:`${m.similarity*100}%`}}/></div></div>)}</div><div className="provenance-note"><b>Memory provenance:</b> simulated event library in this prototype. Validated historical event records can replace it later.</div></div>}
function Hot({data}){return <div className="wide"><div className="section-title"><p className="eyebrow">HOT MOMENT INTELLIGENCE</p><h2>Find the vulnerable window before it becomes obvious.</h2><p>AquaPulse estimates environmental vulnerability from triggers, susceptibility, recurrence and current warning signals — not future pollution as a certainty.</p></div><div className="hot-grid"><div className="dial"><span>HOT MOMENT SCORE</span><strong>{Math.round(data.hot_moment*100)}%</strong><small>{data.hot_moment_window}</small><div className="dial-ring"><i style={{transform:`rotate(${data.hot_moment*270-135}deg)`}}/></div></div><div className="panel"><h2>Drivers</h2>{data.hot_moment_drivers.map((d,i)=><div className="driver" key={d}><span>0{i+1}</span>{d}</div>)}<div className="small-callout">Interpretation: vulnerability window for prioritization, not a prediction of contamination.</div></div></div></div>}
function Evidence({evidence}){if(!evidence)return <div className="wide"><div className="panel"><p>Loading evidence registry…</p></div></div>;return <div className="wide"><div className="section-title"><p className="eyebrow">EVIDENCE & PROVENANCE</p><h2>Know what is real, derived, and simulated.</h2><p>AquaPulse keeps source provenance visible so the intelligence layer can be evaluated without confusing contextual evidence for live telemetry.</p></div><div className="source-grid">{evidence.sources.map(s=><div className="source-card" key={s.id}><div className="source-top"><span className={`source-badge ${s.type}`}>{s.type.toUpperCase()}</span><span className="source-status">{s.status}</span></div><h3>{s.name}</h3><p>{s.role}</p><small>{s.limitation}</small></div>)}</div><div className="grid evidence-grid"><div className="panel"><div className="panel-head compact"><div><h2>CPCB contextual evidence</h2><p>{evidence.cpcb.record_count} normalized observations · {evidence.cpcb.contextual_baselines} contextual baselines</p></div></div><div className="evidence-table">{evidence.cpcb.highlights.slice(0,8).map(r=><div className="evidence-row" key={r.observation_id}><span>{r.segment_name}</span><span>{r.parameter}</span><b>{r.value} {r.unit}</b><small>{r.season} {r.date}</small></div>)}</div><div className="small-callout">These are official contextual observations, not continuous measurements of the current event.</div></div><div className="panel"><div className="panel-head compact"><div><h2>Interpretation rules</h2><p>Guardrails used by the prototype.</p></div></div><ul className="evidence">{evidence.interpretation_rules.map((x,i)=><li key={i}>{x}</li>)}</ul></div></div></div>}
function AquaPulseGuide({data,evidence,open,onToggle}){
  const e=data?.event;
  const [messages,setMessages]=useState([{role:'bot',text:'Hi — I’m AquaPulse Guide. I can explain the current event, evidence, River Memory, Hot Moments, or what a field verifier should check next.'}]);
  const [input,setInput]=useState('');
  const answer=(raw)=>{
    const q=raw.toLowerCase().trim(); if(!q) return;
    let text='';
    const targets=data?.verification_targets||[];
    const top=targets[0];
    if(/what.*happen|current event|what.*see|status/.test(q)) text=`Current event: ${pretty(e.event_pattern)} at ${e.segment_id}. Event confidence is ${Math.round(e.confidence*100)}%, with ${e.potential_impact} potential impact and ${e.evidence_quality} evidence quality. This is an event hypothesis for investigation, not proof of pollution or a health diagnosis.`;
    else if(/why|reason|evidence|signal/.test(q)) text=`AquaPulse is combining rainfall (${Math.round(e.evidence.rainfall_signal*100)}%), water signal (${Math.round(e.evidence.water_quality_signal*100)}%), citizen observations (${Math.round(e.evidence.citizen_signal*100)}%), historical similarity (${Math.round(e.evidence.historical_similarity*100)}%), spatial coherence (${Math.round(e.evidence.spatial_coherence*100)}%) and temporal coherence (${Math.round(e.evidence.temporal_coherence*100)}%). Negative evidence can reduce confidence.`;
    else if(/where|look|verify|investigat|priority/.test(q)) text=top?`Start with ${top.segment_id}. It currently has ${Math.round(top.priority*100)}% verification priority. ${top.reasons.join(' ')}`:'No verification target is available yet.';
    else if(/memory|histor/.test(q)) text=`River Memory compares the current event feature fingerprint with the prototype historical event library. The closest match is ${e.historical_matches?.[0]?pretty(e.historical_matches[0].event_pattern):'not available'} at ${e.historical_matches?.[0]?Math.round(e.historical_matches[0].similarity*100):0}% similarity. Similarity supports investigation; it does not prove cause.`;
    else if(/hot moment|hot window|vulnerab/.test(q)) text=`The current Hot Moment score is ${Math.round(data.hot_moment*100)}% for ${data.hot_moment_window}. It represents a vulnerability/prioritization window, not a certainty that contamination will occur.`;
    else if(/real data|source|cpcb|nasa|sentinel|provenance/.test(q)) text=evidence?`The evidence registry separates REAL, DERIVED and SIMULATED inputs. CPCB records are real contextual observations; the high-frequency event scenarios and prototype historical library are simulated. NASA IMERG and Sentinel-2 are registered as contextual external sources rather than fabricated live values.`:'Open Evidence to inspect the provenance registry.';
    else if(/one health/.test(q)) text='One Health connects ecosystem, animal and human well-being. AquaPulse uses environmental signals and citizen observations to support earlier ecosystem investigation while keeping health conclusions with qualified professionals.';
    else if(/pollution|toxic|safe|health|drink|disease/.test(q)) text=`AquaPulse does not determine whether water is safe to drink, diagnose illness, or declare pollution from this prototype. It surfaces an environmental event hypothesis and tells a qualified human where to investigate first.`;
    else if(/ai|machine learning|model/.test(q)) text='This submission uses an explainable rule-based intelligence prototype rather than pretending a black-box model is already trained. The architecture leaves room for validated ML models later, while keeping human verification in the loop.';
    else if(/help|what can you|questions/.test(q)) text='Try: “What is happening?”, “Why is confidence high?”, “Where should I verify?”, “What is River Memory?”, “What data is real?”, or “Is this pollution?”';
    else text='I can explain the current event, evidence mix, River Memory, Hot Moments, verification priorities, data provenance, One Health connection, or the prototype AI approach.';
    setMessages(m=>[...m,{role:'user',text:raw},{role:'bot',text}]); setInput('');
  };
  const quick=['What is happening?','Why?','Where should I verify?','What data is real?'];
  return <>
    <button className={`guide-fab ${open?'open':''}`} onClick={onToggle} aria-expanded={open} aria-label="Open AquaPulse Guide"><span>✦</span>{open?'Close Guide':'AquaPulse Guide'}</button>
    {open&&<aside className="guide-panel" aria-label="AquaPulse Guide chatbot">
      <div className="guide-head"><div><p className="eyebrow">AQUAPULSE GUIDE</p><h2>Ask the river intelligence.</h2><small>Evidence-aware prototype assistant · no health diagnosis</small></div><button onClick={onToggle} aria-label="Close chatbot">×</button></div>
      <div className="guide-quick">{quick.map(q=><button key={q} onClick={()=>answer(q)}>{q}</button>)}</div>
      <div className="guide-messages">{messages.map((m,i)=><div className={`guide-message ${m.role}`} key={i}>{m.text}</div>)}</div>
      <form className="guide-input" onSubmit={ev=>{ev.preventDefault();answer(input)}}><input value={input} onChange={ev=>setInput(ev.target.value)} placeholder="Ask about this event…" aria-label="Ask AquaPulse Guide"/><button disabled={!input.trim()}>Send</button></form>
    </aside>}
  </>;
}

function Verify({data,segments}){const [busy,setBusy]=useState(''),[done,setDone]=useState({}),[actionError,setActionError]=useState('');const review=async(id,status)=>{setBusy(id+status);setActionError('');try{const r=await fetch(`${API}/api/v1/verification`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({status,note:`Prototype review for ${id}`,segment_id:id,event_id:data.event.event_id})});if(!r.ok)throw Error();setDone(x=>({...x,[id]:status}));}catch(_){setActionError('Could not save the verification action. Check that the backend is running.')}finally{setBusy('')}};return <div className="wide"><div className="section-title"><p className="eyebrow">VERIFICATION CENTRE</p><h2>If you can investigate only three places, start here.</h2><p>Priorities combine event confidence, potential impact, information value and recurrence. The final call stays with a human verifier.</p></div>{actionError&&<div className="action-error">{actionError}</div>}<div className="verify-list">{data.verification_targets.map((t,i)=><div className="verify-row" key={t.segment_id}><span className="rank">0{i+1}</span><div><h3>{segments[t.segment_id]?.name||t.segment_id}</h3><p>{t.reasons.join(' · ')}</p>{done[t.segment_id]&&<span className="reviewed">✓ Marked {done[t.segment_id].replace('_',' ')}</span>}</div><strong>{Math.round(t.priority*100)}<small> priority</small></strong><div className="review-actions"><button disabled={!!busy} onClick={()=>review(t.segment_id,'confirmed')}>Confirm</button><button disabled={!!busy} onClick={()=>review(t.segment_id,'insufficient_evidence')}>Needs evidence</button></div></div>)}</div></div>}
