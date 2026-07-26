# 模組開發指南

## 環境

1. 自行從 [官方通路（Patreon · HEXATAIL）](https://www.patreon.com/cw/hexatail) 取得 **Agent17** 遊戲。
2. 依 [INSTALL.md](INSTALL.md) 安裝本載入器。
3. 模組目錄：`遊戲根目錄/game/mods/`。

本倉庫**不含**遊戲本體、資源包、存檔。

## 最小模組

```
game/mods/my_mod/
  mod.json
  script.rpy
```

### mod.json

| 欄位 | 必填 | 說明 |
|------|------|------|
| `id` | 建議 | 唯一 ID，給 `is_mod_enabled("id")` 使用 |
| `name` | 建議 | 介面顯示名稱（繁中） |
| `name_en` | 否 | 英文顯示名 |
| `version` | 否 | 例如 `1.0.0` |
| `author` | 否 | 作者 |
| `description` | 否 | 簡短說明 |
| `default_enabled` | 否 | 預設是否開啟（預設 `false`） |
| `requires_restart` | 否 | 切換後是否提示重啟（預設 `true`） |
| `priority` | 否 | 列表排序，數字越小越前 |

沒有 `mod.json` 時，仍會以資料夾名稱當模組（功能受限）。

### script.rpy

Ren'Py 會載入 `game/` 下腳本；**請用開關包住行為**：

```renpy
init python:
    if is_mod_enabled("my_mod"):
        # 只在「模組管理」開啟時執行
        pass
```

畫面、overlay 同理：

```renpy
screen my_banner():
    if is_mod_enabled("my_mod") and renpy.get_screen("main_menu"):
        text "Hello" xalign 0.5 yalign 0.1

init python:
    if "my_banner" not in config.overlay_screens:
        config.overlay_screens.append("my_banner")
```

## API

| 符號 | 說明 |
|------|------|
| `is_mod_enabled(mod_id)` | 是否開啟 |
| `mod_manager.list_mods()` | 模組列表 |
| `mod_manager.set_enabled(id, True/False)` | 設定開關 |
| `mod_manager.refresh()` | 重新掃描 `mods/` |
| `mod_manager.open_mods_folder()` | 開啟資料夾 |

狀態存放：

- `persistent.mod_enabled`
- `game/mods_state.json`（備份）

## 注意

- 資料夾名不要用 `_` 開頭（會被忽略）。
- 多數腳本改動需**重啟遊戲**才完整生效。
- 勿散佈遊戲本體或破解檔；模組請遵守原作服務條款與當地法律。
- 本載入器為第三方工具，**與 HEXATAIL / Agent17 官方無隸屬關係**。

## 除錯

1. 按 **F9** 是否出現模組列表。
2. `mod.json` 的 `id` 是否與 `is_mod_enabled("...")` 一致。
3. 看 `log.txt` / `traceback.txt`（遊戲根目錄）。
