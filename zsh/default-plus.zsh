# Default+ palette for zsh
#
# bg #1E1E1E, fg #FFFFFF, muted #4D4D4D, blue #35B0D8, yellow #FFE76D,
# red #FC4651, magenta #F2248C, cyan #56D0B3, green #2EA85B
#
# Source this file from your ~/.zshrc, e.g.:
#   source ~/Developer/Default+/zsh/default-plus.zsh

# `ls` colors (macOS CLICOLOR + GNU-style LS_COLORS for tools that read it)
export CLICOLOR=YES
export LSCOLORS="CxDxGxFxBxEgEdAbAgAcAd"
export LS_COLORS="di=1;38;2;53;176;216:ln=38;2;255;231;109:so=38;2;242;36;140:pi=38;2;242;36;140:ex=1;38;2;252;70;81:bd=38;2;53;176;216;48;2;30;30;30:cd=38;2;53;176;216;48;2;30;30;30:su=38;2;30;30;30;48;2;252;70;81:sg=38;2;30;30;30;48;2;255;231;109:tw=38;2;30;30;30;48;2;86;208;179:ow=38;2;30;30;30;48;2;255;231;109"

# Completion list colors (uses LS_COLORS above)
zstyle ':completion:*' list-colors "${(s.:.)LS_COLORS}"
zstyle ':completion:*:descriptions' format '%F{#56D0B3}-- %d --%f'

# VCS / prompt colors
zstyle ':vcs_info:git:*' formats '%F{#FFE76D}%b%f '

setopt PROMPT_SUBST
PROMPT=$'%F{#56D0B3}%~%f ${vcs_info_msg_0_}\n%F{#8E8E8E}$%f '
