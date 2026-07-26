# SPDX-License-Identifier: MIT
# Force F9 hotkey screen onto Ren'Py "top" layer (no visible button).

init 9999 python:
    def _mod_force_top():
        try:
            if not renpy.has_screen("mod_entry_hotkey"):
                return
            if renpy.get_screen("mod_entry_hotkey", layer="top") is None:
                renpy.show_screen("mod_entry_hotkey", _layer="top")
        except Exception:
            pass

    try:
        config.always_shown_screens = [
            s for s in config.always_shown_screens
            if s not in ("mod_entry_button", "mod_entry_hotkey")
        ]
    except Exception:
        pass

    if _mod_force_top not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_mod_force_top)

    def _mod_start():
        _mod_force_top()

    if _mod_start not in config.start_callbacks:
        config.start_callbacks.append(_mod_start)

    config.keymap["mod_open"] = ["K_F9"]
    try:
        config.underlay.append(renpy.Keymap(mod_open=Function(ModToggleManager)))
    except Exception:
        pass
