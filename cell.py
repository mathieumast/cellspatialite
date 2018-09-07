import math

class Cell:
    def __init__(self, q, r, s):
        self.q = round(q) # q position
        self.r = round(r) # r position
        self.s = round(s) # size (11: world scale, 3: local scale)
        
    def __eq__(self, other):
        return self.q == other.q and self.r == other.r and self.s == other.s

    def __hash__(self):
        return hash(self.q, self.r, self.s)

    def neighbors(self):
        """return neighbors"""
        return [Cell(self.q + 1, self.r, self.s), Cell(self.q + 1, self.r-1, self.s), Cell(self.q, self.r - 1, self.s),
        Cell(self.q - 1, self.r, self.s), Cell(self.q - 1, self.r + 1, self.s), Cell(self.q, self.r + 1, self.s)]

    def corners(self):
        """return corners in 3857"""
        center = self.center()
        res = []
        for i in range(0, 6):
            rad = (30.0 + 60.0 * i) * math.pi / 180.0
            res.append(Pos(self.s * math.cos(rad) + center.x, self.s * math.sin(rad) + center.y))
        return res

    def center(self):
        """return center in 3857"""
        x = float(self.s) * math.sqrt(3.0) * (float(self.q) + (float(self.r) / 2.0))
        y = float(self.s) * float(self.r) * 3.0 / 2.0
        return Pos(x, y)
    
    def wkt(self):
        """return wkt in 3857"""
        strs = ["POLYGON(("]
        corners = self.corners()
        for corner in corners:
            if len(strs) != 0:
                strs.append(", ")
            else:
                strs.append("POLYGON((")
            strs.append(corner.x)
            strs.append(" ")
            strs.append(corner.y)
        strs.append(corners[0].x)
        strs.append(" ")
        strs.append(corners[0].y)
        strs.append("))")
        return ''.join(strs)

class Pos:
    def __init__(self, x, y):
        self.x = float(x) # x in 3857
        self.y = float(y) # y in 3857
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x, self.y)

    def cell(self, s):
        """return cell"""
        q = (float(self.x) * math.sqrt(3.0) / 3.0 - (float(self.y) / 3.0)) / s
        r = (float(self.y) * 2.0 / 3.0) / s
        tx = q
        ty = -q - r
        tz = r
        rtx = round(tx)
        rty = round(ty)
        rtz = round(tz)
        tx_diff = abs(rtx - tx)
        ty_diff = abs(rty - ty)
        tz_diff = abs(rtz - tz)
        if tx_diff > ty_diff and tx_diff > tz_diff:
            rtx = -rty - rtz
        elif ty_diff > tz_diff:
            rty = -rtx - rtz
        else:
            rtz = -rtx - rty
        return Cell(rtx, rtz, s)
