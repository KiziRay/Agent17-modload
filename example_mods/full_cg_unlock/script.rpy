# 全 CG 解鎖 + 主介面圖鑑（照片／劇集／直播／影片）
# 模組 ID: full_cg_unlock

default full_cg_tab = "picture"   # picture | show | stream | movie
default full_cg_page = 0
default full_cg_view_key = None
default full_cg_view_kind = "image"  # image | movie

init python:
    FULL_CG_PER_PAGE = 12

    # ---------- unlock pictures into inventory ----------
    def full_cg_unlock_all():
        if not is_mod_enabled("full_cg_unlock"):
            return 0
        global g_InventoryPicture
        try:
            table = TB_Picture
            inv = g_InventoryPicture
        except Exception:
            return 0
        if not isinstance(table, dict) or not table:
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

    # ---------- resolve displayables safely (no "Image not found") ----------
    _full_cg_file_cache = {}
    _full_cg_all_files = None

    def _full_cg_list_files():
        global _full_cg_all_files
        if _full_cg_all_files is None:
            try:
                _full_cg_all_files = list(renpy.list_files())
            except Exception:
                _full_cg_all_files = []
        return _full_cg_all_files

    def full_cg_find_asset(name):
        """依名稱找 images/ 或 movie/ 資源，找不到回 None。"""
        if not name:
            return None
        if name in _full_cg_file_cache:
            return _full_cg_file_cache[name]

        # 直接路徑
        candidates = [
            name,
            "images/" + name,
            "images/" + name + ".webp",
            "images/" + name + ".png",
            "images/" + name + ".jpg",
            "movie/" + name + ".webm",
            "movie/" + name + ".mp4",
        ]
        # 空白變底線
        n2 = name.replace(" ", "_")
        if n2 != name:
            candidates.extend([
                "images/" + n2 + ".webp",
                "movie/" + n2 + ".webm",
            ])

        for c in candidates:
            try:
                if renpy.loadable(c):
                    _full_cg_file_cache[name] = ("file", c)
                    return _full_cg_file_cache[name]
            except Exception:
                pass

        # 已註冊 image tag
        try:
            if renpy.has_image(name, exact=False):
                _full_cg_file_cache[name] = ("image", name)
                return _full_cg_file_cache[name]
        except Exception:
            pass

        # 模糊搜尋檔名
        key = name.lower().replace(" ", "")
        best = None
        for f in _full_cg_list_files():
            fl = f.lower().replace("\\", "/")
            base = fl.rsplit("/", 1)[-1]
            stem = base.rsplit(".", 1)[0].replace(" ", "")
            if stem == key or key in stem:
                if fl.endswith((".webp", ".png", ".jpg", ".jpeg", ".webm", ".mp4")):
                    # prefer exact stem
                    if stem == key:
                        best = f
                        break
                    if best is None:
                        best = f
        if best:
            kind = "movie" if best.lower().endswith((".webm", ".mp4")) else "file"
            _full_cg_file_cache[name] = (kind, best)
            return _full_cg_file_cache[name]

        _full_cg_file_cache[name] = None
        return None

    def full_cg_thumb_name(entry):
        """entry: dict with image/thumbnail/file fields or raw string."""
        if isinstance(entry, dict):
            for k in ("image", "thumbnail", "icon", "poster", "file"):
                if entry.get(k):
                    return entry.get(k)
            return None
        return entry

    def full_cg_displayable(name_or_entry, placeholder=True):
        name = full_cg_thumb_name(name_or_entry)
        found = full_cg_find_asset(name) if name else None
        if found:
            kind, path = found
            if kind == "movie":
                # 縮圖用靜態：若同名 webp 不在，用 Movie 第一幀可能失敗，改 placeholder + 標籤
                # Ren'Py Movie as displayable works in some versions
                try:
                    return Movie(play=path, loop=True)
                except Exception:
                    pass
            try:
                return path
            except Exception:
                pass
        if placeholder:
            return Solid("#2a2a2a")
        return Solid("#2a2a2a")

    def full_cg_is_missing(name_or_entry):
        name = full_cg_thumb_name(name_or_entry)
        return full_cg_find_asset(name) is None

    # ---------- catalog: all series ----------
    def full_cg_catalog():
        """
        回傳 list of dict:
          id, title, kind (image|movie), src (image name or movie path), tab, missing
        """
        items = []

        # 1) 照片圖鑑
        try:
            for k, v in TB_Picture.items():
                img = v.get("image") if isinstance(v, dict) else None
                items.append({
                    "id": "pic:" + str(k),
                    "title": str(k),
                    "kind": "image",
                    "src": img or k,
                    "tab": "picture",
                    "raw": v,
                })
        except Exception:
            pass

        # 2) Nutflex 劇集
        try:
            for k, v in TB_Nutflex.items():
                if not isinstance(v, dict):
                    continue
                title = k
                try:
                    title = renpy.translate_string(v.get("name", k))
                except Exception:
                    title = str(v.get("name", k))
                ep = v.get("episode", "")
                if ep:
                    title = "%s（%s集）" % (title, ep)
                items.append({
                    "id": "show:" + str(k),
                    "title": title,
                    "kind": "image",
                    "src": v.get("image") or k,
                    "tab": "show",
                    "raw": v,
                })
        except Exception:
            pass

        # 3) 直播／串流
        try:
            for k, v in TB_Stream.items():
                if not isinstance(v, dict):
                    continue
                title = k
                try:
                    title = renpy.translate_string(v.get("name", k))
                except Exception:
                    title = str(v.get("name", k))
                items.append({
                    "id": "stream:" + str(k),
                    "title": title,
                    "kind": "image",
                    "src": v.get("thumbnail") or v.get("image") or k,
                    "tab": "stream",
                    "raw": v,
                })
        except Exception:
            pass

        # 4) 全部 movie/*.webm 劇情影片
        try:
            for f in _full_cg_list_files():
                fl = f.replace("\\", "/")
                if fl.startswith("movie/") and fl.endswith((".webm", ".mp4")):
                    stem = fl.rsplit("/", 1)[-1].rsplit(".", 1)[0]
                    items.append({
                        "id": "movie:" + stem,
                        "title": stem,
                        "kind": "movie",
                        "src": fl,
                        "tab": "movie",
                        "raw": fl,
                    })
        except Exception:
            pass

        # 標記 missing（僅 image 類型需解析）
        for it in items:
            if it["kind"] == "movie":
                it["missing"] = not renpy.loadable(it["src"])
            else:
                it["missing"] = full_cg_is_missing(it["src"])

        return items

    def full_cg_filtered():
        tab = getattr(store, "full_cg_tab", "picture") or "picture"
        all_items = full_cg_catalog()
        # 預設隱藏「完全找不到資源」的照片（避免整排 not found）；劇集/直播保留標題
        out = []
        for it in all_items:
            if it["tab"] != tab:
                continue
            if tab == "picture" and it.get("missing"):
                # 仍列入但顯示灰卡，不呼叫無效 image tag
                pass
            out.append(it)
        return out

    def full_cg_page_count():
        n = len(full_cg_filtered())
        if n <= 0:
            return 1
        return max(1, (n + FULL_CG_PER_PAGE - 1) // FULL_CG_PER_PAGE)

    def full_cg_page_items():
        items = full_cg_filtered()
        p = int(getattr(store, "full_cg_page", 0) or 0)
        p = max(0, min(p, full_cg_page_count() - 1))
        store.full_cg_page = p
        start = p * FULL_CG_PER_PAGE
        return items[start : start + FULL_CG_PER_PAGE]

    def full_cg_set_tab(tab):
        store.full_cg_tab = tab
        store.full_cg_page = 0
        renpy.restart_interaction()

    def full_cg_open():
        if not is_mod_enabled("full_cg_unlock"):
            return
        full_cg_try_unlock()
        store.full_cg_page = 0
        if not getattr(store, "full_cg_tab", None):
            store.full_cg_tab = "picture"
        renpy.show_screen("full_cg_gallery", _layer="top")
        renpy.restart_interaction()

    def full_cg_close():
        for scr in ("full_cg_gallery", "full_cg_viewer"):
            renpy.hide_screen(scr, layer="top")
            try:
                renpy.hide_screen(scr)
            except Exception:
                pass
        # 停掉可能在播的影片
        try:
            renpy.music.stop(channel="movie")
        except Exception:
            pass
        renpy.restart_interaction()

    def full_cg_view(item):
        store.full_cg_view_key = item.get("id")
        store.full_cg_view_kind = item.get("kind", "image")
        store.full_cg_view_src = item.get("src")
        store.full_cg_view_title = item.get("title", "")
        renpy.show_screen("full_cg_viewer", _layer="top")
        renpy.restart_interaction()

    def full_cg_close_viewer():
        renpy.hide_screen("full_cg_viewer", layer="top")
        try:
            renpy.hide_screen("full_cg_viewer")
        except Exception:
            pass
        try:
            renpy.music.stop(channel="movie")
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
        if not is_mod_enabled("full_cg_unlock"):
            return False
        for scr in ("mod_manager", "full_cg_gallery", "full_cg_viewer"):
            if renpy.get_screen(scr, layer="top") or renpy.get_screen(scr):
                return False
        if renpy.get_screen("main_menu") is not None:
            if getattr(persistent, "select_language", False) and renpy.get_screen("language_screen") is None:
                return True
        if renpy.get_screen("home_ui_system_button") is not None:
            return True
        return False

    def full_cg_tab_label(tab):
        n = 0
        try:
            for it in full_cg_catalog():
                if it["tab"] == tab:
                    n += 1
        except Exception:
            pass
        names = {
            "picture": "照片",
            "show": "劇集",
            "stream": "直播",
            "movie": "影片",
        }
        return "%s (%d)" % (names.get(tab, tab), n)


# 入口：底部中央小鈕（不擋開始／讀取／設定／語言／右上系統）
screen full_cg_entry_button():
    zorder 9000

    if full_cg_show_entry_button():
        textbutton "CG":
            xalign 0.5
            yalign 1.0
            ypos -52
            text_size 24
            text_color "#ffffff"
            text_outlines [ (1, "#000000", 0, 0) ]
            xpadding 18
            ypadding 6
            background "#b3324099"
            hover_background "#e04a60"
            action Function(full_cg_open)


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
        xsize 1500
        ysize 960
        background "#1a1a1e"
        padding (22, 18)

        vbox:
            spacing 10
            xfill True

            hbox:
                spacing 16
                text "CG 圖鑑" size 42 color "#ffffff"
                text "第 " + str(int(full_cg_page) + 1) + " / " + str(full_cg_page_count()) + " 頁" size 22 color "#aaaaaa" yalign 0.5
                null width 10
                textbutton "上一頁":
                    text_size 24
                    text_color "#cccccc"
                    text_hover_color "#ff6080"
                    action Function(full_cg_page_prev)
                textbutton "下一頁":
                    text_size 24
                    text_color "#cccccc"
                    text_hover_color "#ff6080"
                    action Function(full_cg_page_next)
                textbutton "關閉":
                    text_size 24
                    text_color "#cccccc"
                    text_hover_color "#ffffff"
                    action Function(full_cg_close)

            # 分類
            hbox:
                spacing 10
                for tab in ("picture", "show", "stream", "movie"):
                    textbutton full_cg_tab_label(tab):
                        text_size 24
                        text_color ("#ffffff" if full_cg_tab == tab else "#999999")
                        background ("#b33240" if full_cg_tab == tab else "#333333")
                        hover_background "#e04a60"
                        xpadding 12
                        ypadding 6
                        action Function(full_cg_set_tab, tab)

            text "點縮圖開啟　·　缺圖會顯示灰底（不噴 Image not found）　·　方向鍵翻頁" size 18 color "#777777"

            $ _items = full_cg_page_items()
            if not _items:
                frame:
                    xfill True
                    ysize 700
                    background "#111111"
                    text "此分類沒有項目" size 30 color "#888888" xalign 0.5 yalign 0.5
            else:
                vpgrid:
                    cols 4
                    spacing 14
                    xalign 0.5
                    ysize 720

                    for it in _items:
                        button:
                            xsize 320
                            ysize 180
                            background "#2a2a2a"
                            hover_background "#404040"
                            action Function(full_cg_view, it)

                            if it.get("missing") and it.get("kind") != "movie":
                                add Solid("#333333") xsize 320 ysize 180
                                text "無圖資源" size 22 color "#888888" xalign 0.5 yalign 0.45
                            else:
                                add full_cg_displayable(it["src"]):
                                    xsize 320
                                    ysize 180
                                    fit "cover"

                            frame:
                                yalign 1.0
                                xfill True
                                background "#000000bb"
                                padding (6, 4)
                                text it["title"] size 15 color "#ffffff" xalign 0.5


screen full_cg_viewer():
    modal True
    zorder 10045

    key "K_ESCAPE" action Function(full_cg_close_viewer)
    key "K_BACKSPACE" action Function(full_cg_close_viewer)

    button:
        xfill True
        yfill True
        background "#000000ee"
        action Function(full_cg_close_viewer)

        if full_cg_view_kind == "movie" or (full_cg_view_src and str(full_cg_view_src).endswith((".webm", ".mp4"))):
            add Movie(play=str(full_cg_view_src), loop=True):
                xalign 0.5
                yalign 0.5
                fit "contain"
                xysize (1920, 1000)
        elif full_cg_is_missing(full_cg_view_src):
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 12
                text "找不到對應圖片資源" size 36 color "#aaaaaa" xalign 0.5
                text str(full_cg_view_src) size 24 color "#666666" xalign 0.5
                text "（遊戲資料表有登錄，但封包內無此圖／未定義 image）" size 20 color "#555555" xalign 0.5
        else:
            add full_cg_displayable(full_cg_view_src, placeholder=False):
                xalign 0.5
                yalign 0.5
                fit "contain"
                xysize (1920, 1000)

    textbutton "關閉":
        xalign 0.98
        yalign 0.02
        text_size 26
        text_color "#ffffff"
        background "#b33240"
        hover_background "#e04a60"
        xpadding 14
        ypadding 8
        action Function(full_cg_close_viewer)

    text str(full_cg_view_title or full_cg_view_src or ""):
        xalign 0.5
        yalign 0.98
        size 20
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
