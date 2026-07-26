# 繁中介面詞彙模組：開啟時覆寫字串翻譯（台灣用語）
# 需 is_mod_enabled("tw_ui_lexicon")

init -5 python:
    # (old, new) — old 可為韓文原文、英文系統句、或既有譯文
    TW_UI_LEXICON = [
        # 主選單／系統（韓文原文）
        ("시작 >", "開始遊戲"),
        ("불러오기", "讀取"),
        ("저장하기", "儲存"),
        ("저장", "儲存"),
        ("환경설정", "設定"),
        ("설정", "設定"),
        ("시스템", "系統"),
        ("시스템 메뉴", "系統選單"),
        ("메인메뉴", "主選單"),
        ("게임 종료", "結束遊戲"),
        ("게임을 종료하시겠습니까?", "確定要結束遊戲嗎？"),
        ("게임을 종료하고 메인메뉴로 가시겠습니까?", "確定要返回主選單嗎？"),
        ("취소", "取消"),
        ("네", "是"),
        ("아니오", "否"),
        ("사진", "照片"),
        ("사진 획득", "獲得照片"),
        ("소지한 사진이 없습니다.", "尚未擁有任何照片。"),
        ("아이템 사용", "使用道具"),
        ("화면 모드", "顯示模式"),
        ("창 화면", "視窗模式"),
        ("전체 화면", "全螢幕"),
        ("소리", "音效"),
        ("배경음 음량", "音樂音量"),
        ("효과음 음량", "音效音量"),
        ("음성 음량", "語音音量"),
        ("텍스트", "文字"),
        ("텍스트 속도", "文字速度"),
        ("자동 진행 속도", "自動播放速度"),
        ("읽지 않은 지문도 넘기기", "快轉未讀文字"),
        ("특수 버튼 활성화", "啟用特殊按鈕"),
        ("자동 진행", "自動播放"),
        ("스킵", "快轉"),
        ("뒤로 가기", "返回"),
        ("UI 숨기기", "隱藏介面"),
        ("새로운 버전 출시!", "有新版本！"),
        ("새 업데이트!", "新更新！"),
        ("무료 다운로드", "免費下載"),
        ("게임 추가 정보", "其他資訊"),
        ("인기투표", "人氣投票"),
        ("패치노트", "更新說明"),
        ("후원 & 다운로드", "贊助與下載"),
        ("제작", "製作名單"),
        ("제목을 입력하세요.", "請輸入標題。"),
        ("빈 슬롯", "空白欄位"),
        ("삭제", "刪除"),
        ("페이지", "頁面"),
        ("자동저장", "自動存檔"),
        ("업로드", "上傳"),
        ("다운로드", "下載"),
        # 英文系統
        ("Are you sure you want to quit?", "確定要結束遊戲嗎？"),
        ("Are you sure you want to quit the game?", "確定要結束遊戲嗎？"),
        ("Are you sure?", "你確定嗎？"),
        ("Yes", "是"),
        ("No", "否"),
        ("Save", "儲存"),
        ("Load", "讀取"),
        ("Preferences", "設定"),
        ("Main Menu", "主選單"),
        ("Quit", "結束"),
        ("Return", "返回"),
        ("History", "對話紀錄"),
        ("Skip", "快轉"),
        ("Auto", "自動"),
        ("Help", "說明"),
        ("About", "關於"),
        ("Fullscreen", "全螢幕"),
        ("Window", "視窗"),
        ("Windowed", "視窗模式"),
        ("Music", "音樂"),
        ("Sound", "音效"),
        ("Voice", "語音"),
        ("Display", "顯示"),
        ("Text Speed", "文字速度"),
        ("Auto-Forward Time", "自動播放速度"),
        ("Empty Slot.", "空白欄位。"),
        ("Empty Slot", "空白欄位"),
        ("Delete", "刪除"),
        ("Page", "頁面"),
        ("Autosave", "自動存檔"),
        ("Start", "開始"),
        ("Continue", "繼續"),
        ("Confirm", "確認"),
        ("Cancel", "取消"),
        ("OK", "確定"),
        ("Language", "語言"),
        ("Keyboard", "鍵盤"),
        ("Mouse", "滑鼠"),
        ("Gamepad", "手把"),
        ("Enter", "Enter（確認）"),
        ("Space", "空白鍵"),
        ("Tab", "Tab"),
        ("Page Up", "Page Up"),
        ("Page Down", "Page Down"),
        ("Click", "點選"),
        ("Skipping", "快轉中"),
        ("Auto-Play", "自動播放"),
        ("System", "系統"),
        ("Settings", "設定"),
        ("Setting", "設定"),
        ("Credit", "製作名單"),
        ("Credits", "製作名單"),
        ("Sponsors", "贊助"),
        ("Upload", "上傳"),
        ("Download", "下載"),
        ("Music Player", "音樂播放器"),
        ("Log", "對話紀錄"),
        ("Used", "已使用"),
        ("Acquired", "已獲得"),
        ("Active", "啟用中"),
        ("Inactive", "未啟用"),
        ("Enable", "啟用"),
        ("Disable", "停用"),
        ("Reset", "重設"),
        ("Default", "預設"),
        ("Off", "關"),
        ("On", "開"),
        # 常見簡體／不自然用語 → 台灣
        ("軟件", "軟體"),
        ("視頻", "影片"),
        ("默認", "預設"),
        ("信息", "資訊"),
        ("網絡", "網路"),
        ("屏幕", "螢幕"),
        ("鼠標", "滑鼠"),
        ("文件夾", "資料夾"),
        ("程序", "程式"),
        ("質量", "品質"),
        ("服務器", "伺服器"),
        ("數據", "資料"),
        ("內存", "記憶體"),
        ("硬件", "硬體"),
        ("芯片", "晶片"),
        ("分辨率", "解析度"),
        ("全屏", "全螢幕"),
        ("加載", "載入"),
        ("登錄", "登入"),
        ("短信", "簡訊"),
        ("用戶", "使用者"),
        ("賬號", "帳號"),
        ("設置", "設定"),
        ("菜單", "選單"),
        ("是的", "是"),
        ("不", "否"),
        ("新遊戲", "開始遊戲"),
        ("確定要離開嗎？", "確定要結束遊戲嗎？"),
        ("确定要离开吗？", "確定要結束遊戲嗎？"),
    ]

    def tw_ui_lexicon_apply():
        if not is_mod_enabled("tw_ui_lexicon"):
            return
        try:
            lang = "chinese_taiwan"
            stl = renpy.game.script.translator.strings[lang]
            renpy.game.script.translator.languages.add(lang)
            for old, new in TW_UI_LEXICON:
                # 直接覆寫（允許取代既有譯文）
                stl.translations[old] = new
            # 同步套到目前語系（若剛好是 chinese_taiwan）
            try:
                renpy.restarts_interaction()
            except Exception:
                pass
        except Exception:
            pass


init 999 python:
    # 開場套用
    tw_ui_lexicon_apply()


# 每次進互動再保險套一次（讀檔後也有效）
init python:
    def _tw_ui_lexicon_on_interact():
        try:
            if is_mod_enabled("tw_ui_lexicon"):
                tw_ui_lexicon_apply()
        except Exception:
            pass

    if _tw_ui_lexicon_on_interact not in config.start_interact_callbacks:
        config.start_interact_callbacks.append(_tw_ui_lexicon_on_interact)
