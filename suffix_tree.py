from __future__ import annotations
from typing import List, Dict, Tuple, NamedTuple
import json


class SuffixDef(object):
    pass


class SuffixNodeLabel(NamedTuple):
    offset: int
    length: int


class SuffixNode(SuffixDef):
    def __init__(self, label: SuffixNodeLabel = SuffixNodeLabel(0, 0), children: Dict[str, SuffixNode] = {}):
        self.label: SuffixNodeLabel = label
        self.children: Dict[str, SuffixNode] = children

    def __repr__(self):
        return f'SuffixNode({self.label})'

class ConstructionError(Exception):
    pass

class SuffixTree():
    def __init__(self, S=''):
        self.S = S
        self.root = SuffixNode(children={self.S[0]: SuffixNode(label=SuffixNodeLabel(0, 1))})
        self.construct()
    
    def construct(self):
        m = len(self.S)
        for i in range(0, m - 1):
            # begin phase i + 1
            for j in range(i + 2):
                # begin extension j
                suffix = self.S[j: i + 1]
                current, parent, offset = self.traverse(suffix)
                if offset == 0:
                    if len(current.children) == 0:
                        # rule 1
                        current.label = SuffixNodeLabel(current.label.offset, current.label.length + 1)
                    else:
                        if self.S[i + 1] in current.children:
                            # rule 3
                            pass
                        else:
                            # rule 2
                            current.children[self.S[i + 1]] = SuffixNode(label=SuffixNodeLabel(i + 1, 1))
                else:
                    if self.S[i + 1] == self.get_char_at_offset(current, offset):
                        # rule 3
                        pass
                    else:
                        # rule 2
                        new_leaf = SuffixNode(label=SuffixNodeLabel(i + 1, 1))
                        subdivision = SuffixNode(label=SuffixNodeLabel(current.label.offset, offset), 
                                                             children={
                                                                 self.S[i + 1]: new_leaf,
                                                                 self.get_char_at_offset(current, offset): current,
                                                             })
                        parent.children[self.get_char_at_offset(current, 0)] = subdivision
                        current.label = current.label[offset:]
                        current.label = SuffixNodeLabel(current.label.offset + offset, current.label.length - offset)

    def traverse(self, s):
        """
        takes a string s and traverses the suffixtree. 

        returns a triple. the offset at a node, the parent node, and the child node. 
        """
        current, parent, offset = self.root, None, 0
        for p, k in enumerate(s):
            if offset == 0:
                if k not in current.children:
                    raise ConstructionError("Suffix {suffix} not found in the tree.")
                parent = current
                current = current.children[k]
                offset += 1
            else:
                if k == self.get_char_at_offset(current, offset):
                    offset += 1
                else:
                    raise ConstructionError("Suffix {suffix} not found in tree.")
        if offset == current.label.length:
            offset = 0

        return current, parent, offset
        

    def match(self, p):
        '''
        matches the string pattern p. Returns instances of p. 
        '''
        pass

    def __repr__(self):
        return f'SuffixTree({self.S[:-1]})'

    def __str__(self):
        tree_dict = self.as_dict()
        return json.dumps(tree_dict)

    def as_dict(self):
        tree_dict: dict = {}
        stack: List[tuple] = [(tree_dict, node) for node in self.root.children.values()]
        while stack:
            p: Tuple[dict, SuffixNode] = stack.pop()
            sub_tree_dict: dict = p[0].setdefault(self.get_label(p[1]), {})
            stack.extend((sub_tree_dict, node) for node in p[1].children.values())
        return tree_dict

    def get_label(self, node: SuffixNode) -> str:
        return self.S[node.label.offset: node.label.offset + node.label.length]

    def get_char_at_offset(self, node: SuffixNode, offset: int):
        true_offset: int = node.label.offset + offset
        return self.S[true_offset]
