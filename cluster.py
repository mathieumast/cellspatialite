import math

class Cell:
    def __init__(self, q, r, s):
        self.q = int(round(q)) # q position
        self.r = int(round(r)) # r position
        self.level = int(round(s)) # level (11: world scale, 3: local scale)
        
    def __eq__(self, other):
        return self.q == other.q and self.r == other.r and self.level == other.level

    def __hash__(self):
        return hash(self.q, self.r, self.level)

    def __str__(self):
        return 'Cell(q=%s, r=%s, level=%s)' % (self.q, self.r, self.level)

    def neighbors(self):
        '''return neighbors'''
        return [Cell(self.q + 1, self.r, self.level), Cell(self.q + 1, self.r-1, self.level), Cell(self.q, self.r - 1, self.level),
        Cell(self.q - 1, self.r, self.level), Cell(self.q - 1, self.r + 1, self.level), Cell(self.q, self.r + 1, self.level)]

    def corners(self):
        '''return corners in 3857'''
        center = self.center()
        res = []
        for i in range(0, 6):
            rad = (30.0 + 60.0 * i) * math.pi / 180.0
            s = 15 * math.pow(3, self.level)
            res.append(Pos(math.cos(rad) * s + center.x, math.sin(rad) * s + center.y))
        return res

    def center(self):
        '''return center in 3857'''
        s = 15 * math.pow(3, self.level)
        x = math.sqrt(3.0) *s * (self.q + (0.5 * self.r))
        y = 1.5 * s * self.r
        return Pos(x, y)
    
    def wkt(self):
        '''return wkt in 3857'''
        strs = []
        corners = self.corners()
        for corner in corners:
            if len(strs) == 0:
                strs.append('POLYGON((')
            strs.append(str(round(corner.x, 7)))
            strs.append(' ')
            strs.append(str(round(corner.y, 7)))
            strs.append(', ')
        strs.append(str(round(corners[0].x, 7)))
        strs.append(' ')
        strs.append(str(round(corners[0].y, 7)))
        strs.append('))')
        return ''.join(strs)

class Pos:
    def __init__(self, x, y):
        self.x = float(x) # x in 3857
        self.y = float(y) # y in 3857
        
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash(self.x, self.y)

    def __str__(self):
        return 'Pos(x=%s, y=%s)' % (self.x, self.y)

    def cell(self, level):
        '''return cell'''
        s = 15 * math.pow(3, level)
        q = ((self.x * math.sqrt(3.0) / 3.0) - (self.y / 3.0)) / s
        r = (self.y * 2.0 / 3.0) / s
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
        return Cell(rtx, rtz, level)
