import os

from setuptools import find_packages, setup

metadata_keys = ["author", "author_email", "version"]
package = "cvCreator"


with open(os.path.join(package, "__metadata__.py"), "r") as file:
    exec(file.read())

metadata = {mdk: eval("__" + mdk + "__") for mdk in metadata_keys}

setup(
    packages=find_packages(), **metadata, name="cvCreator",
)
