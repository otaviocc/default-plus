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

| App | Path | Install |
|---|---|---|
| Xcode | [`xcode/Default+.xccolortheme`](./xcode/Default+.xccolortheme) | Copy to `~/Library/Developer/Xcode/UserData/FontAndColorThemes/`, then select **Default+** in Xcode → Settings → Themes. |
| Ghostty | [`ghostty/Default+`](./ghostty/Default+) | Copy to `~/.config/ghostty/themes/Default+`, then set `theme = "Default+"` in `~/.config/ghostty/config`. |
| tig | [`tig/config`](./tig/config) | Copy to `~/.config/tig/config` (or merge into your existing one). |
| lazygit | [`lazygit/theme.yml`](./lazygit/theme.yml) | Merge the `theme:` block into `~/.config/lazygit/config.yml` under `gui:`. |
| opencode | [`opencode/default-plus.json`](./opencode/default-plus.json) | Copy to `~/.config/opencode/themes/default-plus.json`, then set `"theme": "default-plus"` in `~/.config/opencode/tui.json`. |
| Neovim | [`nvim/colors/default-plus.lua`](./nvim/colors/default-plus.lua) | Copy to `~/.config/nvim/colors/default-plus.lua`, then `vim.cmd.colorscheme("default-plus")`. |
| zsh | [`zsh/default-plus.zsh`](./zsh/default-plus.zsh) | `source ~/Developer/Default+/zsh/default-plus.zsh` from your `~/.zshrc` (or copy the file and source your copy). Sets `LS_COLORS`, prompt, and completion colors. |
| herdr | [`herdr/theme.toml`](./herdr/theme.toml) | Merge the `[theme]` / `[theme.custom]` blocks into `~/.config/herdr/config.toml`. |
| hunk | [`hunk/theme.toml`](./hunk/theme.toml) | Merge the `theme = "custom"` line and `[custom_theme]` / `[custom_theme.syntax_scopes]` blocks into `~/.config/hunk/config.toml`. |

## Repo layout

```
Default+/
├── palette.yaml     Canonical source of truth for all colors
├── xcode/           Original Xcode Font & Color Theme
├── ghostty/         Ghostty terminal theme
├── tig/             tig config with Default+ colors (256-color mapped)
├── lazygit/         lazygit theme snippet
├── opencode/         opencode TUI theme
├── nvim/            Neovim colorscheme
├── zsh/             Sourceable zsh color/prompt snippet
├── herdr/           herdr theme snippet
└── hunk/            hunk theme snippet
```

## License

MIT, see [LICENSE](./LICENSE).
