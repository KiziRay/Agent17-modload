# SPDX-License-Identifier: MIT
# Example mod — only active when enabled in 模組管理

screen example_hello_banner():
    zorder 50
    if is_mod_enabled("example_hello") and renpy.get_screen("main_menu"):
        text "【範例模組已開啟】":
            xalign 0.5
            yalign 0.08
            size 28
            color "#88ff88"
            outlines [ (1, "#000000", 0, 0) ]


init python:
    if "example_hello_banner" not in config.overlay_screens:
        config.overlay_screens.append("example_hello_banner")
