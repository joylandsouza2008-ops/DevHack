// MeenuRaksha dashboard: shows the simulator stream (current risk, pond view,
// risk gauge, time until danger, oxygen chart, latest readings) in Kannada or
// English. Alert text (reasons, time until danger) comes from the API in both
// languages; only the page labels are translated here.
//
// Motion (motion.js, pond-view.js, gauge.js, do-chart.js) helps farmers notice
// changes; every status is still shown as colour + icon + word.
// scene.js draws the day/night sky for the simulated time; cursor-fx.js adds
// the mouse and tap effects (never on the numbers themselves).

"use strict";

const TEXT = {
  en: {
    appName: "MeenuRaksha",
    tagline: "Pond water early warning",
    welcomeTagline: "Pond water warnings before your fish are in danger.",
    start: "Start",
    themeLight: "Light", themeDark: "Dark",
    builtBy: "Built by Team Orbit",
    sourcesTitle: "Data sources", sourcesClose: "Close",
    sourcesIntro: "The simulated pond uses these open datasets and public services. Only the Live sensor card shows readings sent by a pond sensor.",
    sourcesPondsUse: "Real sensor readings from 3 fish ponds in Andhra Pradesh (2022-23). Used to make the simulated demo pond and to test our oxygen predictions.",
    sourcesPondsLicence: "Licence: unknown (not stated by the uploader).",
    sourcesMeteoUse: "Tonight's real weather forecast for Mangaluru, for the night oxygen-crash warning.",
    sourcesMeteoLicence: "Licence: data CC BY 4.0. Free API, non-commercial use only.",
    sourcesGuidesUse: "Published guides and research papers behind the Safe / Warning / Danger limits and the “What to do now” steps.",
    sourcesGuidesLicence: "Copyright of each publisher. We cite their facts; we don't copy them.",
    sourcesMendeleyUse: "Checked but not used: some values are impossible (e.g. water at 84 °C).",
    sourcesMendeleyLicence: "Licence: CC BY 4.0.",
    sourcesFishUse: "Fish disease photos for research only. Not used in the app.",
    sourcesFishLicence: "Licence: CC0 (public domain).",
    sourcesFull: "Full list with links and licences",
    simulatedNote: "Not a real pond. For demonstration only.",
    pond: "Pond", pond1: "Pond 1", pond2: "Pond 2", pond3: "Pond 3",
    scenario: "Scenario", scenarioNormal: "Normal day", scenarioCrash: "Night oxygen crash",
    restart: "Restart", pause: "Pause", resume: "Resume",
    simTime: "Simulated time",
    connecting: "Connecting…",
    ended: "Demo finished. Press Restart to play again.",
    connectionLost: "Connection lost. Press Restart.",
    pondViewTitle: "Pond view",
    gaugeTitle: "Risk level",
    ttdTitle: "Time until danger",
    countdownLabel: "Danger expected in",
    chartTitle: "Dissolved oxygen, last 12 hours",
    readingsTitle: "Latest readings",
    infoOnly: "For information",
    pondCaption: {
      safe: "Fish are swimming normally.",
      warning: "Fish are slowing down.",
      danger: "Fish are gasping for air at the surface.",
      unknown: "Waiting for readings.",
    },
    duration: (h, m) => (h ? `${h} h ${String(m).padStart(2, "0")} min` : `${m} min`),
    around: (clock) => `around ${clock}`,
    chartSummary: (now, min) => `Now ${now} mg/L. Lowest in this period: ${min} mg/L.`,
    weatherTitle: "Tonight's weather",
    weatherLoading: "Checking the forecast…",
    weatherUnavailable: "No internet and no saved forecast. Tonight's weather is not known.",
    crashRisk: (level) => `Oxygen crash risk: ${level}`,
    weatherDetails: (c, w, t) => `Day cloud ${c}% · Night wind ${w} km/h · Night ${t} °C · Forecast: Open-Meteo`,
    weatherOffline: (when) => (when ? `Offline: showing the forecast saved on ${when}.` : "Offline."),
    actionsTitle: "What to do now",
    actionsSource: "Based on FAO, TNAU and university extension guides. No chemicals.",
    actionsProgress: (done, total) => (done === total ? `All ${total} done.` : `${done} of ${total} done`),
    alertTitle: "Alert preview",
    previewNote: "Preview only. No real SMS or WhatsApp message is sent.",
    alertFor: "Alert for", alertForSim: "Simulated", alertForSensor: "Live sensor", alertForKit: "Test kit",
    liveTitle: "Live sensor",
    liveWaiting: "Connecting to the live sensor…",
    liveNoReading: (pond) => `No reading from the ${pond} sensor yet. Readings appear here as soon as the sensor sends one.`,
    liveMeasured: (when, ago) => `Measured ${when} · received ${ago}`,
    liveAgo: (s) => (s < 60 ? `${s} s ago` : `${Math.floor(s / 60)} min ago`),
    liveStale: (min) => `No new reading for ${min} min. Check the sensor's power and Wi-Fi.`,
    liveLost: "Lost connection to the server. Trying again…",
    liveNote: "Readings are kept only while the server is running. On the free server they are cleared when it sleeps.",
    kitTitle: "Enter test-kit readings",
    kitHelp: "Type the numbers from your pond test kit. Leave a box empty if you did not test it.",
    kitDO: "Dissolved oxygen", kitNoUnit: "no unit", kitTemp: "Water temperature", kitAmmonia: "Total ammonia",
    kitCheck: "Check readings", kitClear: "Clear",
    kitEmpty: "Enter at least one reading.",
    kitBadNumber: "Use numbers only, like 6.5.",
    kitFailed: "Could not check the readings. Please try again.",
    simulatedTag: "Simulated data",
    healthTitle: "Pond health score",
    healthScale: "Safe 75‑100 · Warning 40‑74 · Danger 0‑39",
    healthText: {
      safe: (s) => `${s} out of 100. All readings are in the safe range.`,
      warning: (s) => `${s} out of 100. The water needs attention.`,
      danger: (s) => `${s} out of 100. The water is dangerous for fish.`,
      unknown: () => "Waiting for readings.",
    },
    voiceListen: "Listen to alert", voiceStop: "Stop",
    voiceNoKannada: "Sorry, this phone has no Kannada voice, so the alert cannot be read aloud in Kannada. Please read the alert on the screen, or switch to English to hear it.",
    voiceNoEnglish: "Sorry, this phone has no English voice. Please read the alert on the screen.",
    voiceUnsupported: "Sorry, this browser cannot read aloud. Please read the alert on the screen.",
    historyTitle: "Alert history",
    historyHelp: "Past warnings, newest first. Saved on this phone only.",
    historyEmpty: "No warnings yet.",
    historyClear: "Clear history",
    historyClearConfirm: "Delete all saved alerts from this phone?",
    guideTitle: "Fish disease guide",
    guideIntro: "Common diseases of carp ponds: the signs to look for, when they happen and how to prevent them.",
    guideLoading: "Loading the guide…",
    guideFailed: "Could not load the disease guide. Please try again.",
    guideDrawing: "drawing of a fish with the signs",
    guideAgent: "Cause", guideBody: "Signs on the body", guideBehaviour: "How the fish behave",
    guideWhen: "When it is most common", guidePrevention: "Prevention", guideDo: "What to do",
    guideSourcesShort: "Sources", guideRead: "Read about it", guideSources: "Sources for every entry",
    checkerTitle: "Symptom checker",
    checkerHelp: "Tick the signs you see on your fish. You get possible matches, not a diagnosis.",
    checkerBody: "On the body", checkerBehaviour: "How the fish behave",
    checkerCheck: "Show possible matches", checkerClear: "Clear",
    checkerEmpty: "Tick at least one sign.",
    checkerMatches: "Possible matches", checkerMatched: "Matching signs",
    checkerMore: (n) => `${n} more diseases match fewer of your signs.`,
    libraryTitle: "Disease library", libraryHelp: "Tap a disease to read more.",
    noPhotoTitle: "Why there's no photo check",
    noPhotoText: "We tested a computer model that guesses the disease from a fish photo. The public photos are mostly aquarium fish, not carps in ponds, and the model was wrong about one time in three. That is not safe enough for your fish, so the app does not do it.",
    noPhotoLink: "See the test results",
    likelyTitle: "Diseases more likely now",
    likelyNote: "This does not mean your fish are sick. Watch them closely and use the Fish disease guide if you see signs.",
    assistantTitle: "Ask MeenuRaksha", assistantLabel: "AI assistant: can make mistakes",
    assistantHelp: "Ask about your readings, safe levels, tonight's weather or fish diseases. Answers come only from this app's own information.",
    assistantPrivacy: "Do not type your name, phone number or other personal details.",
    assistantSuggested: "Suggested questions (ready answers)",
    assistantAsk: "Your question", assistantSend: "Ask", assistantYou: "You",
    assistantThinking: "Thinking…",
    assistantAiAnswer: "AI answer", assistantReady: "Ready answer from the app", assistantSafety: "Safety answer from the app",
    assistantListen: "Listen", assistantNotice: "Message from the app",
    assistantEmpty: "Type a question first, or tap a suggested question.",
    assistantFailed: "Could not reach the app server. Tap a suggested question for a ready answer.",
    historyKit: "Test kit",
    historySensor: "Live sensor", historyDemo: "Demo device",
    historySimTime: "Simulated time",
    historyActionTaken: "Action taken:",
    historyNoAction: "No action ticked yet.",
  },
  kn: {
    appName: "ಮೀನುರಕ್ಷಾ",
    tagline: "ಕೊಳದ ನೀರಿನ ಮುನ್ನೆಚ್ಚರಿಕೆ",
    welcomeTagline: "ಮೀನುಗಳಿಗೆ ಅಪಾಯ ಬರುವ ಮೊದಲೇ ಕೊಳದ ನೀರಿನ ಎಚ್ಚರಿಕೆ.",
    start: "ಪ್ರಾರಂಭಿಸಿ",
    themeLight: "ತಿಳಿ", themeDark: "ಗಾಢ",
    builtBy: "ನಿರ್ಮಾಣ: ಟೀಮ್ ಆರ್ಬಿಟ್",
    sourcesTitle: "ಡೇಟಾ ಮೂಲಗಳು", sourcesClose: "ಮುಚ್ಚಿ",
    sourcesIntro: "ಅನುಕರಿಸಿದ ಕೊಳವು ಈ ಮುಕ್ತ ಡೇಟಾಸೆಟ್‌ಗಳು ಮತ್ತು ಸಾರ್ವಜನಿಕ ಸೇವೆಗಳನ್ನು ಬಳಸುತ್ತದೆ. ಕೊಳದ ಸೆನ್ಸರ್ ಕಳುಹಿಸಿದ ಅಳತೆಗಳನ್ನು ಲೈವ್ ಸೆನ್ಸರ್ ಕಾರ್ಡ್ ಮಾತ್ರ ತೋರಿಸುತ್ತದೆ.",
    sourcesPondsUse: "ಆಂಧ್ರಪ್ರದೇಶದ 3 ಮೀನು ಕೊಳಗಳ ನಿಜವಾದ ಸೆನ್ಸರ್ ಅಳತೆಗಳು (2022-23). ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಪ್ರದರ್ಶನ ಕೊಳವನ್ನು ಮಾಡಲು ಮತ್ತು ನಮ್ಮ ಆಮ್ಲಜನಕ ಮುನ್ಸೂಚನೆಗಳನ್ನು ಪರೀಕ್ಷಿಸಲು ಬಳಸಲಾಗಿದೆ.",
    sourcesPondsLicence: "ಪರವಾನಗಿ: ತಿಳಿದಿಲ್ಲ (ಅಪ್‌ಲೋಡ್ ಮಾಡಿದವರು ತಿಳಿಸಿಲ್ಲ).",
    sourcesMeteoUse: "ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತದ ಎಚ್ಚರಿಕೆಗಾಗಿ ಮಂಗಳೂರಿನ ಇಂದು ರಾತ್ರಿಯ ನಿಜವಾದ ಹವಾಮಾನ ಮುನ್ಸೂಚನೆ.",
    sourcesMeteoLicence: "ಪರವಾನಗಿ: ಡೇಟಾ CC BY 4.0. ಉಚಿತ API, ವಾಣಿಜ್ಯೇತರ ಬಳಕೆಗೆ ಮಾತ್ರ.",
    sourcesGuidesUse: "ಸುರಕ್ಷಿತ / ಎಚ್ಚರಿಕೆ / ಅಪಾಯ ಮಿತಿಗಳು ಮತ್ತು “ಈಗ ಏನು ಮಾಡಬೇಕು” ಹಂತಗಳಿಗೆ ಆಧಾರವಾದ ಪ್ರಕಟಿತ ಮಾರ್ಗದರ್ಶಿಗಳು ಮತ್ತು ಸಂಶೋಧನಾ ಲೇಖನಗಳು.",
    sourcesGuidesLicence: "ಹಕ್ಕುಸ್ವಾಮ್ಯ ಆಯಾ ಪ್ರಕಾಶಕರದು. ನಾವು ಅವುಗಳ ಮಾಹಿತಿಯನ್ನು ಉಲ್ಲೇಖಿಸುತ್ತೇವೆ, ನಕಲು ಮಾಡುವುದಿಲ್ಲ.",
    sourcesMendeleyUse: "ಪರಿಶೀಲಿಸಲಾಗಿದೆ, ಆದರೆ ಬಳಸಿಲ್ಲ: ಕೆಲವು ಮೌಲ್ಯಗಳು ಅಸಾಧ್ಯ (ಉದಾ: 84 °C ನೀರು).",
    sourcesMendeleyLicence: "ಪರವಾನಗಿ: CC BY 4.0.",
    sourcesFishUse: "ಮೀನು ರೋಗದ ಫೋಟೋಗಳು, ಸಂಶೋಧನೆಗೆ ಮಾತ್ರ. ಆಪ್‌ನಲ್ಲಿ ಬಳಸಿಲ್ಲ.",
    sourcesFishLicence: "ಪರವಾನಗಿ: CC0 (ಸಾರ್ವಜನಿಕ ಸ್ವತ್ತು).",
    sourcesFull: "ಲಿಂಕ್‌ಗಳು ಮತ್ತು ಪರವಾನಗಿಗಳ ಪೂರ್ಣ ಪಟ್ಟಿ",
    simulatedNote: "ನಿಜವಾದ ಕೊಳವಲ್ಲ. ಪ್ರದರ್ಶನಕ್ಕಾಗಿ ಮಾತ್ರ.",
    pond: "ಕೊಳ", pond1: "ಕೊಳ 1", pond2: "ಕೊಳ 2", pond3: "ಕೊಳ 3",
    scenario: "ಸನ್ನಿವೇಶ", scenarioNormal: "ಸಾಮಾನ್ಯ ದಿನ", scenarioCrash: "ರಾತ್ರಿ ಆಮ್ಲಜನಕ ಕುಸಿತ",
    restart: "ಮರುಪ್ರಾರಂಭಿಸಿ", pause: "ವಿರಾಮ", resume: "ಮುಂದುವರಿಸಿ",
    simTime: "ಅನುಕರಿಸಿದ ಸಮಯ",
    connecting: "ಸಂಪರ್ಕಿಸಲಾಗುತ್ತಿದೆ…",
    ended: "ಪ್ರದರ್ಶನ ಮುಗಿದಿದೆ. ಮತ್ತೆ ನೋಡಲು ಮರುಪ್ರಾರಂಭಿಸಿ ಒತ್ತಿ.",
    connectionLost: "ಸಂಪರ್ಕ ಕಡಿದುಹೋಗಿದೆ. ಮರುಪ್ರಾರಂಭಿಸಿ ಒತ್ತಿ.",
    pondViewTitle: "ಕೊಳದ ನೋಟ",
    gaugeTitle: "ಅಪಾಯದ ಮಟ್ಟ",
    ttdTitle: "ಅಪಾಯದವರೆಗಿನ ಸಮಯ",
    countdownLabel: "ಅಪಾಯಕ್ಕೆ ಉಳಿದ ಸಮಯ",
    chartTitle: "ಕರಗಿದ ಆಮ್ಲಜನಕ, ಕಳೆದ 12 ಗಂಟೆಗಳು",
    readingsTitle: "ಇತ್ತೀಚಿನ ಅಳತೆಗಳು",
    infoOnly: "ಮಾಹಿತಿಗಾಗಿ",
    pondCaption: {
      safe: "ಮೀನುಗಳು ಸಾಮಾನ್ಯವಾಗಿ ಈಜುತ್ತಿವೆ.",
      warning: "ಮೀನುಗಳು ನಿಧಾನವಾಗಿ ಈಜುತ್ತಿವೆ.",
      danger: "ಮೀನುಗಳು ಮೇಲ್ಮೈಗೆ ಬಂದು ಗಾಳಿಗಾಗಿ ಒದ್ದಾಡುತ್ತಿವೆ.",
      unknown: "ಅಳತೆಗಳಿಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ.",
    },
    duration: (h, m) => (h ? `${h} ಗಂಟೆ ${String(m).padStart(2, "0")} ನಿಮಿಷ` : `${m} ನಿಮಿಷ`),
    around: (clock) => `ಸುಮಾರು ${clock} ಹೊತ್ತಿಗೆ`,
    chartSummary: (now, min) => `ಈಗ ${now} mg/L. ಈ ಅವಧಿಯ ಕನಿಷ್ಠ: ${min} mg/L.`,
    weatherTitle: "ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ",
    weatherLoading: "ಮುನ್ಸೂಚನೆ ನೋಡಲಾಗುತ್ತಿದೆ…",
    weatherUnavailable: "ಇಂಟರ್ನೆಟ್ ಇಲ್ಲ, ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆಯೂ ಇಲ್ಲ. ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ತಿಳಿದಿಲ್ಲ.",
    crashRisk: (level) => `ಆಮ್ಲಜನಕ ಕುಸಿತದ ಅಪಾಯ: ${level}`,
    weatherDetails: (c, w, t) => `ಹಗಲಿನ ಮೋಡ ${c}% · ರಾತ್ರಿ ಗಾಳಿ ${w} km/h · ರಾತ್ರಿ ${t} °C · ಮುನ್ಸೂಚನೆ: Open-Meteo`,
    weatherOffline: (when) => (when ? `ಆಫ್‌ಲೈನ್: ${when} ರಂದು ಉಳಿಸಿದ ಮುನ್ಸೂಚನೆ ತೋರಿಸಲಾಗುತ್ತಿದೆ.` : "ಆಫ್‌ಲೈನ್."),
    actionsTitle: "ಈಗ ಏನು ಮಾಡಬೇಕು",
    actionsSource: "FAO, TNAU ಮತ್ತು ವಿಶ್ವವಿದ್ಯಾಲಯದ ಕೃಷಿ ವಿಸ್ತರಣಾ ಮಾರ್ಗದರ್ಶಿಗಳನ್ನು ಆಧರಿಸಿದೆ. ಯಾವುದೇ ರಾಸಾಯನಿಕಗಳಿಲ್ಲ.",
    actionsProgress: (done, total) => (done === total ? `ಎಲ್ಲಾ ${total} ಮುಗಿದಿವೆ.` : `${total} ರಲ್ಲಿ ${done} ಮುಗಿದಿದೆ`),
    alertTitle: "ಎಚ್ಚರಿಕೆ ಸಂದೇಶದ ಮುನ್ನೋಟ",
    previewNote: "ಮುನ್ನೋಟ ಮಾತ್ರ. ಯಾವುದೇ ನಿಜವಾದ SMS ಅಥವಾ WhatsApp ಸಂದೇಶ ಕಳುಹಿಸುವುದಿಲ್ಲ.",
    alertFor: "ಯಾವುದಕ್ಕೆ ಎಚ್ಚರಿಕೆ", alertForSim: "ಅನುಕರಿಸಿದ", alertForSensor: "ಲೈವ್ ಸೆನ್ಸರ್", alertForKit: "ಟೆಸ್ಟ್ ಕಿಟ್",
    liveTitle: "ಲೈವ್ ಸೆನ್ಸರ್",
    liveWaiting: "ಲೈವ್ ಸೆನ್ಸರ್‌ಗೆ ಸಂಪರ್ಕಿಸಲಾಗುತ್ತಿದೆ…",
    liveNoReading: (pond) => `${pond} ಸೆನ್ಸರ್‌ನಿಂದ ಇನ್ನೂ ಯಾವುದೇ ಅಳತೆ ಬಂದಿಲ್ಲ. ಸೆನ್ಸರ್ ಅಳತೆ ಕಳುಹಿಸಿದ ತಕ್ಷಣ ಇಲ್ಲಿ ಕಾಣಿಸುತ್ತದೆ.`,
    liveMeasured: (when, ago) => `ಅಳತೆ ಸಮಯ ${when} · ${ago} ಬಂದಿದೆ`,
    liveAgo: (s) => (s < 60 ? `${s} ಸೆಕೆಂಡ್ ಹಿಂದೆ` : `${Math.floor(s / 60)} ನಿಮಿಷ ಹಿಂದೆ`),
    liveStale: (min) => `${min} ನಿಮಿಷಗಳಿಂದ ಹೊಸ ಅಳತೆ ಬಂದಿಲ್ಲ. ಸೆನ್ಸರ್‌ನ ವಿದ್ಯುತ್ ಮತ್ತು Wi-Fi ಪರಿಶೀಲಿಸಿ.`,
    liveLost: "ಸರ್ವರ್ ಸಂಪರ್ಕ ಕಡಿದುಹೋಗಿದೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಲಾಗುತ್ತಿದೆ…",
    liveNote: "ಸರ್ವರ್ ಚಾಲನೆಯಲ್ಲಿರುವವರೆಗೆ ಮಾತ್ರ ಅಳತೆಗಳನ್ನು ಉಳಿಸಲಾಗುತ್ತದೆ. ಉಚಿತ ಸರ್ವರ್ ನಿದ್ರೆಗೆ ಹೋದಾಗ ಅವು ಅಳಿಸಿಹೋಗುತ್ತವೆ.",
    kitTitle: "ಟೆಸ್ಟ್ ಕಿಟ್ ಅಳತೆಗಳನ್ನು ನಮೂದಿಸಿ",
    kitHelp: "ನಿಮ್ಮ ಕೊಳದ ಟೆಸ್ಟ್ ಕಿಟ್‌ನ ಸಂಖ್ಯೆಗಳನ್ನು ಬರೆಯಿರಿ. ಪರೀಕ್ಷಿಸದಿದ್ದರೆ ಆ ಡಬ್ಬಿಯನ್ನು ಖಾಲಿ ಬಿಡಿ.",
    kitDO: "ಕರಗಿದ ಆಮ್ಲಜನಕ", kitNoUnit: "ಘಟಕ ಇಲ್ಲ", kitTemp: "ನೀರಿನ ತಾಪಮಾನ", kitAmmonia: "ಒಟ್ಟು ಅಮೋನಿಯಾ",
    kitCheck: "ಅಳತೆ ಪರಿಶೀಲಿಸಿ", kitClear: "ಅಳಿಸಿ",
    kitEmpty: "ಕನಿಷ್ಠ ಒಂದು ಅಳತೆ ನಮೂದಿಸಿ.",
    kitBadNumber: "ಸಂಖ್ಯೆಗಳನ್ನು ಮಾತ್ರ ಬರೆಯಿರಿ, ಉದಾ: 6.5.",
    kitFailed: "ಅಳತೆ ಪರಿಶೀಲಿಸಲು ಆಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
    simulatedTag: "ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ",
    healthTitle: "ಕೊಳದ ಆರೋಗ್ಯ ಅಂಕ",
    healthScale: "ಸುರಕ್ಷಿತ 75‑100 · ಎಚ್ಚರಿಕೆ 40‑74 · ಅಪಾಯ 0‑39",
    healthText: {
      safe: (s) => `100 ರಲ್ಲಿ ${s}. ಎಲ್ಲಾ ಅಳತೆಗಳು ಸುರಕ್ಷಿತ ಮಟ್ಟದಲ್ಲಿವೆ.`,
      warning: (s) => `100 ರಲ್ಲಿ ${s}. ನೀರಿನ ಕಡೆ ಗಮನ ಕೊಡಿ.`,
      danger: (s) => `100 ರಲ್ಲಿ ${s}. ನೀರು ಮೀನುಗಳಿಗೆ ಅಪಾಯಕಾರಿಯಾಗಿದೆ.`,
      unknown: () => "ಅಳತೆಗಳಿಗಾಗಿ ಕಾಯಲಾಗುತ್ತಿದೆ.",
    },
    voiceListen: "ಎಚ್ಚರಿಕೆ ಕೇಳಿ", voiceStop: "ನಿಲ್ಲಿಸಿ",
    voiceNoKannada: "ಕ್ಷಮಿಸಿ, ಈ ಫೋನ್‌ನಲ್ಲಿ ಕನ್ನಡ ಧ್ವನಿ ಇಲ್ಲ, ಆದ್ದರಿಂದ ಎಚ್ಚರಿಕೆಯನ್ನು ಕನ್ನಡದಲ್ಲಿ ಓದಿ ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ, ಅಥವಾ ಕೇಳಲು English ಆಯ್ಕೆಮಾಡಿ.",
    voiceNoEnglish: "ಕ್ಷಮಿಸಿ, ಈ ಫೋನ್‌ನಲ್ಲಿ ಇಂಗ್ಲಿಷ್ ಧ್ವನಿ ಇಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ.",
    voiceUnsupported: "ಕ್ಷಮಿಸಿ, ಈ ಬ್ರೌಸರ್ ಓದಿ ಹೇಳಲು ಆಗುವುದಿಲ್ಲ. ದಯವಿಟ್ಟು ಪರದೆಯ ಮೇಲಿನ ಎಚ್ಚರಿಕೆಯನ್ನು ಓದಿ.",
    historyTitle: "ಎಚ್ಚರಿಕೆಗಳ ಇತಿಹಾಸ",
    historyHelp: "ಹಿಂದಿನ ಎಚ್ಚರಿಕೆಗಳು, ಹೊಸದು ಮೊದಲು. ಈ ಫೋನ್‌ನಲ್ಲಿ ಮಾತ್ರ ಉಳಿಸಲಾಗಿದೆ.",
    historyEmpty: "ಇನ್ನೂ ಯಾವುದೇ ಎಚ್ಚರಿಕೆ ಇಲ್ಲ.",
    historyClear: "ಇತಿಹಾಸ ಅಳಿಸಿ",
    historyClearConfirm: "ಈ ಫೋನ್‌ನಲ್ಲಿ ಉಳಿಸಿದ ಎಲ್ಲಾ ಎಚ್ಚರಿಕೆಗಳನ್ನು ಅಳಿಸಬೇಕೆ?",
    guideTitle: "ಮೀನು ರೋಗ ಮಾರ್ಗದರ್ಶಿ",
    guideIntro: "ಗೆಂಡೆ ಮೀನಿನ ಕೊಳಗಳ ಸಾಮಾನ್ಯ ರೋಗಗಳು: ಗಮನಿಸಬೇಕಾದ ಲಕ್ಷಣಗಳು, ಅವು ಯಾವಾಗ ಬರುತ್ತವೆ ಮತ್ತು ಹೇಗೆ ತಡೆಯುವುದು.",
    guideLoading: "ಮಾರ್ಗದರ್ಶಿ ತೆರೆಯಲಾಗುತ್ತಿದೆ…",
    guideFailed: "ರೋಗ ಮಾರ್ಗದರ್ಶಿ ತೆರೆಯಲು ಆಗಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
    guideDrawing: "ಲಕ್ಷಣಗಳಿರುವ ಮೀನಿನ ಚಿತ್ರ",
    guideAgent: "ಕಾರಣ", guideBody: "ದೇಹದ ಮೇಲಿನ ಲಕ್ಷಣಗಳು", guideBehaviour: "ಮೀನುಗಳ ವರ್ತನೆ",
    guideWhen: "ಯಾವಾಗ ಹೆಚ್ಚು ಬರುತ್ತದೆ", guidePrevention: "ತಡೆಗಟ್ಟುವಿಕೆ", guideDo: "ಏನು ಮಾಡಬೇಕು",
    guideSourcesShort: "ಮೂಲಗಳು", guideRead: "ಇದರ ಬಗ್ಗೆ ಓದಿ", guideSources: "ಪ್ರತಿ ಮಾಹಿತಿಯ ಮೂಲಗಳು",
    checkerTitle: "ಲಕ್ಷಣ ಪರಿಶೀಲಕ",
    checkerHelp: "ನಿಮ್ಮ ಮೀನುಗಳಲ್ಲಿ ಕಾಣುವ ಲಕ್ಷಣಗಳನ್ನು ಗುರುತಿಸಿ. ನಿಮಗೆ ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳು ಸಿಗುತ್ತವೆ, ರೋಗನಿರ್ಣಯವಲ್ಲ.",
    checkerBody: "ದೇಹದ ಮೇಲೆ", checkerBehaviour: "ಮೀನುಗಳ ವರ್ತನೆ",
    checkerCheck: "ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳನ್ನು ತೋರಿಸಿ", checkerClear: "ಅಳಿಸಿ",
    checkerEmpty: "ಕನಿಷ್ಠ ಒಂದು ಲಕ್ಷಣ ಗುರುತಿಸಿ.",
    checkerMatches: "ಸಾಧ್ಯವಿರುವ ಹೊಂದಾಣಿಕೆಗಳು", checkerMatched: "ಹೊಂದುವ ಲಕ್ಷಣಗಳು",
    checkerMore: (n) => `ಇನ್ನೂ ${n} ರೋಗಗಳು ನಿಮ್ಮ ಕಡಿಮೆ ಲಕ್ಷಣಗಳಿಗೆ ಹೊಂದುತ್ತವೆ.`,
    libraryTitle: "ರೋಗಗಳ ಪಟ್ಟಿ", libraryHelp: "ಹೆಚ್ಚು ಓದಲು ಒಂದು ರೋಗದ ಮೇಲೆ ಒತ್ತಿ.",
    noPhotoTitle: "ಫೋಟೋ ಪರಿಶೀಲನೆ ಏಕೆ ಇಲ್ಲ",
    noPhotoText: "ಮೀನಿನ ಫೋಟೋದಿಂದ ರೋಗವನ್ನು ಊಹಿಸುವ ಕಂಪ್ಯೂಟರ್ ಮಾದರಿಯನ್ನು ನಾವು ಪರೀಕ್ಷಿಸಿದೆವು. ಸಾರ್ವಜನಿಕ ಫೋಟೋಗಳು ಹೆಚ್ಚಾಗಿ ಅಕ್ವೇರಿಯಂ ಮೀನುಗಳದ್ದು, ಕೊಳದ ಗೆಂಡೆ ಮೀನುಗಳದ್ದಲ್ಲ, ಮತ್ತು ಮಾದರಿ ಸುಮಾರು ಮೂರರಲ್ಲಿ ಒಂದು ಬಾರಿ ತಪ್ಪಾಗಿತ್ತು. ಇದು ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ಸಾಕಷ್ಟು ಸುರಕ್ಷಿತವಲ್ಲ, ಆದ್ದರಿಂದ ಆ್ಯಪ್ ಇದನ್ನು ಮಾಡುವುದಿಲ್ಲ.",
    noPhotoLink: "ಪರೀಕ್ಷೆಯ ಫಲಿತಾಂಶಗಳನ್ನು ನೋಡಿ",
    likelyTitle: "ಈಗ ಹೆಚ್ಚು ಸಾಧ್ಯತೆಯಿರುವ ರೋಗಗಳು",
    likelyNote: "ಇದರ ಅರ್ಥ ನಿಮ್ಮ ಮೀನುಗಳಿಗೆ ರೋಗ ಬಂದಿದೆ ಎಂದಲ್ಲ. ಅವುಗಳನ್ನು ಗಮನವಿಟ್ಟು ನೋಡಿ, ಲಕ್ಷಣಗಳು ಕಂಡರೆ ಮೀನು ರೋಗ ಮಾರ್ಗದರ್ಶಿ ಬಳಸಿ.",
    assistantTitle: "ಮೀನುರಕ್ಷಾವನ್ನು ಕೇಳಿ", assistantLabel: "AI ಸಹಾಯಕ: ತಪ್ಪುಗಳಾಗಬಹುದು",
    assistantHelp: "ನಿಮ್ಮ ಅಳತೆಗಳು, ಸುರಕ್ಷಿತ ಮಟ್ಟಗಳು, ಇಂದು ರಾತ್ರಿಯ ಹವಾಮಾನ ಅಥವಾ ಮೀನು ರೋಗಗಳ ಬಗ್ಗೆ ಕೇಳಿ. ಉತ್ತರಗಳು ಈ ಆ್ಯಪ್‌ನ ಸ್ವಂತ ಮಾಹಿತಿಯಿಂದ ಮಾತ್ರ ಬರುತ್ತವೆ.",
    assistantPrivacy: "ನಿಮ್ಮ ಹೆಸರು, ಫೋನ್ ಸಂಖ್ಯೆ ಅಥವಾ ಇತರ ವೈಯಕ್ತಿಕ ವಿವರಗಳನ್ನು ಬರೆಯಬೇಡಿ.",
    assistantSuggested: "ಸೂಚಿಸಿದ ಪ್ರಶ್ನೆಗಳು (ಸಿದ್ಧ ಉತ್ತರಗಳು)",
    assistantAsk: "ನಿಮ್ಮ ಪ್ರಶ್ನೆ", assistantSend: "ಪ್ರಶ್ನೆ ಕೇಳಿ", assistantYou: "ನೀವು",
    assistantThinking: "ಯೋಚಿಸುತ್ತಿದೆ…",
    assistantAiAnswer: "AI ಉತ್ತರ", assistantReady: "ಆ್ಯಪ್‌ನ ಸಿದ್ಧ ಉತ್ತರ", assistantSafety: "ಆ್ಯಪ್‌ನ ಸುರಕ್ಷತಾ ಉತ್ತರ",
    assistantListen: "ಆಲಿಸಿ", assistantNotice: "ಆ್ಯಪ್‌ನ ಸಂದೇಶ",
    assistantEmpty: "ಮೊದಲು ಪ್ರಶ್ನೆ ಬರೆಯಿರಿ, ಅಥವಾ ಸೂಚಿಸಿದ ಪ್ರಶ್ನೆಯೊಂದನ್ನು ಒತ್ತಿ.",
    assistantFailed: "ಆ್ಯಪ್ ಸರ್ವರ್ ತಲುಪಲು ಆಗಲಿಲ್ಲ. ಸಿದ್ಧ ಉತ್ತರಕ್ಕಾಗಿ ಸೂಚಿಸಿದ ಪ್ರಶ್ನೆಯೊಂದನ್ನು ಒತ್ತಿ.",
    historyKit: "ಟೆಸ್ಟ್ ಕಿಟ್",
    historySensor: "ಲೈವ್ ಸೆನ್ಸರ್", historyDemo: "ಡೆಮೊ ಸಾಧನ",
    historySimTime: "ಅನುಕರಿಸಿದ ಸಮಯ",
    historyActionTaken: "ತೆಗೆದುಕೊಂಡ ಕ್ರಮ:",
    historyNoAction: "ಇನ್ನೂ ಯಾವುದೇ ಕ್ರಮವನ್ನು ಗುರುತಿಸಿಲ್ಲ.",
  },
};

