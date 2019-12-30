import pytest
from main import is_in_grammar

inputs = ((('S->A', 'B->ab', 'A->B'), 'ab'),
          (('S->ABCd', 'A->a', 'A->1', 'B->AC', 'C->1', 'C->c'), 'aacd'),
          (('A->B', 'A->a', 'B->C', 'B->b', 'C->DD', 'C->c'), 'acc'),
          (('S->Ac', 'A->SD', 'D->aD', 'A->a'), 'aaca'),
          (('S->AB', 'S->CD', 'A->EF', 'G->AD', 'C->c', 'D->cC'), 'ccc'),
          (('S->AS', 'S->BS', 'S->s', 'E->EF', 'E->FF', 'A->a', 'F->f'),
           'aaass'),
          (('S->aXbX', 'S->aZ', 'X->aY', 'X->bY', 'X->1', 'Y->X', 'Y->cc',
            'Z->ZX'), 'aaaabbbba'),
          ((
               'A->1', 'A->BB', 'A->CD', 'B->BB', 'B->CD', 'C->(', 'D->BE',
               'D->)',
               'E->)'), '(((()()(())))())'),
          ((
               'A->1', 'A->BB', 'A->CD', 'B->BB', 'B->CD', 'C->(', 'D->BE',
               'D->)',
               'E->)'), '()(()()))()'))


def test_one():
    assert is_in_grammar(*inputs[0]) == True


def test_two():
    assert is_in_grammar(*inputs[1]) == True


def test_three():
    assert is_in_grammar(*inputs[2]) == False


def test_four():
    assert is_in_grammar(*inputs[3]) == False


def test_five():
    assert is_in_grammar(*inputs[4]) == True


def test_six():
    assert is_in_grammar(*inputs[5]) == False


def test_seven():
    assert is_in_grammar(*inputs[6]) == True


def test_eight():
    assert is_in_grammar(*inputs[7]) == True


def test_nine():
    assert is_in_grammar(*inputs[8]) == False
