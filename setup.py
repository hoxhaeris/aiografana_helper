import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aiografana_helper-hoxhaeris",
    version="0.0.1",
    author="Eris Hoxha",
    author_email="eris.hoxh@gmail.com",
    description="A grafana helper package, for managing the dashboards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hoxhaeris/aiografana_helper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)