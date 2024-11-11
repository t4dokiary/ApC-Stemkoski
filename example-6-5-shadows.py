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
from core_ext.renderer import Renderer
from core_ext.scene import Scene
from core_ext.camera import Camera
from core_ext.mesh import Mesh
from core_ext.texture import Texture
from light.ambient import AmbientLight
from light.directional import DirectionalLight
from material.phong import PhongMaterial
from material.texture import TextureMaterial
from geometry.rectangle import RectangleGeometry
from geometry.sphere import SphereGeometry
from extras.movement_rig import MovementRig
from extras.directional_light import DirectionalLightHelper


class Example(Base):
    """
    Renderizar sombras usando paso de sombras por buffers de profundidad para la luz direccional.
    """
    def initialize(self):
        self.renderer = Renderer([0.2, 0.2, 0.2])
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 2, 5])

        luz_ambiental = AmbientLight(color=[0.2, 0.2, 0.2])
        self.scene.add(luz_ambiental)
        self.directional_light = DirectionalLight(color=[0.5, 0.5, 0.5], direction=[-1, -1, 0])
        # La luz direccional puede tomar cualquier posición porque cubre todo el espacio.
        # El ayudante de luz direccional es un hijo de la luz direccional.
        # Así que cambiar la matriz global del padre lleva a cambiar
        # la matriz global de su hijo.
        self.directional_light.set_position([2, 4, 0])
        self.scene.add(self.directional_light)
        direct_helper = DirectionalLightHelper(self.directional_light)
        self.directional_light.add(direct_helper)

        esfera_geometría = SphereGeometry()
        material_phong = PhongMaterial(
            texture=Texture("images/grid.jpg"),
            number_of_light_sources=2,
            use_shadow=True
        )

        esfera1 = Mesh(esfera_geometría, material_phong)
        esfera1.set_position([-2, 1, 0])
        self.scene.add(esfera1)

        esfera2 = Mesh(esfera_geometría, material_phong)
        esfera2.set_position([1, 2.2, -0.5])
        self.scene.add(esfera2)

        self.renderer.enable_shadows(self.directional_light)

        """
        # opcional: renderizar textura de profundidad a malla en la escena
        textura_profundidad = self.renderer.shadow_object.render_target.texture
        mostrar_sombra = Mesh(RectangleGeometry(), TextureMaterial(textura_profundidad))
        mostrar_sombra.set_position([-1, 3, 0])
        self.scene.add(mostrar_sombra)
        """

        piso = Mesh(RectangleGeometry(width=20, height=20), material_phong)
        piso.rotate_x(-math.pi / 2)
        self.scene.add(piso)

    def update(self):
        #"""
        # ver sombras dinámicas -- necesita aumentar el rango de la cámara de sombras
        self.directional_light.rotate_y(0.01337, False)
        #"""
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)
        """
        # renderizar escena desde la cámara de sombras
        cámara_sombra = self.renderer.shadow_object.camera
        self.renderer.render(self.scene, cámara_sombra)
        """


# Instanciar esta clase y ejecutar el programa
Example(screen_size=[800, 600]).run()
