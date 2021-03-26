import os

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration


required_conan_version = ">=1.33.0"


class NanaConan(ConanFile):
    name = "nana"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/cnjinhao/nana"
    topics = ("gui", "conan")
    license = "BSL-1.0 License"
    description = "Nana is a C++ standard-like GUI library designed to allow developers to easily create cross-platform GUI applications"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    generators = "cmake"

    exports_sources = "CMakeLists.txt", "patches/**"

    def requirements(self):
        if self.settings.os == "Linux":
            self.requires("xorg/system")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.options.shared:
            del self.options.fPIC

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename("nana-" + self.version, self._source_subfolder)

    def _patch_sources(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)

    def build(self):
        self._patch_sources()
        cmake = CMake(self)
        if self.settings.compiler == "Visual Studio":
            rt = "ON" if "MT" in str(self.settings.compiler.runtime)  else "OFF"
            cmake.definitions["MSVC_USE_STATIC_RUNTIME"] = rt
        cmake.configure(build_folder=self._build_subfolder)
        cmake.build()

    def package(self):
        self.copy("*", src=os.path.join(self._source_subfolder, "include"), dst="include")
        self.copy("*.lib", src=os.path.join(self._build_subfolder, "lib"), dst="lib")
        self.copy("*.a", src=os.path.join(self._build_subfolder, "lib"), dst="lib")
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses", keep_path=False)

    def package_info(self):

        self.cpp_info.libs = ["nana"]
