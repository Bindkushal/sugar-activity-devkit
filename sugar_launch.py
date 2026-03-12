#!/usr/bin/env python3
"""
sugar_launch.py — Run any Sugar activity without Sugar desktop.
Usage: python3 sugar_launch.py /path/to/YourActivity.activity
"""

import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

def setup_env(bundle_path):
    """Set all env vars Sugar activities expect."""
    activity_root = os.path.expanduser('~/.sugar/default/run')
    os.makedirs(activity_root, exist_ok=True)
    os.makedirs(os.path.join(activity_root, 'data'), exist_ok=True)
    os.makedirs(os.path.join(activity_root, 'tmp'), exist_ok=True)

    os.environ['SUGAR_BUNDLE_PATH'] = bundle_path
    os.environ['SUGAR_ACTIVITY_ROOT'] = activity_root
    os.environ['SUGAR_BUNDLE_ID'] = 'org.laptop.standalone'
    os.environ['SUGAR_BUNDLE_NAME'] = 'Standalone'
    os.environ['SUGAR_BUNDLE_VERSION'] = '1'
    os.environ['SUGAR_PREF_PATH'] = os.path.expanduser('~/.sugar/default')

    # Add activity to Python path
    sys.path.insert(0, bundle_path)

class MockActivityHandle:
    """Fake Sugar activity handle — mimics what Sugar shell passes in."""
    def __init__(self):
        self.activity_id = 'standalone-0000-0000-0000-000000000000'
        self.object_id = None
        self.uri = None
        self.invited = False
        self.pservice_id = None
        self.dom_id = 0

def launch(bundle_path):
    bundle_path = os.path.abspath(bundle_path)
    print(f"[sugar_launch] Bundle path: {bundle_path}")
    setup_env(bundle_path)

    # Read activity.info to find the class
    info_path = os.path.join(bundle_path, 'activity', 'activity.info')
    class_name = None
    module_name = None

    if os.path.exists(info_path):
        with open(info_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('class'):
                    # e.g. class = calculate:CalculateActivity
                    val = line.split('=', 1)[1].strip()
                    if ':' in val:
                        module_name, class_name = val.split(':', 1)
                    else:
                        class_name = val
                    break

    if not class_name:
        print("[sugar_launch] Could not find class in activity.info")
        print("[sugar_launch] Trying to run calculate.py directly...")
        import subprocess
        subprocess.run([sys.executable, os.path.join(bundle_path, 'calculate.py')])
        return

    print(f"[sugar_launch] Launching {module_name}:{class_name}")

    try:
        import importlib
        mod = importlib.import_module(module_name)
        ActivityClass = getattr(mod, class_name)
        handle = MockActivityHandle()
        win = Gtk.Window()
        win.set_title(class_name)
        win.set_default_size(1024, 768)
        win.connect('destroy', Gtk.main_quit)

        activity = ActivityClass(handle)
        win.show_all()
        Gtk.main()

    except Exception as e:
        print(f"[sugar_launch] Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        # Default to calculate activity
        path = os.path.expanduser('~/Activities/Calculate.activity')
    else:
        path = sys.argv[1]

    launch(path)
