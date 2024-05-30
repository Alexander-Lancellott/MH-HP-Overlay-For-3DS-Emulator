from setuptools import setup, find_packages

setup(
    name='MH-HP-Overlay-For-3DS-Emulator',
    author='Alexander-Lancellott',
    author_email='alejandrov.lancellotti@gmail.com',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'cursor==1.3.5',
        'PySide6==6.7.1',
        'cx_Freeze==7.1.0',
        'colorama==0.4.6',
        'art==6.2',
        'ahk[binary]==1.7.4'
    ],
    python_requires='>=3.8',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'build = modules.build:main'
        ],
    },
)
