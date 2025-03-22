from setuptools import setup, find_packages

setup(
    name="coco-to-roboflow",
    version="0.1.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'coco-to-roboflow=coco_to_roboflow.coco_to_roboflow:main',
        ],
    },
    install_requires=[],
    python_requires=">=3.6",
    author="Tait Larson",
    author_email="taitlarson@gmail.com",
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
