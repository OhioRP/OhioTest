#!/bin/env python3

from subprocess import run
from shutil import rmtree, copytree, copy
from sys import exit
from os import unlink
from os.path import isdir, isfile

CLONE_URL = "https://github.com/minetest/minetest"
# CLONE_URL = "https://github.com/rollerozxa/rollertest"

if __name__ == "__main__":
    print("[INFO] Downloading minetest...")
    if not isdir("minetest"):
        if isfile("minetest"):
            print("[ERROR] Path `minetest` exists and is a file")
            exit(1)
        run(["git", "clone", "--depth=1",
             CLONE_URL, "minetest"])
    else:
        print("[WARN] `./minetest` already exists, not redownloading...")

    print("[INFO] Patching `minetest/builtin`")
    rmtree("./minetest/builtin")
    copytree("./builtin", "./minetest/builtin")

    print("[INFO] Patching `minetest/src/defaultsettings.cpp`")
    unlink("./minetest/src/defaultsettings.cpp")
    copy("./src/defaultsettings.cpp", "./minetest/src/defaultsettings.cpp")

    print("[INFO] Downloading OhioCraft...")
    ohiocraft_path = "./minetest/games/ohiocraft"
    if not isdir("./ohiocraft"):
        run(["git", "clone", "https://github.com/OhioRP/OhioCraft",
             "./ohiocraft"])
        run(["bash", "./build.sh"], cwd="./ohiocraft")
    else:
        print(f"[WARN] `{ohiocraft_path}` already exists, not redownloading...")
    if isdir(ohiocraft_path):
        rmtree(ohiocraft_path)
    copytree("./ohiocraft/Build", ohiocraft_path)

    irrlicht_path = "./minetest/lib/irrlichtmt"
    print("[INFO] Downloading Irrlicht...")
    if not isdir(irrlicht_path):
        run(["git", "clone", "https://github.com/minetest/irrlicht",
             irrlicht_path])
    else:
        print(f"[WARN] `{irrlicht_path}` already exists, not redownloading...")

    if isdir("./minetest/games/devtest"):
        print("[INFO] Removing `minetest/games/devtest`...")
        rmtree("./minetest/games/devtest")

    print("[INFO] Patching `minetest/util/buildbot/common.sh`")
    unlink("./minetest/util/buildbot/common.sh")
    copy("./util/buildbot/common.sh", "./minetest/util/buildbot/common.sh")

    print("\033[1;32mDONE! Now you can compile minetest in the" +
          " `./minetest` directory by following the instructions in" +
          f" `{CLONE_URL}`\033[m")
