from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="reachy2-code-generation",
    version="1.0.2",
    author="Simon Revelly",
    author_email="contact@pollen-robotics.com",
    description="A code generation interface for the Reachy 2 robot",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/revelsi/reachy2_code_generation",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Human Machine Interfaces",
    ],
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "reachy2-gradio=launch_code_gen:main",
        ],
    },
) 