from conan import ConanFile
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout


class GalaxyPocoConan(ConanFile):
    name = "galaxy_poco"
    version = "1.0.0"
    package_type = "library"

    license = "BSL-1.0"
    author = "you"
    description = "Galaxy Poco - Poco C++ libraries packaged for Galaxy project"

    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": True, "fPIC": True}

    exports_sources = "CMakeLists.txt", "cmake/*", "Foundation/*", "Net/*", "XML/*", \
        "JSON/*", "Util/*", "Data/*", "Prometheus/*", "JWT/*", "NetSSL_OpenSSL/*", \
        "Crypto/*", "ActiveRecord/*", "dependencies/*", "libversion", "VERSION", "README", "LICENSE"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def layout(self):
        self.folders.build = "build_conan"
        self.folders.source = "."
        cmake_layout(self)

    def generate(self):
        tc = CMakeToolchain(self)
        tc.variables["ENABLE_ZIP"]="OFF"
        tc.variables["ENABLE_MONGODB"]="OFF"
        tc.variables["ENABLE_REDIS"]="OFF"
        tc.variables["ENABLE_PAGECOMPILER_FILE2PAGE"]="OFF"
        tc.variables["ENABLE_PAGECOMPILER"]="OFF"
        tc.variables["ENABLE_ENCODINGS"]="OFF"
        tc.variables["ENABLE_ENCODINGS_COMPILER"]="OFF"
        tc.variables["ENABLE_DATA"]="OFF"
        tc.variables["ENABLE_DATA_SQLITE"]="OFF"
        tc.variables["ENABLE_DATA_MYSQL"]="OFF"
        tc.variables["ENABLE_DATA_POSTGRESQL"]="OFF"
        tc.variables["ENABLE_DATA_ODBC"]="OFF"
        tc.variables["ENABLE_ACTIVERECORD"]="OFF"
        tc.variables["ENABLE_TESTS"] = "OFF"
        tc.variables["ENABLE_SAMPLES"] = "OFF"
        tc.variables["ENABLE_CPPUNIT"] = "OFF"
        tc.variables["CMAKE_INSTALL_RPATH"] = "$ORIGIN"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.set_property("cmake_target_name", "galaxy_poco::galaxy_poco")
        self.cpp_info.set_property("cmake_file_name", "galaxy_poco")
        self.cpp_info.libs = []
