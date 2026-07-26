# 安裝載入器

## 你需要先有遊戲

本倉庫**不包含** Agent17 遊戲檔。

請至官方通路取得正版：

**[Patreon · HEXATAIL](https://www.patreon.com/cw/hexatail)**

安裝並確認可用 `Agent17.exe`（或官方提供的啟動檔）開啟遊戲。

## 安裝步驟

1. 下載本倉庫（Clone 或 Code → Download ZIP）。
2. 將 `loader/` 內三個檔案複製到遊戲的 **`game/`** 資料夾：

   | 來源（本倉庫） | 放到 |
   |----------------|------|
   | `loader/00_mod_manager.rpy` | `遊戲/game/00_mod_manager.rpy` |
   | `loader/mod_manager_ui.rpy` | `遊戲/game/mod_manager_ui.rpy` |
   | `loader/zzz_mod_force.rpy` | `遊戲/game/zzz_mod_force.rpy` |

3. （可選）複製範例模組：

   ```
   example_mods/example_hello/  →  遊戲/game/mods/example_hello/
   ```

4. 只啟動官方遊戲執行檔（例如 `Agent17.exe`），**不需要**額外 BAT。

## 如何開啟模組選單

| 時機 | 操作 |
|------|------|
| 主選單 | 畫面**最下方正中央**「模組」小鈕 |
| 任何時候 | 鍵盤 **F9**（或 F8 / F10） |

選單內可：開關模組、重新整理、開啟 `game/mods` 資料夾。

## 目錄示意

```
Agent17/                    ← 官方遊戲根目錄（自備）
  Agent17.exe
  game/
    archive.rpa             ← 官方內容（本倉庫不提供）
    00_mod_manager.rpy      ← 本載入器
    mod_manager_ui.rpy
    zzz_mod_force.rpy
    mods/
      example_hello/
        mod.json
        script.rpy
```

## 移除

刪除上述三個 `.rpy`（及對應 `.rpyc` 快取），並視需要刪除 `game/mods/`、`game/mods_state.json`。
