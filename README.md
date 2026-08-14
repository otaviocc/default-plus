# Default+

Default+ is a dark colorscheme originally created as an Xcode Font & Color
Theme, ported to the terminal and various command-line tools.

The canonical palette lives in [`palette.yaml`](./palette.yaml). Every file
in this repo is derived from it — if you want to tweak a color, change it
there first and propagate the change to the relevant port(s).

## Palette

| Role      | Hex       | Swatch |
|-----------|-----------|--------|
| Background        | `#1E1E1E` | ![#1E1E1E](https://placehold.co/15x15/1E1E1E/1E1E1E.png) |
| Foreground        | `#FFFFFF` | ![#FFFFFF](https://placehold.co/15x15/FFFFFF/FFFFFF.png) |
| Selection          | `#54554A` | ![#54554A](https://placehold.co/15x15/54554A/54554A.png) |
| Muted              | `#4D4D4D` | ![#4D4D4D](https://placehold.co/15x15/4D4D4D/4D4D4D.png) |
| Muted text         | `#8E8E8E` | ![#8E8E8E](https://placehold.co/15x15/8E8E8E/8E8E8E.png) |
| Red                | `#FC4651` | ![#FC4651](https://placehold.co/15x15/FC4651/FC4651.png) |
| Green              | `#2EA85B` | ![#2EA85B](https://placehold.co/15x15/2EA85B/2EA85B.png) |
| Yellow             | `#FFE76D` | ![#FFE76D](https://placehold.co/15x15/FFE76D/FFE76D.png) |
| Blue               | `#35B0D8` | ![#35B0D8](https://placehold.co/15x15/35B0D8/35B0D8.png) |
| Magenta            | `#F2248C` | ![#F2248C](https://placehold.co/15x15/F2248C/F2248C.png) |
| Cyan               | `#56D0B3` | ![#56D0B3](https://placehold.co/15x15/56D0B3/56D0B3.png) |

The Xcode source theme also defines a handful of extended accents used only
for finer-grained syntax highlighting there (attribute, macro/preprocessor,
url, system types/functions). See `palette.yaml` for those.

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
| zsh | `source` [`zsh/default-plus.zsh`](./zsh/default-plus.zsh) from your `~/.zshrc`. Sets `LS_COLORS`, prompt, and completion colors. |
| herdr | Merge the `[theme]` / `[theme.custom]` blocks from [`herdr/theme.toml`](./herdr/theme.toml) into `~/.config/herdr/config.toml`. |
| hunk | Merge the `[custom_theme]` blocks from [`hunk/theme.toml`](./hunk/theme.toml) into `~/.config/hunk/config.toml`. |
| Claude Code | Copy [`claude-code/default-plus.json`](./claude-code/default-plus.json) to `~/.claude/themes/default-plus.json`, then pick **Default+** in `/theme`. Requires Claude Code v2.1.118+. |
| Slack | See [`slack/theme.txt`](./slack/theme.txt) for the paste values. |
| iTerm2 | Double-click [`iterm/Default+.itermcolors`](./iterm/Default+.itermcolors) (or drag it into Preferences → Profiles → Colors → Color Presets → Import), then select **Default+**. |
| Apple Terminal | Double-click [`terminal/Default+.terminal`](./terminal/Default+.terminal) to add it, then select **Default+** in Terminal → Settings → Profiles. |

## Repo layout

```
Default+/
├── palette.yaml     Canonical source of truth for all colors
├── xcode/           Original Xcode Font & Color Theme
├── ghostty/         Ghostty terminal theme
├── tig/             tig config with Default+ colors (256-color mapped)
├── lazygit/         lazygit theme snippet
├── opencode/        opencode TUI theme
├── zsh/             Sourceable zsh color/prompt snippet
├── herdr/           herdr theme snippet
├── hunk/            hunk theme snippet
├── claude-code/     Claude Code custom theme
├── slack/           Slack sidebar theme
├── iterm/           iTerm2 color preset
└── terminal/        Apple Terminal profile
```

Ports with their own repositories:

- [default-plus-nvim](https://github.com/otaviocc/default-plus-nvim) — Neovim colorscheme
- [default-plus-obsidian](https://github.com/otaviocc/default-plus-obsidian) — Obsidian theme
- [default-plus-vscode](https://github.com/otaviocc/default-plus-vscode) — VS Code color theme extension

## License

MIT, see [LICENSE](./LICENSE).