// Order, units and number format of the reading cards.
const PARAMETERS = [
  ["dissolved_oxygen", "mg/L", 1],
  ["ph", "", 2],
  ["temperature", "°C", 1],
  ["ammonia", "mg/L", 3],
  ["nitrate", "mg/L", 1],
  ["turbidity", "NTU", 1],
];

// Loading state: a small fish circling a water drop (CSS animation, so it
// stops by itself when the loader is replaced or hidden; still with "reduce motion").
const LOADER = '<svg class="orbit-loader" viewBox="0 0 40 40" aria-hidden="true" focusable="false"><circle class="ol-path" cx="20" cy="21" r="15"/><path class="ol-drop" d="M20 11c0 0 6.5 7.2 6.5 11.6a6.5 6.5 0 0 1-13 0C13.5 18.2 20 11 20 11Z"/><g class="ol-fish"><path d="M26.5 6C24.4 3.5 20.8 3.1 18.2 4.4 17.2 4.9 16.6 5.6 16.2 6c.4.4 1 1.1 2 1.6 2.6 1.3 6.2.9 8.3-1.6ZM16.2 6 13 3.6l.7 2.4-.7 2.4Z"/></g></svg>';

const ICONS = {
  safe: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20Zm-1.5 14.5-4-4 1.4-1.4 2.6 2.6 5.6-5.6 1.4 1.4-7 7Z"/></svg>',
  warning: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M1 21h22L12 2 1 21Zm12-3h-2v-2h2v2Zm0-4h-2v-4h2v4Z"/></svg>',
  danger: '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M15.7 3H8.3L3 8.3v7.4L8.3 21h7.4l5.3-5.3V8.3L15.7 3ZM13 17h-2v-2h2v2Zm0-4h-2V7h2v6Z"/></svg>',
  unknown: "",
};

