from tkinter import *
import tkinter.filedialog
import os
import numpy as np
import math

vertices1 = []
vertices1p = []
vertices2 = []
vertices2p = []
vertices3 = []
vertices3p = []
vertices4 = []
vertices4p = []


class Scene(Frame):

    def __init__(self):
        super().__init__()
        self.initUI()


    def initUI(self):
        self.master.title("Scene")
        self.pack(fill=BOTH, expand=1)

        global canvas
        canvas = Canvas(self)
        onOpen()
        self.display(canvas)


    def display(self, canvas):
        canvas.delete("all")
        for dr in [vertices1p, vertices2p, vertices3p, vertices4p]:
            canvas.create_line(dr[0].x, dr[0].y, dr[1].x, dr[1].y)
            canvas.create_line(dr[1].x, dr[1].y, dr[2].x, dr[2].y)
            canvas.create_line(dr[2].x, dr[2].y, dr[3].x, dr[3].y)
            canvas.create_line(dr[3].x, dr[3].y, dr[0].x, dr[0].y)

            canvas.create_line(dr[5].x, dr[5].y, dr[4].x, dr[4].y)
            canvas.create_line(dr[5].x, dr[5].y, dr[6].x, dr[6].y)
            canvas.create_line(dr[6].x, dr[6].y, dr[7].x, dr[7].y)
            canvas.create_line(dr[4].x, dr[4].y, dr[7].x, dr[7].y)

            canvas.create_line(dr[0].x, dr[0].y, dr[4].x, dr[4].y)
            canvas.create_line(dr[1].x, dr[1].y, dr[5].x, dr[5].y)
            canvas.create_line(dr[2].x, dr[2].y, dr[6].x, dr[6].y)
            canvas.create_line(dr[3].x, dr[3].y, dr[7].x, dr[7].y)

        canvas.pack(fill=BOTH, expand=1)


    def moveto(self, o, direct):
        transform_matrix = np.array(
                [[1, 0, 0, 0], 
                [0, 1, 0, 0], 
                [0, 0, 1, 0], 
                [0, 0, 0, 1]], dtype=float)
        if o == 'x':
            transform_matrix[0, 3] = direct
        else:
            transform_matrix[1, 3] = direct
        for dr, drp in zip([vertices1, vertices2, vertices3, vertices4], [vertices1p, vertices2p, vertices3p, vertices4p]):
            i = 0
            for point in dr:
                origin = np.diag([point.x, point.y, point.z, 1])
                result = np.matmul(transform_matrix, origin)
                point.x = result[0][0] + result[0][3]
                point.y = result[1][1] + result[1][3]
                drp[i] = projection(result[:3])
                i += 1
            for point in dr:
                print(point.x, point.y)    
        self.display(canvas)


    def zoom(self, direct):
        for dr, drp in zip([vertices1, vertices2, vertices3, vertices4], [vertices1p, vertices2p, vertices3p, vertices4p]):
            i = 0
            for point in dr:
                point.x *= direct
                point.y *= direct
                point.z *= direct
                result = np.diag([point.x, point.y, point.z, 1])
                drp[i] = projection(result[:3])
                i += 1
            for point in dr:
                print(point.x, point.y)    
        self.display(canvas)

    
    def turnover(self, o, direct):
        ang = direct * 10 * np.pi / 180
        transform_matrix = np.array(
                [[1, 0, 0, 0], 
                [0, 1, 0, 0], 
                [0, 0, 1, 0], 
                [0, 0, 0, 1]], dtype=float)
        if o == 'x':
            transform_matrix[1:3, 1:3] = np.array([
                [math.cos(ang), -math.sin(ang)],
                [math.sin(ang), math.cos(ang)]
            ])
        else:
            transform_matrix[0:3, 0:3] = np.array([
                [math.cos(ang), 0, math.sin(ang)],
                [0, 1, 0],
                [-math.sin(ang), 0, math.cos(ang)]
            ])

        
        for dr, drp in zip([vertices1, vertices2, vertices3, vertices4], [vertices1p, vertices2p, vertices3p, vertices4p]):
            i = 0
            for point in dr:
                origin = np.diag([point.x, point.y, point.z, 1])
                result = np.matmul(transform_matrix, origin)
                point.x = result[0][0] + result[0][2]
                point.y = result[1][1] + result[1][2]
                point.z = result[2][2] + result[2][0] + result[2][1]
                drp[i] = basic_projection(point)
                i += 1
            for point in dr:
                print(point.x, point.y)    
        self.display(canvas)



