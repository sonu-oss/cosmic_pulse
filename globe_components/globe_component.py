"""
Cyber-tech 3D Globe Component for Streamlit
============================================
Drop-in replacement for a 2D Plotly orthographic globe.

Renders an interactive (rotate / zoom / pan) 3D Earth using globe.gl
(Three.js + WebGL) inside a Streamlit app via st.components.v1.html.

Features
--------
- True 3D globe with atmosphere glow, starfield, dark cyber Earth texture
- Multiple satellites as glowing points + pulsing rings
- Animated dashed ground tracks (orbit paths) at altitude
- Floating HUD: live UTC clock + selected-satellite lat/lon/alt
- Auto-rotate (toggleable) and click-to-focus a satellite
- Pure HTML/JS payload -> works on Streamlit Cloud, no extra pip install

Usage
-----
    import streamlit as st
    from globe_component import render_satellite_globe

    render_satellite_globe(
        satellites=[
            {"name": "ISS",       "lat": 45.51, "lon": -40.43, "alt_km": 408, "color": "#00e5ff"},
            {"name": "HUBBLE",    "lat": 12.7,  "lon":  77.5,  "alt_km": 540, "color": "#ff3df0"},
        ],
        ground_tracks=[
            {"name": "ISS",    "points": iss_track_points,    "color": "#00e5ff"},
            {"name": "HUBBLE", "points": hubble_track_points, "color": "#ff3df0"},
        ],
        height=720,
        auto_rotate=True,
    )

`points` is a list of (lat, lon) tuples (or [lat, lon] lists).
"""

from __future__ import annotations

import json
from typing import Iterable, List, Sequence, Tuple, Union

import streamlit.components.v1 as components

LatLon = Union[Tuple[float, float], List[float]]


# ---------- public API -------------------------------------------------------

def render_satellite_globe(
    satellites: Sequence[dict] | None = None,
    ground_tracks: Sequence[dict] | None = None,
    *,
    height: int = 700,
    auto_rotate: bool = True,
    auto_rotate_speed: float = 0.35,
    show_hud: bool = True,
    accent_color: str = "#00e5ff",
    background_color: str = "#03060d",
):
    """Render the cyber 3D globe inside the current Streamlit container.

    Parameters
    ----------
    satellites : list[dict]
        Each dict: {name, lat, lon, alt_km (optional), color (optional)}
    ground_tracks : list[dict]
        Each dict: {name, points: [(lat, lon), ...], color, alt_km (optional)}
    height : int
        Canvas height in pixels.
    auto_rotate : bool
        Whether the globe slowly auto-rotates on load.
    auto_rotate_speed : float
        OrbitControls auto-rotate speed.
    show_hud : bool
        Whether to overlay the cyber HUD (clock + selected sat info).
    accent_color : str
        Primary cyber accent (atmosphere, HUD borders).
    background_color : str
        Canvas background (set very dark for the cyber look).
    """
    sats = _normalize_satellites(satellites or [])
    tracks = _normalize_tracks(ground_tracks or [], default_color=accent_color)

    payload = {
        "satellites": sats,
        "tracks": tracks,
        "autoRotate": bool(auto_rotate),
        "autoRotateSpeed": float(auto_rotate_speed),
        "showHud": bool(show_hud),
        "accent": accent_color,
        "bg": background_color,
    }

    components.html(_build_html(payload, height), height=height + 4, scrolling=False)


# ---------- helpers ----------------------------------------------------------

def _normalize_satellites(sats: Iterable[dict]) -> List[dict]:
    out = []
    for s in sats:
        out.append({
            "name": str(s.get("name", "SAT")),
            "lat": float(s["lat"]),
            "lon": float(s["lon"]),
            "alt_km": float(s.get("alt_km", 408)),
            "color": s.get("color", "#00e5ff"),
        })
    return out


def _normalize_tracks(tracks: Iterable[dict], default_color: str) -> List[dict]:
    out = []
    for t in tracks:
        pts = []
        for p in t.get("points", []):
            if len(p) >= 2:
                pts.append([float(p[0]), float(p[1])])
        out.append({
            "name": str(t.get("name", "TRACK")),
            "points": pts,
            "color": t.get("color", default_color),
            "alt_km": float(t.get("alt_km", 408)),
        })
    return out


# ---------- HTML/JS payload --------------------------------------------------

def _build_html(payload: dict, height: int) -> str:
    data_json = json.dumps(payload)
    return _TEMPLATE.replace("__DATA_JSON__", data_json).replace("__HEIGHT__", str(height))


