"""
Setup script for E5052B driver.
"""

from setuptools import setup, find_packages

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="e5052b-driver",
    install_requires=required,
    packages=find_packages(),
    # entry_points={
    #     "console_scripts": [
    #         "aqctl_artiq_ablation_camera = artiq_ablation_camera.aqctl_artiq_ablation_camera:main",
    #     ],
    # },
)
