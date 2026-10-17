# Setting up the PC side (Windows, PowerShell)

The bridge runs on your PC. It needs **Python 3.12**: `shazamio` crashes on Python 3.14
(the process dies with an access violation while importing it).

## 1. Install Python 3.12 (once)

```powershell
py -0                              # lists the Pythons you have; look for 3.12
winget install Python.Python.3.12  # only if 3.12 is missing, then reopen the terminal
```

## 2. Create the virtual environment (once per clone)

Run from the repo root:

```powershell
py -3.12 -m venv .venv
```

## 3. Get into the environment (every new terminal)

```powershell
.venv\Scripts\Activate.ps1
```

The prompt now starts with `(.venv)`. Check you are in the right one:

```powershell
python --version                   # should say 3.12.x
(Get-Command python).Source        # should point inside .venv\Scripts
```

Leave it with `deactivate`.

Using CMD instead of PowerShell: `.venv\Scripts\activate.bat`

You can also skip activating and call the environment's Python directly:

```powershell
.venv\Scripts\python bridge\bridge.py
```

## 4. Install the requirements (once, and again if requirements.txt changes)

```powershell
pip install -r requirements.txt        # just to run the bridge
pip install -r requirements-dev.txt    # also installs mpremote and esptool
```

To lock the exact versions once everything works: `pip freeze > requirements.lock.txt`

## 5. Create your settings file (once)

```powershell
Copy-Item .env.example .env
```

Open `.env` and fill in your values. No quotes, no `r"..."`. `.env` is ignored by git.

## 6. Run the bridge (every session)

1. Close anything that holds the serial port (Thonny, an `mpremote` REPL, a serial monitor).
2. Press **EN** on the ESP32 so it starts fresh.
3. In an activated terminal:

```powershell
python bridge\bridge.py
```

You should see `bridge running on COM5 (Ctrl-C to stop)`. Stop it with Ctrl-C before
using `mpremote` again, because only one program can use the port at a time.

## Putting code on the board

With the bridge stopped:

```powershell
cd hardware
mpremote connect COM5 fs cp main.py :main.py
mpremote connect COM5 fs cp sh1106.py :sh1106.py
mpremote connect COM5 fs cp -r src :
mpremote connect COM5 mip install ssd1306      # only needed once
```

Then press **EN**.

## Troubleshooting

| What you see | What it means | Fix |
|---|---|---|
| `Set-ExecutionPolicy ... overridden by a policy defined at a more specific scope` | A harmless message. Your effective policy already allows activation. | Ignore it, or just run the activate line without `Set-ExecutionPolicy`. |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | PowerShell is blocking the script. | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, then try again. |
| `No module named 'serial'` (or `requests`, `PIL`, ...) | You are in the wrong environment, or the requirements are not installed. | Check the prompt shows `(.venv)`, then `pip install -r requirements.txt`. |
| `Windows fatal exception: access violation` when importing shazamio | You are on Python 3.14. | Use the Python 3.12 environment above. |
| `could not open port 'COM5': Access is denied` | Another program is using the port. | Close Thonny, `mpremote` or any serial monitor, then retry. |
| `MUSICBOX_API_URL is missing` | There is no `.env`, or the name is misspelled. | Copy `.env.example` to `.env` and fill it in. |
| `warning: unknown key ...` in the bridge output | A setting name in `.env` is wrong. | Use the names from `.env.example`. |
| The box shows `No PC link` | The bridge is not running, crashed, or is waiting on something slow. | Look at the bridge terminal for an error line. |
