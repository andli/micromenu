import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="micromenu",
    version="1.1.0",
    py_modules=["micromenu"],
    author="Andreas Ehrlund",
    author_email="a.ehrlund@gmail.com",
    description="A minimalistic command line menu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andli/micromenu",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={"dev": ["wheel", "pytest", "mock", "pytest-cov"],},
)