const LEVEL_WORDS = {
  safe: { en: "Safe", kn: "ಸುರಕ್ಷಿತ" },
  warning: { en: "Warning", kn: "ಎಚ್ಚರಿಕೆ" },
  danger: { en: "Danger", kn: "ಅಪಾಯ" },
  unknown: { en: "Unknown", kn: "ತಿಳಿದಿಲ್ಲ" },
};

const state = {
  lang: "kn", source: null, paused: false, last: null,
  station: "station1", level: null, chartTime: null, effectsReady: false,
  weather: null,
  manual: null, alertChannel: "sms", alertSource: "simulated",
  live: null, liveSource: null, liveStation: null, liveOffset: 0, liveLost: false,
  history: [], historyKey: {}, voiceNote: null,
};

const $ = (id) => document.getElementById(id);
const M = window.Motion;
const H = window.AlertHistory;
const V = window.VoiceAlert;

// ---------------------------------------------------------------- language

function loadLanguage() {
  try { return localStorage.getItem("meenuraksha-lang") || "kn"; } catch { return "kn"; }
}

function levelWords(lang) {
  return { safe: LEVEL_WORDS.safe[lang], warning: LEVEL_WORDS.warning[lang], danger: LEVEL_WORDS.danger[lang] };
}

function setLanguage(lang) {
  if (state.lang !== lang) { V.stop(); state.voiceNote = null; }   // don't keep talking in the old language
  state.lang = lang;
  try { localStorage.setItem("meenuraksha-lang", lang); } catch { /* storage blocked: ignore */ }
  document.documentElement.lang = lang;
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    el.textContent = TEXT[lang][el.dataset.i18n];
  });
  document.querySelectorAll(".language-toggle button[data-lang]").forEach((b) => {
    b.setAttribute("aria-pressed", String(b.dataset.lang === lang));
  });
  $("pause").textContent = TEXT[lang][state.paused ? "resume" : "pause"];
  if (state.effectsReady) {
    window.RiskGauge.setWords(levelWords(lang));
    window.DOChart.setWords(levelWords(lang));
    // Headings re-appear word by word in the new language (feedback for the switch).
    document.querySelectorAll("#dashboard .text-effect").forEach((h) => M.textEffect(h));
    moveHighlight(true);                       // option widths change with the language
    window.Scene.setLanguage(lang);
  }
  if (state.last) render(state.last);
  renderWeather();
  renderManual();
  renderLive();
  renderAlert();
  window.DiseaseGuide.render(lang, TEXT[lang]);
  window.Assistant.setLanguage(lang, TEXT[lang]);
  if (!state.last) renderHealth(null, "unknown", lang);
  renderHistory();
  renderVoice();
}

