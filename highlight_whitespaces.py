'''
Marks all tabs and two or more spaces in each line with separate colors

Config summary (see README.md for details):

    # key binding
    { "keys": ["ctrl+alt+w"], "command": "hws_toggle_whitespaces" }

    # file settings
    {
    "highlight_whitespaces_space_highlight_scope_name": "invalid",
    "highlight_whitespaces_tab_highlight_scope_name": "invalid",
    "highlight_whitespaces_file_max_size": 1048576,
    "highlight_whitespaces_enabled": true,
    "highlight_whitespaces_check_spaces": true,
    "highlight_whitespaces_check_tabs": true,
    "highlight_last_whitespace": true
    }

Forked from https://github.com/SublimeText/TrailingSpaces/ by Jean-Denis Vauguet <jd@vauguet.fr>, Oktay Acikalin <ok@ryotic.de>

@author: Kemal Hadimli <disq@sf.net>
@license: MIT (http://www.opensource.org/licenses/mit-license.php)
@since: 2012-10-05
'''

import sublime
import sublime_plugin

DEFAULT_MAX_FILE_SIZE = 1048576
DEFAULT_COLOR_SCOPE_NAME = "invalid"
DEFAULT_IS_ENABLED = True
DEFAULT_CHECK_SPACES = True
DEFAULT_CHECK_TABS = True
DEFAULT_LAST_WHITESPACE = False

#Set whether the plugin is on or off
hws_settings = sublime.load_settings('highlight_whitespaces.sublime-settings')
hws_enabled = bool(hws_settings.get('highlight_whitespaces_enabled',
                                               DEFAULT_IS_ENABLED))

# Determine if the view is a find results view
def is_find_results(view):
    return view.settings().get('syntax') and "Find Results" in view.settings().get('syntax')

# Return an array of regions matching whitespaces.
def find_whitespaces_spaces(view):
    last_whitespace = bool(hws_settings.get('highlight_last_whitespace',DEFAULT_LAST_WHITESPACE))
    regex = ' {2,}'
    if last_whitespace:
	regex += '| {1,}$'

    return view.find_all(regex)

def find_whitespaces_tabs(view):
    return view.find_all('\t+')


# Highlight whitespaces
def highlight_whitespaces(view):
    max_size = hws_settings.get('highlight_whitespaces_file_max_size',
                               DEFAULT_MAX_FILE_SIZE)
    space_scope_name = hws_settings.get('highlight_whitespaces_space_highlight_scope_name',
                                       DEFAULT_COLOR_SCOPE_NAME)
    tab_scope_name = hws_settings.get('highlight_whitespaces_tab_highlight_scope_name',
                                       DEFAULT_COLOR_SCOPE_NAME)
    if view.size() <= max_size and not is_find_results(view):
        if hws_settings.get('highlight_whitespaces_check_spaces', DEFAULT_CHECK_SPACES):
            space_regions = find_whitespaces_spaces(view)
            view.add_regions('WhitespacesHighlightListener',
                             space_regions, space_scope_name, '',
                             sublime.DRAW_EMPTY)
        if hws_settings.get('highlight_whitespaces_check_tabs', DEFAULT_CHECK_TABS):
            tab_regions = find_whitespaces_tabs(view)
            view.add_regions('WhitespacesHighlightListener2',
                             tab_regions, tab_scope_name, '',
                             sublime.DRAW_EMPTY)


# Clear all white spaces
def clear_whitespaces_highlight(window):
    for view in window.views():
        view.erase_regions('WhitespacesHighlightListener')
        view.erase_regions('WhitespacesHighlightListener2')


# Toggle the event listner on or off
class HwsToggleWhitespacesCommand(sublime_plugin.WindowCommand):
    def run(self):
        global hws_enabled
        hws_enabled = False if hws_enabled else True

        # If toggling on, go ahead and perform a pass,
        # else clear the highlighting in all views
        if hws_enabled:
            highlight_whitespaces(self.window.active_view())
        else:
            clear_whitespaces_highlight(self.window)


# Highlight matching regions.
class WhitespacesHighlightListener(sublime_plugin.EventListener):
    def on_modified(self, view):
        if hws_enabled:
            highlight_whitespaces(view)

    def on_activated(self, view):
        if hws_enabled:
            highlight_whitespaces(view)

    def on_load(self, view):
        if hws_enabled:
            highlight_whitespaces(view)

class WhitespacesHighlightListener2(sublime_plugin.EventListener):
    def on_modified(self, view):
        if hws_enabled:
            highlight_whitespaces(view)

    def on_activated(self, view):
        if hws_enabled:
            highlight_whitespaces(view)

    def on_load(self, view):
        if hws_enabled:
            highlight_whitespaces(view)

