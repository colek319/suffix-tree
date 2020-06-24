from types import List, Dict

SuffixDef(object):
    pass

class SuffixTree(SuffixDef):
    def __init__(self, S: str = ""):
        self.S = S + self._get_unsed_char(S)
        self._construct()


    def _construct(self):
        m = len(S)
        self.root = SuffixNode(children={self.S[0]: SuffixNode(self.S[0])})
        
        for i in range(1, m):
            # begin phase i + 1
            for j in range(i + 1)
                '''
                    
                Follow the path from the root labeled S[j], ..., S[i] and, if 
                needed, extend it by adding character S[i + 1]

                '''
                curr_node = self.root
                parent_node = None
                offset = 0
                at_node = True
                prefix = S[j: i + 1]
                for p, k in enumerate(prefix):
                    if at_node:
                        if p not in curr_node.children:
                            raise SomethingWentWrong("Failed to find character in \
                                                      tree. This shouldn't happen.")
                        at_node = False
                        parent_node = curr_node
                        curr_node = curr_node.children[p]
                        offset += 1
                    else:
                        if offset == len(curr_node.parent_label):
                            offset = 0
                            at_node = True
                        elif p == curr_node.parent_label[offset]:
                            offset += 1
                        else:
                            raise SomethingWentWrong("Failed to find character in \
                                                      tree. This shouldn't happen.")
                if at_node:
                    if len(curr_node.children) == 0:
                        # Rule 1
                        pass
                    else:
                        if S[i + 1] in curr_node.children:
                            # Rule 3
                            pass
                        else:
                            # Rule 2
                            pass
                else:
                    if S[i + 1] == curr_node.parent_label[offset]:
                        # Rule 3
                        pass
                    else:
                        # Rule 2
                        pass
                        



    def follow_path(self, P: str):
        '''
            Takes a pattern string P, and returns:
                1. None, if P is already in the tree
                2. (node, offset), if P ends in the middle 
                3. (node, None), if P ends at a leaf
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
            

class SuffixNode(SuffixDef):
    def __init__(self, parent_label: str = '', children: Dict[str, SuffixNode] = {}):
        self.parent_label = parent_label
        self.children = children
        

class SomethingWentWrong(Exception):
    pass