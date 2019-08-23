#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, CMake, tools, RunEnvironment
import os

class NatsConan(ConanFile):
    name = "nats.c"
    version = "2.1.0"
    description = "A C client for NATS"
    topics = ("conan", "nats.c", "communication", "messaging", "protocols")
    url = "https://github.com/zinnion/conan-nats.c"
    homepage = "https://github.com/nats-io/nats.c"
    author = "Zinnion <mauro@zinnion.com>"
    license = "MIT"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt"]
    settings = "os", "compiler", "build_type", "arch"
    short_paths = True
    generators = "cmake"
    source_subfolder = "source_subfolder"
    build_subfolder = "build_subfolder"
    options = {}
    default_options = ()

    #def requirements(self):
        #self.requires.add("OpenSSL/1.1.1b@zinnion/stable")

    def source(self):
        self.run("git clone https://github.com/nats-io/nats.c.git source_subfolder")
	#self.run("git clone https://github.com/nats-io/nats.c.git source_subfolder")
        #tools.get("{0}/archive/v{1}.tar.gz".format(self.homepage, self.version))
	#self.run("git clone https://github.com/nats-io/nats.c.git source_subfolder")
        #extracted_dir = self.name + "-" + self.version
        #os.rename(extracted_dir, self.source_subfolder)

    def configure(self):
        del self.settings.compiler.libcxx

    def configure_cmake(self):
        cmake = CMake(self)
        #cmake.definitions['OPENSSL_ROOT_DIR'] = self.deps_cpp_info['OpenSSL'].rootpath
        #cmake.definitions['OPENSSL_INCLUDE_DIR'] = self.deps_cpp_info['OpenSSL'].include_paths[0]
        #cmake.definitions['OPENSSL_LIB_DIR'] = self.deps_cpp_info['OpenSSL'].lib_paths[0]
        #cmake.definitions['OPENSSL_LIBRARIES'] = ';'.join(self.deps_cpp_info['OpenSSL'].libs)
        cmake.definitions['NATS_PROTOBUF_DIR'] = "/usr/local/include/protobuf-c"
        cmake.definitions['NATS_BUILD_LIB_SHARED'] = "ON"
        cmake.definitions['NATS_BUILD_LIB_STATIC'] = "OFF"
        cmake.definitions['NATS_BUILD_TLS_USE_OPENSSL_1_1_API'] = "ON"
        cmake.configure(source_folder=self.source_subfolder, build_folder=self.build_subfolder)
        return cmake

    def build(self):
        env_build = RunEnvironment(self)
        with tools.environment_append(env_build.vars):
           cmake = self.configure_cmake()
           cmake.build()

    def package(self):
	#print "There are ", self.settings.os , "births"

        self.copy(pattern="LICENSE.txt", dst="license", src=self.source_subfolder)
        if self.settings.os == "Linux":
           self.copy(src=self.source_subfolder, pattern="*.so", dst="lib", keep_path=False)
           self.copy(src=self.source_subfolder, pattern="*.so", dst="lib/debug", keep_path=False)
        elif self.settings.os == "Macos":
           self.copy(pattern="LICENSE.txt", dst="license", src=self.source_subfolder)
           self.copy(src=self.source_subfolder, pattern="*.a", dst="lib", keep_path=False)
           self.copy(src=self.source_subfolder, pattern="*.dylib", dst="lib", keep_path=False)
           self.copy(src=self.source_subfolder, pattern="*.a", dst="lib/debug", keep_path=False)
           self.copy(src=self.source_subfolder, pattern="*.dylib", dst="lib/debug", keep_path=False)

        cmake = self.configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        #self.cpp_info.libs = ["nats", "protobuf-c"]
        #if self.settings.build_type == "Debug":
        #    self.cpp_info.libdirs = ["lib/debug"]
