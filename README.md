## Synopsis

This is a plugin for [Sublime Text 2](http://www.sublimetext.com/2) and [3](http://www.sublimetext.com/3).

**Highlight whitespaces in documents**

This plugin will highlight each tab or more-than-one space in the document.

## Installation

Go to your `Packages` subdirectory under ST2's data directory:

* Windows: `%APPDATA%\Sublime Text 2`
* OS X: `~/Library/Application Support/Sublime Text 2/Packages`
* Linux: `~/.config/sublime-text-2`
* Portable Installation: `Sublime Text 2/Data`

Then clone this repository:

```git clone git://github.com/disq/HighlightWhitespaces.git```

That's it!

Note for ST3 users: For Sublime Text 3, replace "2" with "3" in path names. (`%APPDATA%\Sublime Text 3` and so on)

## Options

Several options are available to customize the plugin look 'n feel. The
config keys goes into config files accessible throught the "Preferences"
menu.

### Toggle highlight shortcut

The default toggle highlight shortcut is ```ctrl+alt+w``` (```cmd+alt+w``` for OS X)

### Disable highlighting when Sublime Text starts up

Change `highlight_whitespaces_enabled` from the default of `true` to `false`.

### Change the highlighting color

One may also change the highlighting color, providing a scope name such
as "invalid", "comment"... in "File Settings - User":

```
{
	"highlight_whitespaces_space_highlight_scope_name": "invalid",
	"highlight_whitespaces_tab_highlight_scope_name": "invalid",
	"highlight_whitespaces_eol_highlight_scope_name": "invalid"
}
```

Actually, "invalid" is the default value. If you'd like to use a custom color,
it should be defined as a color scope in your theme file. Feel free to ask me
how to do it.

### Disabling highlighting for large files

Highlighting may be disabled for large files. The default threshold is around
1M chars. This is configurable (in "File Settings - User"); unit is number of chars:

```
{ "highlight_whitespaces_file_max_size": 1000}
```

### Credits

This is a modified version of the TrailingSpaces plugin by Jean-Denis Vauguet and Oktay Acikalin

TrailingSpaces is at https://github.com/SublimeText/TrailingSpaces/
