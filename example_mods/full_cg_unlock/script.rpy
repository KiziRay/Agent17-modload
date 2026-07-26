# 全 CG 解鎖 + 主介面「CG」按鈕開啟圖鑑選擇
# 模組 ID: full_cg_unlock

default full_cg_page = 0
default full_cg_view_key = None

init python:
    FULL_CG_PER_PAGE = 12  # 4x3

    def full_cg_unlock_all():
        if not is_mod_enabled("full_cg_unlock"):
            return 0

        global g_InventoryPicture

        try:
            table = TB_Picture
        except Exception:
            return 0

        if not isinstance(table, dict) or not table:
            return 0

        try:
            inv = g_InventoryPicture
        except Exception:
            return 0

        existing = set()
        try:
            for item in inv:
                existing.add(item.pKey)
        except Exception:
            pass

        try:
            if len(existing) >= len(table):
                return 0
        except Exception:
            pass

        added = 0
        for pKey in table.keys():
            if pKey in existing:
                continue
            try:
                pic = PictureData(pKey)
                pic.Add(1)
                inv.append(pic)
                existing.add(pKey)
                added += 1
            except Exception:
                continue
        return added

    def full_cg_try_unlock():
        try:
            full_cg_unlock_all()
        except Exception:
            pass

    def full_cg_keys():
        """全部 CG 鍵（已排序）。"""
        try:
            return sorted(list(TB_Picture.keys()))
        except Exception:
            return []

    def full_cg_page_count():
        keys = full_cg_keys()
        if not keys:
            return 1
        return max(1, (len(keys) + FULL_CG_PER_PAGE - 1) // FULL_CG_PER_PAGE)

    def full_cg_page_keys():
        keys = full_cg_keys()
        p = int(getattr(store, "full_cg_page", 0) or 0)
        p = max(0, min(p, full_cg_page_count() - 1))
        store.full_cg_page = p
        start = p * FULL_CG_PER_PAGE
        return keys[start : start + FULL_CG_PER_PAGE]

    def full_cg_open():
        if not is_mod_enabled("full_cg_unlock"):
            return
        full_cg_try_unlock()
        store.full_cg_page = 0
        renpy.show_screen("full_cg_gallery", _layer="top")
        renpy.restart_interaction()

    def full_cg_close():
        renpy.hide_screen("full_cg_gallery", layer="top")
        try:
            renpy.hide_screen("full_cg_gallery")
        except Exception:
            pass
        renpy.hide_screen("full_cg_viewer", layer="top")
        try:
            renpy.hide_screen("full_cg_viewer")
        except Exception:
            pass
        renpy.restart_interaction()

    def full_cg_view(pKey):
        store.full_cg_view_key = pKey
        renpy.show_screen("full_cg_viewer", pKey=pKey, _layer="top")
        renpy.restart_interaction()

    def full_cg_close_viewer():
        renpy.hide_screen("full_cg_viewer", layer="top")
        try:
            renpy.hide_screen("full_cg_viewer")
        except Exception:
            pass
        renpy.restart_interaction()

    def full_cg_page_prev():
        store.full_cg_page = max(0, int(store.full_cg_page) - 1)
        renpy.restart_interaction()

    def full_cg_page_next():
        store.full_cg_page = min(full_cg_page_count() - 1, int(store.full_cg_page) + 1)
        renpy.restart_interaction()

    def full_cg_show_entry_button():
        """主選單或遊戲主介面（系統列）時顯示 CG 按鈕。"""
        if not is_mod_enabled("full_cg_unlock"):
            return False
        if renpy.get_screen("mod_manager", layer="top") or renpy.get_screen("mod_manager"):
            return False
        if renpy.get_screen("full_cg_gallery", layer="top") or renpy.get_screen("full_cg_gallery"):
            return False
        if renpy.get_screen("full_cg_viewer", layer="top") or renpy.get_screen("full_cg_viewer"):
            return False
        # 主選單
        if renpy.get_screen("main_menu") is not None:
            if getattr(persistent, "select_language", False):
                if renpy.get_screen("language_screen") is None:
                    return True
        # 遊戲內主介面（有系統選單鈕時）
        if renpy.get_screen("home_ui_system_button") is not None:
            return True
        return False

    def full_cg_thumb(pKey):
        try:
            return PictureData(pKey).Image()
        except Exception:
            return Solid("#333333")


# 入口按鈕（不擋：主選單放在開始鍵上方偏左；遊戲內右上系統鈕下方）
screen full_cg_entry_button():
    zorder 9000

    if full_cg_show_entry_button():
        if renpy.get_screen("main_menu") is not None:
            # 主選單：開始／讀取上方，不擋右上設定與左下語言
            textbutton "CG 圖鑑":
                xalign 0.3
                yalign 0.55
                text_size 36
                text_color "#ffffff"
                text_hover_color "#ffb0c0"
                text_outlines [ (2, "#000000", 0, 0) ]
                xpadding 22
                ypadding 10
                background "#b33240cc"
                hover_background "#e04a60"
                action Function(full_cg_open)
        else:
            # 遊戲內：右上系統鈕下方
            textbutton "CG":
                xalign 1.0
                yalign 0.0
                xpos -8
                ypos 140
                text_size 28
                text_color "#ffffff"
                text_outlines [ (1, "#000000", 0, 0) ]
                xpadding 14
                ypadding 8
                background "#00000099"
                hover_background "#b33240cc"
                action Function(full_cg_open)


# CG 列表選擇
screen full_cg_gallery():
    modal True
    zorder 10040

    key "K_ESCAPE" action Function(full_cg_close)
    key "K_LEFT" action Function(full_cg_page_prev)
    key "K_RIGHT" action Function(full_cg_page_next)

    add "#000000dd"

    frame:
        xalign 0.5
        yalign 0.5
        xsize 1400
        ysize 920
        background "#1a1a1e"
        padding (24, 20)

        vbox:
            spacing 12
            xfill True

            hbox:
                spacing 20
                text "CG 圖鑑" size 44 color "#ffffff"
                text "共 " + str(len(full_cg_keys())) + " 張　·　第 " + str(int(full_cg_page) + 1) + " / " + str(full_cg_page_count()) + " 頁" size 24 color "#aaaaaa" yalign 0.5
                null width 20
                textbutton "上一頁":
                    text_size 26
                    text_color "#cccccc"
                    text_hover_color "#ff6080"
                    action Function(full_cg_page_prev)
                textbutton "下一頁":
                    text_size 26
                    text_color "#cccccc"
                    text_hover_color "#ff6080"
                    action Function(full_cg_page_next)
                textbutton "關閉":
                    text_size 26
                    text_color "#cccccc"
                    text_hover_color "#ffffff"
                    action Function(full_cg_close)

            text "點選縮圖開啟大圖　·　方向鍵翻頁" size 22 color "#888888"

            if not full_cg_keys():
                frame:
                    xfill True
                    ysize 700
                    background "#111111"
                    text "尚無 CG 資料（可能尚未載入遊戲資料表）" size 32 color "#888888" xalign 0.5 yalign 0.5
            else:
                vpgrid:
                    cols 4
                    spacing 16
                    xalign 0.5
                    ysize 720

                    for pKey in full_cg_page_keys():
                        button:
                            xsize 300
                            ysize 170
                            background "#2a2a2a"
                            hover_background "#3a3a3a"
                            action Function(full_cg_view, pKey)
                            add full_cg_thumb(pKey):
                                xsize 300
                                ysize 170
                                fit "cover"
                            # 標題條
                            frame:
                                yalign 1.0
                                xfill True
                                background "#000000aa"
                                padding (6, 4)
                                text str(pKey) size 16 color "#ffffff" xalign 0.5


# 大圖檢視
screen full_cg_viewer(pKey):
    modal True
    zorder 10045

    key "K_ESCAPE" action Function(full_cg_close_viewer)
    key "mousedown_1" action Function(full_cg_close_viewer)
    key "K_BACKSPACE" action Function(full_cg_close_viewer)

    button:
        xfill True
        yfill True
        background "#000000ee"
        action Function(full_cg_close_viewer)

        add full_cg_thumb(pKey):
            xalign 0.5
            yalign 0.5
            fit "contain"
            xysize (1920, 1080)

    textbutton "關閉":
        xalign 0.98
        yalign 0.02
        text_size 28
        text_color "#ffffff"
        background "#b33240"
        hover_background "#e04a60"
        xpadding 16
        ypadding 8
        action Function(full_cg_close_viewer)

    text str(pKey):
        xalign 0.5
        yalign 0.98
        size 22
        color "#ffffffaa"


init 999 python:
    def _full_cg_on_start():
        full_cg_try_unlock()

    if _full_cg_on_start not in config.start_callbacks:
        config.start_callbacks.append(_full_cg_on_start)

    def _full_cg_on_interact():
        full_cg_try_unlock()

    if _full_cg_on_interact not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_full_cg_on_interact)

    # 入口畫面掛到 top
    def _full_cg_force_btn():
        try:
            if not is_mod_enabled("full_cg_unlock"):
                if renpy.get_screen("full_cg_entry_button", layer="top"):
                    renpy.hide_screen("full_cg_entry_button", layer="top")
                return
            if renpy.get_screen("full_cg_entry_button", layer="top") is None:
                if renpy.has_screen("full_cg_entry_button"):
                    renpy.show_screen("full_cg_entry_button", _layer="top")
        except Exception:
            pass

    if _full_cg_force_btn not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_full_cg_force_btn)

    if "full_cg_entry_button" not in config.overlay_screens:
        config.overlay_screens.append("full_cg_entry_button")
