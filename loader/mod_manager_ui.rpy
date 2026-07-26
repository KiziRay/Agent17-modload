# SPDX-License-Identifier: MIT
# Agent17-modload — third-party mod loader (not affiliated with HEXATAIL)
# 預設僅 F9 開啟模組選單（無畫面按鈕）

init -50 python:
    def ModOpenManager():
        try:
            mod_manager.refresh()
        except Exception:
            pass
        renpy.show_screen("mod_manager", _layer="top")
        renpy.restart_interaction()

    def ModToggle(mod_id):
        try:
            mod_manager.toggle(mod_id)
        except Exception:
            pass
        renpy.restart_interaction()

    def ModRequestRestart():
        try:
            mod_manager.clear_restart_flag()
        except Exception:
            pass
        renpy.full_restart()

    def ModCloseManager():
        renpy.hide_screen("mod_manager", layer="top")
        try:
            renpy.hide_screen("mod_manager")
        except Exception:
            pass
        renpy.restart_interaction()

    def ModToggleManager():
        if renpy.get_screen("mod_manager", layer="top") or renpy.get_screen("mod_manager"):
            ModCloseManager()
        else:
            ModOpenManager()

    def _mod_force_show():
        try:
            if not renpy.has_screen("mod_entry_hotkey"):
                return
            if renpy.get_screen("mod_entry_hotkey", layer="top") is None:
                renpy.show_screen("mod_entry_hotkey", _layer="top")
        except Exception:
            pass


screen mod_entry_hotkey():
    zorder 10000
    key "K_F9" action Function(ModToggleManager)


screen mod_manager():
    modal True
    zorder 10050

    key "K_ESCAPE" action Function(ModCloseManager)
    key "K_F9" action Function(ModCloseManager)

    add "#000000cc"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 960
        ysize 860
        background "#1a1a1e"
        padding (28, 24)

        vbox:
            spacing 12
            xfill True

            hbox:
                spacing 16
                text "模組管理" size 46 color "#ffffff"
                textbutton "重新整理":
                    text_size 26
                    text_color "#cccccc"
                    text_hover_color "#ff6080"
                    action Function(mod_manager.refresh)
                textbutton "開啟資料夾":
                    text_size 26
                    text_color "#cccccc"
                    text_hover_color "#ff6080"
                    action Function(mod_manager.open_mods_folder)
                textbutton "關閉 (F9)":
                    text_size 26
                    text_color "#cccccc"
                    text_hover_color "#ffffff"
                    action Function(ModCloseManager)

            text "開啟方式：按 F9　·　模組目錄 game/mods/" size 22 color "#aaaaaa"

            if mod_manager.needs_restart():
                frame:
                    xfill True
                    background "#5a2030"
                    padding (14, 10)
                    hbox:
                        spacing 16
                        text "已變更模組，建議重新啟動。" size 26 color "#ffdddd"
                        textbutton "立即重啟":
                            text_size 26
                            text_color "#ffffff"
                            action Function(ModRequestRestart)

            if not mod_manager.list_mods():
                frame:
                    xfill True
                    ysize 500
                    background "#111111"
                    vbox:
                        xalign 0.5
                        yalign 0.5
                        spacing 12
                        text "尚未安裝任何模組" size 34 color "#888888" xalign 0.5
                        text "路徑：game/mods/<名稱>/" size 24 color "#666666" xalign 0.5
                        textbutton "開啟模組資料夾":
                            xalign 0.5
                            text_size 28
                            action Function(mod_manager.open_mods_folder)
            else:
                viewport:
                    xfill True
                    ysize 580
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 10
                        xfill True

                        for m in mod_manager.list_mods():
                            $ _on = mod_manager.is_enabled(m.id)
                            frame:
                                xfill True
                                background ("#2a2a2a" if _on else "#222222")
                                padding (14, 12)

                                hbox:
                                    spacing 14
                                    xfill True
                                    vbox:
                                        xsize 640
                                        spacing 4
                                        text mod_manager.display_name(m) size 30 color ("#ffffff" if _on else "#cccccc")
                                        text "v" + m.version + ("  ·  " + m.author if m.author else "") size 20 color "#888888"
                                        if m.description:
                                            text m.description size 22 color "#aaaaaa"
                                    textbutton ("開啟中" if _on else "已關閉"):
                                        xalign 1.0
                                        yalign 0.5
                                        xsize 140
                                        ysize 56
                                        text_size 26
                                        text_xalign 0.5
                                        text_color "#ffffff"
                                        background ("#2d7a3e" if _on else "#555555")
                                        hover_background ("#3a9a50" if _on else "#777777")
                                        action Function(ModToggle, m.id)

            text mod_manager.mods_root() size 16 color "#555555"


init 999 python:
    if "mod_entry_hotkey" not in config.always_shown_screens:
        config.always_shown_screens.append("mod_entry_hotkey")
    if "mod_entry_hotkey" not in config.overlay_screens:
        config.overlay_screens.append("mod_entry_hotkey")

    if _mod_force_show not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_mod_force_show)

    config.keymap["mod_open"] = ["K_F9"]
    try:
        config.underlay.append(renpy.Keymap(mod_open=Function(ModToggleManager)))
    except Exception:
        pass
