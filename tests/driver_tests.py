from text_editor.text_driver import TextDriver

import pytest


@pytest.fixture
def empty_driver():
    return TextDriver(5, '')


@pytest.mark.parametrize(
    ('absolute_offset', 'text_with_right_move', 'text_with_left_move'), [
        (6, ['H', 'e', 'l', 'l', 'o', '!', '!', '!', '', '', '', '', ''],
         ['H', 'e', '', '', '', '', '', 'l', 'l', 'o', '!', '!', '!']),
        (10, ['H', 'e', 'l', 'l', 'o', '!', '!', '!', '', '', '', '', ''],
         ['', '', '', '', '', 'H', 'e', 'l', 'l', 'o', '!', '!', '!'])
    ]
)
def test_move_on(absolute_offset, text_with_right_move, text_with_left_move):
    driver = TextDriver(5, 'Hello!!!')
    driver.move_on(absolute_offset)
    assert driver.text == text_with_right_move
    driver.move_on(-absolute_offset)
    assert driver.text == text_with_left_move


def test_simple_insert(empty_driver):
    empty_driver.insert('123')
    assert empty_driver.text == ['1', '2', '3', '', '']
    assert empty_driver.gap_start == 3
    assert empty_driver.gap_end == 4
    empty_driver.insert('4')
    assert empty_driver.text == ['1', '2', '3', '4', '']
    assert empty_driver.gap_end == empty_driver.gap_start == 4


def test_insert_with_special_chars(empty_driver):
    empty_driver.insert('\\nl')
    assert empty_driver.text == ['\n', 'l', '', '', '']
    empty_driver.insert('\\t')
    assert empty_driver.text == ['\n', 'l', '\t', '', '']


def test_insert_with_recreating_buffer(empty_driver):
    empty_driver.insert('12345')
    assert empty_driver.text == ['1', '2', '3', '4', '5', '', '', '', '', '']
    assert empty_driver.gap_start == 5
    assert empty_driver.gap_end == 9


def test_backspace():
    driver = TextDriver(5, '12345')
    driver.backspace()
    assert driver.text == ['1', '2', '3', '4', '', '', '', '', '']
    assert driver.gap_start == 4
    assert driver.gap_end == 8
    driver.move_on(-1)
    driver.backspace()
    assert driver.text == ['1', '2', '', '', '', '', '', '4']
    assert driver.gap_start == 2
    assert driver.gap_end == 6


def test_delete():
    driver = TextDriver(5, '12345')
    driver.move_on(-8)
    driver.delete()
    assert driver.text == ['', '', '', '', '', '2', '3', '4', '5']
    assert driver.gap_start == 0
    assert driver.gap_end == 4
    driver.move_on(1)
    driver.delete()
    assert driver.text == ['2', '', '', '', '', '', '4', '5']
    assert driver.gap_start == 1
    assert driver.gap_end == 5


def test_copy_left():
    driver = TextDriver(5, 'Hello, dear.')
    driver.copy_left(5, False)
    assert driver.copy_buffer == ['d', 'e', 'a', 'r', '.']
    assert driver.get_text() == 'Hello, dear.'
    driver.copy_left(7, True)
    assert driver.copy_buffer == [',', ' ', 'd', 'e', 'a', 'r', '.']
    assert driver.get_text() == 'Hello'


def test_copy_right():
    driver = TextDriver(5, 'Hello, dear.')
    driver.move_on(-13)
    driver.copy_right(5, False)
    assert driver.copy_buffer == ['H', 'e', 'l', 'l', 'o']
    assert driver.get_text() == 'Hello, dear.'
    driver.copy_right(7, True)
    assert driver.copy_buffer == ['H', 'e', 'l', 'l', 'o', ',', ' ']
    assert driver.get_text() == 'dear.'


def test_set_text():
    driver = TextDriver(5, '')
    driver.insert('lalalalalalala')
    driver.move_on(-6)
    driver.set_text(['L', 'a'])
    assert driver.text == ['L', 'a', '', '', '', '', '']
    assert driver.gap_start == 2
    assert driver.gap_end == 6
