import os

from conans import ConanFile, CMake, tools
from conans.errors import ConanInvalidConfiguration


required_conan_version = ">=1.33.0"


class NanaConan(ConanFile):
    name = "nana"
    url = "https://github.com/conan-io/conan-center-index"
    homepage = "https://github.com/cnjinhao/nana"
    topics = ("entity", "conan")
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

    exports_sources = "CMakeLists.txt"

    _cmake = None

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


    def _configure_cmake(self):
        if self._cmake:
            return self._cmake
        self._cmake = CMake(self)
        self._cmake.definitions["NANA_CMAKE_STD_FILESYSTEM_FORCE"] = "ON"
        if self.settings.compiler == "Visual Studio":
            rt = "ON" if "MT" in str(self.settings.compiler.runtime)  else "OFF"
            self._cmake.definitions["MSVC_USE_STATIC_RUNTIME"] = rt
        self._cmake.configure(build_folder=self._build_subfolder)
        return self._cmake

    def build(self):
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        cmake = self._configure_cmake()
        cmake.install()
        self.copy("LICENSE", src=self._source_subfolder, dst="licenses", keep_path=False)

    def package_info(self):
        debug = "-d" if self.settings.build_type == "Debug" else ""
        self.cpp_info.libs = ["nana"]