// ---------------------------------------------------------------- theme (light / dark)
// The first theme is set before the page paints (small script in index.html):
// the saved choice, else the phone's setting. The toggle saves the farmer's choice.

const THEME_KEY = "meenuraksha-theme";
const lightQuery = window.matchMedia("(prefers-color-scheme: light)");

function savedTheme() {
  try { const t = localStorage.getItem(THEME_KEY); return t === "light" || t === "dark" ? t : null; } catch { return null; }
}

function setTheme(theme, save) {
  document.documentElement.setAttribute("data-theme", theme);
  if (save) { try { localStorage.setItem(THEME_KEY, theme); } catch { /* storage blocked: ignore */ } }
  document.querySelectorAll("#theme-toggle button").forEach((b) => {
    b.setAttribute("aria-pressed", String(b.dataset.themeChoice === theme));
  });
  // Browser bar colour on phones follows the page background.
  const background = getComputedStyle(document.documentElement).getPropertyValue("--background").trim();
  document.querySelector('meta[name="theme-color"]').setAttribute("content", background);
  if (state.effectsReady) window.DOChart.restyle();   // the chart draws on a canvas: it needs the new colours
}

// ---------------------------------------------------------------- helpers

function formatTime(iso) {
  const d = new Date(iso);
  const date = d.toLocaleDateString(state.lang === "kn" ? "kn-IN" : "en-IN", { day: "numeric", month: "short" });
  return `${date}, ${clock(d)}`;
}

