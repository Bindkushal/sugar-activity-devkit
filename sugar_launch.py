#!/usr/bin/env python3
"""
sugar_launch.py — Run any Sugar Labs activity without Sugar desktop.

Usage:
    python3 sugar_launch.py /path/to/YourActivity.activity
    python3 sugar_launch.py  (defaults to ~/Activities/Calculate.activity)

Author: Kushal Kant Bind (https://github.com/Bindkushal)
License: GPLv3
"""

import os
import sys
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import dbus
import dbus.mainloop.glib

# Must be initialized before any Sugar imports
dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)


def setup_env(bundle_path):
    """Set all environment variables Sugar activities expect from the shell."""
    activity_root = os.path.expanduser('~/.sugar/default/run')
    os.makedirs(os.path.join(activity_root, 'data'), exist_ok=True)
    os.makedirs(os.path.join(activity_root, 'tmp'), exist_ok=True)

    # Read bundle metadata from activity.info
    bundle_id = 'org.laptop.Activity'
    bundle_name = 'Activity'
    bundle_version = '1'

    info_path = os.path.join(bundle_path, 'activity', 'activity.info')
    if os.path.exists(info_path):
        with open(info_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith('bundle_id'):
                    bundle_id = line.split('=', 1)[1].strip()
                elif line.startswith('name'):
                    bundle_name = line.split('=', 1)[1].strip()
                elif line.startswith('activity_version'):
                    bundle_version = line.split('=', 1)[1].strip()

    os.environ['SUGAR_BUNDLE_PATH'] = bundle_path
    os.environ['SUGAR_ACTIVITY_ROOT'] = activity_root
    os.environ['SUGAR_BUNDLE_ID'] = bundle_id
    os.environ['SUGAR_BUNDLE_NAME'] = bundle_name
    os.environ['SUGAR_BUNDLE_VERSION'] = bundle_version
    os.environ['SUGAR_PREF_PATH'] = os.path.expanduser('~/.sugar/default')

    # Add activity directory to Python path
    sys.path.insert(0, bundle_path)

    print(f"[sugar-launch] Activity  : {bundle_name}")
    print(f"[sugar-launch] Bundle ID : {bundle_id}")
    print(f"[sugar-launch] Path      : {bundle_path}")


class MockHandle:
    """
    Fake Sugar activity handle.
    Mimics what the Sugar shell normally passes to an activity on launch.
    """
    def __init__(self):
        self.activity_id = 'standalone0000'
        self.object_id = None
        self.uri = None
        self.invited = False
        self.pservice_id = None
        self.dom_id = 0


def get_activity_class(bundle_path):
    """Parse activity.info to find the module and class to launch."""
    info_path = os.path.join(bundle_path, 'activity', 'activity.info')
    if not os.path.exists(info_path):
        print(f"[sugar-launch] ERROR: activity.info not found at {info_path}")
        sys.exit(1)

    with open(info_path) as f:
        for line in f:
            if line.strip().startswith('exec'):
                # exec = sugar-activity3 module.ClassName -s
                val = line.split('=', 1)[1].strip()
                for part in val.split():
                    if '.' in part and not part.startswith('-'):
                        module_name, class_name = part.rsplit('.', 1)
                        return module_name, class_name

    print("[sugar-launch] ERROR: Could not find 'exec' line in activity.info")
    sys.exit(1)


def launch(bundle_path):
    bundle_path = os.path.abspath(bundle_path)

    if not os.path.isdir(bundle_path):
        print(f"[sugar-launch] ERROR: Directory not found: {bundle_path}")
        sys.exit(1)

    setup_env(bundle_path)
    module_name, class_name = get_activity_class(bundle_path)
    print(f"[sugar-launch] Launching : {module_name}.{class_name}\n")

    try:
        import importlib
        mod = importlib.import_module(module_name)
        ActivityClass = getattr(mod, class_name)
        handle = MockHandle()
        activity = ActivityClass(handle)
        activity.connect('destroy', Gtk.main_quit)
        activity.show_all()
        Gtk.main()

    except Exception as e:
        print(f"[sugar-launch] ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


def main():
    if len(sys.argv) < 2:
        bundle = os.path.expanduser('~/Activities/Calculate.activity')
        print(f"[sugar-launch] No path given, defaulting to {bundle}")
    else:
        bundle = sys.argv[1]
    launch(bundle)


if __name__ == '__main__':
    main()
