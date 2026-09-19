#!/usr/bin/env python3
"""Generate and validate the Default+ ports from palette.yaml.

Three modes, all of which exit non-zero on failure:

  --check      palette.yaml still matches xcode/Default+.xccolortheme, and every
               value under `derived` is what its stated rule produces.
  --generate   rewrite the ports whose formats are flat enough to emit safely.
  --validate   scan every port file for hex colours that are not in the palette.

With no arguments it runs all three, check first.

Why this exists: twelve port files were hand-maintained against a YAML nobody
parsed, and three mutually inconsistent palettes ended up in circulation. The
validate pass is what catches the next one.

Python 3 standard library only — no PyYAML. The palette is a deliberately small
YAML subset (two levels, scalar values) so it can be parsed without a dependency.
"""

from __future__ import annotations

import argparse
import plistlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PALETTE = ROOT / "palette.yaml"
XCODE_THEME = ROOT / "xcode" / "Default+.xccolortheme"

# Matches #RRGGBB and #RRGGBBAA. The alpha suffix is stripped before lookup, so
# a translucent tint of a palette colour validates while a wrong hue still fails.
HEX_RE = re.compile(r"#([0-9A-Fa-f]{6})(?:[0-9A-Fa-f]{2})?\b")


# ─── palette.yaml ──────────────────────────────────────────────────────────


