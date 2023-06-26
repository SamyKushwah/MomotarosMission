from setuptools import setup
from setuptools import find_packages

setup(
    name="momotaro",  # Name of the PyPI package
    version="0.1",
    packages=find_packages(),
    url="https://github.com/SamyKushwah/MomotarosMission",
    #license="GPL 3",
    author="Jessica Halvorsen, Shawn Rhoads, Kevin Chen, Ruhi Reddi, Samradhi Kushwah",
    # author_email="jjb@eng.ufl.edu",
    description="A platformer inspired by Momotaro's story",
    install_requires=["pygame"],
    entry_points=
    {"console_scripts":
        [
            "play_momotaro = momotaro.drivers.main:main",
        ]
    },
    package_data={
      'momotaro': ['images/backgrounds/*.png', 'images/DemonSprites/*.png', 'images/game_ui/*.png','images/level_1/*.png','images/level_select_scene_UI/*.png','images/lose_screen/*.png','images/MomotaroSprites/*.png','images/ObstacleButtonSprites/*.png','images/pause_screen/*.png','images/player2/*.png','images/tiles/*.png','images/tiles/stone/*.png','images/title_screen_scene_UI/*.png','images/win_screen/*.png','save_data/game_data','drivers/snapitc.ttf'],
   },
)