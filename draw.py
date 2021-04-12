from display import *
from matrix import *
import math

def add_circle( points, cx, cy, cz, r, step ):
    
    x_param = lambda t: r * math.cos(t) + cx
    y_param = lambda t: r * math.sin(t) + cy
    for t in range(0, 100, int(step * 100)):
        adj_t = t * step
        theta = adj_t * 2 * math.pi
        theta_next = (adj_t + step) * 2 * math.pi
        x0 = x_param(theta)
        y0 = y_param(theta)
        x1 = x_param(theta_next)
        y1 = y_param(theta_next)
        z0, z1 = cz,cz
        add_edge(points, x0, y0, z0, x1, y1, z1)

def add_hermite(matrix, x0, y0, x1, y1, rx0, ry0, rx1, ry1, step):
    a_x = (2*x0) - (2*x1) + rx0 + rx1
    a_y = (2*y0) - (2*y1) + ry0 + ry1
    b_x = (-3 * x0) + (3*x1) - (2 * rx0) - rx1
    b_y = (-3 * y0) + (3*y1) - (2 * ry0) - ry1
    c_x = rx0
    c_y = ry0
    d_x = x0
    d_y = y0
    x_param = lambda t: (a_x * (t ** 3)) + (b_x * (t ** 2)) + (c_x * t) + d_x
    y_param = lambda t: (a_y * (t ** 3)) + (b_y * (t ** 2)) + (c_y * t) + d_y
    for t in range(0, 100, int(step * 100)):
        adj_t = t * step
        x0 = x_param(adj_t)
        y0 = y_param(adj_t)
        x1 = x_param(adj_t + step)
        y1 = y_param(adj_t + step)
        z0, z1 = 0, 0
        add_edge(matrix, x0, y0, z0, x1, y1, z1)

def add_bezier(matrix, x0, y0, x1, y1, x2, y2, x3, y3, step):
    a_x = -x0 + (3*x1) - (3*x2) + x3
    a_y = -y0 + (3*y1) - (3*y2) + y3
    b_x = (3*x0) - (6*x1) + (3*x2)
    b_y = (3*y0) - (6*y1) + (3*y2)
    c_x = (-3*x0) + (3*x1)
    c_y = (-3*y0) + (3*y1)
    d_x = x0
    d_y = y0
    x_param = lambda t: (a_x * (t ** 3)) + (b_x * (t ** 2)) + (c_x * t) + d_x
    y_param = lambda t: (a_y * (t ** 3)) + (b_y * (t ** 2)) + (c_y * t) + d_y
    for t in range(0, 100, int(step * 100)):
        adj_t = t * step
        x0 = x_param(adj_t)
        y0 = y_param(adj_t)
        x1 = x_param(adj_t + step)
        y1 = y_param(adj_t + step)
        z0, z1 = 0, 0
        add_edge(matrix, x0, y0, z0, x1, y1, z1)

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):
    if curve_type == "bezier":
        add_bezier(points, x0, y0, x1, y1, x2, y2, x3, y3, step)
    elif curve_type == "hermite":
        add_hermite(points, x0, y0, x1, y1, x2, y2, x3, y3, step)
    else:
        print(f"unsupported curve type: {curve_type}")


def draw_lines( matrix, screen, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   screen, color)    
        point+= 2
        
def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)
    
def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )
    



def draw_line( x0, y0, x1, y1, screen, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        x0 = x1
        y0 = y1
        x1 = xt
        y1 = yt

    x = x0
    y = y0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)

    #octants 1 and 8
    if ( abs(x1-x0) >= abs(y1 - y0) ):

        #octant 1
        if A > 0:            
            d = A + B/2

            while x < x1:
                plot(screen, color, x, y)
                if d > 0:
                    y+= 1
                    d+= B
                x+= 1
                d+= A
            #end octant 1 while
            plot(screen, color, x1, y1)
        #end octant 1

        #octant 8
        else:
            d = A - B/2

            while x < x1:
                plot(screen, color, x, y)
                if d < 0:
                    y-= 1
                    d-= B
                x+= 1
                d+= A
            #end octant 8 while
            plot(screen, color, x1, y1)
        #end octant 8
    #end octants 1 and 8

    #octants 2 and 7
    else:
        #octant 2
        if A > 0:
            d = A/2 + B

            while y < y1:
                plot(screen, color, x, y)
                if d < 0:
                    x+= 1
                    d+= A
                y+= 1
                d+= B
            #end octant 2 while
            plot(screen, color, x1, y1)
        #end octant 2

        #octant 7
        else:
            d = A/2 - B;

            while y > y1:
                plot(screen, color, x, y)
                if d > 0:
                    x+= 1
                    d+= A
                y-= 1
                d-= B
            #end octant 7 while
            plot(screen, color, x1, y1)
        #end octant 7
    #end octants 2 and 7
#end draw_line
