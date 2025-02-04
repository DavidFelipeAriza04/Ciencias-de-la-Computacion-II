from manim import *
import numpy as np
from Main import Init

class InteractiveRadious(ThreeDScene):
    def construct(self):
        init = Init()
        # Punto interactivo
        cursor_dot = Dot3D().move_to([3, 2, 0])  # Usar Dot3D para puntos en 3D

        # Crear puntos en el espacio para el plano XY
        '''
        points = [
            [x, y, z]  # Fijamos z en 1 para trazar solo en XY
            for x in range(1, 6)
            for y in range(1, 6)
            for z in range(1,6)
        ]
        '''

        print(init.salones)

        #Obtener ID
        name_classrooms = [str(classroom.id) for classroom in init.salones]
        print(name_classrooms)
        points = []

        z_value = 0
        x_value = 0
        y_value = 0
        index = 0
        for name_classroom in name_classrooms:
            if z_value == int(name_classroom[0])-1:
                print(index)
                x_value = index // 2
                y_value = index % 2
            else:
                z_value = int(name_classroom[0]) -1
                x_value = 0
                y_value = 0
                index=0
            points.append([x_value,y_value,z_value])
            index+=1

        # Crear puntos visi.bles
        dots = VGroup(*[Dot3D(point=point, color=YELLOW) for point in points])
        lines = VGroup(*[
            Line3D(start=points[i], end=points[i + 1], color=RED)
            for i in range(len(points) - 1)
            if (i + 1) % 5 != 0  # Evitar salto entre bloques de X
        ])
        '''
        # Crear líneas en el eje X (mismo Y, Z)
        lines_x = VGroup(*[
            Line3D(start=points[i], end=points[i + 1], color=RED)
            for i in range(len(points) - 1)
            if (i + 1) % 5 != 0  # Evitar salto entre bloques de X
        ])

        # Crear líneas en el eje Y (mismo X, Z)
        lines_y = VGroup(*[
            Line3D(start=points[i], end=points[i + 5], color=GREEN)
            for i in range(len(points) - 5)
            if (i + 5) % 25 >= 5  # Evitar conexión entre bloques de Y
        ])

        # Crear líneas en el eje Z (mismo X, Y)
        lines_z = VGroup(*[
            Line3D(start=points[i], end=points[i + 25], color=BLUE)
            for i in range(len(points) - 25)
        ])

        # Añadir ejes, círculo, punto y esferas
        self.add(cursor_dot, dots,lines_x,lines_y,lines_z)
        '''
        self.add(cursor_dot, dots)
        # Ajustar cámara 3D
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        self.cursor_dot = cursor_dot

        self.interactive_embed()

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        if symbol == pyglet_key.G:
            self.play(
                self.cursor_dot.animate.move_to(self.mouse_point.get_center())
            )
        super().on_key_press(symbol, modifiers)