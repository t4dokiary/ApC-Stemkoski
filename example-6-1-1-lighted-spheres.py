#!/usr/bin/python3
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
from extras.movement_rig import MovementRig
from geometry.sphere import SphereGeometry
from light.ambient import AmbientLight
from light.directional import DirectionalLight
from light.point import PointLight
from material.flat import FlatMaterial
from material.lambert import LambertMaterial
from material.phong import PhongMaterial


class Example(Base):
    """
    Demostrar:
    - el modelo de sombreado plano;
    - el modelo de iluminación de Lambert y el modelo de sombreado de Phong;
    - el modelo de iluminación de Phong y el modelo de sombreado de Phong.
    El modelo de iluminación de Lambert utiliza una combinación de iluminación ambiental y difusa.
    El modelo de iluminación de Phong utiliza iluminación ambiental, difusa y especular.
    En el modelo de sombreado plano, los cálculos de luz se realizan en el shader de vértices.
    En el modelo de sombreado de Phong, los cálculos de luz se realizan en el shader de fragmentos.

    Mover una cámara: WASDRF(mover), QE(girar), TG(mirar).
    """
    def initialize(self):
        print("Inicializando el programa...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.rig.set_position([0, 0, 6])
        self.scene.add(self.rig)

        # cuatro fuentes de luz
        ambient_light = AmbientLight(color=[0.1, 0.1, 0.1])
        self.scene.add(ambient_light)
        directional_light = DirectionalLight(color=[0.8, 0.8, 0.8], direction=[-1, -1, -2])
        self.scene.add(directional_light)
        point_light1 = PointLight(color=[0.9, 0, 0], position=[4, 0, 0])
        self.scene.add(point_light1)
        point_light2 = PointLight(color=[0, 0.9, 0], position=[-4, 0, 0])
        self.scene.add(point_light2)

        # materiales iluminados con un color
        flat_material = FlatMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=4
        )
        lambert_material = LambertMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=4
        )
        phong_material = PhongMaterial(
            property_dict={"baseColor": [0.2, 0.5, 0.5]},
            number_of_light_sources=4
        )

        # esferas iluminadas con un color
        sphere_geometry = SphereGeometry()
        sphere_left_top = Mesh(sphere_geometry, flat_material)
        sphere_left_top.set_position([-2.5, 1.5, 0])
        self.scene.add(sphere_left_top)
        sphere_center_top = Mesh(sphere_geometry, lambert_material)
        sphere_center_top.set_position([0, 1.5, 0])
        self.scene.add(sphere_center_top)
        sphere_right_top = Mesh(sphere_geometry, phong_material)
        sphere_right_top.set_position([2.5, 1.5, 0])
        self.scene.add(sphere_right_top)

        # materiales iluminados con una textura
        textured_flat_material = FlatMaterial(
            texture=Texture("images/grid.jpg"),
            number_of_light_sources=4
        )
        textured_lambert_material = LambertMaterial(
            texture=Texture("images/grid.jpg"),
            number_of_light_sources=4
        )
        textured_phong_material = PhongMaterial(
            texture=Texture("images/grid.jpg"),
            number_of_light_sources=4
        )

        # esferas iluminadas con una textura
        sphere_left_bottom = Mesh(sphere_geometry, textured_flat_material)
        sphere_left_bottom.set_position([-2.5, -1.5, 0])
        self.scene.add(sphere_left_bottom)
        sphere_center_bottom = Mesh(sphere_geometry, textured_lambert_material)
        sphere_center_bottom.set_position([0, -1.5, 0])
        self.scene.add(sphere_center_bottom)
        sphere_right_bottom = Mesh(sphere_geometry, textured_phong_material)
        sphere_right_bottom.set_position([2.5, -1.5, 0])
        self.scene.add(sphere_right_bottom)

    def update(self):
        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)


# Instanciar esta clase y ejecutar el programa
Example(screen_size=[800, 600]).run()
