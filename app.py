from __future__ import annotations

from pathlib import Path
from typing import Any

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse

from src.evidence_model import load_evidence, load_scenarios, score_markets
from src.nova_readiness_v3 import load_nodes, queue_scenario, verify_project_scores
from src.site_pathway_v4 import required_delivery_points, score_pathways
from src.utility_model_v2 import (
    Scenario,
    comed_high_voltage_core_delivery_proxy,
    dominion_gs5_obligations,
    oncor_transmission_core_delivery_proxy,
)

ROOT = Path(__file__).resolve().parent

app = FastAPI(
    title="Speed-to-Power",
    description="U.S. Data Center Energy Readiness & Interconnection Risk",
    version="4.0.0",
)


def _records(df: pd.DataFrame) -> list[dict[str, Any]]:
    clean = df.copy()
    clean = clean.astype(object).where(pd.notna(clean), None)
    return clean.to_dict(orient="records")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "4.0.0"}


@app.get("/api/v4")
def v4(
    load_mw: int = Query(300, ge=100, le=500),
    target_year: int = Query(2029, ge=2026, le=2032),
) -> dict[str, Any]:
    scored = score_pathways(load_mw, target_year)
    precedents = scored[scored["technical_pathway_score"].notna()].sort_values(
        "technical_pathway_score", ascending=False
    )
    corridors = scored[scored["technical_pathway_score"].isna()]
    landuse = pd.read_csv(ROOT / "data" / "loudoun_landuse_v4.csv")
    return {
        "scenario": {
            "load_mw": load_mw,
            "target_year": target_year,
            "minimum_delivery_points": required_delivery_points(load_mw),
        },
        "precedents": _records(precedents),
        "corridors": _records(corridors),
        "land_use": _records(landuse),
    }


@app.get("/api/v3")
def v3(load_mw: int = Query(300, ge=100, le=500)) -> dict[str, Any]:
    projects = verify_project_scores().sort_values("tdri_score", ascending=False)
    nodes = load_nodes()
    return {
        "queue": queue_scenario(load_mw),
        "queue_context": {
            "requests_with_connection_dates_mw": 25000,
            "requests_in_study_batches_mw": 45000,
            "total_advancing_mw": 70000,
            "dominion_zone_peak_mw": 24678,
        },
        "nodes": _records(nodes),
        "projects": _records(projects),
    }


@app.get("/api/v2")
def v2(
    load_mw: int = Query(300, ge=100, le=500),
    load_factor: float = Query(0.90, ge=0.50, le=1.00),
    four_cp_factor: float = Query(0.90, ge=0.40, le=1.00),
    comed_demand_factor: float = Query(1.00, ge=0.50, le=1.00),
    dominion_credit_reduction_pct: float = Query(0.0, ge=0.0, le=70.0),
) -> dict[str, Any]:
    scenario = Scenario(load_mw=load_mw, load_factor=load_factor)
    oncor = oncor_transmission_core_delivery_proxy(
        scenario, four_cp_factor=four_cp_factor
    )
    comed = comed_high_voltage_core_delivery_proxy(
        scenario, billing_demand_factor=comed_demand_factor
    )
    dominion = dominion_gs5_obligations(
        scenario, credit_reduction_pct=dominion_credit_reduction_pct
    )
    return {
        "scenario": {
            "load_mw": load_mw,
            "load_factor": load_factor,
            "annual_mwh": scenario.annual_mwh,
        },
        "oncor": oncor,
        "comed": comed,
        "dominion": dominion,
    }


@app.get("/api/v1")
def v1(profile: str = "balanced") -> dict[str, Any]:
    scenarios = load_scenarios()
    if profile not in scenarios:
        profile = "balanced"
    scored = score_markets(load_evidence(), scenarios[profile]).sort_values(
        "screening_score", ascending=False
    )
    return {
        "profile": profile,
        "weights": scenarios[profile],
        "markets": _records(scored),
    }


