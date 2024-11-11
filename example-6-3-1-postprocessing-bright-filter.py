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
from geometry.rectangle import RectangleGeometry
from geometry.sphere import SphereGeometry
from material.texture import TextureMaterial
from extras.movement_rig import MovementRig
from extras.postprocessor import Postprocessor
from effects.bright_filter import BrightFilterEffect


class Example(Base):
    """
    Demostrar un efecto de filtro brillante
    """
    def initialize(self):
        print("Inicializando programa...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([0, 1, 4])
        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(texture=Texture(file_name="images/sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)

        grass_geometry = RectangleGeometry(width=100, height=100)
        grass_material = TextureMaterial(
            texture=Texture(file_name="images/grass.jpg"),
            property_dict={"repeatUV": [50, 50]}
        )
        grass = Mesh(grass_geometry, grass_material)
        grass.rotate_x(-math.pi/2)
        self.scene.add(grass)

        sphere_geometry = SphereGeometry()
        sphere_material = TextureMaterial(Texture("images/grid.jpg"))
        self.sphere = Mesh(sphere_geometry, sphere_material)
        self.sphere.set_position([0, 1, 0])
        self.scene.add(self.sphere)

        self.postprocessor = Postprocessor(self.renderer, self.scene, self.camera)
        self.postprocessor.add_effect(BrightFilterEffect())

    def update(self):
        self.sphere.rotate_y(0.01337)
        self.rig.update(self.input, self.delta_time)
        self.postprocessor.render()


# Instanciar esta clase y ejecutar el programa
Example(screen_size=[800, 600]).run()
