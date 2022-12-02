import os


def run(cmd):
    ret = os.system(cmd)
    if ret != 0:
        raise Exception(f"Failed cmd: {cmd}")


def load(f):
    return open(f, "r").read()


def export_pkgs(pkgs):
    for pkg in pkgs:
        name, version = pkg.split("/")
        run(f"conan export recipes/{name}/all {version}@")

def build_pkgs(pkgs):
    profiles = os.listdir("myprofiles")
    for pkg in pkgs:
        name, version = pkg.split("/")
        for profile in profiles:
            run(f"conan install {name}/{version}@ -pr=myprofiles/{profile} --build=missing")


run("conan config install https://github.com/conan-io/hooks.git -sf hooks -tf hooks")
run("conan config set hooks.conan-center")



pkgs = load("mypkgs.list").splitlines()
export_pkgs(pkgs)
build_pkgs(pkgs)
run("conan search *")
remote = os.getenv('MYREMOTE')
if remote is None:
    raise Exception("Define env-var MYREMOTE with your remote name")
run(f"conan upload * -r={remote} --all -c")
run("conan remove * -f")