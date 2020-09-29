hi clear
set background={{{ _color_theme }}}
if exists("syntax_on")
    syntax reset
end
let g:colors_name = "uuu"

if !(has('termguicolors') && &termguicolors) && !has('gui_running')
        \ && &t_Co != 256
    finish
endif

" The color definitions. The first item is the true color value and the second
" is the 256 color value.
"
" base00 - Default Background
" base01 - Lighter Background (Used for status bars)
" base02 - Selection Background
" base03 - Comments, Invisibles, Line Highlighting
" base04 - Dark Foreground (Used for status bars)
" base05 - Default Foreground, Caret, Delimiters, Operators
" base06 - Light Foreground (Not often used)
" base07 - Light Background (Not often used)
" base08 - Variables, XML Tags, Markup Link Text, Markup Lists, Diff Deleted
" base09 - Integers, Boolean, Constants, XML Attributes, Markup Link Url
" base0A - Classes, Markup Bold, Search Text Background
" base0B - Strings, Inherited Class, Markup Code, Diff Inserted
" base0C - Support, Regular Expressions, Escape Characters, Markup Quotes
" base0D - Functions, Methods, Attribute IDs, Headings
" base0E - Keywords, Storage, Selector, Markup Italic, Diff Changed
" base0F - Deprecated, Opening/Closing Embedded Language Tags
let s:base00 = ['#{{{ _color_base00_hex }}}']
let s:base01 = ['#{{{ _color_base01_hex }}}']
let s:base02 = ['#{{{ _color_base02_hex }}}']
let s:base03 = ['#{{{ _color_base03_hex }}}']
let s:base04 = ['#{{{ _color_base04_hex }}}']
let s:base05 = ['#{{{ _color_base05_hex }}}']
let s:base06 = ['#{{{ _color_base06_hex }}}']
let s:base07 = ['#{{{ _color_base07_hex }}}']
let s:base08 = ['#{{{ _color_base08_hex }}}']
let s:base09 = ['#{{{ _color_base09_hex }}}']
let s:base0A = ['#{{{ _color_base0A_hex }}}']
let s:base0B = ['#{{{ _color_base0B_hex }}}']
let s:base0C = ['#{{{ _color_base0C_hex }}}']
let s:base0D = ['#{{{ _color_base0D_hex }}}']
let s:base0E = ['#{{{ _color_base0E_hex }}}']
let s:base0F = ['#{{{ _color_base0F_hex }}}']
let s:none   = ['none', 'none']

" The available attributes that can be used in color definitions.
let s:attrs = {
    \ 'bold':      'bold',
    \ 'inverse':   'inverse',
    \ 'underline': 'underline',
    \}

" Declares a highlight groups with the specified options.
"
" * [group] is the name of the highlight group to define.
" * [hi] is a dictionary that contains the keys `fg`, `bg`, and `attrs` to use
"   in the definition. All of these keys are optional and will be filled with a
"   default that is simply the foreground color.
function! s:hi(group, hi)
    let l:fg = has_key(a:hi, 'fg') ? a:hi.fg : s:none
    let l:bg = has_key(a:hi, 'bg') ? a:hi.bg : s:none
    let l:attrs = join(has_key(a:hi, 'attrs') ? a:hi.attrs : ['none'], ',')
    execute join([
        \ 'highlight',
        \ a:group,
        \ 'guibg='   . l:bg[0],
        \ 'guifg='   . l:fg[0],
        \ 'gui='     . l:attrs,
        \], ' ')
endfunction

