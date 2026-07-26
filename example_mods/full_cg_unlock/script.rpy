# 全 CG 解鎖：將 TB_Picture 全部放入 g_InventoryPicture
# 僅在模組開啟時執行（不覆蓋 after_load 標籤，避免與本體衝突）

init python:
    def full_cg_unlock_all():
        """解鎖全部照片 CG（靜默，不連彈視窗）。"""
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

        # 已齊則跳過
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


init 999 python:
    def _full_cg_on_start():
        full_cg_try_unlock()

    if _full_cg_on_start not in config.start_callbacks:
        config.start_callbacks.append(_full_cg_on_start)

    def _full_cg_on_interact():
        # 讀檔／開新進度後補齊；已滿則幾乎零成本
        full_cg_try_unlock()

    if _full_cg_on_interact not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_full_cg_on_interact)
