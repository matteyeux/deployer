import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="my_deployer",
    version="0.0.1",
    author="matteyeux",
    author_email="matteyeux@0day.cool",
    description="An awesome deployment tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/matteyeux/my_deployer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
