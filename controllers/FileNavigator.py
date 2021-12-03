import os, shutil
from PyQt5 import QtGui


class FileNavigator:

    icons = {
        'folder': 'assets/directory_icon.png',
        'file': 'assets/file_icon.png',
        'file_extensions': {
            'pdf': 'assets/pdf_file_icon.png',
            'py': 'assets/python_file_icon.png',
            'lnk': 'assets/ink_file_icon.png',
            'html': 'assets/html_file_icon.png',
            'css': 'assets/css_file_icon.png',
            'js': 'assets/js_file_icon.png',
            'php': 'assets/php_file_icon.png'
        }
    }

    exec_file = {
        'default': 'notepad',
        'html': 'chrome'
    }

    current_directory = ''
    main_path = os.path.dirname(os.path.realpath(__file__)).replace('controllers', '')

    def __init__(self):
        self.current_directory = os.environ['HOMEPATH'].replace('\\', '/') + '/Desktop/'

    def get_file_extension(self, file_):
        parts = file_.split('.')

        return parts[-1]

    def file_or_folder(self, content):
        return 'folder' if os.path.isdir(content) else 'file'

    def get_full_path(self, content):
        return self.current_directory + content

    def open_file(self, file_):
        extension = self.get_file_extension(file_)
        program_used = ''

        try:
            program_used = self.exec_file[extension]
        except KeyError:
            program_used = self.exec_file['default']

        os.system('start {} "{}"'.format(program_used, file_))

    def get_content_icon(self, content):
        content_full_path = self.current_directory + content
        content_type = self.file_or_folder(content_full_path)

        if content_type == 'file':
            extension = self.get_file_extension(content)

            try:
                icon_pixmap = QtGui.QPixmap(self.icons['file_extensions'][extension])
            except KeyError:
                icon_pixmap = QtGui.QPixmap(self.icons['file'])
        else:
            icon_pixmap = QtGui.QPixmap(self.icons['folder'])

        return icon_pixmap

    def show_content(self):
        content = os.listdir(self.current_directory)
        each_content_with_its_data = []

        for c in content:
            data = {'full_path': self.get_full_path(c), 'name': c, 'icon': self.get_content_icon(c)}
            data['type'] = self.file_or_folder(data['full_path'])

            each_content_with_its_data.append(data)

        return each_content_with_its_data

    def go(self, directory_name):
        new_directory = directory_name + '/'

        if os.path.isdir(self.current_directory + new_directory):
            self.current_directory += new_directory
            return True
        else:
            return False

    def go_to(self, path):
        if path[-1] != '/':
            path += '/'

        if os.path.isdir(path):
            self.current_directory = path

            return True
        else:
            return False

    def back(self):
        splitted_directories = self.current_directory.split('/')

        if splitted_directories[-1] == '':
            splitted_directories.pop(-1)

        if len(splitted_directories) > 1:
            splitted_directories.pop(-1)

        self.current_directory = '/'.join(splitted_directories) + '/'

        return True

    def rename_content(self, filename, new_name):
        current_content_path = self.current_directory + filename
        new_current_path = self.current_directory + new_name

        try:
            os.rename(current_content_path, new_current_path)
        except FileNotFoundError:
            print('O conteúdo já não existe mais')

        return True

    def delete_content(self, filename):
        content_path = self.current_directory + filename

        try:
            if self.file_or_folder(content_path) == 'file':
                os.remove(content_path)
            else:
                shutil.rmtree(content_path)
        except FileNotFoundError:
            print('O conteúdo já não existe mais')
