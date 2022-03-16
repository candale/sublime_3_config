"""
This is meant to be used with the command
subl -n --command add_datetime_now_at_end /path/to/journal.log

such that, with a key combination <alt+n>, I can run it and I can instantly get a
new log available
"""

from datetime import datetime
import sublime
import sublime_plugin


VIEW_ID = None


class AddDatetimeNowAtEndTxtCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        if self.view.is_loading():
            print('ERROR: wut?')

        datetime.utcnow().isoformat()
        self.view.insert(edit, 0, "### -- {} --\n\n\n".format(datetime.utcnow().isoformat()))

        pt = self.view.text_point(1, 0)

        self.view.sel().clear()
        self.view.sel().add(sublime.Region(pt))

        self.view.show(pt)
        markdown_sytanx = sublime.Syntax(
            'Packages/Markdown/Markdown.sublime-syntax',
            'Markdown',
            False,
            None
        )
        self.view.assign_syntax(markdown_sytanx)


class AddDatetimeNowAtEndCommand(sublime_plugin.WindowCommand):

    def run(self):
        global VIEW_ID
        views = self.window.views()

        if len(views) != 1:
            return

        view = views[0]
        if view.is_loading():
            # register the view id and let the listener do the job
            VIEW_ID = view.id()


class InsertDatetimeEventListner(sublime_plugin.ViewEventListener):

    def on_load(self):
        if VIEW_ID and self.view.id() == VIEW_ID:
            self.view.run_command('add_datetime_now_at_end_txt')
