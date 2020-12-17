from typing import List

from text_editor.text_driver import TextDriver


class Word:
    def __init__(self, word: str):
        self.word = word
        self.width = len(word)

    def __repr__(self):
        return self.word


class Controller:
    def __init__(self, gap_size=50, text='', row_length=128):
        self.commands = {'move_on': self._move_on,
                         'backspace': self._backspace,
                         'delete': self._delete,
                         'copy': self._copy,
                         'cut': self._cut,
                         'past': self._past}
        self.driver = TextDriver(gap_size, text)
        self.row_length = row_length
        self.count = 0

    def open_file(self, file_way: str):
        text = []
        with open(file_way, encoding='utf-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                list_line = list(line)
                text.extend(list_line)
        self.driver.set_text(text)

    def save_file(self, file_way: str):
        text = self.driver.get_text()
        print(f'\n{text}\n')
        with open(file_way, 'w', encoding='utf-8') as file:
            file.write(text)

    def _move_on(self):
        self.driver.move_on(self.count)

    def _backspace(self):
        for i in range(self.count):
            self.driver.backspace()

    def _delete(self):
        for i in range(self.count):
            self.driver.delete()

    def insert(self, string: str):
        self.driver.insert(string)

    def _copy(self):
        if self.count < 0:
            self.driver.copy_left(-self.count, False)
        else:
            self.driver.copy_right(self.count, False)

    def _cut(self):
        if self.count < 0:
            self.driver.copy_left(-self.count, True)
        else:
            self.driver.copy_right(self.count, True)

    def _past(self):
        self.driver.past()

    def _get_words(self) -> List['Word']:
        word = []
        words = []
        for char in self.driver.text:
            word.append(char)
            if char == ' ':
                words.append(Word(''.join(word)))
                word = []
        words.append(Word(''.join(word)))
        return words

    def get_driver_text(self) -> List[List[str]]:
        words = self._get_words()
        row_length = 0
        row = []
        text = []
        for word in words:
            if row_length + word.width > self.row_length and row_length != 0:
                text.append(row)
                row = []
                row_length = 0
            row.append(str(word))
            row_length += word.width
        text.append(row)
        return text

    def get_cursor(self) -> int:
        return self.driver.gap_start
