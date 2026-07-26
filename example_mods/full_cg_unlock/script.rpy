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

    # ---------- resolve displayables safely (no "Image not found" / no webm-as-image) ----------
    _full_cg_file_cache = {}
    _full_cg_all_files = None
    _VIDEO_EXT = (".webm", ".mp4", ".mkv", ".avi", ".ogv")

    def _full_cg_list_files():
        global _full_cg_all_files
        if _full_cg_all_files is None:
            try:
                _full_cg_all_files = list(renpy.list_files())
            except Exception:
                _full_cg_all_files = []
        return _full_cg_all_files

    def full_cg_is_video_path(path):
        p = str(path or "").lower().replace("\\", "/")
        return p.endswith(_VIDEO_EXT)

    def _full_cg_kind_for_path(path):
        return "movie" if full_cg_is_video_path(path) else "file"

    def full_cg_find_asset(name):
        """依名稱找 images/ 或 movie/。回傳 (kind, path) 或 None。kind=image|file|movie"""
        if not name:
            return None
        if name in _full_cg_file_cache:
            return _full_cg_file_cache[name]

        # 已是影片路徑
        name_s = str(name).replace("\\", "/")
        if full_cg_is_video_path(name_s):
            try:
                if renpy.loadable(name_s):
                    _full_cg_file_cache[name] = ("movie", name_s)
                    return _full_cg_file_cache[name]
            except Exception:
                pass

        candidates = [
            name_s,
            "images/" + name_s,
            "images/" + name_s + ".webp",
            "images/" + name_s + ".png",
            "images/" + name_s + ".jpg",
            "movie/" + name_s + ".webm",
            "movie/" + name_s + ".mp4",
            "movie/" + name_s,
        ]
        n2 = name_s.replace(" ", "_")
        if n2 != name_s:
            candidates.extend([
                "images/" + n2 + ".webp",
                "images/" + n2 + ".png",
                "movie/" + n2 + ".webm",
            ])

        for c in candidates:
            try:
                if renpy.loadable(c):
                    kind = _full_cg_kind_for_path(c)
                    # webm 絕不可當 file/image
                    _full_cg_file_cache[name] = (kind, c)
                    return _full_cg_file_cache[name]
            except Exception:
                pass

        try:
            if renpy.has_image(name_s, exact=False):
                _full_cg_file_cache[name] = ("image", name_s)
                return _full_cg_file_cache[name]
        except Exception:
            pass

        key = name_s.lower().replace(" ", "")
        best = None
        for f in _full_cg_list_files():
            fl = f.replace("\\", "/")
            base = fl.rsplit("/", 1)[-1]
            stem = base.rsplit(".", 1)[0].replace(" ", "").lower()
            if stem == key or (len(key) > 4 and key in stem):
                low = fl.lower()
                if low.endswith((".webp", ".png", ".jpg", ".jpeg") + _VIDEO_EXT):
                    if stem == key:
                        best = fl
                        break
                    if best is None:
                        best = fl
        if best:
            _full_cg_file_cache[name] = (_full_cg_kind_for_path(best), best)
            return _full_cg_file_cache[name]

        _full_cg_file_cache[name] = None
        return None

    def full_cg_thumb_name(entry):
        if isinstance(entry, dict):
            for k in ("image", "thumbnail", "icon", "poster", "file", "src"):
                if entry.get(k):
                    return entry.get(k)
            return None
        return entry

    def full_cg_ensure_movie_channel(channel, volume=1.0):
        """註冊影片 channel（獨立 sfx mixer，避免跟 BGM 搶／被一起靜音）。"""
        try:
            # 用 sfx：與 music BGM 分開，音量可獨立拉滿
            if not renpy.music.channel_defined(channel):
                renpy.music.register_channel(
                    channel,
                    "sfx",
                    loop=True,
                    stop_on_mute=False,
                    movie=True,
                    framedrop=False,
                    force=True,
                )
            renpy.music.set_volume(max(0.0, min(1.0, float(volume))), delay=0, channel=channel)
            # 確保 sfx 混音器本身有聲
            try:
                _preferences.set_volume("sfx", max(_preferences.get_volume("sfx"), 0.8))
            except Exception:
                pass
        except Exception:
            pass

    def full_cg_movie(path, size=None, channel=None, audio=True):
        """建立可預覽的 Movie（webm 內建音軌會走 channel 播出）。"""
        path = str(path).replace("\\", "/")
        if not path:
            return Solid("#1a1a2e")
        try:
            if not renpy.loadable(path):
                return Solid("#1a1a2e")
        except Exception:
            return Solid("#1a1a2e")

        if channel is None:
            if audio:
                channel = "full_cg_movie"
            else:
                stem = path.rsplit("/", 1)[-1].rsplit(".", 1)[0]
                channel = "fcg_" + "".join(ch if ch.isalnum() else "_" for ch in stem)[:40]

        full_cg_ensure_movie_channel(channel, volume=(1.0 if audio else 0.0))

        try:
            if size:
                return Movie(play=path, channel=channel, loop=True, size=size)
            return Movie(play=path, channel=channel, loop=True)
        except TypeError:
            try:
                return Movie(play=path, channel=channel, loop=True)
            except Exception:
                return Solid("#1a1a2e")
        except Exception:
            return Solid("#1a1a2e")

    def full_cg_play_with_sound(path):
        """全畫面播放：畫面 + 聲音。"""
        path = str(path).replace("\\", "/")
        ch = "full_cg_movie"
        full_cg_ensure_movie_channel(ch, volume=1.0)
        # 先停掉同 channel 殘留
        try:
            renpy.music.stop(channel=ch, fadeout=0.05)
        except Exception:
            pass
        # Movie displayable 會在 show 時 play；再保險手動 play 一次以帶音
        try:
            renpy.music.play([path], channel=ch, loop=True)
        except Exception:
            try:
                renpy.music.play(path, channel=ch, loop=True)
            except Exception:
                pass
        return full_cg_movie(path, size=(1920, 1000), channel=ch, audio=True)

    def full_cg_stop_sound():
        for ch in ("full_cg_movie", "movie"):
            try:
                renpy.music.stop(channel=ch, fadeout=0.15)
            except Exception:
                pass
    def full_cg_displayable(name_or_entry, placeholder=True, size=None):
        """
        回傳可安全 add 的 displayable。
        - 影片一律 Movie()
        - 靜態圖用路徑或 image name
        - 失敗用灰底 Solid（不觸發 Image not found）
        """
        # 目錄項 dict
        if isinstance(name_or_entry, dict):
            if name_or_entry.get("kind") == "movie" or full_cg_is_video_path(name_or_entry.get("src")):
                return full_cg_movie(name_or_entry.get("src"), size=size)
            name = full_cg_thumb_name(name_or_entry)
        else:
            name = name_or_entry
            if full_cg_is_video_path(name):
                return full_cg_movie(name, size=size)

        found = full_cg_find_asset(name) if name else None
        if found:
            kind, path = found
            if kind == "movie" or full_cg_is_video_path(path):
                return full_cg_movie(path, size=size)
            # 靜態：只回傳可當 image 的路徑／tag，絕不回傳 webm
            if full_cg_is_video_path(path):
                return full_cg_movie(path, size=size)
            return path

        if placeholder:
            return Solid("#2a2a2a")
        return Solid("#2a2a2a")

    def full_cg_is_missing(name_or_entry):
        if isinstance(name_or_entry, dict):
            if name_or_entry.get("kind") == "movie":
                src = name_or_entry.get("src")
                try:
                    return not renpy.loadable(str(src))
                except Exception:
                    return True
            name = full_cg_thumb_name(name_or_entry)
        else:
            name = name_or_entry
            if full_cg_is_video_path(name):
                try:
                    return not renpy.loadable(str(name))
                except Exception:
                    return True
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
        full_cg_stop_sound()
        try:
            renpy.music.stop(channel="movie", fadeout=0.1)
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
        full_cg_stop_sound()
        try:
            renpy.music.stop(channel="movie", fadeout=0.1)
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
        """模組開啟就顯示，避免條件過嚴找不到按鈕。"""
        if not is_mod_enabled("full_cg_unlock"):
            return False
        for scr in ("mod_manager", "full_cg_gallery", "full_cg_viewer"):
            if renpy.get_screen(scr, layer="top") or renpy.get_screen(scr):
                return False
        return True

    def full_cg_toggle_gallery():
        """F10：開／關 CG 圖鑑。"""
        if not is_mod_enabled("full_cg_unlock"):
            try:
                renpy.notify("請先在模組管理(F9)開啟「全 CG 解鎖」")
            except Exception:
                pass
            return
        if renpy.get_screen("full_cg_gallery", layer="top") or renpy.get_screen("full_cg_gallery"):
            full_cg_close()
        else:
            full_cg_open()

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


