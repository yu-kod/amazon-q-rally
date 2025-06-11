from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="amazon-q-rally",
    version="1.0.0",
    author="Amazon Q Rally Team",
    description="A realistic rally racing game built with Python and Pygame",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/amazon-q-rally",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Racing",
        "Topic :: Games/Entertainment :: Simulation",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "amazon-q-rally=main:main",
        ],
    },
    keywords="game, racing, rally, pygame, simulation, car, physics",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/amazon-q-rally/issues",
        "Source": "https://github.com/yourusername/amazon-q-rally",
    },
)