HOME_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Speed-to-Power</title>
<style>
:root{--bg:#07101d;--panel:#0d1a2b;--panel2:#102238;--text:#e8eef7;--muted:#9eb0c5;--line:#20354e;--accent:#67b7ff;--good:#7ee0a3;--warn:#ffd479}
*{box-sizing:border-box} body{margin:0;background:linear-gradient(180deg,#07101d,#091625 45%,#07101d);color:var(--text);font:15px/1.5 Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
.wrap{max-width:1180px;margin:auto;padding:28px 20px 70px}.hero{padding:30px 0 20px}.kicker{color:var(--accent);font-size:12px;font-weight:800;letter-spacing:.13em;text-transform:uppercase}
h1{font-size:clamp(34px,6vw,66px);line-height:1.02;margin:8px 0 14px;letter-spacing:-.04em}h2{font-size:26px;margin:0 0 14px}h3{font-size:17px;margin:0 0 10px}.lede{max-width:820px;color:var(--muted);font-size:18px}
.nav{display:flex;gap:8px;flex-wrap:wrap;margin:22px 0}.nav a{color:var(--text);text-decoration:none;border:1px solid var(--line);padding:8px 12px;border-radius:999px;background:#0b1726}
.section{margin-top:28px;padding:24px;border:1px solid var(--line);border-radius:18px;background:rgba(13,26,43,.94);box-shadow:0 16px 48px rgba(0,0,0,.18)}
.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px}.grid4{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:14px}
.card{background:var(--panel2);border:1px solid var(--line);border-radius:14px;padding:16px}.metric{font-size:28px;font-weight:800;letter-spacing:-.03em}.label{color:var(--muted);font-size:12px;text-transform:uppercase;letter-spacing:.08em}
.controls{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:14px 0 18px}.control label{display:block;color:var(--muted);font-size:12px;margin-bottom:6px}.control input,.control select{width:100%;background:#07111f;color:var(--text);border:1px solid var(--line);border-radius:10px;padding:10px}
table{width:100%;border-collapse:collapse;margin-top:12px;font-size:13px}th,td{text-align:left;border-bottom:1px solid var(--line);padding:10px 8px;vertical-align:top}th{color:var(--muted);font-weight:600}
.bar{height:8px;background:#07111f;border-radius:999px;overflow:hidden;margin-top:6px}.bar span{display:block;height:100%;background:linear-gradient(90deg,var(--accent),var(--good))}
.note{color:var(--muted);font-size:13px;margin-top:10px}.warning{padding:12px 14px;border-left:3px solid var(--warn);background:#2a2315;color:#f9e9bd;border-radius:8px;margin-top:14px}
.footer{color:var(--muted);font-size:12px;margin-top:28px}.pill{display:inline-block;border:1px solid var(--line);padding:4px 8px;border-radius:999px;color:var(--muted);font-size:12px}
@media(max-width:850px){.grid,.grid4,.controls{grid-template-columns:1fr}.section{padding:18px}}
</style>
</head>
<body>
<div class="wrap">
  <div class="hero">
    <div class="kicker">Energy infrastructure research</div>
    <h1>Speed-to-Power</h1>
    <div class="lede">A multi-layer framework for screening large-load energy readiness, utility economics, transmission development, and Northern Virginia candidate pathways.</div>
    <div class="nav">
      <a href="#v4">Candidate Pathways V4</a><a href="#v3">Northern Virginia V3</a><a href="#v2">Utility V2</a><a href="#v1">Regional V1</a>
    </div>
  </div>

  <section class="section" id="v4">
    <span class="pill">V4</span><h2>Candidate development pathways</h2>
    <div class="controls">
      <div class="control"><label>Scenario campus load (MW)</label><input id="v4load" type="range" min="100" max="500" step="25" value="300"><div id="v4loadval">300 MW</div></div>
      <div class="control"><label>Target full service year</label><select id="v4year"><option >2026</option><option >2027</option><option >2028</option><option selected>2029</option><option >2030</option><option >2031</option><option >2032</option></select></div>
      <div class="card"><div class="label">Minimum delivery points</div><div class="metric" id="v4dp">1</div></div>
    </div>
    <div id="v4cards" class="grid"></div>
    <div class="warning">Technical pathway evidence is not spare substation capacity, parcel availability, or a guaranteed energization date. Land-use entitlement is a separate gate.</div>
    <h3 style="margin-top:20px">Future corridor evidence</h3><div id="v4corridors"></div>
  </section>

  <section class="section" id="v3">
    <span class="pill">V3</span><h2>Northern Virginia transmission development</h2>
    <div id="v3metrics" class="grid4"></div>
    <h3 style="margin-top:20px">Transmission Development Readiness Index</h3>
    <div id="v3projects"></div>
  </section>

  <section class="section" id="v2">
    <span class="pill">V2</span><h2>Utility-level economics</h2>
    <div class="controls">
      <div class="control"><label>Facility load (MW)</label><input id="v2load" type="range" min="100" max="500" step="25" value="300"><div id="v2loadval">300 MW</div></div>
      <div class="control"><label>Load factor</label><input id="v2lf" type="range" min="0.75" max="1" step="0.01" value="0.90"><div id="v2lfval">90%</div></div>
      <div class="control"><label>Oncor 4CP exposure</label><input id="v24cp" type="range" min="0.40" max="1" step="0.05" value="0.90"><div id="v24cpval">90%</div></div>
    </div>
    <div id="v2cards" class="grid"></div>
    <div class="note">Oncor and ComEd figures are core delivery proxies. Dominion displays GS-5 contractual exposure rather than an equivalent annual delivery bill.</div>
  </section>

  <section class="section" id="v1">
    <span class="pill">V1</span><h2>Regional market screening</h2>
    <div class="control" style="max-width:340px"><label>Decision profile</label><select id="v1profile"><option>balanced</option><option>speed_first</option><option>cost_first</option><option>reliability_first</option></select></div>
    <div id="v1markets"></div>
  </section>

  <div class="footer">Source-backed screening model. Public evidence is kept separate from non-public capacity and project-specific engineering conclusions.</div>
</div>
<script>
const fmtM=n=>'$'+(n/1e6).toFixed(2)+'M';
const pct=n=>Math.round(n*100)+'%';
const num=n=>Number(n).toLocaleString(undefined,{maximumFractionDigits:1});

async function loadV4(){
  const load=document.getElementById('v4load').value, year=document.getElementById('v4year').value;
  document.getElementById('v4loadval').textContent=load+' MW';
  const d=await fetch('/api/v4?load_mw='+load+'&target_year='+year).then(r=>r.json());
  document.getElementById('v4dp').textContent=d.scenario.minimum_delivery_points;
  document.getElementById('v4cards').innerHTML=d.precedents.map(x=>`
    <div class="card"><div class="label">${x.pathway_name}</div><div class="metric">${num(x.technical_pathway_score)}</div>
    <div class="bar"><span style="width:${x.technical_pathway_score}%"></span></div>
    <div class="note">${num(x.documented_load_mw)} MW documented · ${x.documented_delivery_points} DP · target ${x.latest_target}</div></div>`).join('');
  document.getElementById('v4corridors').innerHTML='<table><tr><th>Corridor</th><th>Area</th><th>Target</th><th>TDRI</th></tr>'+
    d.corridors.map(x=>`<tr><td>${x.pathway_name}</td><td>${x.area_context}</td><td>${x.latest_target||'—'}</td><td>${x.direct_project_tdri||'—'}</td></tr>`).join('')+'</table>';
}
async function loadV3(){
  const d=await fetch('/api/v3?load_mw=300').then(r=>r.json());
  const q=d.queue_context;
  document.getElementById('v3metrics').innerHTML=[
    ['Queue with dates',num(q.requests_with_connection_dates_mw)+' MW'],
    ['In study batches',num(q.requests_in_study_batches_mw)+' MW'],
    ['Total advancing',num(q.total_advancing_mw)+' MW'],
    ['Zone peak cited',num(q.dominion_zone_peak_mw)+' MW']
  ].map(x=>`<div class="card"><div class="label">${x[0]}</div><div class="metric">${x[1]}</div></div>`).join('');
  document.getElementById('v3projects').innerHTML='<table><tr><th>Project</th><th>Voltage</th><th>Stage</th><th>TDRI</th></tr>'+
    d.projects.map(x=>`<tr><td>${x.project}</td><td>${x.voltage_kv}</td><td>${x.development_stage}</td><td>${x.tdri_score}</td></tr>`).join('')+'</table>';
}
async function loadV2(){
  const load=document.getElementById('v2load').value, lf=document.getElementById('v2lf').value, cp=document.getElementById('v24cp').value;
  document.getElementById('v2loadval').textContent=load+' MW'; document.getElementById('v2lfval').textContent=pct(lf); document.getElementById('v24cpval').textContent=pct(cp);
  const d=await fetch('/api/v2?load_mw='+load+'&load_factor='+lf+'&four_cp_factor='+cp).then(r=>r.json());
  document.getElementById('v2cards').innerHTML=`
    <div class="card"><div class="label">Oncor / ERCOT</div><div class="metric">${fmtM(d.oncor.annual_usd)}/yr</div><div class="note">Core delivery proxy · $${d.oncor.usd_per_mwh.toFixed(2)}/MWh</div></div>
    <div class="card"><div class="label">ComEd / PJM</div><div class="metric">${fmtM(d.comed.annual_usd)}/yr</div><div class="note">Core delivery proxy · $${d.comed.usd_per_mwh.toFixed(2)}/MWh</div></div>
    <div class="card"><div class="label">Dominion / PJM</div><div class="metric">${fmtM(d.dominion.net_collateral_usd)}</div><div class="note">GS-5 collateral exposure · ${num(d.dominion.minimum_transmission_demand_mw)} MW transmission floor</div></div>`;
}
async function loadV1(){
  const p=document.getElementById('v1profile').value;
  const d=await fetch('/api/v1?profile='+p).then(r=>r.json());
  document.getElementById('v1markets').innerHTML='<table><tr><th>Market</th><th>Score</th><th>Resource adequacy</th><th>Cost</th><th>Process maturity</th></tr>'+
    d.markets.map(x=>`<tr><td>${x.market}</td><td>${x.screening_score}</td><td>${x.resource_adequacy_score.toFixed(1)}</td><td>${x.cost_score.toFixed(1)}</td><td>${x.large_load_process_maturity_score}</td></tr>`).join('')+'</table>';
}
['v4load','v4year'].forEach(id=>document.getElementById(id).addEventListener('input',loadV4));
['v2load','v2lf','v24cp'].forEach(id=>document.getElementById(id).addEventListener('input',loadV2));
document.getElementById('v1profile').addEventListener('change',loadV1);
Promise.all([loadV4(),loadV3(),loadV2(),loadV1()]);
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return HOME_HTML