" Vim Editor
call s:hi('Normal',           {'fg': s:base05, 'bg': s:base00})
call s:hi('Bold',             {'attrs': [s:attrs.bold]})
call s:hi('ColorColumn',      {'bg': s:base01})
call s:hi('Conceal',          {'fg': s:base0D, 'bg': s:base00})
call s:hi('Cursor',           {'fg': s:base00, 'bg': s:base05})
call s:hi('CursorColumn',     {'bg': s:base02})
call s:hi('CursorLine',       {'bg': s:base02})
call s:hi('CursorLineNr',     {'fg': s:base04})
call s:hi('Debug',            {'fg': s:base08})
call s:hi('Directory',        {'fg': s:base0D})
call s:hi('Error',            {'fg': s:base00, 'bg': s:base08})
call s:hi('ErrorMsg',         {'fg': s:base08, 'bg': s:base00})
call s:hi('Exception',        {'fg': s:base08})
call s:hi('FoldColumn',       {'fg': s:base0C, 'bg': s:base01})
call s:hi('Folded',           {'fg': s:base03, 'bg': s:base01})
call s:hi('IncSearch',        {'fg': s:base01, 'bg': s:base09})
call s:hi('Italic',           {})
call s:hi('LineNr',           {'fg': s:base03})
call s:hi('Macro',            {'fg': s:base08})
call s:hi('MatchParen',       {'bg': s:base03})
call s:hi('ModeMsg',          {'fg': s:base0B})
call s:hi('MoreMsg',          {'fg': s:base0B})
call s:hi('NonText',          {'fg': s:base03})
call s:hi('PMenu',            {'fg': s:base05, 'bg': s:base01})
call s:hi('PMenuSel',         {'fg': s:base01, 'bg': s:base05})
call s:hi('Question',         {'fg': s:base0D})
call s:hi('QuickFixLine',     {'bg': s:base01})
call s:hi('Search',           {'fg': s:base01, 'bg': s:base0A})
call s:hi('SignColumn',       {'fg': s:base03, 'bg': s:base01})
call s:hi('SpecialKey',       {'fg': s:base03})
call s:hi('SpellBad',         {'fg': s:base08, 'attrs': [s:attrs.underline]})
call s:hi('SpellCap',         {'fg': s:base0C, 'attrs': [s:attrs.underline]})
call s:hi('SpellLocal',       {'fg': s:base09, 'attrs': [s:attrs.underline]})
call s:hi('SpellRare',        {'fg': s:base0C, 'attrs': [s:attrs.underline]})
call s:hi('StatusLine',       {'fg': s:base04, 'bg': s:base01})
call s:hi('StatusLineNC',     {'fg': s:base03, 'bg': s:base01})
call s:hi('StatusLineTerm',   {'fg': s:base05, 'bg': s:base01})
call s:hi('StatusLineTermNC', {'fg': s:base04, 'bg': s:base01})
call s:hi('Substitute',       {'fg': s:base01, 'bg': s:base0A})
call s:hi('TabLine',          {'fg': s:base03, 'bg': s:base01})
call s:hi('TabLineFill',      {'fg': s:base03, 'bg': s:base01})
call s:hi('TabLineSel',       {'fg': s:base0B, 'bg': s:base01})
call s:hi('Title',            {'fg': s:base0D})
call s:hi('TooLong',          {'fg': s:base08})
call s:hi('Underlined',       {'attrs': [s:attrs.underline]})
call s:hi('VertSplit',        {'fg': s:base01, 'bg': s:base01})
call s:hi('Visual',           {'bg': s:base02})
call s:hi('VisualNOS',        {'fg': s:base08})
call s:hi('WarningMsg',       {'fg': s:base08})
call s:hi('WildMenu',         {'fg': s:base08, 'bg': s:base0A})

