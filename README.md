# Agent17-modload

Agent17 **第三方模組載入器**與開發說明。

- 授權：**MIT**（見 [LICENSE](LICENSE)）
- **不含**遊戲本體、資源包、存檔或破解檔
- 與 HEXATAIL / Agent17 **無官方隸屬關係**

## 遊戲請至官方通路下載

請自行購買／下載正版遊戲：

### [Patreon · HEXATAIL](https://www.patreon.com/cw/hexatail)

本倉庫只提供「載入器原始碼 + 文件 + 範例模組骨架」。

## 功能

- 仍用官方 `Agent17.exe` 啟動（不需 BAT）
- 預設**僅快捷鍵 F9** 開啟模組管理（無畫面按鈕，不擋原版 UI）
- 掃描 `game/mods/<id>/`，介面開關，狀態可持久化

## 快速開始

1. 從 [Patreon · HEXATAIL](https://www.patreon.com/cw/hexatail) 取得遊戲  
2. 依 [docs/INSTALL.md](docs/INSTALL.md) 把 `loader/*.rpy` 放進 `game/`  
3. （可選）複製 `example_mods/*` 到 `game/mods/`  
   - `example_hello` — 測試用提示  
   - `tw_ui_lexicon` — 台灣繁中介面詞彙  
   - `full_cg_unlock` — 全照片 CG 圖鑑解鎖  
4. 啟動遊戲 → 按 **F9** 開啟模組管理

## 倉庫結構

```
loader/                 載入器（複製到遊戲 game/）
  00_mod_manager.rpy
  mod_manager_ui.rpy
  zzz_mod_force.rpy
example_mods/
  example_hello/        範例模組
docs/
  INSTALL.md            安裝
  DEVELOPMENT.md        開發模組
LICENSE                 MIT
README.md
```

## 開發模組

見 **[docs/DEVELOPMENT.md](docs/DEVELOPMENT.md)**。

最小結構：

```
game/mods/my_mod/
  mod.json
  script.rpy
```

```renpy
init python:
    if is_mod_enabled("my_mod"):
        pass  # 你的邏輯
```

## 免責

- 請遵守原作服務條款與所在地法律。  
- 使用模組導致存檔損壞、無法啟動等，請自行負責。  
- 禁止在本專案討論或散佈盜版遊戲檔。

## License

MIT © 2026 KiziRay
