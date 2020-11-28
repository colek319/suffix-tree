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


class SuffixTree(SuffixDef):
    def __init__(self, S: str = ""):
        self.S: str = S
        self.leaves: Dict[int, SuffixNode] = {}
        self.root: SuffixNode = self._construct()

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

    def _construct(self):
        m: int = len(self.S)
        root: SuffixNode = SuffixNode(children={self.S[0]: SuffixNode(label=SuffixNodeLabel(0, 1))})
        for i in range(0, m - 1):
            # begin phase i + 1
            for j in range(i + 2):
                '''
                Follow the path from the root labeled S[j], ..., S[i] and, if 
                needed, extend it by adding character S[i + 1]
                '''
                curr_node: SuffixNode = root
                parent_node: SuffixNode = None
                offset: int = 0
                at_node: bool = True
                prefix: str = self.S[j: i + 1]

                '''
                Go through characters self.S[i:j], then determine what to do with character self.S[j].

                '''
                for p, k in enumerate(prefix):
                    if at_node:
                        # move pointer to next unseen character in the nodes label
                        if k not in curr_node.children:
                            raise SomethingWentWrong("Failed to find character in \
                                                      tree. This shouldn't happen.")
                        at_node = False
                        parent_node = curr_node
                        curr_node = curr_node.children[k]
                        offset += 1
                    else:
                        # print(self.get_char_at_offset(curr_node, offset))
                        if k == self.get_char_at_offset(curr_node, offset):
                            # We are still traversing an edge
                            offset += 1
                        else:
                            # freak disaster
                            raise SomethingWentWrong("Failed to find character in \
                                                      tree. This shouldn't happen.")

                        # CHECK OFFSET hERE????
                    if offset == curr_node.label.length:
                        offset = 0
                        at_node = True
                if at_node:
                    '''

                    Rule 1 := "we are at a leaf"

                    Rule 2 := "No path from the end of prefix ends with S[i + 1]"
                    
                    Rule 3 := "Some path from the end of prefix starts with S[i + 1]"

                    '''

                    if len(curr_node.children) == 0:
                        # Rule 1 () 
                        curr_node.label = SuffixNodeLabel(curr_node.label.offset, curr_node.label.length + 1)

                    else:
                        if self.S[i + 1] in curr_node.children:
                            # Rule 3
                            pass
                        else:
                            # Rule 2
                            curr_node.children[self.S[i + 1]] = SuffixNode(label=SuffixNodeLabel(i + 1, 1))
                            self.leaves[j] = curr_node.children[self.S[i + 1]]
                else:
                    if self.S[i + 1] == self.get_char_at_offset(curr_node, offset):
                        # Rule 3
                        pass
                    else:
                        # Rule 2
                        new_leaf: SuffixNode = SuffixNode(label=SuffixNodeLabel(i + 1, 1))
                        subdivision: SuffixNode = SuffixNode(label=SuffixNodeLabel(curr_node.label.offset, offset), 
                                                             children={
                                                                 self.S[i + 1]: new_leaf,
                                                                 self.get_char_at_offset(curr_node, offset): curr_node,
                                                             })
                        parent_node.children[self.get_char_at_offset(curr_node, 0)] = subdivision
                        curr_node.label = curr_node.label[offset:]
                        curr_node.label = SuffixNodeLabel(curr_node.label.offset + offset, curr_node.label.length - offset)
                        self.leaves[j] = new_leaf 
        return root
                        
    def get_char_at_offset(self, node: SuffixNode, offset: int):
        true_offset: int = node.label.offset + offset
        return self.S[true_offset]

    @staticmethod
    def get_label_length(node: SuffixNode):
        return node.label.length

    def get_label(self, node: SuffixNode) -> str:
        return self.S[node.label.offset: node.label.offset + node.label.length]

    def follow_path(self, P: str):
        '''
            Takes a pattern string P, and returns:
                1. (), if P is already in the tree
                2. (parent, offset, child), if P ends in the middle 
                3. (node, None, None), if P ends at a leaf
        '''
        for c in P:
            pass



    @staticmethod
    def _get_unsed_char(S: str):
        """
        Takes a string S, and returns a char not used in S.

        Complexity: O(log(n)) where n == len(S)
        """
        all_chars = set(chr(i) for i in range(256))
        for s in S:
            all_chars.discard(s)
        
        if len(all_chars) == 0:
            raise Exception("There are no unused characters in S.")
        
        return all_chars.pop()
        

class SomethingWentWrong(Exception):
    pass