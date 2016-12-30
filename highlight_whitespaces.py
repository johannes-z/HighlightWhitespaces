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
  "highlight_whitespaces_single_space": false,
  "highlight_last_whitespace": true
  }

Forked from https://github.com/SublimeText/TrailingSpaces/
  by Jean-Denis Vauguet <jd@vauguet.fr>, Oktay Acikalin <ok@ryotic.de>

@author: Kemal Hadimli <disq@sf.net>
@contrib: Salvatore Poliandro III <popsikle@gmail.com>
@license: MIT (http://www.opensource.org/licenses/mit-license.php)
@since: 2015-06-05
'''

import sublime
import sublime_plugin

DEFAULT_MAX_FILE_SIZE = 1048576
DEFAULT_COLOR_SCOPE_NAME = "invalid"
DEFAULT_IS_ENABLED = True
DEFAULT_CHECK_SPACES = True
DEFAULT_SINGLE_SPACE = False
DEFAULT_CHECK_EOL = True
DEFAULT_CHECK_TABS = True
DEFAULT_CHECK_MIXED = True
DEFAULT_LAST_WHITESPACE = False
DEFAULT_SHOW_BORDERS = True

hws_toggled = False
hws_v3 = (int(sublime.version()) >= 3000)


def plugin_loaded():
  global hws_v3

  if is_enabled(True) and hws_v3:
    highlight_whitespaces(sublime.active_window().active_view())


def is_enabled(init=False):
  global hws_toggled

  if init:
    hws_toggled = bool(get_settings().get('highlight_whitespaces_enabled',
                                          DEFAULT_IS_ENABLED))
  return hws_toggled


def get_settings():
  return sublime.load_settings('highlight_whitespaces.sublime-settings')


# Determine if the view is a find results view
def is_find_results(view):
  return (view.settings().get('syntax') and
          "Find Results" in view.settings().get('syntax'))


# Return an array of regions matching whitespaces.
def find_whitespaces_spaces(view):
  hws_settings = get_settings()
  last_whitespace = bool(hws_settings.get('highlight_last_whitespace',
                                          DEFAULT_LAST_WHITESPACE))
  single_space = bool(hws_settings.get('highlight_whitespaces_single_space',
                                       DEFAULT_SINGLE_SPACE))
  if single_space:
    regex = ' +'
  else:
    regex = ' {2,}|\t | \t'
    if last_whitespace:
      regex += '| {1,}$'

  return view.find_all(regex)


def find_whitespaces_tabs(view):
  return view.find_all('\t+')


def find_whitespaces_eol(view):
    return view.find_all('[\t ]+$')


def find_whitespaces_mixed(view):
    return view.find_all('(\t )|( \t)')


# Highlight whitespaces
def highlight_whitespaces(view):
  hws_settings = get_settings()

  show_borders = \
    hws_settings.get('highlight_whitespaces_show_borders', DEFAULT_SHOW_BORDERS)

  region = sublime.DRAW_EMPTY if show_borders else sublime.HIDDEN

  max_size = hws_settings.get('highlight_whitespaces_file_max_size',
                              DEFAULT_MAX_FILE_SIZE)
  space_scope_name = \
      hws_settings.get('highlight_whitespaces_space_highlight_scope_name',
                       DEFAULT_COLOR_SCOPE_NAME)
  tab_scope_name = \
      hws_settings.get('highlight_whitespaces_tab_highlight_scope_name',
                       DEFAULT_COLOR_SCOPE_NAME)

  eol_scope_name = \
      hws_settings.get('highlight_whitespaces_eol_highlight_scope_name',
                       DEFAULT_COLOR_SCOPE_NAME)

  mixed_scope_name = \
      hws_settings.get('highlight_whitespaces_mixed_highlight_scope_name',
                       DEFAULT_COLOR_SCOPE_NAME)

  if view.size() <= max_size and not is_find_results(view):
    if hws_settings.get('highlight_whitespaces_check_spaces',
                        DEFAULT_CHECK_SPACES):
      space_regions = find_whitespaces_spaces(view)
      view.add_regions('WhitespacesHighlightListener',
                       space_regions, space_scope_name, '',
                       region)

    if hws_settings.get('highlight_whitespaces_check_tabs',
                        DEFAULT_CHECK_TABS):
      tab_regions = find_whitespaces_tabs(view)
      view.add_regions('WhitespacesHighlightListener2',
                       tab_regions, tab_scope_name, '',
                       region)

    if hws_settings.get('highlight_whitespaces_check_eol', DEFAULT_CHECK_EOL):
      eol_regions = find_whitespaces_eol(view)
      view.add_regions('WhitespacesHighlightListener3',
                       eol_regions, eol_scope_name, '',
                       region)

    if hws_settings.get('highlight_whitespaces_check_mixed',
                        DEFAULT_CHECK_MIXED):
      mixed_regions = find_whitespaces_mixed(view)
      view.add_regions('WhitespacesHighlightListener4',
                       mixed_regions, mixed_scope_name, '',
                       region)


# Clear all white spaces
def clear_whitespaces_highlight(window):
  for view in window.views():
    view.erase_regions('WhitespacesHighlightListener')
    view.erase_regions('WhitespacesHighlightListener2')
    view.erase_regions('WhitespacesHighlightListener3')
    view.erase_regions('WhitespacesHighlightListener4')


# Toggle the event listner on or off
class HwsToggleWhitespacesCommand(sublime_plugin.WindowCommand):
  def run(self):
    global hws_toggled
    hws_toggled = False if hws_toggled else True

    # If toggling on, go ahead and perform a pass,
    # else clear the highlighting in all views
    if hws_toggled:
      highlight_whitespaces(self.window.active_view())
    else:
      clear_whitespaces_highlight(self.window)


# Highlight matching regions.
class WhitespacesHighlightListener(sublime_plugin.EventListener):
  def on_modified(self, view):
    if hws_toggled:
      highlight_whitespaces(view)

  def on_activated(self, view):
    if hws_toggled:
      highlight_whitespaces(view)

  def on_load(self, view):
    if hws_toggled:
      highlight_whitespaces(view)


class WhitespacesHighlightListener2(sublime_plugin.EventListener):
  def on_modified(self, view):
    if hws_toggled:
      highlight_whitespaces(view)

  def on_activated(self, view):
    if hws_toggled:
      highlight_whitespaces(view)

  def on_load(self, view):
    if hws_toggled:
      highlight_whitespaces(view)


class WhitespacesHighlightListener3(sublime_plugin.EventListener):
    def on_modified(self, view):
        if hws_toggled:
            highlight_whitespaces(view)

    def on_activated(self, view):
        if hws_toggled:
            highlight_whitespaces(view)

    def on_load(self, view):
        if hws_toggled:
            highlight_whitespaces(view)


class WhitespacesHighlightListener4(sublime_plugin.EventListener):
    def on_modified(self, view):
        if hws_toggled:
            highlight_whitespaces(view)

    def on_activated(self, view):
        if hws_toggled:
            highlight_whitespaces(view)

    def on_load(self, view):
        if hws_toggled:
            highlight_whitespaces(view)


# pluging init for ST2
if not hws_v3:
  plugin_loaded()
