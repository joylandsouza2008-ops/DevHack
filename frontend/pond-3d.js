// Pond 3D: a small Three.js pond, seen from the side like a glass tank:
// gently moving water, a few fish, and bubbles whose number follows the
// dissolved oxygen (more oxygen, more bubbles). Night and day lighting, the
// moon and stars follow the SIMULATED time (scene.js sends the sky colours).
//
// Used in two places:
//   - the "Pond view" card on the Pond page (pond-view.js decides when)
//   - the right half of the start screen on wide screens (welcome.js)
//
// Speed and safety rules (cheap phones):
//   - At most 30 frames per second, pixel ratio at most 1.5.
//   - Stops drawing when the pond is off screen or the browser tab is hidden.
//   - Nothing is created per frame: fixed fish, a fixed pool of bubbles.
//   - If WebGL is missing or the GPU drops the context, onFail() is called and
//     the caller shows the 2D pond instead (pond-view.js / the 2D welcome pond).
// Water tones are murky blues and greys, never the Safe / Warning / Danger
// colours; the status is always said in words next to the picture.
//
// Loaded as a module (<script type="module">). It sets window.Pond3D and
// fires a "pond3d-ready" event, so the classic scripts can use it.

import * as THREE from "./vendor/three/three.module.min.js";

const FRAME_MS = 1000 / 30;            // 30 fps cap
const MAX_BUBBLES = 48;
const TANK = { w: 8, h: 3, d: 3.2 };   // water box, centred on the origin
const SURFACE_Y = TANK.h / 2;

// Same tones as the 2D pond view (pond-view.js): clearer when safe, murkier when not.
const WATER = {
  safe:    { top: 0x2f7f96, deep: 0x0e3a4a },
  warning: { top: 0x3c6467, deep: 0x132b2d },
  danger:  { top: 0x454d57, deep: 0x161b21 },
  unknown: { top: 0x2f5c6c, deep: 0x0e2630 },
};
const WATER_COLOURS = Object.fromEntries(Object.entries(WATER).map(([level, c]) =>
  [level, { top: new THREE.Color(c.top), deep: new THREE.Color(c.deep) }]));
// Fish: swim speed, height in the tank (-1.5 floor .. 1.5 surface), nose-up tilt, tail speed.
const FISH = {
  safe:    { speed: 1,    y: -0.3, tilt: 0,    tail: 6 },
  warning: { speed: 0.45, y: 0.5,  tilt: 0.12, tail: 9 },
  danger:  { speed: 0.12, y: 1.25, tilt: 0.45, tail: 14 },
  unknown: { speed: 0.6,  y: 0,    tilt: 0,    tail: 7 },
};

const FISH_PARAMS = ["speed", "y", "tilt", "tail"];

function supported() {
  try {
    const canvas = document.createElement("canvas");
    return !!(window.WebGLRenderingContext && (canvas.getContext("webgl2") || canvas.getContext("webgl")));
  } catch {
    return false;
  }
}

// Bubbles for a dissolved-oxygen reading (mg/L): 4 at 0 mg/L, up to 44 at 12 mg/L.
function bubblesFor(oxygen) {
  if (oxygen == null || Number.isNaN(oxygen)) return 16;
  const o = Math.min(12, Math.max(0, oxygen));
  return Math.round(4 + (o / 12) * 40);
}