" Syntax
call s:hi('Boolean',        {'fg': s:base09})
call s:hi('Character',      {'fg': s:base08})
call s:hi('Comment',        {'fg': s:base03})
call s:hi('Conditional',    {'fg': s:base0E})
call s:hi('Constant',       {'fg': s:base09})
call s:hi('Define',         {'fg': s:base0E})
call s:hi('Delimiter',      {'fg': s:base0F})
call s:hi('Float',          {'fg': s:base09})
call s:hi('Function',       {'fg': s:base0D})
call s:hi('Identifier',     {'fg': s:base08})
call s:hi('Include',        {'fg': s:base0D})
call s:hi('Keyword',        {'fg': s:base0E})
call s:hi('Label',          {'fg': s:base0A})
call s:hi('Number',         {'fg': s:base09})
call s:hi('Operator',       {'fg': s:base05})
call s:hi('PreCondit',      {'fg': s:base0E})
call s:hi('PreProc',        {'fg': s:base0A})
call s:hi('Repeat',         {'fg': s:base0A})
call s:hi('Special',        {'fg': s:base0C})
call s:hi('SpecialChar',    {'fg': s:base0F})
call s:hi('SpecialComment', {'fg': s:base0C})
call s:hi('Statement',      {'fg': s:base08})
call s:hi('StorageClass',   {'fg': s:base0A})
call s:hi('String',         {'fg': s:base0B})
call s:hi('Structure',      {'fg': s:base0E})
call s:hi('Tag',            {'fg': s:base0A})
call s:hi('Todo',           {'fg': s:base0A, 'bg': s:base01})
call s:hi('Type',           {'fg': s:base0A})
call s:hi('Typedef',        {'fg': s:base0A})
hi link vimUserFunc Function

" User
call s:hi('User1', {'fg': s:base00, 'bg': s:base08})
call s:hi('User2', {'fg': s:base00, 'bg': s:base09})
call s:hi('User3', {'fg': s:base00, 'bg': s:base0A})
call s:hi('User4', {'fg': s:base00, 'bg': s:base0B})
call s:hi('User5', {'fg': s:base00, 'bg': s:base0C})
call s:hi('User6', {'fg': s:base00, 'bg': s:base0D})
call s:hi('User7', {'fg': s:base00, 'bg': s:base0E})
call s:hi('User8', {'fg': s:base00, 'bg': s:base0F})

" C
call s:hi('cOperator',  {'fg': s:base0C})
call s:hi('cPreCondit', {'fg': s:base0E})

" C#
call s:hi('csAttribute',            {'fg': s:base0A})
call s:hi('csClass',                {'fg': s:base0A})
call s:hi('csContextualStatement',  {'fg': s:base0E})
call s:hi('csModifier',             {'fg': s:base0E})
call s:hi('csNewDecleration',       {'fg': s:base08})
call s:hi('csType',                 {'fg': s:base08})
call s:hi('csUnspecifiedStatement', {'fg': s:base0D})

" CSS
call s:hi('cssBraces',    {'fg': s:base05})
call s:hi('cssClassName', {'fg': s:base0E})
call s:hi('cssColor',     {'fg': s:base0C})

" Diff
call s:hi('DiffAdd',          {'fg': s:base0B, 'bg': s:base01})
call s:hi('DiffAdded',        {'fg': s:base0B, 'bg': s:base00})
call s:hi('DiffChange',       {'fg': s:base0A, 'bg': s:base01})
call s:hi('DiffChangeDelete', {'fg': s:base0A, 'bg': s:base01})
call s:hi('DiffDelete',       {'fg': s:base08, 'bg': s:base01})
call s:hi('DiffFile',         {'fg': s:base08, 'bg': s:base00})
call s:hi('DiffLine',         {'fg': s:base0D, 'bg': s:base00})
call s:hi('DiffNewFile',      {'fg': s:base0B, 'bg': s:base00})
call s:hi('DiffRemoved',      {'fg': s:base08, 'bg': s:base00})
call s:hi('DiffText',         {'fg': s:base0D, 'bg': s:base01})

