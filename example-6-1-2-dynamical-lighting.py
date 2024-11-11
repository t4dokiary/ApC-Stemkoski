#!/usr/bin/python3
import math
import pathlib
import sys

# Obtener el directorio del paquete
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Agregar el directorio del paquete a sys.path si es necesario
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from core.base import Base
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.texture import Texture
from extras.directional_light import DirectionalLightHelper
from extras.movement_rig import MovementRig
from extras.point_light import PointLightHelper
from geometry.sphere import SphereGeometry
from light.ambient import AmbientLight
from light.directional import DirectionalLight
from light.point import PointLight
from material.flat import FlatMaterial
from material.lambert import LambertMaterial
from material.phong import PhongMaterial


class Example(Base):
    """
    Demostrar iluminación dinámica con:
    - el modelo de sombreado plano;
    - el modelo de iluminación Lambert y el modelo de sombreado Phong;
    - el modelo de iluminación Phong y el modelo de sombreado Phong;
    y renderizar ayudantes de luz que muestran una posición de luz y
    una dirección de luz para una luz puntual y una luz direccional,
    respectivamente.

    Mover una cámara: WASDRF(mover), QE(girar), TG(mirar).
    """
    def initialize(self):
        print("Inicializando programa...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 0, 6])
        self.scene.add(self.rig)

        # tres fuentes de luz
        ambient_light = AmbientLight(color=[0.1, 0.1, 0.1])
        self.scene.add(ambient_light)
        self.directional_light = DirectionalLight(color=[0.8, 0.8, 0.8], direction=[-1, -1, 0])
        self.scene.add(self.directional_light)
        self.point_light = PointLight(color=[0.9, 0, 0], position=[1, 1, 0.8])
        self.scene.add(self.point_light)

        # materiales iluminados con un color
        flat_material = FlatMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=3
        )
        lambert_material = LambertMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=3
        )
        phong_material = PhongMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=3
        )

        # esferas iluminadas con un color
        sphere_geometry = SphereGeometry()
        sphere_left = Mesh(sphere_geometry, flat_material)
        sphere_left.set_position([-2.5, 0, 0])
        self.scene.add(sphere_left)
        sphere_center = Mesh(sphere_geometry, lambert_material)
        sphere_center.set_position([0, 0, 0])
        self.scene.add(sphere_center)
        sphere_right = Mesh(sphere_geometry, phong_material)
        sphere_right.set_position([2.5, 0, 0])
        self.scene.add(sphere_right)

        # ayudantes
        directional_light_helper = DirectionalLightHelper(self.directional_light)
        # La luz direccional puede tomar cualquier posición porque cubre todo el espacio.
        # El ayudante de luz direccional es un hijo de la luz direccional.
        # Así que cambiar la matriz global del padre lleva a cambiar
        # la matriz global de su hijo.
        self.directional_light.set_position([0, 2, 0])
        self.directional_light.add(directional_light_helper)
        point_light_helper = PointLightHelper(self.point_light)
        self.point_light.add(point_light_helper)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.directional_light.set_direction([-1, math.sin(0.5 * self.time), 0])
        self.point_light.set_position([1, math.sin(self.time), 1])
        self.renderer.render(self.scene, self.camera)


# Instanciar esta clase y ejecutar el programa
Example(screen_size=[800, 600]).run()
