from typing import List

from text_editor.controller import Controller
import os


class Console:
    def __init__(self):
        self.controller = Controller()

    @staticmethod
    def _show_help():
        print('move_on x: переходит на х символов вправо, если х > 0, иначе влево;')
        print('backspace x: удаляет х символов перед курсором, если они есть;')
        print('delete x: удаляет х символов после курсора;')
        print('insert: перейти в режим набора строки;')
        print('copy x: копирует х символов от курсора, х > 0 - берет символы справа, х < 0 - слева;')
        print('cut x: вырезает х символов от курсора, х > 0 - берет символы справа, х < 0 - слева;')
        print('past: вставляет скопированное/вырезанное ранее;')
        print('get_current_position: выводит текущую позицию курсора;')
        print('exit: выход.')
        print()
        print('Для возвращения на главную нажмите enter')
        input()

    def _show_main_layer(self):
        text = self.controller.get_driver_text()
        for row in text:
            print(''.join(row))
        print('\n')
        print('help - получить помощь')
        print()

    def _set_arguments(self, arguments: List[str]) -> bool:
        try:
            if len(arguments) >= 1:
                self.controller.count = int(arguments[0])
        except ValueError:
            return True
        return False

    def _show_cursor(self):
        print(f'Текущая позиция: {self.controller.get_cursor()}')
        input('Для продолжения нажмите enter')

    def _insert_mode(self):
        print('Режим набора текста. \\n - перенос строки, \\t - табуляция.'
              '\nДля подтверждения нажмите enter.\n')
        self.controller.insert(input())

    def start(self):
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            self._show_main_layer()
            user_input = input('Введите команду: ').split(' ')
            if user_input[0] == 'help':
                self._show_help()
                continue
            if user_input[0] == 'exit':
                exit(0)
            if user_input[0] == 'get_current_position':
                self._show_cursor()
                continue
            if user_input[0] == 'insert':
                self._insert_mode()
                continue
            if user_input[0] not in self.controller.commands:
                print('\nНеизвестная команда')
                continue
            any_errors = self._set_arguments(user_input[1:])
            if any_errors:
                print('Введите аргументы правильно. Аргументы должны быть целыми числами.')
                input('Для продолжения нажмите enter')
                continue
            result = self.controller.commands[user_input[0]]()
            if result:
                print(result)
                input('Для продолжения нажмите enter')