" Git
call s:hi('gitcommitBranch',        {'fg': s:base09, 'attrs': [s:attrs.bold]})
call s:hi('gitcommitComment',       {'fg': s:base03})
call s:hi('gitcommitDiscarded',     {'fg': s:base03})
call s:hi('gitcommitDiscardedFile', {'fg': s:base08, 'attrs': [s:attrs.bold]})
call s:hi('gitcommitDiscardedType', {'fg': s:base0D})
call s:hi('gitcommitHeader',        {'fg': s:base0E})
call s:hi('gitcommitOverflow',      {'fg': s:base08})
call s:hi('gitcommitSelected',      {'fg': s:base03})
call s:hi('gitcommitSelectedFile',  {'fg': s:base0B, 'attrs': [s:attrs.bold]})
call s:hi('gitcommitSelectedType',  {'fg': s:base0D})
call s:hi('gitcommitSummary',       {'fg': s:base0B})
call s:hi('gitcommitUnmergedFile',  {'fg': s:base08, 'attrs': [s:attrs.bold]})
call s:hi('gitcommitUnmergedType',  {'fg': s:base0D})
call s:hi('gitcommitUntracked',     {'fg': s:base03})
call s:hi('gitcommitUntrackedFile', {'fg': s:base0A})

" Goyo
let g:goyo_bg = s:base00[0]

" JavaScript
call s:hi('javaScript',       {'fg': s:base05})
call s:hi('javaScriptBraces', {'fg': s:base05})
call s:hi('javaScriptNumber', {'fg': s:base09})
" pangloss/vim-javascript
call s:hi('jsBuiltins',          {'fg': s:base0A})
call s:hi('jsClassDefinition',   {'fg': s:base0A})
call s:hi('jsClassFuncName',     {'fg': s:base0D})
call s:hi('jsClassMethodType',   {'fg': s:base0E})
call s:hi('jsExceptions',        {'fg': s:base0A})
call s:hi('jsFuncCall',          {'fg': s:base0D})
call s:hi('jsFuncName',          {'fg': s:base0D})
call s:hi('jsFunction',          {'fg': s:base0E})
call s:hi('jsGlobalNodeObjects', {'fg': s:base0A})
call s:hi('jsGlobalObjects',     {'fg': s:base0A})
call s:hi('jsOperator',          {'fg': s:base0D})
call s:hi('jsRegexpString',      {'fg': s:base0C})
call s:hi('jsReturn',            {'fg': s:base0E})
call s:hi('jsStatement',         {'fg': s:base0E})
call s:hi('jsThis',              {'fg': s:base08})

" Limelight
let g:limelight_conceal_guifg = s:base03[0]

" Markdown
call s:hi('markdownCode',             {'fg': s:base0B})
call s:hi('markdownCodeBlock',        {'fg': s:base0B})
call s:hi('markdownError',            {'fg': s:base05, 'bg': s:base00})
call s:hi('markdownHeadingDelimiter', {'fg': s:base0D})

" NERDTree
call s:hi('NERDTreeDirSlash', {'fg': s:base0D})
call s:hi('NERDTreeFile',     {'fg': s:base05})
call s:hi('NERDTreeExecFile', {'fg': s:base05})

" Python
call s:hi('pythonInclude',   {'fg': s:base0E})
call s:hi('pythonOperator',  {'fg': s:base0E})
call s:hi('pythonRepeat',    {'fg': s:base0E})
call s:hi('pythonStatement', {'fg': s:base0E})

" Ruby
call s:hi('rubyAttribute',              {'fg': s:base0D})
call s:hi('rubyConstant',               {'fg': s:base0A})
call s:hi('rubyInterpolationDelimiter', {'fg': s:base0F})
call s:hi('rubyRegexp',                 {'fg': s:base0C})
call s:hi('rubyStringDelimiter',        {'fg': s:base0B})
call s:hi('rubySymbol',                 {'fg': s:base0B})

" SASS
call s:hi('sassClassChar', {'fg': s:base09})
call s:hi('sassidChar',    {'fg': s:base08})
call s:hi('sassInclude',   {'fg': s:base0E})
call s:hi('sassMixing',    {'fg': s:base0E})
call s:hi('sassMixinName', {'fg': s:base0D})