function clock(d) {
  return d.toLocaleTimeString("en-GB", { hour: "2-digit", minute: "2-digit" });
}

function badgeHTML(level, lang) {
  return `${ICONS[level] || ""}${LEVEL_WORDS[level][lang]}`;
}

// Rebuild a badge only when its level or language changes, not on every reading
// (less work per second on cheap phones).
function setBadge(el, level, lang, className) {
  const key = `${level}|${lang}`;
  if (el.dataset.key === key) return;
  el.dataset.key = key;
  el.className = className;
  if (level === "info") el.textContent = TEXT[lang].infoOnly;
  else el.innerHTML = level === "unknown" ? "" : badgeHTML(level, lang);
}

// ---------------------------------------------------------------- reading cards (built once, updated in place)

const cards = {};

function buildReadingCards() {
  const box = $("readings");
  for (const [parameter, unit] of PARAMETERS) {
    const card = document.createElement("article");
    card.className = "reading in-view";
    card.hidden = true;
    card.innerHTML =
      `<span class="reading-name"></span>` +
      `<span class="reading-value"><span class="reading-number">-</span><span class="reading-unit">${unit}</span></span>` +
      `<span class="badge"></span>`;
    box.append(card);
    cards[parameter] = {
      card,
      name: card.querySelector(".reading-name"),
      number: card.querySelector(".reading-number"),
      badge: card.querySelector(".badge"),
    };
  }
}

function renderReadings(data, lang) {
  const risk = data.risk;
  const graded = Object.fromEntries(risk.parameters.map((p) => [p.parameter, p]));
  const info = Object.fromEntries(risk.info.map((p) => [p.parameter, p]));
  for (const [parameter, , decimals] of PARAMETERS) {
    const c = cards[parameter];
    const result = graded[parameter] || info[parameter];
    c.card.hidden = !result;
    if (!result) continue;
    const level = graded[parameter] ? result.level : "info";
    if (!c.card.classList.contains(`level-${level}`)) c.card.className = `reading in-view level-${level}`;
    c.name.textContent = result.name[lang];
    // Animated Number: the value counts to the new reading.
    M.animateNumber(c.number, data.reading[parameter], (v) => v.toFixed(decimals));
    setBadge(c.badge, level, lang, `badge badge-${level}`);
  }
}

// ---------------------------------------------------------------- status, pond view, gauge, countdown, chart

function renderStatus(risk, lang) {
  const banner = $("status");
  const changed = state.level !== null && state.level !== risk.level;
  banner.className = `status-banner status-${risk.level}`;
  banner.setAttribute("role", risk.level === "danger" ? "alert" : "status");
  $("status-icon").innerHTML = ICONS[risk.level] || "";
  $("status-level").textContent = risk.level_name[lang];
  $("status-summary").textContent = risk.summary[lang];
  // Smooth change of level: colours cross-fade (CSS), the words settle in.
  if (changed && !M.reduce()) {
    M.gsap.fromTo(["#status-icon", "#status-text"], { opacity: 0, y: 6 },
      { opacity: 1, y: 0, duration: 0.5, ease: "power2.out", stagger: 0.05, overwrite: "auto" });
  }
  state.level = risk.level;
}

function renderPondAndGauge(level, lang) {
  window.PondView.setLevel(level);
  window.RiskGauge.setLevel(level);
  const badge = $("pond-view-badge");
  setBadge(badge, level, lang, `badge badge-${level}`);
  badge.hidden = level === "unknown";
  $("pond-view-text").textContent = TEXT[lang].pondCaption[level] || TEXT[lang].pondCaption.unknown;
  setBadge($("gauge-label"), level, lang, `gauge-label gauge-label-${level}`);
}

function renderCountdown(ttd, level, lang) {
  const box = $("countdown");
  const expected = ttd.status === "danger_expected";
  box.hidden = !expected;
  box.classList.toggle("countdown-urgent", expected && level === "warning");
  if (!expected) return;
  // Same rounding as the message: to the nearest 10 minutes.
  const minutes = Math.max(10, Math.round((ttd.hours_to_danger * 60) / 10) * 10);
  M.animateNumber($("countdown-value"), minutes, (v) => {
    const m = Math.round(v / 10) * 10;
    return TEXT[state.lang].duration(Math.floor(m / 60), m % 60);
  }, 0.8);
  const at = new Date(ttd.danger_at);
  at.setMinutes(Math.round(at.getMinutes() / 10) * 10, 0, 0);
  $("countdown-at").textContent = TEXT[lang].around(clock(at));
}

function renderChart(data, lang) {
  if (state.chartTime !== data.time) {          // one point per reading, not per re-render
    state.chartTime = data.time;
    window.DOChart.add(clock(new Date(data.time)), data.reading.dissolved_oxygen);
  }
  const values = (window.DOChart.values && window.DOChart.values()) || [];
  const now = data.reading.dissolved_oxygen;
  const min = values.length ? Math.min(...values) : now;
  $("chart-summary").textContent = now == null ? "" : TEXT[lang].chartSummary(now.toFixed(1), min.toFixed(1));
}

