import sublime
import sublime_plugin
import os
import re


class SassToCssCommand(sublime_plugin.TextCommand):

    def __init__(self, view):
        self.view = view
        # check if the sass-media_query_combiner gem is installed
        if os.system('gem list sass-media_query_combiner | grep sass-media_query_combiner') is not 0:
            self.extra_params = '-r sass-media_query_combiner '
        else:
            self.extra_params = ''

    def run(self, edit):
        input_filename = self.view.file_name()
        # only process scss or sass files
        if not input_filename.endswith('.scss') and not input_filename.endswith('.sass'):
            return
        # do not process partials
        if os.path.basename(input_filename).startswith('_'):
            return
        output_filename = re.sub('\.s(c|a)ss$', '.css', input_filename)
        # run the sass binary to compile
        if os.system('sass -t expanded ' + self.extra_params + input_filename + ' ' + output_filename) is not 0:
            sublime.error_message('The file "' + input_filename + '" could not be compiled.\n\nThis may be because sass binary could was not found on your system.')
            return
        sublime.status_message('Succesfully compiled ' + output_filename)


class SassToCssSave(sublime_plugin.EventListener):

    def on_post_save_async(self, view):
        view.run_command('sass_to_css')
