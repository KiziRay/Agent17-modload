# SPDX-License-Identifier: MIT
# Agent17-modload — third-party mod loader (not affiliated with HEXATAIL)
# 模組管理核心 — 仍由 Agent17.exe 啟動，不需額外 BAT
# 模組目錄：game/mods/<id>/mod.json + 可選 script.rpy

init -200 python:
    import json
    import os
    import codecs

    class _ModInfo(object):
        def __init__(self, path, data):
            self.path = path
            self.id = str(data.get("id") or os.path.basename(path))
            self.name = data.get("name") or self.id
            self.name_en = data.get("name_en") or self.name
            self.version = str(data.get("version") or "0.0.0")
            self.author = data.get("author") or ""
            self.description = data.get("description") or ""
            self.default_enabled = bool(data.get("default_enabled", False))
            self.requires_restart = bool(data.get("requires_restart", True))
            self.priority = int(data.get("priority", 100))

    class ModManager(object):
        """掃描 game/mods、讀寫開關狀態。"""

        STATE_NAME = "mods_state.json"

        def __init__(self):
            self.mods = []  # type: list[_ModInfo]
            self._by_id = {}
            self._enabled = {}  # id -> bool
            self._dirty_restart = False
            self._loaded = False

        def mods_root(self):
            return os.path.join(config.gamedir, "mods")

        def state_path(self):
            return os.path.join(config.gamedir, self.STATE_NAME)

        def _read_json(self, path):
            try:
                with codecs.open(path, "r", "utf-8") as f:
                    return json.load(f)
            except Exception:
                return None

        def _write_json(self, path, obj):
            try:
                d = os.path.dirname(path)
                if d and not os.path.isdir(d):
                    os.makedirs(d)
                with codecs.open(path, "w", "utf-8") as f:
                    json.dump(obj, f, ensure_ascii=False, indent=2)
                return True
            except Exception:
                return False

        def scan(self):
            self.mods = []
            self._by_id = {}
            root = self.mods_root()
            if not os.path.isdir(root):
                try:
                    os.makedirs(root)
                except Exception:
                    pass
                return
            try:
                names = sorted(os.listdir(root))
            except Exception:
                names = []
            for name in names:
                if name.startswith(".") or name.startswith("_"):
                    continue
                folder = os.path.join(root, name)
                if not os.path.isdir(folder):
                    continue
                meta_path = os.path.join(folder, "mod.json")
                data = self._read_json(meta_path)
                if not isinstance(data, dict):
                    # 沒有 mod.json 也允許：用資料夾名當 id
                    data = {
                        "id": name,
                        "name": name,
                        "description": "（無 mod.json）",
                        "default_enabled": False,
                    }
                if not data.get("id"):
                    data["id"] = name
                info = _ModInfo(folder, data)
                # 避免重複 id
                if info.id in self._by_id:
                    info.id = name
                self.mods.append(info)
                self._by_id[info.id] = info
            self.mods.sort(key=lambda m: (m.priority, m.name.lower(), m.id))

        def load_state(self):
            # persistent 優先，檔案作備份
            disk = self._read_json(self.state_path()) or {}
            disk_en = disk.get("enabled") if isinstance(disk, dict) else {}
            if not isinstance(disk_en, dict):
                disk_en = {}

            pe = getattr(persistent, "mod_enabled", None)
            if not isinstance(pe, dict):
                pe = {}
                persistent.mod_enabled = pe

            self._enabled = {}
            for m in self.mods:
                if m.id in pe:
                    self._enabled[m.id] = bool(pe[m.id])
                elif m.id in disk_en:
                    self._enabled[m.id] = bool(disk_en[m.id])
                else:
                    self._enabled[m.id] = m.default_enabled
                    pe[m.id] = self._enabled[m.id]
            # 清掉已不存在的 id
            for k in list(pe.keys()):
                if k not in self._by_id:
                    del pe[k]
            self._persist()

        def _persist(self):
            pe = getattr(persistent, "mod_enabled", None)
            if not isinstance(pe, dict):
                pe = {}
                persistent.mod_enabled = pe
            for mid, val in self._enabled.items():
                pe[mid] = bool(val)
            try:
                renpy.save_persistent()
            except Exception:
                pass
            self._write_json(
                self.state_path(),
                {
                    "enabled": dict(self._enabled),
                    "version": 1,
                },
            )

        def ensure_ready(self):
            if not self._loaded:
                self.scan()
                self.load_state()
                self._loaded = True

        def refresh(self):
            self.scan()
            self.load_state()
            self._loaded = True

        def is_enabled(self, mod_id):
            self.ensure_ready()
            return bool(self._enabled.get(mod_id, False))

        def set_enabled(self, mod_id, value):
            self.ensure_ready()
            if mod_id not in self._by_id:
                return False
            value = bool(value)
            old = bool(self._enabled.get(mod_id, False))
            if old == value:
                return True
            self._enabled[mod_id] = value
            info = self._by_id[mod_id]
            if info.requires_restart:
                self._dirty_restart = True
            self._persist()
            return True

        def toggle(self, mod_id):
            return self.set_enabled(mod_id, not self.is_enabled(mod_id))

        def needs_restart(self):
            return bool(self._dirty_restart)

        def clear_restart_flag(self):
            self._dirty_restart = False

        def get(self, mod_id):
            self.ensure_ready()
            return self._by_id.get(mod_id)

        def list_mods(self):
            self.ensure_ready()
            return list(self.mods)

        def open_mods_folder(self):
            root = self.mods_root()
            if not os.path.isdir(root):
                try:
                    os.makedirs(root)
                except Exception:
                    return False
            try:
                if renpy.windows:
                    os.startfile(root)  # type: ignore[attr-defined]
                elif renpy.macintosh:
                    import subprocess
                    subprocess.Popen(["open", root])
                else:
                    import subprocess
                    subprocess.Popen(["xdg-open", root])
                return True
            except Exception:
                return False

        def display_name(self, mod):
            # 繁中介面優先 name
            lang = str(getattr(_preferences, "language", None) or "")
            if lang in ("chinese_taiwan", "chinese_traditional", "chinese_simplified"):
                return mod.name
            return mod.name_en or mod.name

    mod_manager = ModManager()


init 0 python:
    # persistent 可用後初始化
    mod_manager.ensure_ready()


# 給模組腳本用的簡寫
init python:
    def is_mod_enabled(mod_id):
        return mod_manager.is_enabled(mod_id)
