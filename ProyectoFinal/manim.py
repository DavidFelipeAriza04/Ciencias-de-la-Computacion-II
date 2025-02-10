from manim import *
import numpy as np
from Main import Init

def obtener_puntos(name_classrooms):
    points = []

    z_value,x_value,y_value,index = 0,0,0,0

    for name_classroom in name_classrooms:
        if z_value == int(name_classroom[0])-1:
            x_value = index // 2
            y_value = index % 2
        else:
            z_value = int(name_classroom[0]) -1
            x_value,y_value,index = 0,0,0
        points.append([x_value,y_value,z_value])
        index+=1
    
    return points

class InteractiveRadious(ThreeDScene):

    def construct(self):
        self.init = Init(3,8) #Piso, #Numero por piso
        update = self.update
        init = self.init
        init.edificio.determinar_habitabilidad()

        classrooms = init.edificio.salones
        surfaces = init.edificio.superficies

        # init.edificio.imprimir_recomendaciones()
        
        # Punto interactivo
        cursor_dot = Dot3D().move_to([3, 2, 0])  # Usar Dot3D para puntos en 3D

        #Obtener ID
        name_classrooms = [str(classroom.id) for classroom in init.salones]
        points = obtener_puntos(name_classrooms)

        # Crear puntos visi.bles
        self.dots = VGroup(*[Dot3D(point=point, color=classrooms[index].habitable) for index,point in enumerate(points)])

        # Crear las etiquetas para los puntos
        labels = VGroup(*[
            Text(f"{name_classrooms[index]}", font_size=13).next_to(point, RIGHT) 
            for index, point in enumerate(points)
        ])

        lines = VGroup()

        for surface in surfaces:
            separate_classrooms = surface.salonesSeparados

            index1 = self.search_position(classrooms,separate_classrooms[0])
            index2 = self.search_position(classrooms,separate_classrooms[1])

            line = Line3D(start=points[index1], end=points[index2], color=surface.material.color)
            lines.add(line)

        self.add(cursor_dot, self.dots,lines,labels)
        #self.add(dots, lines, labels)
        # Ajustar cámara 3D
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
        
        self.cursor_dot = cursor_dot

        self.interactive_embed()

    def update(self, classrooms):
        self.remove(self.dots)
        self.init.edificio._reorganizar_actividades()
        name_classrooms = [str(classroom.id) for classroom in self.init.salones]
        points = obtener_puntos(name_classrooms)

        # Crear puntos visi.bles
        dots = VGroup(*[Dot3D(point=point, color=classrooms[index].habitable) for index,point in enumerate(points)])
        self.add(dots)
        self.init.edificio.imprimir_recomendaciones()
        

    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key as pyglet_key
        if symbol == pyglet_key.G:
            self.play(
                self.cursor_dot.animate.move_to(self.mouse_point.get_center())
            )
        super().on_key_press(symbol, modifiers)

    def search_position(self, classrooms, classroom):
        for index,x in enumerate(classrooms):
            if x == classroom:
                return index