// options: { transparent, level, oxygen, night, onFail }
function create(container, options = {}) {
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ antialias: (window.devicePixelRatio || 1) < 2, alpha: !!options.transparent,
                                         powerPreference: "low-power" });
  } catch {
    return null;
  }
  const canvas = renderer.domElement;
  canvas.className = "pond3d-canvas";
  canvas.setAttribute("aria-hidden", "true");
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.5));
  if (options.transparent) renderer.setClearColor(0x000000, 0);

  const scene = new THREE.Scene();
  const sky = new THREE.Color(0x060351);
  if (!options.transparent) scene.background = sky;
  const camera = new THREE.PerspectiveCamera(32, 16 / 9, 0.1, 60);
  const disposables = [];
  const track = (...items) => { disposables.push(...items); return items[0]; };

  // ---- lights: soft sky light + one sun / moon light
  const hemi = new THREE.HemisphereLight(0xb8d8f0, 0x0a0f1a, 1);
  const key = new THREE.DirectionalLight(0xffffff, 1.4);
  key.position.set(3, 6, 4);
  scene.add(hemi, key);

  // ---- water: a dark inside (back faces), a light glassy front, and a moving surface
  const boxGeo = track(new THREE.BoxGeometry(TANK.w, TANK.h, TANK.d));
  const deepMat = track(new THREE.MeshStandardMaterial({ color: WATER.unknown.deep, emissive: WATER.unknown.deep,
    emissiveIntensity: 0.9, side: THREE.BackSide, transparent: true, opacity: 0.96, roughness: 0.9, depthWrite: false }));
  const glassMat = track(new THREE.MeshStandardMaterial({ color: WATER.unknown.top, emissive: WATER.unknown.top,
    emissiveIntensity: 0.35, transparent: true, opacity: 0.38, roughness: 0.25, metalness: 0.05, depthWrite: false }));
  const deep = new THREE.Mesh(boxGeo, deepMat);
  const glass = new THREE.Mesh(boxGeo, glassMat);
  deep.renderOrder = 0;
  glass.renderOrder = 3;

  const surfaceGeo = track(new THREE.PlaneGeometry(TANK.w, TANK.d, 40, 16));
  surfaceGeo.rotateX(-Math.PI / 2);
  const surfaceMat = track(new THREE.MeshStandardMaterial({ color: 0x6fb8cf, emissive: 0x2f7f96, emissiveIntensity: 0.35,
    transparent: true, opacity: 0.8, roughness: 0.18, metalness: 0.15, depthWrite: false }));
  const surface = new THREE.Mesh(surfaceGeo, surfaceMat);
  surface.position.y = SURFACE_Y;
  surface.renderOrder = 4;
  const surfacePos = surfaceGeo.attributes.position;
  const restXZ = Float32Array.from({ length: surfacePos.count * 2 }, (_, i) =>
    surfacePos.getComponent(i >> 1, (i & 1) ? 2 : 0));

  const floorMat = track(new THREE.MeshStandardMaterial({ color: 0x141d27, roughness: 1 }));
  const floor = new THREE.Mesh(track(new THREE.PlaneGeometry(TANK.w, TANK.d)), floorMat);
  floor.rotation.x = -Math.PI / 2;
  floor.position.y = -SURFACE_Y + 0.01;
  scene.add(deep, floor, surface, glass);

  // Pebbles and reeds: slate and ink, never green (green means Safe in this app).
  const stoneGeo = track(new THREE.IcosahedronGeometry(1, 0));
  const stoneMat = track(new THREE.MeshStandardMaterial({ color: 0x2a3644, roughness: 1, flatShading: true }));
  [[-3.1, 0.9, 0.22], [-2.6, -0.8, 0.14], [-0.9, 1.1, 0.18], [1.4, 0.6, 0.26], [2.2, -1.0, 0.15], [3.3, 0.2, 0.2]]
    .forEach(([x, z, s]) => {
      const stone = new THREE.Mesh(stoneGeo, stoneMat);
      stone.scale.set(s * 1.4, s * 0.7, s);
      stone.position.set(x, -SURFACE_Y + s * 0.4, z);
      scene.add(stone);
    });
  const reedMat = track(new THREE.MeshStandardMaterial({ color: 0x1c2738, roughness: 0.9 }));
  const reeds = [[-3.5, -1.2, 2.2], [-3.3, -1.0, 1.7], [3.4, -1.2, 2.5], [3.6, -0.9, 1.9]].map(([x, z, h]) => {
    const reed = new THREE.Mesh(track(new THREE.CylinderGeometry(0.02, 0.04, h, 5)), reedMat);
    reed.position.set(x, -SURFACE_Y + h / 2, z);
    scene.add(reed);
    return reed;
  });

  // ---- moon and stars (fade in at night)
  const moonMat = track(new THREE.MeshBasicMaterial({ color: 0xeef5fb, transparent: true, opacity: 0 }));
  const haloMat = track(new THREE.MeshBasicMaterial({ color: 0xdef0f8, transparent: true, opacity: 0, depthWrite: false }));
  const moon = new THREE.Mesh(track(new THREE.CircleGeometry(0.3, 40)), moonMat);
  const halo = new THREE.Mesh(track(new THREE.CircleGeometry(0.62, 40)), haloMat);
  moon.position.set(3.6, 2.7, -6);
  halo.position.set(3.6, 2.7, -6.05);
  const starPositions = new Float32Array(70 * 3);
  let seed = 1802;
  const rand = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
  for (let i = 0; i < 70; i++) starPositions.set([(rand() - 0.5) * 22, 1.9 + rand() * 4.5, -9 - rand() * 3], i * 3);
  const starGeo = track(new THREE.BufferGeometry());
  starGeo.setAttribute("position", new THREE.BufferAttribute(starPositions, 3));
  const starMat = track(new THREE.PointsMaterial({ color: 0xdef0f8, size: 0.05, transparent: true, opacity: 0 }));
  scene.add(halo, moon, new THREE.Points(starGeo, starMat));

  // ---- fish: three simple bodies with a wagging tail
  const fishMat = track(new THREE.MeshStandardMaterial({ color: 0x0a1a22, roughness: 0.55 }));
  const bodyGeo = track(new THREE.SphereGeometry(0.34, 18, 12));
  const tailGeo = track(new THREE.ConeGeometry(0.17, 0.32, 4));
  const finGeo = track(new THREE.ConeGeometry(0.07, 0.18, 3));
  const fishes = [0, 1, 2].map((i) => {
    const group = new THREE.Group();
    const body = new THREE.Mesh(bodyGeo, fishMat);
    body.scale.set(1.15, 0.44, 0.3);
    const tailPivot = new THREE.Group();
    tailPivot.position.x = -0.36;
    const tail = new THREE.Mesh(tailGeo, fishMat);
    tail.rotation.z = Math.PI / 2;
    tail.position.x = -0.13;
    tail.scale.set(1, 1, 0.35);
    tailPivot.add(tail);
    const fin = new THREE.Mesh(finGeo, fishMat);
    fin.position.set(0.02, 0.16, 0);
    fin.rotation.z = -0.5;
    const tilt = new THREE.Group();          // nose-up tilt (Danger: gasping at the surface)
    tilt.add(body, tailPivot, fin);
    group.add(tilt);
    const size = 1 - i * 0.14;
    group.scale.setScalar(size);
    scene.add(group);
    return { group, tilt, tailPivot, angle: i * 2.1, rx: 2.9 - i * 0.45, rz: 0.95 - i * 0.22, lane: i, y: 0, size };
  });

  // ---- bubbles: one instanced mesh, a fixed pool
  const bubbleMat = track(new THREE.MeshStandardMaterial({ color: 0xe6f6fc, emissive: 0x24485a, transparent: true,
    opacity: 0.6, roughness: 0.1, depthWrite: false }));
  const bubbleMesh = new THREE.InstancedMesh(track(new THREE.SphereGeometry(1, 10, 8)), bubbleMat, MAX_BUBBLES);
  bubbleMesh.renderOrder = 2;
  bubbleMesh.frustumCulled = false;
  scene.add(bubbleMesh);
  const SOURCES = [[-2.4, 0.4], [-0.6, -0.6], [1.2, 0.8], [2.8, -0.3]];   // where bubbles start, on the floor
  const bubbles = Array.from({ length: MAX_BUBBLES }, (_, i) => ({
    x: 0, y: -SURFACE_Y - 1, z: 0, r: 0, speed: 0, phase: i * 1.7, on: false,
  }));
  const dummy = new THREE.Object3D();
  function spawn(b, anywhere) {
    const [sx, sz] = SOURCES[Math.floor(Math.random() * SOURCES.length)];
    b.x = sx + (Math.random() - 0.5) * 0.5;
    b.z = sz + (Math.random() - 0.5) * 0.5;
    b.y = anywhere ? -SURFACE_Y + Math.random() * TANK.h : -SURFACE_Y + 0.05;
    b.r = 0.025 + Math.random() * 0.045;
    b.speed = 0.45 + Math.random() * 0.45;
    b.on = true;
  }

  // ---- state (targets are reached smoothly; nothing jumps)
  const state = {
    level: options.level || "unknown",
    wantBubbles: bubblesFor(options.oxygen),
    night: options.night ?? 1,
    skyTarget: new THREE.Color(0x060351),
    horizon: new THREE.Color(0x1a1f7a),
    water: { top: new THREE.Color(WATER.unknown.top), deep: new THREE.Color(WATER.unknown.deep) },
    fish: { ...FISH.unknown },
  };
  bubbles.forEach((b, i) => { if (i < state.wantBubbles) spawn(b, true); });

  // ---- size: keep the whole tank in view at any width
  function fit() {
    const w = Math.max(1, container.clientWidth), h = Math.max(1, container.clientHeight);
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    const vHalf = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    const hHalf = vHalf * camera.aspect;
    // Fit the tank's width (plus a small margin) or its height with room for the sky above.
    const dist = Math.max((TANK.w / 2 + 0.6) / hHalf, (TANK.h / 2 + 0.75) / vHalf) + TANK.d / 2;
    camera.position.set(0, 1.2 + dist * 0.2, dist);     // a little above: the moving surface shows
    camera.lookAt(0, 0.35, 0);
    camera.updateProjectionMatrix();
    draw(0);
  }

  // ---- one frame
  const ease = (dt, rate) => 1 - Math.exp(-dt * rate);
  let clock = 0;

  function update(dt) {
    clock += dt;
    const k = ease(dt, 1.2);

    // Water colour and sky follow their targets.
    const target = WATER_COLOURS[state.level] || WATER_COLOURS.unknown;
    state.water.top.lerp(target.top, k);
    state.water.deep.lerp(target.deep, k);
    glassMat.color.copy(state.water.top);
    glassMat.emissive.copy(state.water.top);
    deepMat.color.copy(state.water.deep);
    deepMat.emissive.copy(state.water.deep);
    surfaceMat.color.copy(state.water.top).offsetHSL(0, 0, 0.14);
    surfaceMat.emissive.copy(state.water.top);
    sky.lerp(state.skyTarget, k);
    hemi.color.copy(state.horizon);

    // Night and day light.
    const n = state.night;
    hemi.intensity = 0.8 + (1 - n) * 0.7;
    key.intensity = 0.7 + (1 - n) * 1.1;
    key.color.setHex(n > 0.5 ? 0xbcd2ff : 0xffffff);
    key.position.set(n > 0.5 ? -3 : 3, 6, 4);
    moonMat.opacity = n;
    haloMat.opacity = n * 0.08;
    starMat.opacity = n * 0.85;

    // Surface waves (gentle).
    for (let i = 0; i < surfacePos.count; i++) {
      const x = restXZ[i * 2], z = restXZ[i * 2 + 1];
      surfacePos.setY(i, 0.045 * Math.sin(x * 1.5 + clock * 1.1) + 0.03 * Math.sin(z * 2.2 - clock * 0.8) +
                         0.015 * Math.sin((x + z) * 3.1 + clock * 1.7));
    }
    surfacePos.needsUpdate = true;
    surfaceGeo.computeVertexNormals();

    // Fish.
    const want = FISH[state.level] || FISH.unknown;
    for (const p of FISH_PARAMS) state.fish[p] += (want[p] - state.fish[p]) * k;
    fishes.forEach((f) => {
      f.angle += dt * 0.32 * state.fish.speed * (1 + f.lane * 0.15);
      const x = Math.cos(f.angle) * f.rx, z = Math.sin(f.angle) * f.rz;
      const yWanted = Math.min(SURFACE_Y - 0.22, state.fish.y + (f.lane - 1) * (state.level === "danger" ? 0.04 : 0.45));
      f.y += (yWanted - f.y) * ease(dt, 0.8);
      f.group.position.set(x, f.y + Math.sin(clock * 1.3 + f.lane) * 0.04, z);
      f.group.rotation.y = Math.atan2(-Math.cos(f.angle) * f.rz, -Math.sin(f.angle) * f.rx);   // face along the path
      f.tilt.rotation.z = state.fish.tilt;
      f.tailPivot.rotation.y = Math.sin(clock * state.fish.tail + f.lane) * 0.45;
    });

    // Reeds sway a little.
    reeds.forEach((r, i) => { r.rotation.z = Math.sin(clock * 0.7 + i) * 0.03; });

    // Bubbles: the pool keeps `wantBubbles` of them rising; extra ones finish and stop.
    let active = 0;
    bubbles.forEach((b, i) => {
      if (!b.on && i < state.wantBubbles && Math.random() < dt * 1.5) spawn(b, false);
      if (b.on) {
        b.y += b.speed * dt;
        b.x += Math.sin(clock * 2.6 + b.phase) * 0.0025;
        if (b.y > SURFACE_Y - b.r) {
          if (i < state.wantBubbles) spawn(b, false); else b.on = false;
        }
      }
      dummy.position.set(b.x, b.y, b.z);
      dummy.scale.setScalar(b.on ? b.r : 0);
      dummy.updateMatrix();
      bubbleMesh.setMatrixAt(i, dummy.matrix);
      if (b.on) active++;
    });
    bubbleMesh.instanceMatrix.needsUpdate = true;
    state.activeBubbles = active;
  }

  function draw(dt) {
    if (dt) update(dt);
    renderer.render(scene, camera);
  }

  // ---- loop: 30 fps, only while visible
  let raf = 0, last = 0, running = false, onScreen = true, frames = 0, fpsStart = 0, fps = 0, dead = false;

  function frame(now) {
    raf = requestAnimationFrame(frame);
    if (now - last < FRAME_MS - 1) return;
    const dt = Math.min(0.1, (now - last) / 1000);
    last = now;
    draw(dt);
    frames++;
    if (now - fpsStart >= 1000) { fps = Math.round((frames * 1000) / (now - fpsStart)); frames = 0; fpsStart = now; }
  }
  function start() {
    if (running || dead || !onScreen || document.hidden) return;
    running = true;
    last = fpsStart = performance.now();
    frames = 0;
    raf = requestAnimationFrame(frame);
  }
  function stop() {
    running = false;
    cancelAnimationFrame(raf);
    fps = 0;
  }

  const io = new IntersectionObserver(([entry]) => {
    onScreen = entry.isIntersecting;
    onScreen ? start() : stop();
  });
  const ro = new ResizeObserver(fit);
  const onVisibility = () => (document.hidden ? stop() : start());

  function destroy() {
    if (dead) return;
    dead = true;
    stop();
    io.disconnect();
    ro.disconnect();
    document.removeEventListener("visibilitychange", onVisibility);
    disposables.forEach((d) => d.dispose && d.dispose());
    bubbleMesh.dispose();
    renderer.dispose();
    canvas.remove();
  }

  canvas.addEventListener("webglcontextlost", (event) => {
    event.preventDefault();
    destroy();
    if (options.onFail) options.onFail();
  });

  container.append(canvas);
  io.observe(container);
  ro.observe(container);
  document.addEventListener("visibilitychange", onVisibility);
  fit();
  start();

  return {
    setLevel(level) { state.level = level in WATER ? level : "unknown"; },
    setOxygen(oxygen) { state.wantBubbles = bubblesFor(oxygen); },
    setSky(top, horizon, night) {
      state.skyTarget.set(top);
      state.horizon.set(horizon);
      state.night = Math.min(1, Math.max(0, night));
    },
    stats: () => ({ fps, running, bubbles: state.activeBubbles || 0, wantBubbles: state.wantBubbles }),
    destroy,
  };
}

window.Pond3D = { supported, create, bubblesFor };
window.dispatchEvent(new Event("pond3d-ready"));