def load_palette(path: Path = PALETTE) -> dict[str, dict[str, str]]:
    """Parse the two-level scalar YAML subset palette.yaml is written in."""
    out: dict[str, dict[str, str]] = {}
    section: dict[str, str] | None = None
    for lineno, raw in enumerate(path.read_text().splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indented = raw.startswith(" ")
        k, _, v = raw.strip().partition(":")
        if not indented:
            section = out.setdefault(k.strip(), {})
            continue
        if section is None:
            raise SystemExit(f"{path}:{lineno}: indented line outside a section")
        v = v.strip()
        # A value may be quoted or bare, and may carry a trailing comment. Hex
        # colours start with '#', so a naive split on '#' would eat the value.
        if v.startswith('"') or v.startswith("'"):
            quote = v[0]
            end = v.index(quote, 1)
            v = v[1:end]
        else:
            v = v.split(" #", 1)[0].strip()
        section[k.strip()] = v
    return out


# ─── colour helpers ────────────────────────────────────────────────────────


def h2r(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def r2h(rgb) -> str:
    return "#%02X%02X%02X" % tuple(max(0, min(255, round(c))) for c in rgb)


def over(fg: str, bg: str, alpha: float) -> str:
    """Composite fg over bg at the given opacity."""
    f, b = h2r(fg), h2r(bg)
    return r2h([f[i] * alpha + b[i] * (1 - alpha) for i in range(3)])


def floats(h: str) -> str:
    """'#FC4651' -> '0.988235 0.27451 0.317647' (Apple's own trimming)."""
    parts = []
    for c in h2r(h):
        s = f"{c / 255:.6f}".rstrip("0").rstrip(".")
        parts.append(s if s else "0")
    return " ".join(parts)


def relative_luminance(h: str) -> float:
    def chan(c: float) -> float:
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    r, g, b = (chan(c) for c in h2r(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = relative_luminance(a), relative_luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


# ─── --check ───────────────────────────────────────────────────────────────

# palette.yaml key -> the key in Default+.xccolortheme it must equal.
# 'syntax.markup_code' is deliberately absent: Apple ships the light theme's
# magenta there in both stock themes, and we correct it. See palette.yaml.
XCODE_BINDINGS = {
    ("base", "background"): "DVTSourceTextBackground",
    ("base", "foreground"): "xcode.syntax.plain",
    ("base", "cursor"): "DVTSourceTextInsertionPointColor",
    ("base", "selection_background"): "DVTSourceTextSelectionColor",
    ("base", "current_line"): "DVTSourceTextCurrentLineHighlightColor",
    ("base", "invisibles"): "DVTSourceTextInvisiblesColor",
    ("base", "muted_text"): "DVTScrollbarMarkerDiffColor",
    ("syntax", "plain"): "xcode.syntax.plain",
    ("syntax", "comment"): "xcode.syntax.comment",
    ("syntax", "string"): "xcode.syntax.string",
    ("syntax", "keyword"): "xcode.syntax.keyword",
    ("syntax", "number"): "xcode.syntax.number",
    ("syntax", "macro"): "xcode.syntax.identifier.macro",
    ("syntax", "attribute"): "xcode.syntax.attribute",
    ("syntax", "url"): "xcode.syntax.url",
    ("syntax", "declaration"): "xcode.syntax.declaration.other",
    ("syntax", "declaration_type"): "xcode.syntax.declaration.type",
    ("syntax", "project_identifier"): "xcode.syntax.identifier.type",
    ("syntax", "system_member"): "xcode.syntax.identifier.function.system",
    ("syntax", "system_type"): "xcode.syntax.identifier.type.system",
    ("status", "error"): "DVTScrollbarMarkerErrorColor",
    ("status", "warning"): "DVTScrollbarMarkerWarningColor",
    ("status", "success"): "DVTConsoleDebuggerPromptTextColor",
    ("status", "runtime_issue"): "DVTScrollbarMarkerRuntimeIssueColor",
    ("status", "analyzer"): "DVTScrollbarMarkerAnalyzerColor",
    ("status", "breakpoint"): "DVTScrollbarMarkerBreakpointColor",
    ("status", "neutral"): "DVTScrollbarMarkerDiffColor",
}


def xcode_colors(path: Path = XCODE_THEME) -> dict[str, str]:
    data = plistlib.loads(path.read_bytes())
    out = {}
    for key, value in data.items():
        if isinstance(value, str) and re.match(r"^[\d.]+ [\d.]+ [\d.]+", value):
            out[key] = r2h([float(x) * 255 for x in value.split()[:3]])
    for key, value in data.get("DVTSourceTextSyntaxColors", {}).items():
        out[key] = r2h([float(x) * 255 for x in value.split()[:3]])
    return out


# derived key -> (source palette ref, alpha over background)
DERIVED_RULES = {
    "diff_added_bg": ("syntax.comment", 0.20),
    "diff_removed_bg": ("syntax.string", 0.20),
    "diff_moved_added_bg": ("syntax.declaration", 0.20),
    "diff_moved_removed_bg": ("syntax.system_member", 0.20),
    "diff_added_content_bg": ("syntax.comment", 0.35),
    "diff_removed_content_bg": ("syntax.string", 0.35),
    "context_content_bg": ("base.muted_text", 0.20),
    "current_line_solid": ("base.current_line", 0.50),
    "accent_muted": ("syntax.declaration", 0.50),
    "muted_green": ("syntax.comment", 0.50),
    "muted_red": ("syntax.string", 0.50),
    "muted_yellow": ("syntax.attribute", 0.50),
    "neutral_raised": ("base.foreground", 0.10),
    "neutral_overlay": ("base.foreground", 0.30),
    "neutral_subtext": ("base.foreground", 0.70),
}

SHIMMER_RULES = {
    "shimmer_blue": "syntax.declaration",
    "shimmer_magenta": "syntax.keyword",
    "shimmer_yellow": "syntax.number",
    "shimmer_orange": "syntax.macro",
    "shimmer_red": "syntax.string",
    "shimmer_green": "syntax.comment",
    "shimmer_indigo": "syntax.url",
    "shimmer_violet": "syntax.system_member",
}


def ref(p, dotted: str) -> str:
    section, key = dotted.split(".")
    return p[section][key]


def check(p) -> list[str]:
    errors = []
    xc = xcode_colors()

    for (section, key), xkey in XCODE_BINDINGS.items():
        want, got = xc.get(xkey), p[section][key]
        if want is None:
            errors.append(f"{xkey} missing from {XCODE_THEME.name}")
        elif want.upper() != got.upper():
            errors.append(f"{section}.{key} is {got}, but {xkey} is {want}")

    bg, fg = p["base"]["background"], p["base"]["foreground"]
    for key, (src, alpha) in DERIVED_RULES.items():
        want = over(ref(p, src), bg, alpha)
        got = p["derived"][key]
        if want.upper() != got.upper():
            errors.append(
                f"derived.{key} is {got}, but {src} at {alpha:.0%} over background is {want}"
            )
    for key, src in SHIMMER_RULES.items():
        want = over(fg, ref(p, src), 0.40)
        got = p["claude_code_extended"][key]
        if want.upper() != got.upper():
            errors.append(
                f"claude_code_extended.{key} is {got}, but {src} 40% toward foreground is {want}"
            )

    # Slots 0 and 8 are background tones and never carry text; everything else
    # in the ANSI ramp must be legible on the background.
    for slot, hexv in p["ansi"].items():
        if slot in ("black", "bright_black"):
            continue
        ratio = contrast(hexv, bg)
        if ratio < 4.5:
            errors.append(f"ansi.{slot} {hexv} is {ratio:.2f}:1 on {bg}, below 4.5:1")

    return errors


# ─── --generate ────────────────────────────────────────────────────────────

ANSI_ORDER = [
    "black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
    "bright_black", "bright_red", "bright_green", "bright_yellow",
    "bright_blue", "bright_magenta", "bright_cyan", "bright_white",
]

BANNER = "Generated by bin/build.py from palette.yaml — do not edit by hand."


def gen_ghostty(p) -> tuple[Path, str]:
    a, b = p["ansi"], p["base"]
    lines = [
        "# Default+",
        f"# {BANNER}",
        "",
        "# Normal and bright are distinct colours, so bold must not also switch hue.",
        "bold-is-bright = false",
        "",
        f"background = {b['background']}",
        f"foreground = {b['foreground']}",
        f"cursor-color = {b['cursor']}",
        f"selection-background = {b['selection_background']}",
        f"selection-foreground = {b['selection_foreground']}",
        "",
        "# ANSI 0–7",
    ]
    for i, slot in enumerate(ANSI_ORDER):
        if i == 8:
            lines += ["", "# ANSI 8–15 (bright)"]
        lines.append(f"palette = {i}={a[slot]}")
    return ROOT / "ghostty" / "Default+", "\n".join(lines) + "\n"


def gen_iterm(p) -> tuple[Path, str]:
    a, b = p["ansi"], p["base"]

    def color(h: str, key: str) -> str:
        r, g, bl = (c / 255 for c in h2r(h))
        return (
            f"\t<key>{key}</key>\n"
            "\t<dict>\n"
            "\t\t<key>Color Space</key>\n\t\t<string>sRGB</string>\n"
            f"\t\t<key>Red Component</key>\n\t\t<real>{r:.6f}</real>\n"
            f"\t\t<key>Green Component</key>\n\t\t<real>{g:.6f}</real>\n"
            f"\t\t<key>Blue Component</key>\n\t\t<real>{bl:.6f}</real>\n"
            "\t\t<key>Alpha Component</key>\n\t\t<real>1</real>\n"
            "\t</dict>"
        )

    body = [color(a[slot], f"Ansi {i} Color") for i, slot in enumerate(ANSI_ORDER)]
    body += [
        color(b["background"], "Background Color"),
        color(b["foreground"], "Foreground Color"),
        color(b["foreground"], "Bold Color"),
        color(b["cursor"], "Cursor Color"),
        color(b["background"], "Cursor Text Color"),
        color(b["selection_background"], "Selection Color"),
        color(b["selection_foreground"], "Selected Text Color"),
        color(p["syntax"]["url"], "Link Color"),
        color(p["syntax"]["string"], "Badge Color"),
    ]
    out = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        f"<!-- Default+. {BANNER} -->\n"
        '<plist version="1.0">\n<dict>\n' + "\n".join(body) + "\n</dict>\n</plist>\n"
    )
    return ROOT / "iterm" / "Default+.itermcolors", out


def _ns_color(h: str) -> bytes:
    """An NSKeyedArchiver-encoded NSColor, the form Apple Terminal stores."""
    archive = {
        "$version": 100000,
        "$archiver": "NSKeyedArchiver",
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "NSRGB": (floats(h) + "\x00").encode("ascii"),
                "NSColorSpace": 1,
                "$class": plistlib.UID(2),
            },
            {"$classname": "NSColor", "$classes": ["NSColor", "NSObject"]},
        ],
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


def _ns_font(name: str, size: float) -> bytes:
    """An NSKeyedArchiver-encoded NSFont, the form Apple Terminal stores."""
    archive = {
        "$version": 100000,
        "$archiver": "NSKeyedArchiver",
        "$top": {"root": plistlib.UID(1)},
        "$objects": [
            "$null",
            {
                "NSSize": size,
                "NSfFlags": 16,
                "NSName": plistlib.UID(2),
                "$class": plistlib.UID(3),
            },
            name,
            {"$classname": "NSFont", "$classes": ["NSFont", "NSObject"]},
        ],
    }
    return plistlib.dumps(archive, fmt=plistlib.FMT_BINARY)


TERMINAL_ANSI_KEYS = [
    "ANSIBlackColor", "ANSIRedColor", "ANSIGreenColor", "ANSIYellowColor",
    "ANSIBlueColor", "ANSIMagentaColor", "ANSICyanColor", "ANSIWhiteColor",
    "ANSIBrightBlackColor", "ANSIBrightRedColor", "ANSIBrightGreenColor",
    "ANSIBrightYellowColor", "ANSIBrightBlueColor", "ANSIBrightMagentaColor",
    "ANSIBrightCyanColor", "ANSIBrightWhiteColor",
]


def gen_terminal(p) -> tuple[Path, bytes]:
    a, b = p["ansi"], p["base"]
    prof: dict[str, object] = {"name": "Default+", "type": "Window Settings"}
    for key, slot in zip(TERMINAL_ANSI_KEYS, ANSI_ORDER):
        prof[key] = _ns_color(a[slot])
    prof["BackgroundColor"] = _ns_color(b["background"])
    prof["TextColor"] = _ns_color(b["foreground"])
    prof["TextBoldColor"] = _ns_color(b["foreground"])
    prof["CursorColor"] = _ns_color(b["cursor"])
    prof["SelectionColor"] = _ns_color(b["selection_background"])
    prof.update(
        {
            "Font": _ns_font("SFMonoTerminal-Regular", 14.0),
            "FontAntialias": True,
            "FontWidthSpacing": 1.004032258064516,
            "ProfileCurrentVersion": 2.09,
            "columnCount": 120,
            "rowCount": 36,
            "CursorType": 0,
            "CursorBlink": True,
            "BlinkText": True,
            "UseBoldFonts": False,
            # Normal and bright differ, so bold must not be promoted to bright.
            "UseBrightBold": False,
            # Terminal rewrites ANSI foreground colours for "readability" when
            # this is on, which silently overrides the palette. The ramp is
            # already contrast-checked in --check, so turn the guesswork off.
            "DynamicANSIForegroundColors": False,
            "Bell": False,
            "VisualBell": False,
            "VisualBellOnlyWhenMuted": False,
            "DisableANSIColor": False,
        }
    )
    return ROOT / "terminal" / "Default+.terminal", plistlib.dumps(
        prof, fmt=plistlib.FMT_XML
    )


# Hand-picked, NOT nearest-RGB. tig 2.6.1 has no truecolor, and nearest-RGB
# collapses selection onto the grey ramp next to `muted`, so the roles stop
# being distinguishable. Each index below is checked to be distinct.
TIG_256 = {
    "background": (233, "#121212"),
    "foreground": (231, "#ffffff"),
    "selection": (60, "#5f5f87"),   # keeps the blue tint; 59 is flat grey
    "muted": (239, "#4e4e4e"),
    "muted_text": (245, "#8a8a8a"),
    "green": (35, "#00af5f"),
    "red": (203, "#ff5f5f"),
    "magenta": (198, "#ff0087"),
    "yellow": (221, "#ffd75f"),
    "tan": (179, "#d7af5f"),
    "blue": (75, "#5fafff"),
    "cyan": (74, "#5fafd7"),
    "teal": (79, "#5fd7af"),
    "purple": (135, "#af5fff"),
}


def gen_tig(p) -> tuple[Path, str]:
    c = {k: f"color{v[0]}" for k, v in TIG_256.items()}
    bg, fg = c["background"], c["foreground"]
    header = [
        "# Default+ theme for tig",
        f"# {BANNER}",
        "#",
        "# tig 2.6.1 has no truecolor support, so each palette entry is mapped to a",
        "# 256-colour index. These are HAND-PICKED, not nearest-RGB: nearest-RGB puts",
        "# the selection colour on the grey ramp right next to `muted`, collapsing two",
        "# distinct roles. This table is the authority for this file.",
        "#",
    ]
    for name, (idx, approx) in TIG_256.items():
        src = {
            "green": "syntax.comment", "red": "syntax.string",
            "magenta": "syntax.keyword", "yellow": "syntax.number",
            "tan": "syntax.attribute", "blue": "syntax.url",
            "cyan": "syntax.declaration", "teal": "syntax.project_identifier",
            "purple": "syntax.system_member",
        }.get(name, f"base.{name}")
        header.append(f"#   {src:28s} -> color{idx} ({approx})")
    body = ["", "set vertical-split = false", "", "# Base UI"]
    for role, f, b in [
        ("default", fg, bg), ("cursor", bg, c["yellow"]),
        ("cursor-blur", fg, c["selection"]), ("status", fg, bg),
        ("title-focus", bg, c["yellow"]), ("title-blur", fg, c["selection"]),
        ("search-result", bg, c["yellow"]), ("header", fg, bg),
        ("line-number", c["muted"], bg), ("delimiter", c["muted"], bg),
        ("id", c["yellow"], bg), ("date", c["muted_text"], bg),
        ("author", c["teal"], bg), ("committer", c["muted_text"], bg),
        ("mode", c["muted"], bg), ("overflow", c["muted"], bg),
        ("directory", c["cyan"], bg), ("file", fg, bg),
        ("file-size", c["muted"], bg),
    ]:
        body.append(f"color {role:16s} {f} {b}")
    body += ["", "# Diff view"]
    for role, f in [("diff-add", c["green"]), ("diff-del", c["red"]),
                    ("diff-header", c["yellow"]), ("diff-chunk", c["cyan"])]:
        body.append(f"color {role:16s} {f} {bg}")
    body += ["", "# Log / commit graph"]
    for role, f, extra in [
        ("graph-commit", c["yellow"], ""), ("main-commit", fg, ""),
        ("main-annotated", c["teal"], ""), ("main-head", c["yellow"], " bold"),
        ("main-remote", c["blue"], ""), ("main-tracked", c["blue"], ""),
        ("main-tag", c["magenta"], ""), ("main-local-tag", c["magenta"], ""),
        ("main-ref", c["teal"], ""), ("main-replace", c["red"], ""),
        ("main-stash", c["purple"], ""), ("main-note", c["green"], ""),
        ("main-prefetch", c["blue"], ""), ("main-other", fg, ""),
    ]:
        body.append(f"color {role:16s} {f} {bg}{extra}")
    body += ["", "# Status view"]
    for role, f in [("stat-none", c["muted"]), ("stat-staged", c["green"]),
                    ("stat-unstaged", c["yellow"]), ("stat-untracked", c["red"])]:
        body.append(f"color {role:16s} {f} {bg}")
    body += ["", "# Help view",
             f"color help-group     {c['yellow']} {bg} bold",
             f"color help-action    {fg} {bg}",
             "", "# Tree view",
             f"color tree.directory {c['cyan']} {bg}",
             f"color tree.file      {fg} {bg}"]
    return ROOT / "tig" / "config", "\n".join(header + body) + "\n"


def gen_lazygit(p) -> tuple[Path, str]:
    b, s, st = p["base"], p["syntax"], p["status"]
    out = f"""# Default+ theme for lazygit
#
# {BANNER}
# This is only the `theme:` block. Merge it under `gui:` in your own
# ~/.config/lazygit/config.yml — lazygit cannot import a separate theme file.
#
# lazygit has no upstream Default+ extra, so every slot below is assigned from
# the semantic roles in palette.yaml.
gui:
  theme:
    activeBorderColor:
      - '{s["declaration"]}'
      - bold
    inactiveBorderColor:
      - '{b["muted"]}'
    searchingActiveBorderColor:
      - '{s["number"]}'
      - bold
    optionsTextColor:
      - '{s["declaration"]}'
    selectedLineBgColor:
      - '{b["selection_background"]}'
    inactiveViewSelectedLineBgColor:
      - '{b["subtle"]}'
    cherryPickedCommitFgColor:
      - '{s["number"]}'
    cherryPickedCommitBgColor:
      - '{b["subtle"]}'
    markedBaseCommitFgColor:
      - '{b["background"]}'
    markedBaseCommitBgColor:
      - '{s["number"]}'
    unstagedChangesColor:
      - '{s["string"]}'
    defaultFgColor:
      - '{b["foreground"]}'
  authorColors:
    '*': '{b["muted_text"]}'
"""
    return ROOT / "lazygit" / "theme.yml", out


def gen_herdr(p) -> tuple[Path, str]:
    b, s, e = p["base"], p["syntax"], p["herdr_extended"]
    out = f"""# Default+ theme for herdr
#
# {BANNER}
# This is the `[theme]` block only. Merge it into your own
# ~/.config/herdr/config.toml — herdr cannot import a separate theme file.
#
# `name` picks a built-in base; [theme.custom] then overrides every token
# herdr exposes, so the base choice does not matter. The token names are
# Catppuccin-flavoured (mauve, peach, surface0/1, overlay0/1, subtext0) but
# they are generic slots — this is herdr's CustomThemeColors struct, and these
# 19 are all of it.
#
# NOTE: `herdr config check` validates the TOML but NOT colour values. A typo'd
# hex reports "config: ok" and silently falls back to the base theme's colour
# for that token, so check by eye, not by exit code. `herdr server
# reload-config` applies changes without a restart.

[theme]
name = "terminal"
auto_switch = false

[theme.custom]
accent        = "{s["declaration"]}"
panel_bg      = "{b["panel_background"]}"
sidebar_bg    = "{e["surface_dim"]}"
active_row_bg = "{b["subtle"]}"
selection_bg  = "{b["selection_background"]}"
surface0      = "{e["surface0"]}"
surface1      = "{e["surface1"]}"
surface_dim   = "{e["surface_dim"]}"
overlay0      = "{b["muted"]}"
overlay1      = "{b["muted_text"]}"
text          = "{b["foreground"]}"
subtext0      = "{e["subtext0"]}"
mauve         = "{s["keyword"]}"
green         = "{s["comment"]}"
yellow        = "{s["number"]}"
red           = "{s["string"]}"
blue          = "{s["url"]}"
teal          = "{s["project_identifier"]}"
peach         = "{e["peach"]}"
"""
    return ROOT / "herdr" / "theme.toml", out


def gen_zsh(p) -> tuple[Path, str]:
    b, s, st = p["base"], p["syntax"], p["status"]

    def dec(h: str) -> str:
        return ";".join(str(c) for c in h2r(h))

    bg = dec(b["background"])
    rules = [
        ("di", f"1;38;2;{dec(s['declaration'])}"),          # directory
        ("ln", f"38;2;{dec(s['number'])}"),                  # symlink
        ("so", f"38;2;{dec(s['keyword'])}"),                 # socket
        ("pi", f"38;2;{dec(s['keyword'])}"),                 # pipe
        ("ex", f"1;38;2;{dec(s['string'])}"),                # executable
        ("bd", f"38;2;{dec(s['declaration'])};48;2;{bg}"),   # block device
        ("cd", f"38;2;{dec(s['declaration'])};48;2;{bg}"),   # char device
        ("su", f"38;2;{bg};48;2;{dec(s['string'])}"),        # setuid
        ("sg", f"38;2;{bg};48;2;{dec(s['number'])}"),        # setgid
        ("tw", f"38;2;{bg};48;2;{dec(s['project_identifier'])}"),  # sticky, writable
        ("ow", f"38;2;{bg};48;2;{dec(s['number'])}"),        # writable, not sticky
    ]
    ls_colors = ":".join(f"{k}={v}" for k, v in rules)
    out = f"""# Default+ palette for zsh
#
# {BANNER}
#
# Source this file from your ~/.zshrc:
#   source ~/Developer/default-plus/zsh/default-plus.zsh

# `ls` colours. LS_COLORS drives GNU ls, eza and zsh completion; LSCOLORS is the
# 8-slot BSD fallback that only /bin/ls reads. They are kept in agreement — the
# two used to disagree on the directory colour.
export CLICOLOR=YES
export LSCOLORS="GxDxFxfxBxEgEdAbAgAcAd"
export LS_COLORS="{ls_colors}"

# Completion list colours (reuses LS_COLORS above)
zstyle ':completion:*' list-colors "${{(s.:.)LS_COLORS}}"
zstyle ':completion:*:descriptions' format '%F{{{s["project_identifier"]}}}-- %d --%f'

# VCS / prompt colours
zstyle ':vcs_info:git:*' formats '%F{{{s["number"]}}}%b%f '

setopt PROMPT_SUBST
PROMPT=$'%F{{{s["project_identifier"]}}}%~%f ${{vcs_info_msg_0_}}\\n%F{{{b["muted_text"]}}}$%f '
"""
    return ROOT / "zsh" / "default-plus.zsh", out


def gen_slack(p) -> tuple[Path, str]:
    b, s = p["base"], p["syntax"]
    modern = f"{b['background']},{b['selection_background']},{s['comment']},{s['string']}"
    legacy = ",".join([
        b["background"], b["subtle"], b["selection_background"], b["foreground"],
        b["subtle"], b["foreground"], s["comment"], s["string"],
    ])
    out = f"""# Default+ theme for Slack
#
# {BANNER}
# Paste either string into any Slack message box and press Enter — Slack shows
# an "Apply Slack theme" button — or use Preferences → Appearance → Custom theme.

# ── Modern format (post-December 2023 redesign) ──────────────────────
# System Navigation, Selected Items, Presence, Notifications.
# Slack snaps these to its nearest built-in palette entry rather than applying
# the hex values verbatim, so results vary slightly.

{modern}

# ── Legacy format (8 values, exact hex control) ──────────────────────
# Preferences → Appearance → Custom theme → "Paste legacy theme".
#
#   1 Column BG        base.background            sidebar background
#   2 Menu BG Hover    base.subtle                workspace header hover
#   3 Active Item      base.selection_background  selected channel row
#   4 Active Item Text base.foreground            text on selected row
#   5 Hover Item       base.subtle                non-active row hover
#   6 Text Color       base.foreground            sidebar text and icons
#   7 Active Presence  syntax.comment             online presence dot
#   8 Mention Badge    syntax.string              unread mention badge

{legacy}
"""
    return ROOT / "slack" / "theme.txt", out


GENERATORS = [
    gen_ghostty, gen_iterm, gen_terminal, gen_tig,
    gen_lazygit, gen_herdr, gen_zsh, gen_slack,
]


def generate(p, dry_run: bool = False) -> list[str]:
    changed = []
    for fn in GENERATORS:
        path, content = fn(p)
        data = content if isinstance(content, bytes) else content.encode()
        old = path.read_bytes() if path.exists() else None
        if old == data:
            continue
        changed.append(str(path.relative_to(ROOT)))
        if not dry_run:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
    return changed


# ─── --validate ────────────────────────────────────────────────────────────

# Files whose colours are not expected to be palette members. README.md is NOT
# exempt: it documents the palette, so a stale swatch there is a real defect.
VALIDATE_SKIP = {"palette.yaml", "LICENSE"}


def xterm256() -> set[str]:
    """The xterm-256 palette, as exact sRGB hex."""
    levels = [0, 95, 135, 175, 215, 255]
    out = set()
    for i in range(216):
        out.add(r2h((levels[i // 36], levels[(i // 6) % 6], levels[i % 6])).upper())
    for i in range(24):
        v = 8 + i * 10
        out.add(r2h((v, v, v)).upper())
    return out


# tig 2.6.1 has no truecolor, so tig/config documents the 256-colour index it
# approximates each palette entry with. Those approximations are legitimately
# not palette members. The allowance is scoped to that one file — everywhere
# else, an xterm-256 colour is a mistake.
VALIDATE_EXTRA_ALLOWED = {"tig/config": xterm256}


# Pure black is not a palette hue — with an alpha suffix it means "transparent"
# or "drop shadow", which several UI schemas require and no theme colour can
# stand in for. Allowed everywhere.
UNIVERSAL_ALLOWED = {"#000000"}


def validate(p, extra_roots: list[Path] | None = None) -> list[str]:
    known = {v.upper() for section in p.values() for v in section.values()
             if v.startswith("#")} | UNIVERSAL_ALLOWED
    # Apple Terminal stores colours as float triples inside binary blobs, and the
    # Xcode theme as float triples too; both are covered by --check instead.
    problems = []
    roots = [ROOT] + (extra_roots or [])
    for root in roots:
        for path in sorted(root.rglob("*")):
            if not path.is_file() or ".git" in path.parts:
                continue
            if path.name in VALIDATE_SKIP or path.suffix in (".png", ".terminal"):
                continue
            if path.name.endswith(".xccolortheme"):
                continue
            # bin/ holds the generator itself, not a port.
            if "bin" in path.relative_to(root).parts:
                continue
            key = path.relative_to(root).as_posix()
            allowed = known | VALIDATE_EXTRA_ALLOWED.get(key, set)()
            try:
                text = path.read_text()
            except (UnicodeDecodeError, OSError):
                continue
            for lineno, line in enumerate(text.splitlines(), 1):
                for m in HEX_RE.finditer(line):
                    rgb = "#" + m.group(1).upper()
                    if rgb not in allowed:
                        rel = path.relative_to(root.parent)
                        problems.append(f"{rel}:{lineno}: {m.group(0)} not in palette")
    return problems


# ─── cli ───────────────────────────────────────────────────────────────────


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--generate", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--dry-run", action="store_true",
                    help="with --generate, report what would change and write nothing")
    ap.add_argument("--also", type=Path, nargs="*", default=[],
                    help="extra repos to include in --validate (the satellite ports)")
    args = ap.parse_args()
    if not (args.check or args.generate or args.validate):
        args.check = args.generate = args.validate = True

    p = load_palette()
    failed = False

    if args.check:
        errors = check(p)
        if errors:
            failed = True
            print("check: FAILED")
            for e in errors:
                print(f"  {e}")
        else:
            print(f"check: ok ({len(XCODE_BINDINGS)} bound to Xcode, "
                  f"{len(DERIVED_RULES) + len(SHIMMER_RULES)} derived, 14 contrast)")

    if args.generate:
        changed = generate(p, dry_run=args.dry_run)
        verb = "would write" if args.dry_run else "wrote"
        print(f"generate: {verb} {len(changed)} file(s)"
              + ("".join(f"\n  {c}" for c in changed) if changed else " (all current)"))

    if args.validate:
        problems = validate(p, [Path(a).resolve() for a in args.also])
        if problems:
            failed = True
            print(f"validate: FAILED ({len(problems)} off-palette)")
            for pr in problems:
                print(f"  {pr}")
        else:
            print("validate: ok (no off-palette hexes)")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
