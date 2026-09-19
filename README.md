# Default+

Default+ is a dark colorscheme originally created as an Xcode Font & Color
Theme, ported to the terminal, editors and various command-line tools.

The canonical palette lives in [`palette.yaml`](./palette.yaml), and its own
source of truth is [`xcode/Default+.xccolortheme`](./xcode/Default+.xccolortheme)
— the Xcode 26 theme every other port is derived from. To change a colour,
change it in Xcode first, then run `bin/build.py`.

## Syntax roles

Default+ does **not** follow the usual terminal convention, and that is the
point of it:

- **comments are green**, not grey
- **strings are red**, not green
- types, functions and variables you declare share one **teal**; SDK members
  are **purple** and SDK types **light purple**

The project-vs-system split is the distinction Xcode draws, and ports reproduce
it via treesitter's `.builtin` captures and the LSP `defaultLibrary` modifier.
A port that "corrects" green comments back to grey stops looking like Default+.

## Palette

| Role | Hex | Swatch |
|---|---|---|
| Background | `#171717` | ![#171717](https://placehold.co/15x15/171717/171717.png) |
| Foreground | `#FFFFFF` | ![#FFFFFF](https://placehold.co/15x15/FFFFFF/FFFFFF.png) |
| Selection | `#515B70` | ![#515B70](https://placehold.co/15x15/515B70/515B70.png) |
| Muted | `#4C4C4C` | ![#4C4C4C](https://placehold.co/15x15/4C4C4C/4C4C4C.png) |
| Muted text | `#8E8E8E` | ![#8E8E8E](https://placehold.co/15x15/8E8E8E/8E8E8E.png) |
| Comment | `#2EA85B` | ![#2EA85B](https://placehold.co/15x15/2EA85B/2EA85B.png) |
| String | `#FC4651` | ![#FC4651](https://placehold.co/15x15/FC4651/FC4651.png) |
| Keyword | `#F2248C` | ![#F2248C](https://placehold.co/15x15/F2248C/F2248C.png) |
| Number | `#FFE76D` | ![#FFE76D](https://placehold.co/15x15/FFE76D/FFE76D.png) |
| Macro | `#FD8F3F` | ![#FD8F3F](https://placehold.co/15x15/FD8F3F/FD8F3F.png) |
| Attribute | `#E09D65` | ![#E09D65](https://placehold.co/15x15/E09D65/E09D65.png) |
| URL | `#4FA5FF` | ![#4FA5FF](https://placehold.co/15x15/4FA5FF/4FA5FF.png) |
| Declaration | `#35B0D8` | ![#35B0D8](https://placehold.co/15x15/35B0D8/35B0D8.png) |
| Declaration (type) | `#66DAFF` | ![#66DAFF](https://placehold.co/15x15/66DAFF/66DAFF.png) |
| Project identifier | `#56D0B3` | ![#56D0B3](https://placehold.co/15x15/56D0B3/56D0B3.png) |
| System member | `#AB64FF` | ![#AB64FF](https://placehold.co/15x15/AB64FF/AB64FF.png) |
| System type | `#D0A8FF` | ![#D0A8FF](https://placehold.co/15x15/D0A8FF/D0A8FF.png) |

### ANSI

Xcode has no ANSI concept, so the 16-colour ramp is designed rather than
transcribed — but every entry is a real Default+ colour. Normal and bright are
genuinely distinct, so terminals should also set `bold-is-bright = false` (or
the equivalent) to keep bold from changing hue as well as weight.

| # | Normal | | # | Bright | |
|---|---|---|---|---|---|
| 0 | `#4C4C4C` | ![#4C4C4C](https://placehold.co/15x15/4C4C4C/4C4C4C.png) | 8 | `#515B70` | ![#515B70](https://placehold.co/15x15/515B70/515B70.png) |
| 1 | `#FC4651` | ![#FC4651](https://placehold.co/15x15/FC4651/FC4651.png) | 9 | `#F74A4A` | ![#F74A4A](https://placehold.co/15x15/F74A4A/F74A4A.png) |
| 2 | `#2EA85B` | ![#2EA85B](https://placehold.co/15x15/2EA85B/2EA85B.png) | 10 | `#41B645` | ![#41B645](https://placehold.co/15x15/41B645/41B645.png) |
| 3 | `#E09D65` | ![#E09D65](https://placehold.co/15x15/E09D65/E09D65.png) | 11 | `#FFE76D` | ![#FFE76D](https://placehold.co/15x15/FFE76D/FFE76D.png) |
| 4 | `#4FA5FF` | ![#4FA5FF](https://placehold.co/15x15/4FA5FF/4FA5FF.png) | 12 | `#66DAFF` | ![#66DAFF](https://placehold.co/15x15/66DAFF/66DAFF.png) |
| 5 | `#F2248C` | ![#F2248C](https://placehold.co/15x15/F2248C/F2248C.png) | 13 | `#AB64FF` | ![#AB64FF](https://placehold.co/15x15/AB64FF/AB64FF.png) |
| 6 | `#35B0D8` | ![#35B0D8](https://placehold.co/15x15/35B0D8/35B0D8.png) | 14 | `#56D0B3` | ![#56D0B3](https://placehold.co/15x15/56D0B3/56D0B3.png) |
| 7 | `#8E8E8E` | ![#8E8E8E](https://placehold.co/15x15/8E8E8E/8E8E8E.png) | 15 | `#FFFFFF` | ![#FFFFFF](https://placehold.co/15x15/FFFFFF/FFFFFF.png) |

Every slot except 0 and 8 — which are background tones and never carry text —
clears WCAG AA (4.5:1) against the background. `bin/build.py --check` enforces it.

## Apps

| App | Install |
|---|---|
| Xcode | Copy [`xcode/Default+.xccolortheme`](./xcode/Default+.xccolortheme) to `~/Library/Developer/Xcode/UserData/FontAndColorThemes/`, then select **Default+** in Xcode → Settings → Themes. |
| Ghostty | Copy [`ghostty/Default+`](./ghostty/Default+) to `~/.config/ghostty/themes/Default+`, then set `theme = "Default+"` in `~/.config/ghostty/config`. |
| Neovim | See [default-plus-nvim](https://github.com/otaviocc/default-plus-nvim) — install via your plugin manager. |
| Obsidian | See [default-plus-obsidian](https://github.com/otaviocc/default-plus-obsidian) — available in the Obsidian community themes list. |
| VS Code | See [default-plus-vscode](https://github.com/otaviocc/default-plus-vscode) — download the `.vsix` from Releases. |
| tig | Copy [`tig/config`](./tig/config) to `~/.config/tig/config` (or merge into your existing one). |
| lazygit | Merge the `theme:` block from [`lazygit/theme.yml`](./lazygit/theme.yml) into `~/.config/lazygit/config.yml` under `gui:`. |
| opencode | Copy [`opencode/default-plus.json`](./opencode/default-plus.json) to `~/.config/opencode/themes/default-plus.json`, then set `"theme": "default-plus"` in `~/.config/opencode/tui.json`. |
| zsh | `source` [`zsh/default-plus.zsh`](./zsh/default-plus.zsh) from your `~/.zshrc`. Sets `LS_COLORS`, `LSCOLORS`, prompt and completion colours. |
| herdr | Merge the `[theme]` / `[theme.custom]` blocks from [`herdr/theme.toml`](./herdr/theme.toml) into `~/.config/herdr/config.toml`. |
| hunk | Merge the `[custom_theme]` blocks from [`hunk/theme.toml`](./hunk/theme.toml) into `~/.config/hunk/config.toml`. |
| vigia | Copy [`vigia/theme`](./vigia/theme) to `~/.config/vigia/theme`, or point `VIGIA_THEME` at it. |
| Claude Code | Copy [`claude-code/default-plus.json`](./claude-code/default-plus.json) to `~/.claude/themes/default-plus.json`, then pick **Default+** in `/theme`. Requires Claude Code v2.1.118+. |
| Slack | See [`slack/theme.txt`](./slack/theme.txt) for the paste values. |
| Kagi | Paste [`kagi/default-plus.css`](./kagi/default-plus.css) into Settings → Appearance → Custom CSS, with the theme set to a dark one. |
| iTerm2 | Double-click [`iterm/Default+.itermcolors`](./iterm/Default+.itermcolors) (or drag it into Preferences → Profiles → Colors → Color Presets → Import), then select **Default+**. |
| Apple Terminal | Double-click [`terminal/Default+.terminal`](./terminal/Default+.terminal) to add it, then select **Default+** in Terminal → Settings → Profiles. |

## Making changes

`bin/build.py` (Python 3 stdlib only) keeps the ports honest:

```sh
bin/build.py              # all three passes
bin/build.py --check      # palette.yaml still matches the Xcode theme
bin/build.py --generate   # rewrite the mechanically-derivable ports
bin/build.py --validate   # no port uses a colour outside the palette
```

`--check` re-reads `xcode/Default+.xccolortheme`, recomputes every value under
`derived` from its stated rule, and contrast-checks the ANSI ramp. `--generate`
owns ghostty, iTerm2, Apple Terminal, tig, lazygit, herdr, zsh and Slack; those
files carry a "do not edit by hand" banner. The rest are hand-maintained, and
`--validate` is what catches drift in them — including in the satellite repos:

```sh
bin/build.py --validate --also ../default-plus-nvim ../default-plus-obsidian ../default-plus-vscode
```

## Repo layout

```
default-plus/
├── palette.yaml     Canonical palette, derived from the Xcode theme
├── bin/build.py     Generator, checker and validator
├── xcode/           Original Xcode Font & Color Theme — the source of truth
├── ghostty/         Ghostty terminal theme                    (generated)
├── iterm/           iTerm2 color preset                       (generated)
├── terminal/        Apple Terminal profile                    (generated)
├── tig/             tig config, mapped to 256 colours         (generated)
├── lazygit/         lazygit theme snippet                     (generated)
├── herdr/           herdr theme snippet                       (generated)
├── zsh/             Sourceable zsh colour/prompt snippet      (generated)
├── slack/           Slack sidebar theme                       (generated)
├── opencode/        opencode TUI theme
├── hunk/            hunk theme snippet
├── vigia/           vigia theme
├── kagi/            Kagi custom CSS
└── claude-code/     Claude Code custom theme
```

Ports with their own repositories:

- [default-plus-nvim](https://github.com/otaviocc/default-plus-nvim) — Neovim colorscheme
- [default-plus-obsidian](https://github.com/otaviocc/default-plus-obsidian) — Obsidian theme
- [default-plus-vscode](https://github.com/otaviocc/default-plus-vscode) — VS Code color theme extension

## License

MIT, see [LICENSE](./LICENSE).
