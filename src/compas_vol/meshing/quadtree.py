from math import sqrt
from compas.geometry import Point


class Quadtree(object):
    sq2 = sqrt(2.0)
    sq3 = sqrt(3.0)

    def __init__(self):
        self._p = Point(0, 0, 0)
        self._ws = 100.0  # world size
        self._ml = 4      # max levels
        self._rn = QuadNode(0, 0, 0, self._ws, 0, 1, 1)
        self._o = None
        self.leafs = []
    
    def divide(self, node):
        d = self._o.get_distance(node._p)
        node.distance = d
        
        if node.level < self._ml:            
            if abs(d) < Quadtree.sq2 * node._el/2.0:
                node.divide_node()
                # node.orient()
      
                for b in node._branches:
                    self.divide(b)
            else:
                node.divide_node()
                # node.orient()

                self.leafs.append(node)
                    
        else:
            # if abs(node.distance) < Quadtree.sq2 * node._el/2.0:
            node.divide_node()
            # node.orient()

            self.leafs.append(node)


class QuadNode(object):
    def __init__(self, x, y, z, e, l, branch_index, orientation):
        self._p = Point(x, y, z)
        self._el = e
        self._l = l
        self._branches = None
        self.distance = 0.0
        self.branch_index = branch_index
        self.orientation = orientation
        self.direction = 0
    
    @property
    def level(self):
        return self._l

    @level.setter
    def level(self, l):
        self._l = float(l)
    
    def divide_node(self):
        self._branches = []
        qs = self._el/4.0
        nl = self.level + 1

        if self.orientation == 1:
            self._branches.append(QuadNode(self._p.x-qs, self._p.y-qs, 0, qs*2, nl, 0, (self.orientation-1)%4))
            self._branches.append(QuadNode(self._p.x-qs, self._p.y+qs, 0, qs*2, nl, 1, self.orientation%4))
            self._branches.append(QuadNode(self._p.x+qs, self._p.y+qs, 0, qs*2, nl, 2, self.orientation%4))
            self._branches.append(QuadNode(self._p.x+qs, self._p.y-qs, 0, qs*2, nl, 3, (self.orientation+1)%4))
        elif self.orientation == 0:
            self._branches.append(QuadNode(self._p.x-qs, self._p.y-qs, 0, qs*2, nl, 0, (self.orientation-1)%4))
            self._branches.append(QuadNode(self._p.x+qs, self._p.y-qs, 0, qs*2, nl, 3, self.orientation%4))         
            self._branches.append(QuadNode(self._p.x+qs, self._p.y+qs, 0, qs*2, nl, 2, self.orientation%4))
            self._branches.append(QuadNode(self._p.x-qs, self._p.y+qs, 0, qs*2, nl, 1, (self.orientation+1)%4))      
        elif self.orientation == 2:
            self._branches.append(QuadNode(self._p.x+qs, self._p.y+qs, 0, qs*2, nl, 2, (self.orientation-1)%4))
            self._branches.append(QuadNode(self._p.x-qs, self._p.y+qs, 0, qs*2, nl, 1, self.orientation%4))
            self._branches.append(QuadNode(self._p.x-qs, self._p.y-qs, 0, qs*2, nl, 0, self.orientation%4))
            self._branches.append(QuadNode(self._p.x+qs, self._p.y-qs, 0, qs*2, nl, 3, (self.orientation+1)%4))                     
        elif self.orientation == 3:
            self._branches.append(QuadNode(self._p.x-qs, self._p.y+qs, 0, qs*2, nl, 1, (self.orientation-1)%4))
            self._branches.append(QuadNode(self._p.x-qs, self._p.y-qs, 0, qs*2, nl, 0, self.orientation%4))
            self._branches.append(QuadNode(self._p.x+qs, self._p.y-qs, 0, qs*2, nl, 3, self.orientation%4))
            self._branches.append(QuadNode(self._p.x+qs, self._p.y+qs, 0, qs*2, nl, 2, (self.orientation+1)%4))
            

    def shift_branches(self, n):
        self._branches = self._branches[n:] + self._branches[:n]
        for i, branch in enumerate(self._branches):
                branch.branch_index = i

    def reverse_branches(self):
        self._branches = self._branches[::-1]
    
    def orient(self):
        if self.orientation == 1:
            pass
        elif self.orientation == 0:
            self.shift_branches(1)
            self.reverse_branches()
        elif self.orientation == 2:
            self.shift_branches(-1)
            self.reverse_branches()
        elif self.orientation == 3:
            self.shift_branches(2)



        # if self.orientation == 0:
        #     self.shift_branches(1)
        #     self.reverse_branches()
        #     self.direction = -1
        # elif self.orientation == 3:
        #     self.shift_branches(-1)
        #     self.reverse_branches()
        #     self.direction = -1

        # if self.branch_index == 0:
        #     if self.direction == -1:
        #         self.reverse_branches()
        #         self.shift_branches(1)
        #     else:
        #         self.shift_branches(1)
        #         self.reverse_branches()

        # elif self.branch_index == 3:
        #     if self.direction == -1:
        #         self.reverse_branches()
        #         self.shift_branches(-1)
        #     else:
        #         self.shift_branches(-1)
        #         self.reverse_branches()


# ==============================================================================
# Main
# ==============================================================================

if __name__ == "__main__":
    pass