function render(data) {
  const lang = state.lang;
  const risk = data.risk;
  $("simulated-label").textContent = data.label[lang];
  $("sim-time").textContent = formatTime(data.time);
  window.Scene.setTime(data.time, lang);        // sky follows the simulated time of day

  renderStatus(risk, lang);
  renderPondAndGauge(risk.level, lang);
  renderHealth(risk.health_score, risk.level, lang);
  recordHistory(data);

  const ttd = data.time_to_danger;
  renderCountdown(ttd, risk.level, lang);
  const ttdEl = $("ttd-message");
  ttdEl.textContent = ttd.message[lang];
  ttdEl.classList.toggle("ttd-alert", ttd.status === "danger_expected" || ttd.status === "already_danger");

  renderChart(data, lang);
  renderReadings(data, lang);

  const errors = risk.sensor_errors.map((e) => e.message[lang]);
  $("sensor-errors").hidden = errors.length === 0;
  $("sensor-errors").textContent = errors.join(" ");

  window.DiseaseGuide.renderLikely($("likely-box"), risk.likely_diseases, lang, TEXT[lang]);
  $("likely-card").hidden = $("likely-box").hidden;

  const box = $("actions-card");
  box.hidden = !risk.actions || risk.actions.length === 0;
  if (!box.hidden) renderChecklist($("action-list"), $("actions-progress"), risk, data.source, lang);
  renderAlert();
  $("voice-button").disabled = false;
}

// ---------------------------------------------------------------- action checklist (Warning and Danger)
// Rebuilt only when the problem changes, not on every reading, so ticks and
// keyboard focus stay put. Ticks are remembered in this browser per problem:
// a new alert (different level or cause) starts a fresh list.

function checklistKey(risk, source) {
  return `${source}|${risk.level}|${risk.actions.map((a) => a.id).join(",")}`;
}

function loadTicks(key) {
  try { return new Set(JSON.parse(localStorage.getItem(`meenuraksha-ticks:${key}`)) || []); } catch { return new Set(); }
}

const MAX_TICK_LISTS = 30;        // ticks are kept for the last 30 different alerts only

function saveTicks(key, ticks) {
  try {
    localStorage.setItem(`meenuraksha-ticks:${key}`, JSON.stringify([...ticks]));
    const keys = [];
    for (let i = 0; i < localStorage.length; i++) {
      const k = localStorage.key(i);
      if (k.startsWith("meenuraksha-ticks:")) keys.push(k);
    }
    // localStorage has no dates; drop the extra lists that aren't the one just saved.
    keys.filter((k) => k !== `meenuraksha-ticks:${key}`).slice(0, Math.max(0, keys.length - MAX_TICK_LISTS))
      .forEach((k) => localStorage.removeItem(k));
  } catch { /* storage blocked */ }
}

function renderChecklist(list, progress, risk, source, lang) {
  const key = checklistKey(risk, source);
  if (list.dataset.key === `${key}|${lang}`) return;
  list.dataset.key = `${key}|${lang}`;
  const ticks = loadTicks(key);
  const total = risk.actions.length;
  const update = () => { progress.textContent = TEXT[state.lang].actionsProgress(ticks.size, total); };
  list.replaceChildren(...risk.actions.map((action) => {
    const item = document.createElement("li");
    item.innerHTML =
      `<label class="action-item"><input type="checkbox">` +
      `<span class="action-box" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="m5 12.5 4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>` +
      `<span class="action-text"></span></label>`;
    item.querySelector(".action-text").textContent = action[lang];
    const box = item.querySelector("input");
    box.checked = ticks.has(action.id);
    box.addEventListener("change", () => {
      if (box.checked) ticks.add(action.id); else ticks.delete(action.id);
      saveTicks(key, ticks);
      update();
      state.history = H.markDone(state.history, key, ticks);   // ticks = "action taken" in the history
      H.save(state.history);
      renderHistory();
    });
    return item;
  }));
  update();
}

// ---------------------------------------------------------------- SMS / WhatsApp preview (nothing is sent)

function escapeHTML(text) {
  return text.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);
}

// WhatsApp shows *bold* and _italic_; SMS is plain text.
function whatsappHTML(text) {
  return escapeHTML(text).replace(/\*([^*\n]+)\*/g, "<strong>$1</strong>").replace(/_([^_\n]+)_/g, "<em>$1</em>");
}

function renderAlert() {
  const lang = state.lang;
  const data = state.alertSource === "manual" ? state.manual
    : state.alertSource === "live_sensor" ? state.live && state.live.latest : state.last;
  const channel = state.alertChannel;
  const bubble = $("alert-bubble");
  const text = data && data.alert ? data.alert[channel][lang] : TEXT[lang].connecting;
  const key = `${channel}|${text}`;
  $("phone-app").textContent = `${channel === "sms" ? "SMS" : "WhatsApp"} · ${TEXT[lang].appName}`;
  $("phone-time").textContent = data ? clock(new Date(data.time)) : "";
  if (bubble.dataset.key === key) return;
  bubble.dataset.key = key;
  bubble.className = `bubble bubble-${channel}${data && data.alert && !data.alert.send ? " bubble-none" : ""}`;
  if (channel === "whatsapp") bubble.innerHTML = whatsappHTML(text);
  else bubble.textContent = text;
}

function pick(groupId, attribute, value) {
  document.querySelectorAll(`#${groupId} button`).forEach((b) => {
    b.setAttribute("aria-pressed", String(b.dataset[attribute] === value));
  });
}

// ---------------------------------------------------------------- manual test-kit entry
// Graded by the same classifier on the server (POST /api/manual). Always shown
// with the "Manual test-kit reading" label, separate from the simulated pond.

const KIT_FIELDS = ["dissolved_oxygen", "ph", "temperature", "ammonia"];

function showKitError(key) {
  const el = $("kit-form-error");
  el.hidden = !key;
  el.dataset.key = key || "";
  el.textContent = key ? TEXT[state.lang][key] : "";
}

async function submitKit(event) {
  event.preventDefault();
  const form = $("kit-form");
  const values = {};
  for (const name of KIT_FIELDS) {
    const input = form.elements[name];
    if (input.validity.badInput) { showKitError("kitBadNumber"); input.focus(); return; }
    if (input.value.trim() !== "") values[name] = Number(input.value);
  }
  if (Object.keys(values).length === 0) { showKitError("kitEmpty"); form.elements.dissolved_oxygen.focus(); return; }
  showKitError(null);
  try {
    const response = await fetch("/api/manual", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(values),
    });
    if (!response.ok) throw new Error(response.statusText);
    state.manual = await response.json();
  } catch {
    showKitError("kitFailed");
    return;
  }
  $("alert-source-picker").querySelector('[data-source="manual"]').disabled = false;
  state.historyKey.manual = null;               // every test-kit check is its own event
  recordHistory(state.manual);
  renderManual();
  renderAlert();
  $("kit-status").focus();
}

function renderManual() {
  const errorEl = $("kit-form-error");
  if (errorEl.dataset.key) errorEl.textContent = TEXT[state.lang][errorEl.dataset.key];
  const data = state.manual;
  $("kit-result").hidden = !data;
  if (!data) return;
  const lang = state.lang;
  const risk = data.risk;
  $("kit-label").textContent = data.label[lang];
  $("kit-time").textContent = ` · ${formatTime(data.time)}`;
  $("kit-status").className = `status-banner status-${risk.level}`;
  $("kit-status-icon").innerHTML = ICONS[risk.level] || "";
  $("kit-status-level").textContent = risk.level_name[lang];
  $("kit-status-summary").textContent = risk.summary[lang];
  const errors = risk.sensor_errors.map((e) => e.message[lang]);
  $("kit-errors").hidden = errors.length === 0;
  $("kit-errors").textContent = errors.join(" ");
  window.DiseaseGuide.renderLikely($("kit-likely"), risk.likely_diseases, lang, TEXT[lang]);
  const hasActions = risk.actions.length > 0;
  $("kit-actions-box").hidden = !hasActions;
  if (hasActions) renderChecklist($("kit-action-list"), $("kit-actions-progress"), risk, data.source, lang);
}

// ---------------------------------------------------------------- live sensor (real readings, not simulated)
// Readings a real sensor sends to POST /api/sensor/{pond}. The server pushes
// each one here straight away (Server-Sent Events). Always shown with the
// "Live sensor" label, apart from the simulated pond; readings from a demo
// device (tools/fake_sensor.py) also get the "Demo device" tag.

const LIVE_STALE_SECONDS = 60;     // no reading for a minute: ask the farmer to check the sensor