# 入口：左側中間 + F10（不擋主選單開始／讀取／右上設定）
screen full_cg_entry_button():
    zorder 10000

    # F10 開／關圖鑑（F9 留給模組管理）
    key "K_F10" action Function(full_cg_toggle_gallery)

    if full_cg_show_entry_button():
        # 左緣垂直中央：避開左下語言、左中開始鍵、右上系統
        button:
            xalign 0.0
            yalign 0.5
            xpos 12
            xminimum 72
            yminimum 120
            padding (10, 16)
            background "#b33240ee"
            hover_background "#ff4060"
            action Function(full_cg_open)

            vbox:
                xalign 0.5
                spacing 6
                text "CG":
                    size 28
                    color "#ffffff"
                    xalign 0.5
                    bold True
                    outlines [ (2, "#000000", 0, 0) ]
                text "F10":
                    size 16
                    color "#ffdddd"
                    xalign 0.5
                    outlines [ (1, "#000000", 0, 0) ]


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

                            # 影片：Movie 預覽（禁止當 Image 載入 webm）
                            if it.get("kind") == "movie" or full_cg_is_video_path(it.get("src")):
                                # 縮圖靜音預覽（多支同時播避免吵）
                                add full_cg_movie(it.get("src"), size=(320, 180), audio=False)
                                text "▶":
                                    size 28
                                    color "#ffffffaa"
                                    xalign 0.5
                                    yalign 0.4
                                    outlines [ (2, "#000000", 0, 0) ]
                            elif it.get("missing"):
                                add Solid("#333333") xsize 320 ysize 180
                                text "無圖資源" size 22 color "#888888" xalign 0.5 yalign 0.45
                            else:
                                add full_cg_displayable(it, size=(320, 180)):
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

        if full_cg_view_kind == "movie" or full_cg_is_video_path(full_cg_view_src):
            # 全畫面：畫面 + 聲音（webm 內建音軌）
            add full_cg_play_with_sound(full_cg_view_src):
                xalign 0.5
                yalign 0.5
        elif full_cg_is_missing(full_cg_view_src):
            vbox:
                xalign 0.5
                yalign 0.5
                spacing 12
                text "找不到對應圖片資源" size 36 color "#aaaaaa" xalign 0.5
                text str(full_cg_view_src) size 24 color "#666666" xalign 0.5
                text "（資料表有登錄，但封包無此圖）" size 20 color "#555555" xalign 0.5
        else:
            add full_cg_displayable(full_cg_view_src, placeholder=True, size=(1920, 1000)):
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
            if not renpy.has_screen("full_cg_entry_button"):
                return
            # 一律掛在 top；是否畫出按鈕由 screen 內 is_mod_enabled 判斷
            if renpy.get_screen("full_cg_entry_button", layer="top") is None:
                renpy.show_screen("full_cg_entry_button", _layer="top")
        except Exception:
            pass

    if _full_cg_force_btn not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_full_cg_force_btn)

    if _full_cg_force_btn not in config.start_callbacks:
        config.start_callbacks.append(_full_cg_force_btn)

    if "full_cg_entry_button" not in config.overlay_screens:
        config.overlay_screens.append("full_cg_entry_button")
    if "full_cg_entry_button" not in config.always_shown_screens:
        config.always_shown_screens.append("full_cg_entry_button")

    # 全域 F10
    config.keymap["full_cg_open"] = ["K_F10"]
    try:
        config.underlay.append(renpy.Keymap(full_cg_open=Function(full_cg_toggle_gallery)))
    except Exception:
        pass
