from cycler.cycler import Cycler

def quadrant(x,y,xBound,yBound):
    """ Returns quadrant of x,y location given an x boundary and
    y boundary
    0-------------x
    |1     |4     |
    |      |cycler|
    |-------------|
    |2     |3     |
    |      |      |
    y-------------.
    """
    if (x < xBound) and (y <= yBound):
        return 1
    elif (x < xBound) and (y > yBound):
        return 2
    elif (x >= xBound) and (y > yBound):
        return 3
    elif (x >= xBound) and (y <= yBound):
        return 4
    else:
        return None #indicates error

def rel_to_abs(loc_prev,loc_now):
    loc_now['relative']=False
    keys = ['x','y','z','a','b']
    for key in keys:
        try:
            loc_now[key] = loc_prev[key] + loc_now[key]
        except KeyError:
            pass
    return loc_now

c = Cycler()
lid = 'open'
xLim = c.bounds['x'][lid]
yLim = c.bounds['y'][lid]

for i in range(1,5):
    print(quadrant(c.quad_nodes[str(i)]['x'],c.quad_nodes[str(i)]['y'],xLim,yLim))

if [3,4] in c.move_between['safe']:
    print('safe')
elif [3,4] in c.move_between['collision']:
    print('collision')
if [3,4] in c.move_between['check_lid']:
    print('lid')

loc_prev = {
    'x' : 30,
    'y' : 20,
    'z' : 10,
    'a' : 20,
    'b' : 32
}

loc_now = {
    'x' : 1,
    'y' : 11,
    'z' : 21,
    'a' : 0,
    'b' : 0
}

print(rel_to_abs(loc_prev,loc_now))