function connectLive() {
  if (state.liveSource && state.liveStation === state.station) return;
  if (state.liveSource) state.liveSource.close();
  state.liveStation = state.station;
  state.live = null;
  state.liveLost = false;
  const source = new EventSource(`/api/sensor/${state.station.replace("station", "pond")}/stream`);
  // The age of a reading is measured with the server's clock, not the phone's.
  const syncClock = (serverTime) => { state.liveOffset = Date.parse(serverTime) - Date.now(); };
  source.addEventListener("sensor", (event) => {
    state.live = JSON.parse(event.data);
    state.liveLost = false;
    syncClock(state.live.server_time);
    const latest = state.live.latest;
    const button = $("alert-source-picker").querySelector('[data-source="live_sensor"]');
    button.disabled = !latest;
    if (!latest && state.alertSource === "live_sensor") {   // new pond has no sensor reading yet
      state.alertSource = "simulated";
      pick("alert-source-picker", "source", "simulated");
    }
    if (latest) recordHistory(latest);
    renderLive();
    renderAlert();
  });
  source.addEventListener("ping", (event) => {
    syncClock(JSON.parse(event.data).server_time);
    state.liveLost = false;
    renderLive();
  });
  // The browser reconnects by itself; the server then sends the current state again.
  source.onerror = () => { state.liveLost = true; renderLive(); };
  state.liveSource = source;
}

function liveAgeSeconds(latest) {
  return Math.max(0, Math.round((Date.now() + state.liveOffset - Date.parse(latest.received_at)) / 1000));
}

function liveValue(parameter, latest, lang) {
  const [, unit, decimals] = PARAMETERS.find(([p]) => p === parameter);
  const result = latest.risk.parameters.find((p) => p.parameter === parameter);
  const row = make("div", "live-value");
  const value = make("dd", "", `${latest.reading[parameter].toFixed(decimals)}${unit ? ` ${unit}` : ""}`);
  if (result && LEVEL_WORDS[result.level] && result.level !== "unknown") {
    const badge = make("span", `badge badge-${result.level}`);
    badge.innerHTML = badgeHTML(result.level, lang);
    value.append(" ", badge);
  }
  row.append(make("dt", "", result ? result.name[lang] : parameter), value);
  return row;
}

function renderLive() {
  const lang = state.lang;
  const t = TEXT[lang];
  const live = state.live;
  const latest = live && live.latest;
  const pondName = t[state.station.replace("station", "pond")];
  $("live-label").textContent = live ? live.label[lang] : t.liveTitle;
  $("live-pond").textContent = ` · ${pondName}`;

  $("live-waiting").hidden = Boolean(latest);
  $("live-waiting").textContent = live ? t.liveNoReading(pondName) : t.liveWaiting;
  $("live-result").hidden = !latest;
  $("live-demo").hidden = !(latest && latest.demo);
  if (latest && latest.demo) $("live-demo").textContent = latest.demo_label[lang];

  const age = latest ? liveAgeSeconds(latest) : 0;
  const stale = Boolean(latest) && age > LIVE_STALE_SECONDS;
  $("live-dot").classList.toggle("live-dot-on", Boolean(latest) && !stale && !state.liveLost);
  const staleEl = $("live-stale");
  staleEl.hidden = !(state.liveLost || stale);
  staleEl.textContent = state.liveLost ? t.liveLost : stale ? t.liveStale(Math.floor(age / 60)) : "";

  const rejected = live && live.rejected;
  $("live-errors").hidden = !rejected;
  if (rejected) {
    $("live-errors").textContent = [rejected.message[lang], ...rejected.sensor_errors.map((e) => e.message[lang])].join(" ");
  }
  if (!latest) return;

  const risk = latest.risk;
  $("live-status").className = `status-banner status-${risk.level}`;
  $("live-status-icon").innerHTML = ICONS[risk.level] || "";
  $("live-status-level").textContent = risk.level_name[lang];
  $("live-status-summary").textContent = risk.summary[lang];
  const order = PARAMETERS.map(([p]) => p).filter((p) => p in latest.reading);
  $("live-values").replaceChildren(...order.map((p) => liveValue(p, latest, lang)));
  window.DiseaseGuide.renderLikely($("live-likely"), risk.likely_diseases, lang, TEXT[lang]);
  const seconds = String(new Date(latest.time).getSeconds()).padStart(2, "0");   // readings come seconds apart
  $("live-time").textContent = t.liveMeasured(`${formatTime(latest.time)}:${seconds}`, t.liveAgo(age));
  const hasActions = risk.actions.length > 0;
  $("live-actions-box").hidden = !hasActions;
  if (hasActions) renderChecklist($("live-action-list"), $("live-actions-progress"), risk, latest.source, lang);
}

function showMessage(key) {
  $("status").className = "status-banner status-unknown";
  $("status-icon").innerHTML = key === "connecting" ? LOADER : "";
  $("status-level").textContent = TEXT[state.lang][key];
  $("status-summary").textContent = "";
}

// ---------------------------------------------------------------- pond health score (0-100 ring)
// The score comes from the server (backend/health_score.py) and always sits
// inside its status's range, so it can never disagree with the banner.

function renderHealth(score, level, lang) {
  if (!state.effectsReady) return;
  const shown = score == null ? "unknown" : level;
  window.HealthRing.set(score, shown);
  const badge = $("health-badge");
  badge.hidden = shown === "unknown";
  if (!badge.hidden) setBadge(badge, shown, lang, `badge badge-${shown}`);
  $("health-text").textContent = TEXT[lang].healthText[shown](score);
}

// ---------------------------------------------------------------- alert history (saved in this browser)
// One entry each time a Warning or Danger alert starts (a new level or cause),
// for the simulated pond and for test-kit checks. Ticked actions are stored
// as "action taken".

function recordHistory(data) {
  const risk = data.risk;
  if (risk.level !== "warning" && risk.level !== "danger") {
    state.historyKey[data.source] = null;        // back to Safe: the next warning is a new event
    return;
  }
  const key = checklistKey(risk, data.source);
  const eventKey = `${data.station || ""}|${key}`;
  if (state.historyKey[data.source] === eventKey) return;
  state.historyKey[data.source] = eventKey;
  const entry = { ...H.entryFrom(data, key), done: [...loadTicks(key)] };
  state.history = H.addEntry(state.history, entry);
  H.save(state.history);
  renderHistory();
}

