import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="eth-blocky",
    version="0.2.3",
    author="Milan Keca",
    author_email="vonum.mk@gmail.com",
    description="Ethereum utilities for mapping blocks to timestamps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vonum/eth-blocky",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "web3==^6.4.0",
        "arrow==^1.2.3"
    ]
)
