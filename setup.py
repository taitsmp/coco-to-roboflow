from setuptools import setup, find_packages

setup(
    name="coco-to-roboflow",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'coco-to-roboflow=coco_to_roboflow.coco_to_roboflow:main',
        ],
    },
    install_requires=[],
    python_requires=">=3.6",
    author="",
    author_email="",
    description="Convert COCO format datasets to Roboflow format",
    keywords="coco, roboflow, dataset, conversion",
    url="",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