function make(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function historyItem(entry, lang) {
  const t = TEXT[lang];
  const simulated = entry.source === "simulated";
  const item = make("li", `history-item level-${entry.level}`);
  const meta = make("div", "history-meta");
  const badge = make("span", `badge badge-${entry.level}`);
  badge.innerHTML = badgeHTML(entry.level, lang);
  meta.append(badge, make("span", "history-time",
    simulated ? `${t.historySimTime}: ${formatTime(entry.time)}` : formatTime(entry.time)));
  if (entry.station) meta.append(make("span", "history-where", t[entry.station.replace("station", "pond")] || entry.station));
  if (simulated) meta.append(make("span", "sim-tag", t.simulatedTag));
  else if (entry.source === "live_sensor") {
    meta.append(make("span", "badge badge-info", t.historySensor));
    if (entry.demo) meta.append(make("span", "sim-tag", t.historyDemo));
  } else meta.append(make("span", "badge badge-info", t.historyKit));

  const actions = make("div", "history-actions");
  actions.append(make("strong", "", `${t.historyActionTaken} `));
  const done = entry.actions.filter((a) => entry.done.includes(a.id));
  if (done.length) {
    const list = make("ul");
    list.append(...done.map((a) => make("li", "", a[lang])));
    actions.append(list);
  } else {
    actions.append(t.historyNoAction);
  }
  item.append(meta, make("p", "history-cause", entry.summary[lang]), actions);
  return item;
}

function renderHistory() {
  $("history-list").replaceChildren(...state.history.map((e) => historyItem(e, state.lang)));
  $("history-empty").hidden = state.history.length > 0;
  $("history-clear").hidden = state.history.length === 0;
}

function clearHistory() {
  if (!window.confirm(TEXT[state.lang].historyClearConfirm)) return;
  state.history = [];
  state.historyKey = {};
  H.save(state.history);
  renderHistory();
}

// ---------------------------------------------------------------- voice alert (plays only when tapped)

// What is read aloud: "Simulated data. Pond 1. Danger. <reason>. <time until danger>."
function alertSpeech(data, lang) {
  const risk = data.risk;
  const parts = [data.label[lang], TEXT[lang][data.station.replace("station", "pond")],
    risk.level_name[lang], risk.summary[lang]];
  const ttd = data.time_to_danger;
  if (ttd && (ttd.status === "danger_expected" || ttd.status === "already_danger")) parts.push(ttd.message[lang]);
  return parts.filter(Boolean).map((p) => p.trim().replace(/[.।]$/, "")).join(". ") + ".";
}

function setVoiceButton(on) {
  $("voice-button").setAttribute("aria-pressed", String(on));
  $("voice-button-text").textContent = TEXT[state.lang][on ? "voiceStop" : "voiceListen"];
}

function renderVoice() {
  setVoiceButton($("voice-button").getAttribute("aria-pressed") === "true" && V.speaking());
  $("voice-button").disabled = !state.last;
  const note = $("voice-note");
  note.hidden = !state.voiceNote;
  note.textContent = state.voiceNote ? TEXT[state.lang][state.voiceNote] : "";
}

async function toggleVoice() {
  if ($("voice-button").getAttribute("aria-pressed") === "true") {
    V.stop();
    setVoiceButton(false);
    return;
  }
  if (!state.last) return;
  const lang = state.lang;
  const result = await V.speak(alertSpeech(state.last, lang), lang, () => setVoiceButton(false));
  // Never fall back to another language: say politely why nothing plays.
  state.voiceNote = result === "unsupported" ? "voiceUnsupported"
    : result === "no-voice" ? (lang === "kn" ? "voiceNoKannada" : "voiceNoEnglish") : null;
  setVoiceButton(result === "started");
  renderVoice();
}

// ---------------------------------------------------------------- tonight's weather (bottom toolbar)
// Real forecast, not simulated. The server falls back to its saved forecast when
// there is no internet; if even the server can't be reached, the copy saved in
// this browser is shown. Either way the note says "offline".

const WEATHER_KEY = "meenuraksha-weather";
const CRASH_BADGE = { low: "safe", medium: "warning", high: "danger" };   // same colour + icon pairs as the status

async function loadWeather() {
  try {
    const response = await fetch("/api/weather/tonight");
    if (!response.ok) throw new Error(response.statusText);
    state.weather = await response.json();
    if (state.weather.status === "ok") {
      try { localStorage.setItem(WEATHER_KEY, JSON.stringify(state.weather)); } catch { /* storage blocked */ }
    }
  } catch {
    let saved = null;
    try { saved = JSON.parse(localStorage.getItem(WEATHER_KEY)); } catch { /* nothing saved */ }
    state.weather = saved ? { ...saved, offline: true }
      : { status: "unavailable", offline: true, saved_at: null,
          message: { en: TEXT.en.weatherUnavailable, kn: TEXT.kn.weatherUnavailable } };
  }
  renderWeather();
}

function renderWeather() {
  const w = state.weather;
  if (!w) return;
  $("weather-loader").hidden = true;            // forecast (or saved copy) is here: moon instead of the loader
  $("weather-moon").removeAttribute("hidden");   // an <svg>: the .hidden property doesn't exist on it
  const lang = state.lang;
  const ok = w.status === "ok";
  const badge = $("weather-badge");
  badge.hidden = !ok;
  if (ok) {
    const level = CRASH_BADGE[w.level];
    badge.className = `badge weather-badge badge-${level}`;
    badge.innerHTML = `${ICONS[level]}${TEXT[lang].crashRisk(w.level_name[lang])}`;
  }
  $("weather-place").textContent = w.location ? ` · ${w.location[lang]}` : "";
  const message = $("weather-message");
  message.removeAttribute("data-i18n");
  message.textContent = w.message[lang];
  $("weather-details").textContent = ok
    ? TEXT[lang].weatherDetails(w.day_cloud_cover_pct, w.night_wind_speed_kmh, w.night_temperature_c) : "";
  const offline = $("weather-offline");
  offline.hidden = !w.offline;
  offline.textContent = TEXT[lang].weatherOffline(w.saved_at ? formatTime(w.saved_at) : null);
}

// ---------------------------------------------------------------- pond picker

function activePondButton() {
  return document.querySelector(`.pond-option[data-station="${state.station}"]`);
}

function moveHighlight(instant = false) {
  M.animatedBackground($("pond-highlight"), activePondButton(), instant);
}

function choosePond(station) {
  if (station === state.station) return;
  state.station = station;
  document.querySelectorAll(".pond-option").forEach((b) => {
    b.setAttribute("aria-pressed", String(b.dataset.station === station));
  });
  moveHighlight();                              // Animated Background slides to the new pond
  start();
}

// ---------------------------------------------------------------- effects (once, when the dashboard first shows)

function initEffects() {
  if (state.effectsReady) return;
  state.effectsReady = true;
  window.PondView.init($("pond-view"));
  window.RiskGauge.init($("gauge"));
  window.RiskGauge.setWords(levelWords(state.lang));
  window.DOChart.init($("do-chart"));
  window.DOChart.setWords(levelWords(state.lang));
  window.HealthRing.init($("health-ring"));
  window.Scene.init();                          // day/night sky + hand-drawn doodles
  window.CursorFX.init();                       // ripples, tilt, spotlight, magnetic buttons, tap ink
  moveHighlight(true);
  M.borderTrail($("pond-highlight"));           // Border Trail on the active pond card
  window.addEventListener("resize", () => moveHighlight(true));
  // In View: cards rise in as they scroll into view; their headings get the Text Effect.
  M.inView([...document.querySelectorAll("#dashboard .in-view")], (card) => {
    const heading = card.querySelector(".text-effect");
    if (heading) M.textEffect(heading);
  });
  renderPondAndGauge("unknown", state.lang);
  renderHealth(null, "unknown", state.lang);
  loadWeather();
  setInterval(loadWeather, 30 * 60 * 1000);     // the server re-downloads at most every 30 minutes
  setInterval(renderLive, 5000);                // "received 12 s ago" keeps counting between readings
}

// ---------------------------------------------------------------- stream

// Connect to the simulator stream. To resume a paused demo, pass the demo's
// original first reading time and how many readings were already shown:
// the scenario (e.g. when the night crash happens) is tied to that start time.
function connect(resume) {
  if (state.source) state.source.close();
  const params = new URLSearchParams({ station: state.station, scenario: $("scenario").value });
  if (resume) { params.set("start", resume.start); params.set("skip", String(resume.skip)); }
  const source = new EventSource(`/api/simulator/stream?${params}`);
  source.addEventListener("reading", (event) => {
    state.last = JSON.parse(event.data);
    if (!state.firstTime) state.firstTime = state.last.time;
    state.shown += 1;
    render(state.last);
  });
  source.addEventListener("end", () => { source.close(); showMessage("ended"); });
  source.onerror = () => { if (source.readyState === EventSource.CLOSED) showMessage("connectionLost"); };
  state.source = source;
}

// Restart the demo from the beginning (new pond, new scenario, Restart button).
function start() {
  initEffects();
  state.paused = false;
  state.last = null;
  state.level = null;
  state.chartTime = null;
  state.firstTime = null;
  state.shown = 0;
  state.historyKey.simulated = null;
  V.stop();
  state.voiceNote = null;
  window.DOChart.reset();
  $("pause").textContent = TEXT[state.lang].pause;
  showMessage("connecting");
  renderHealth(null, "unknown", state.lang);
  setVoiceButton(false);
  renderVoice();
  connect(null);
  connectLive();                                // live sensor of the chosen pond (stays open across Restart)
}

// Pause really stops the stream; Resume continues with the very next reading,
// so no readings are skipped while paused.
function togglePause() {
  state.paused = !state.paused;
  $("pause").textContent = TEXT[state.lang][state.paused ? "resume" : "pause"];
  if (state.paused) {
    if (state.source) state.source.close();
    state.source = null;
    return;
  }
  if (!state.firstTime) { start(); return; }
  connect({ start: state.firstTime, skip: state.shown });
}

// ---------------------------------------------------------------- wiring

buildReadingCards();
document.querySelectorAll(".language-toggle button[data-lang]").forEach((b) => {
  b.addEventListener("click", () => setLanguage(b.dataset.lang));
});
document.querySelectorAll(".pond-option").forEach((b) => {
  b.addEventListener("click", () => choosePond(b.dataset.station));
});
$("restart").addEventListener("click", start);
$("scenario").addEventListener("change", start);
$("pause").addEventListener("click", togglePause);
// Data sources panel (footer button). <dialog> gives Esc-to-close and keeps focus inside.
$("sources-open").addEventListener("click", () => $("sources-dialog").showModal());
$("sources-close").addEventListener("click", () => $("sources-dialog").close());
$("sources-dialog").addEventListener("click", (e) => {
  if (e.target === e.currentTarget) e.currentTarget.close();   // tap outside the panel closes it
});
$("kit-form").addEventListener("submit", submitKit);
$("kit-form").addEventListener("reset", () => showKitError(null));
$("kit-status").tabIndex = -1;
document.querySelectorAll("#channel-picker button").forEach((b) => {
  b.addEventListener("click", () => {
    state.alertChannel = b.dataset.channel;
    pick("channel-picker", "channel", b.dataset.channel);
    renderAlert();
  });
});
document.querySelectorAll("#alert-source-picker button").forEach((b) => {
  b.addEventListener("click", () => {
    state.alertSource = b.dataset.source;
    pick("alert-source-picker", "source", b.dataset.source);
    renderAlert();
  });
});

$("history-clear").addEventListener("click", clearHistory);
document.querySelectorAll("#theme-toggle button").forEach((b) => {
  b.addEventListener("click", () => setTheme(b.dataset.themeChoice, true));
});
// No saved choice yet: follow the phone if its light/dark setting changes.
lightQuery.addEventListener("change", (e) => { if (!savedTheme()) setTheme(e.matches ? "light" : "dark", false); });
setTheme(document.documentElement.getAttribute("data-theme") === "light" ? "light" : "dark", false);
$("voice-button").addEventListener("click", toggleVoice);
state.history = H.load();
window.DiseaseGuide.init(loadLanguage(), TEXT[loadLanguage()]);   // the guide works before Start, too
// The assistant gets the readings the page is showing; the server grades them again itself.
window.Assistant.init(() => ({
  station: state.station,
  simulated: state.last ? state.last.reading : null,
  manual: state.manual ? state.manual.reading : null,
  live_sensor: state.live && state.live.latest ? state.live.latest.reading : null,
}), loadLanguage(), TEXT[loadLanguage()]);

setLanguage(loadLanguage());

// The welcome screen (welcome.js) calls start() when the farmer presses Start.
// Without a welcome screen, start straight away.
window.MeenuRaksha = { start, setLanguage, historyCount: () => state.history.length };   // historyCount: for ?debug
if (!document.getElementById("welcome")) start();