class point (object):

   def __init__(self, x, y, z):
      self.x = x
      self.y = y
      self.z = z


class point2d (object):

   def __init__(self, x, y):
      self.x = x
      self.y = y



def onOpen():
    ftypes = [('Text files', '*.txt')]
    dir = '.'
    path = "coords.txt"
    global line_no, n
    line_no = 0
    n = 0
    try:
        f = open(path, 'r') 
        stat = os.stat(path)
        if os.stat(path).st_size == 0:
            return "File is empty!"
        for line in f:
            verify_line(line)
            line_no += 1
            line = line.replace("\n", "")
            if line.find("#") != 0:
                if n == 1:
                    line = line.split(" | ")
                    if len(line) != 3:
                        return "Invalid arguments' amount. Exception occured in line " + str(line_no)
                    p = point(int(line[0]), int(line[1]), int(line[2]))
                    p2 = basic_projection(p)
                    vertices1.append(p)
                    vertices1p.append(p2)
                if n == 2:
                    line = line.split(" | ")
                    if len(line) != 3:
                        return "Invalid arguments' amount. Exception occured in line " + str(line_no)
                    p = point(int(line[0]), int(line[1]), int(line[2]))
                    p2 = basic_projection(p)
                    vertices2.append(p)
                    vertices2p.append(p2)
                if n == 3:
                    line = line.split(" | ")
                    if len(line) != 3:
                        return "Invalid arguments' amount. Exception occured in line " + str(line_no)
                    p = point(int(line[0]), int(line[1]), int(line[2]))
                    p2 = basic_projection(p)
                    vertices3.append(p)
                    vertices3p.append(p2)
                if n == 4:
                    line = line.split(" | ")
                    if len(line) != 3:
                        return "Invalid arguments' amount. Exception occured in line " + str(line_no)
                    p = point(int(line[0]), int(line[1]), int(line[2]))
                    p2 = basic_projection(p)
                    vertices4.append(p)
                    vertices4p.append(p2)

        if n<4:
            return "Minimum amount of cubes is not reached."
    except (OSError, FileNotFoundError):
        return "Could not find/read file:" + str(path)


def basic_projection(p):
    p2 = point2d(0, 0)
    F = -10
    r = 1/F
    p2.x = p.x / (r * p.z + 1)
    p2.y = p.y / (r * p.z + 1)
    return p2


def projection(matrix):
    p2 = point2d(0, 0)
    F = -10
    r = 1/F
    p2.x = (matrix[0][0] / (r * matrix[2][2] + 1)) + matrix[0][3]
    p2.y = (matrix[1][1] / (r * matrix[2][2] + 1)) + matrix[1][3]
    return p2


def verify_line(line):
    global n
    if line.find("#") == 0:
        n += 1


def key_pressed(event):
    tk.bind('<Up>', lambda event, o = 'y', direct = 1: sc.moveto(o, direct))
    tk.bind('<Down>', lambda event, o = 'y', direct = -1: sc.moveto(o, direct))
    tk.bind('<Left>', lambda event, o = 'x', direct = 1: sc.moveto(o, direct))
    tk.bind('<Right>', lambda event, o = 'x', direct = -1: sc.moveto(o, direct))
    tk.bind('<0>', lambda event, direct = 1.1: sc.zoom(direct))
    tk.bind('<minus>', lambda event, direct = 0.9: sc.zoom(direct))
    tk.bind('<Shift_L>', lambda event, o = 'x', direct = -1: sc.turnover(o, direct))
    tk.bind('<Shift_R>', lambda event, o = 'x', direct = 1: sc.turnover(o, direct))
    tk.bind('<Alt_L>', lambda event, o = 'y', direct = 1: sc.turnover(o, direct))
    tk.bind('<Alt_R>', lambda event, o = 'y', direct = -1: sc.turnover(o, direct))
    tk.bind('<Escape>', exit)


global sc    
tk = Tk()
sc = Scene()
tk.geometry("700x550")
tk.bind('<Key>', lambda i : key_pressed(i))
   
tk.mainloop()