_TEMPLATE = r"""
<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<style>
  :root {
    --accent: #00e5ff;
    --accent-soft: rgba(0, 229, 255, 0.18);
    --bg: #03060d;
    --grid: rgba(0, 229, 255, 0.07);
    --text: #d6f3ff;
    --muted: #6e8ba0;
  }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--text);
    font-family: 'JetBrains Mono', 'IBM Plex Mono', ui-monospace, Menlo, Consolas, monospace;
    overflow: hidden; }
  #wrap { position: relative; width: 100%; height: __HEIGHT__px;
    background:
      radial-gradient(ellipse at 50% 50%, #06121f 0%, #02050b 70%, #000 100%),
      linear-gradient(var(--grid) 1px, transparent 1px) 0 0 / 40px 40px,
      linear-gradient(90deg, var(--grid) 1px, transparent 1px) 0 0 / 40px 40px;
    border: 1px solid var(--accent-soft);
    box-shadow: inset 0 0 80px rgba(0, 229, 255, 0.06), 0 0 0 1px rgba(0,0,0,0.6);
    overflow: hidden; }
  #globe { position: absolute; inset: 0; }

  /* corner brackets */
  .bracket { position: absolute; width: 28px; height: 28px;
    border-color: var(--accent); border-style: solid; opacity: .85;
    filter: drop-shadow(0 0 6px var(--accent)); }
  .bracket.tl { top: 10px; left: 10px; border-width: 2px 0 0 2px; }
  .bracket.tr { top: 10px; right: 10px; border-width: 2px 2px 0 0; }
  .bracket.bl { bottom: 10px; left: 10px; border-width: 0 0 2px 2px; }
  .bracket.br { bottom: 10px; right: 10px; border-width: 0 2px 2px 0; }

  /* HUD panels */
  .hud { position: absolute; padding: 10px 14px;
    background: rgba(3, 8, 16, 0.72); backdrop-filter: blur(6px);
    border: 1px solid var(--accent-soft);
    box-shadow: 0 0 24px rgba(0, 229, 255, 0.08), inset 0 0 12px rgba(0, 229, 255, 0.05);
    color: var(--text); font-size: 12px; letter-spacing: .12em; line-height: 1.55;
    text-transform: uppercase; pointer-events: none; }
  .hud .label { color: var(--muted); font-size: 10px; }
  .hud .val   { color: var(--accent); font-size: 14px; text-shadow: 0 0 8px var(--accent-soft); }
  #hud-clock  { top: 18px; left: 50%; transform: translateX(-50%); text-align: center; min-width: 220px; }
  #hud-sat    { bottom: 18px; left: 18px; min-width: 220px; }
  #hud-legend { bottom: 18px; right: 18px; text-align: right; }
  #hud-legend .row { display: flex; align-items: center; justify-content: flex-end; gap: 8px; margin-top: 4px; }
  #hud-legend .dot { width: 8px; height: 8px; border-radius: 50%;
    box-shadow: 0 0 8px currentColor, 0 0 14px currentColor; }

  /* sat label sticking out of the globe */
  .sat-label { color: var(--accent); font-family: inherit; font-size: 11px;
    letter-spacing: .14em; text-transform: uppercase; white-space: nowrap;
    transform: translate(12px, -50%);
    text-shadow: 0 0 6px rgba(0, 229, 255, 0.6);
    pointer-events: none; }
  .sat-label::before { content: ""; display: inline-block; width: 18px; height: 1px;
    background: var(--accent); vertical-align: middle; margin-right: 6px;
    box-shadow: 0 0 6px var(--accent); }

  /* scanlines for cyber feel */
  #wrap::after { content: ""; position: absolute; inset: 0; pointer-events: none;
    background: repeating-linear-gradient(0deg, rgba(0,229,255,0.025) 0 1px, transparent 1px 3px);
    mix-blend-mode: screen; opacity: .35; }
</style>
</head>
<body>
  <div id="wrap">
    <div id="globe"></div>
    <span class="bracket tl"></span><span class="bracket tr"></span>
    <span class="bracket bl"></span><span class="bracket br"></span>

    <div id="hud-clock"  class="hud" style="display:none;">
      <div class="label">UTC // SYS TIME</div>
      <div class="val" id="clock-val">--:--:--</div>
    </div>
    <div id="hud-sat" class="hud" style="display:none;">
      <div class="label">TRACKING</div>
      <div class="val" id="sat-name">--</div>
      <div class="label" style="margin-top:6px;">LAT / LON / ALT</div>
      <div class="val" id="sat-coords">--</div>
    </div>
    <div id="hud-legend" class="hud" style="display:none;">
      <div class="label">FLEET</div>
      <div id="legend-rows"></div>
    </div>
  </div>

<script src="https://unpkg.com/three@0.155.0/build/three.min.js"></script>
<script src="https://unpkg.com/globe.gl@2.32.4/dist/globe.gl.min.js"></script>
<script>
(function () {
  const DATA = __DATA_JSON__;
  const EARTH_R_KM = 6371;

  // accent color override via CSS var
  document.documentElement.style.setProperty('--accent', DATA.accent);
  document.documentElement.style.setProperty('--bg', DATA.bg);

  // --- build globe -----------------------------------------------------------
  const world = Globe()
    (document.getElementById('globe'))
    .backgroundColor('rgba(0,0,0,0)')
    // dark cyber Earth: dark night map + topology bump
    .globeImageUrl('https://unpkg.com/three-globe@2.31.1/example/img/earth-night.jpg')
    .bumpImageUrl('https://unpkg.com/three-globe@2.31.1/example/img/earth-topology.png')
    .showAtmosphere(true)
    .atmosphereColor(DATA.accent)
    .atmosphereAltitude(0.22);

  // softer Earth tint -> cyber blue-black
  setTimeout(() => {
    try {
      const mat = world.globeMaterial();
      mat.bumpScale = 8;
      if (mat.color) mat.color.setHex(0x0b1726);
      mat.emissive && mat.emissive.setHex(0x0a1a2a);
      mat.emissiveIntensity = 0.35;
    } catch (e) {}
  }, 50);

  // --- satellites as points + pulsing rings ----------------------------------
  const sats = DATA.satellites || [];
  const altUnit = (km) => km / EARTH_R_KM;  // globe.gl altitude unit = Earth radii

  world
    .pointsData(sats)
    .pointLat(d => d.lat)
    .pointLng(d => d.lon)
    .pointAltitude(d => altUnit(d.alt_km))
    .pointRadius(0.35)
    .pointColor(d => d.color)
    .pointResolution(8)
    .pointsMerge(false);

  world
    .ringsData(sats)
    .ringLat(d => d.lat)
    .ringLng(d => d.lon)
    .ringColor(d => (t) => `rgba(${hexToRgb(d.color)}, ${1 - t})`)
    .ringMaxRadius(4.5)
    .ringPropagationSpeed(2.2)
    .ringRepeatPeriod(1400)
    .ringAltitude(d => altUnit(d.alt_km) - 0.001);

  // --- ground tracks (orbit paths) -------------------------------------------
  const tracks = (DATA.tracks || []).map(t => ({
    ...t,
    coords: t.points.map(p => [p[0], p[1], altUnit(t.alt_km || 408)])
  }));
  world
    .pathsData(tracks)
    .pathPoints(d => d.coords)
    .pathPointLat(p => p[0])
    .pathPointLng(p => p[1])
    .pathPointAlt(p => p[2])
    .pathColor(d => [d.color, d.color])
    .pathStroke(2.2)
    .pathDashLength(0.04)
    .pathDashGap(0.015)
    .pathDashAnimateTime(8000)
    .pathTransitionDuration(0);

  // --- floating HTML labels next to each satellite ---------------------------
  world
    .htmlElementsData(sats)
    .htmlLat(d => d.lat)
    .htmlLng(d => d.lon)
    .htmlAltitude(d => altUnit(d.alt_km))
    .htmlElement(d => {
      const el = document.createElement('div');
      el.className = 'sat-label';
      el.textContent = d.name;
      el.style.color = d.color;
      el.style.textShadow = `0 0 6px ${d.color}`;
      return el;
    });

  // controls / auto-rotate
  const controls = world.controls();
  controls.autoRotate = !!DATA.autoRotate;
  controls.autoRotateSpeed = DATA.autoRotateSpeed;
  controls.enableDamping = true;
  controls.dampingFactor = 0.08;

  // initial camera
  const first = sats[0];
  if (first) {
    world.pointOfView({ lat: first.lat, lng: first.lon, altitude: 2.4 }, 1500);
  } else {
    world.pointOfView({ lat: 20, lng: 0, altitude: 2.6 }, 1500);
  }

  // resize
  function fit() {
    const wrap = document.getElementById('wrap');
    world.width(wrap.clientWidth);
    world.height(wrap.clientHeight);
  }
  fit(); window.addEventListener('resize', fit);

  // --- HUD -------------------------------------------------------------------
  if (DATA.showHud) {
    document.getElementById('hud-clock').style.display = 'block';
    document.getElementById('hud-sat').style.display   = sats.length ? 'block' : 'none';
    document.getElementById('hud-legend').style.display = sats.length ? 'block' : 'none';

    // legend
    const lr = document.getElementById('legend-rows');
    sats.forEach(s => {
      const row = document.createElement('div');
      row.className = 'row';
      row.innerHTML = `<span style="color:${s.color}">${s.name}</span>
                       <span class="dot" style="color:${s.color}; background:${s.color}"></span>`;
      lr.appendChild(row);
    });

    // selected sat readout
    let selected = sats[0] || null;
    function refreshSatHud() {
      if (!selected) return;
      document.getElementById('sat-name').textContent = selected.name;
      document.getElementById('sat-coords').textContent =
        `${selected.lat.toFixed(4)}°  ${selected.lon.toFixed(4)}°  ${Math.round(selected.alt_km)} KM`;
    }
    refreshSatHud();

    world.onPointClick(d => {
      selected = d;
      refreshSatHud();
      world.pointOfView({ lat: d.lat, lng: d.lon, altitude: 1.8 }, 1200);
    });

    // clock
    setInterval(() => {
      const now = new Date();
      const hh = String(now.getUTCHours()).padStart(2, '0');
      const mm = String(now.getUTCMinutes()).padStart(2, '0');
      const ss = String(now.getUTCSeconds()).padStart(2, '0');
      document.getElementById('clock-val').textContent = `${hh}:${mm}:${ss}`;
    }, 1000);
  }

  function hexToRgb(hex) {
    const h = hex.replace('#', '');
    const n = parseInt(h.length === 3 ? h.split('').map(c => c + c).join('') : h, 16);
    return `${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}`;
  }
})();
</script>
</body>
</html>
"""
