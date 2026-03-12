# Sugar Activity Developer Kit 🍬

> Run, test, and fix Sugar Labs math & educational activities directly in VS Code — no Sugar desktop, no 2GB ISO, no logging out.

Built out of frustration with the official setup process. One file. A few copy-paste commands. Full GUI running in your terminal.

---

## The Problem with Official Setup

The [official Sugar Labs development guide](https://github.com/sugarlabs/sugar/blob/master/docs/development-environment.md) asks you to either:

- Download a **2GB Live ISO**, flash it to USB, and boot into it, OR
- Clone **5 separate repos**, run `autogen.sh` + `make` + `sudo make install` on each, then **log out and log back in** every time you make a change

That's a huge barrier — especially for GSoC contributors who just want to fix a bug and submit a PR.

---

## What This Does

`sugar_launch.py` mocks the Sugar shell environment so activities launch as a normal GTK window on your existing desktop. It:

- Sets all `SUGAR_*` environment variables the activity expects
- Creates a mock activity handle (what the Sugar shell normally provides)
- Initializes the D-Bus mainloop
- Reads `activity/activity.info` to find the right class automatically
- Opens the activity in a window — no logout, no VM, no ISO

---

## Requirements

Ubuntu 20.04 / 22.04 / 24.04 (or any Debian-based Linux with GTK3)

```bash
sudo apt install sucrose git
```

That single command pulls in everything needed:
- `python3-sugar3` — Sugar toolkit Python bindings
- `python3-dbus` — D-Bus support
- `python3-gi` + `python3-gi-cairo` — GTK Python bindings
- `gir1.2-gtk-3.0` — GTK3 introspection
- `sugar-themes` — Sugar icons and CSS

---

## Setup

```bash
# 1. Clone this repo
git clone https://github.com/Bindkushal/sugar-activity-devkit
cd sugar-activity-devkit

# 2. Create your Activities folder
mkdir -p ~/Activities
```

---

## Running Activities

### Calculate (Scientific Calculator)
```bash
git clone https://github.com/sugarlabs/calculate-activity.git ~/Activities/Calculate.activity
python3 sugar_launch.py ~/Activities/Calculate.activity
```

### Broken Calculator (Math Puzzle)
```bash
git clone https://github.com/sugarlabs/Broken-Calculator.git ~/Activities/Broken-Calculator.activity
python3 sugar_launch.py ~/Activities/Broken-Calculator.activity
```

### Physics (Box2D Sandbox)
```bash
git clone https://github.com/sugarlabs/physics.git ~/Activities/Physics.activity
python3 sugar_launch.py ~/Activities/Physics.activity
```

### Abacus
```bash
git clone https://github.com/sugarlabs/activity-abacus.git ~/Activities/Abacus.activity
python3 sugar_launch.py ~/Activities/Abacus.activity
```

### Memorize
```bash
git clone https://github.com/sugarlabs/memorize-activity.git ~/Activities/Memorize.activity
python3 sugar_launch.py ~/Activities/Memorize.activity
```

---

## Compatible Activities

Works with all Python + GTK3 Sugar activities. Tested:

| Activity | Repo |
|---|---|
| Calculate | sugarlabs/calculate-activity |
| Broken Calculator | sugarlabs/Broken-Calculator |
| Euclid's Game | sugarlabs/Euclid-s-Game |
| Physics | sugarlabs/physics |
| Abacus | sugarlabs/activity-abacus |
| Memorize | sugarlabs/memorize-activity |
| NumberRush | sugarlabs/numberrush-activity |

**Does not work** with activities that need external runtimes: Write (AbiWord), Browse (WebKit), Speak (eSpeak audio pipeline), Etoys.

---

## Contributing to Sugar Labs

This tool is built for contributors. Once an activity is running:

1. Open the activity folder in VS Code
2. Find open issues on the activity's GitHub repo
3. Make your fix
4. Re-run `python3 sugar_launch.py ~/Activities/YourActivity.activity` to test
5. Fork → branch → commit → PR

No rebuild step. No logout. Just save and re-run.

### Finding issues to fix

- [calculate-activity issues](https://github.com/sugarlabs/calculate-activity/issues)
- [Broken-Calculator issues](https://github.com/sugarlabs/Broken-Calculator/issues)
- [physics issues](https://github.com/sugarlabs/physics/issues)
- [All Sugar Labs repos](https://github.com/orgs/sugarlabs/repositories)

---

## How It Works

Sugar activities crash when run directly with `python3` because they expect several environment variables set by the Sugar shell:

```
SUGAR_BUNDLE_PATH   — path to the activity directory
SUGAR_ACTIVITY_ROOT — path for activity data/tmp storage
SUGAR_BUNDLE_ID     — activity identifier (e.g. org.laptop.Calculate)
SUGAR_BUNDLE_NAME   — human readable name
SUGAR_BUNDLE_VERSION
```

They also expect a D-Bus mainloop and a `handle` object with an `activity_id`. `sugar_launch.py` sets all of this up before importing and instantiating the activity class.

---

## Author

**Kushal Kant Bind** — [github.com/Bindkushal](https://github.com/Bindkushal)

B.Tech — Mobile & Distributed Computing, Chandigarh University  
ML Researcher | GSoC 2026 Applicant @ Sugar Labs

---

## License

GPLv3 — same as Sugar Labs projects.
