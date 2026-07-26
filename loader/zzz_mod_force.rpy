# SPDX-License-Identifier: MIT
# Force mod entry UI onto Ren'Py built-in "top" layer.
# Does not include any game content.

init 9999 python:
    import os

    def _mod_force_top():
        try:
            if not renpy.has_screen("mod_entry_button"):
                return
            if renpy.get_screen("mod_entry_button", layer="top") is None:
                renpy.show_screen("mod_entry_button", _layer="top")
        except Exception:
            pass

    # Prefer manual show on top layer (avoid duplicate always_shown on screens layer)
    try:
        config.always_shown_screens = [
            s for s in config.always_shown_screens if s != "mod_entry_button"
        ]
    except Exception:
        pass

    if _mod_force_top not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_mod_force_top)

    def _mod_start():
        _mod_force_top()

    if _mod_start not in config.start_callbacks:
        config.start_callbacks.append(_mod_start)

    config.keymap["mod_open"] = ["K_F8", "K_F9", "K_F10"]
    try:
        config.underlay.append(renpy.Keymap(mod_open=Function(ModOpenManager)))
    except Exception:
        pass
