import pytest
from suffix_tree import SuffixTree

def test_build_tree():
    x = SuffixTree('abcd')
    print(x)