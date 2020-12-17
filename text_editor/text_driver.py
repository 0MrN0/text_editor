from typing import List


class TextDriver:
    def __init__(self, gap_size: int, text: str):
        self.text = list(text)
        self.gap_size = gap_size
        for i in range(gap_size):
            self.text.append('')
        self.gap_start = len(self.text) - self.gap_size
        self.gap_end = len(self.text) - 1
        self.copy_buffer = []

    def get_text(self) -> str:
        return ''.join(self.text)

    def set_text(self, text: List[str]):
        self.text = text
        for i in range(self.gap_size):
            self.text.append('')
        self.gap_start = len(self.text) - self.gap_size
        self.gap_end = len(self.text) - 1
        self.copy_buffer = []

    # offset > 0 - right, else left
    def move_on(self, offset: int):
        if offset < 0:
            for i in range(-offset):
                if self.gap_start - 1 == -1:
                    break
                self.gap_start -= 1
                self.gap_end -= 1
                self.text[self.gap_end + 1] = self.text[self.gap_start]
                self.text[self.gap_start] = ''
        else:
            for i in range(offset):
                if self.gap_end + 1 == len(self.text):
                    break
                self.gap_start += 1
                self.gap_end += 1
                self.text[self.gap_start - 1] = self.text[self.gap_end]
                self.text[self.gap_end] = ''

    def _recreate_buffer(self):
        temp_buffer = []
        for i in range(self.gap_start, len(self.text)):
            temp_buffer.append(self.text[i])
        for i in range(self.gap_start, self.gap_start + self.gap_size):
            if i == len(self.text):
                self.text.append('')
            else:
                self.text[i] = ''
        self.gap_end = len(self.text) - 1
        for i in range(self.gap_end + 1, self.gap_end + 1 + len(temp_buffer)):
            if i == len(self.text):
                self.text.append(temp_buffer[i - self.gap_end - 1])
            else:
                self.text[i] = temp_buffer[i - self.gap_end - 1]

    def insert(self, string: str):
        continue_iteration = False
        for i in range(len(string)):
            if continue_iteration:
                continue_iteration = False
                continue
            if i + 1 < len(self.text) and string[i] == '\\' and (string[i + 1] == 'n'
                                                                 or string[i + 1] == 't'):
                if string[i + 1] == 'n':
                    self.text[self.gap_start] = '\n'
                elif string[i + 1] == 't':
                    self.text[self.gap_start] = '\t'
                continue_iteration = True
            else:
                self.text[self.gap_start] = string[i]
            self.gap_start += 1
            if self.gap_start > self.gap_end:
                self._recreate_buffer()

    def _shift(self):
        for i in range(self.gap_end, len(self.text) - 1):
            self.text[i] = self.text[i + 1]
        self.gap_end -= 1
        self.text.pop()

    def backspace(self):
        if self.gap_start == 0:
            return
        self.gap_start -= 1
        self.text[self.gap_start] = ''
        self._shift()

    def delete(self):
        if self.gap_end == len(self.text) - 1:
            return
        self.gap_end += 1
        self.text[self.gap_end] = ''
        self._shift()

    def copy_left(self, length: int, is_cut: bool):
        self.copy_buffer = []
        for i in range(self.gap_start - 1, self.gap_start - length - 1, -1):
            if i < 0:
                self.copy_buffer.reverse()
                return
            self.copy_buffer.append(self.text[i])
            if is_cut:
                self.backspace()
        self.copy_buffer.reverse()

    # при удалении длина текста уменьшается, но i продолжает расти,
    # поэтому размер текста фиксируется вначале
    def copy_right(self, length: int, is_cut: bool):
        self.copy_buffer = []
        text_length = len(self.text)
        for i in range(self.gap_end + 1, self.gap_end + length + 1):
            if i >= text_length:
                return
            if is_cut:
                self.copy_buffer.append(self.text[self.gap_end + 1])
                self.delete()
            else:
                self.copy_buffer.append(self.text[i])


    def past(self):
        self.insert(''.join(self.copy_buffer))
