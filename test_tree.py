import pytest
from suffix_tree import SuffixTree

def test_implicit():
    st = SuffixTree('abcd')
    st_d = st.as_dict()
    assert(st_d == {'d': {}, 'cd': {}, 'bcd': {}, 'abcd': {}})