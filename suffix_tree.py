from __future__ import annotations
from typing import List, Dict, Tuple


class SuffixDef(object):
    pass


class SuffixNode(SuffixDef):
    def __init__(self, label: Tuple(int, int) = tuple([None, None]), children: Dict[str, SuffixNode] = {}):
        self.label: Tuple(int, int) = label
        self.children: Dict[str, SuffixNode] = children


class SuffixTree(SuffixDef):
    def __init__(self, S: str = ""):
        self.S: str = S + self._get_unsed_char(S)
        self.leaves: Dict[int, SuffixNode] = {}
        self._construct()

    def __repr__(self):
        pass

    def _construct(self):
        m: int = len(self.S)
        self.root: SuffixNode = SuffixNode(children={self.S[0]: SuffixNode(label=tuple([0, 0]))})
        
        for i in range(0, m - 2):
            # begin phase i + 1
            print (f'i: {i}')
            for j in range(i + 1):
                print(f'j: {j}')
                '''
                    
                Follow the path from the root labeled S[j], ..., S[i] and, if 
                needed, extend it by adding character S[i + 1]

                '''
                curr_node: SuffixNode = self.root
                parent_node: SuffixNode = None
                offset: int = 0
                at_node: bool = True
                prefix: str = self.S[j: i]


                '''


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
                        if k == curr_node.label[offset]:
                            # We are still traversing an edge
                            offset += 1
                        else:
                            # freak disaster
                            raise SomethingWentWrong("Failed to find character in \
                                                      tree. This shouldn't happen.")

                        # CHECK OFFSET hERE????
                    if offset == self.get_label_length(curr_node):
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
                        curr_node.label = (curr_node.label[0], i + 1)
                    else:
                        if self.S[i + 1] in curr_node.children:
                            # Rule 3
                            pass
                        else:
                            # Rule 2
                            curr_node.children[self.S[i + 1]] = SuffixNode(label=(i + 1, i + 1))
                            self.leaves[j] = curr_node.children[self.S[i + 1]]
                else:
                    if self.S[i + 1] == self.get_char_at_offset(curr_node, offset):
                        # Rule 3
                        pass
                    else:
                        # Rule 2
                        new_leaf: SuffixNode = SuffixNode(label=self.S[i + 1])
                        subdivision: SuffixNode = SuffixNode(label=curr_node.label[:offset], 
                                                             children={
                                                                 self.S[i + 1]: new_leaf,
                                                                 curr_node.label[offset]: curr_node,
                                                             })
                        parent_node.children[curr_node.label[0]] = subdivision
                        curr_node.label = curr_node.label[offset:]
                        self.leaves[j] = new_leaf 
                        
    def get_char_at_offset(self, node: SuffixNode, offset: int):
        true_offset: int = node.label[0] + offset
        return self.S[true_offset]

    @staticmethod
    def get_label_length(node: SuffixNode):
        return node.label[1] - node.label[0] + 1

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