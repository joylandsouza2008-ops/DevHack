# Putting MeenuRaksha online (free)

Goal: one link the judges can open on a laptop or phone.

## Recommended host: Render (free web service)

| | Render free web service |
|---|---|
| Cost | Free. You only pay if you choose a paid plan or go over the free limits. |
| Runs | Our FastAPI app as-is (Python, `uvicorn`), set up by `render.yaml` in this repo |
| Link | `https://meenuraksha.onrender.com` (or similar if the name is taken) |
| **Sleeps when idle** | After **15 minutes with no visitors** the app goes to sleep. The next visitor waits **about 1 minute** while it wakes up, then it is fast again. |
| Hours | 750 free hours per month: enough for one app running all month |
| Files | Anything the app saves (the weather cache in `data/`) is lost when it sleeps or redeploys. That's fine: it just downloads the forecast again. |
| Updates | Every `git push` to `main` redeploys automatically (takes a few minutes) |
| Other | One instance only, no shell access, and Render may restart it at any time |

Source: [Render docs: Deploy for Free](https://render.com/docs/free) (checked 4 Oct 2026).

**Why Render?** The other common free options didn't fit (checked October 2026):

- **Koyeb**: its free Starter plan is being withdrawn for new users after its acquisition by Mistral AI. Paid plans start at $29/month.
- **Hugging Face Spaces**: a third-party comparison says Docker Spaces, which a FastAPI app needs, have needed a paid plan since July 2026. We couldn't confirm this in Hugging Face's own docs.
- **Vercel / Netlify**: built for websites and short functions, not a long-running server. Our live simulator stream would be cut off.

### Before the judging

- **Wake it up first.** Open the link 2–3 minutes before the judges do, so they don't see the 1-minute wait.
- Optional: to keep it awake all day, a free uptime checker (for example UptimeRobot) can open `https://<your-app>.onrender.com/api/health` every 10 minutes. One app running non-stop uses about 744 of the 750 free hours a month.

## What runs online

- The dashboard, the simulator, risk alerts, the test-kit form, the weather card (it downloads from Open-Meteo) and the alert preview all work online.
- The datasets are **not** online. `data/` is not in git, and the Pondsdata licence on Kaggle is listed as "Unknown", so we don't publish it or files made from it. Without it, the simulator uses fixed typical healthy pond levels (`FALLBACK_LEVELS` in `backend/simulator.py`, chosen by us). The day/night oxygen cycle, the Normal day / Night oxygen crash scenarios and all warnings work the same. Only the small day-to-day changes from the real dataset are missing.
- All readings are still labelled **"Simulated data" / "ಅನುಕರಿಸಿದ (ಸಿಮ್ಯುಲೇಟೆಡ್) ಡೇಟಾ"**.
- The saved DO forecast model (`models/`) isn't used by the app, so nothing changes there.

## Steps you need to do yourself (about 15 minutes)

1. **Push the code.** Make sure the latest code is on GitHub (`git push`). Render reads it from there.
2. **Create a Render account.**
   - Go to https://render.com and click **Get Started**.
   - Choose **Sign up with GitHub** and allow access. The GitHub account must be the one that owns the `DevHack` repository.
3. **Give Render access to the repository.**
   - When Render asks which repositories it may see, choose **Only select repositories** and pick **DevHack**.
   - If you skipped this, go to Render **Account Settings → GitHub → Configure**.
4. **Create the app from the blueprint.**
   - In the Render dashboard click **New + → Blueprint**.
   - Pick the **DevHack** repository and the `main` branch.
   - Render finds `render.yaml` and shows one web service called **meenuraksha** on the **Free** plan.
   - Click **Apply** (or **Deploy Blueprint**).
   - Check that the plan says **Free**. If Render asks for a card anyway, the free plan still costs nothing, but check with whoever owns the card first.
5. **Wait for the first build** (about 3–6 minutes).
   - Open the **meenuraksha** service and watch **Logs**.
   - It's done when you see `Your service is live` and the status turns green.
6. **Test the link.** Open the link at the top of the service page (`https://….onrender.com`) on your laptop and on your phone:
   - The welcome screen loads in Kannada. Tap **ಪ್ರಾರಂಭಿಸಿ** (Start).
   - The readings start moving and show the "Simulated data" tag.
   - Choose **Night oxygen crash** and the warning appears within about a minute.
   - The **Tonight's weather** card shows a forecast.
7. **Share the link** with the judges, and add it to the top of `README.md`.

### If something goes wrong

- **Build fails at `pip install` with a Python version error**: in `render.yaml`, change `PYTHON_VERSION` to `3.13.0`, commit and push.
- **The page shows "Connection lost"**: the free instance was probably asleep or restarted. Press **Restart** in the app.
- **"Service suspended"**: the 750 free hours ran out for the month (only possible with several apps on the same account). Delete unused services, or wait for the 1st of the month.
