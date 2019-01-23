from conans import ConanFile, AutoToolsBuildEnvironment, tools


class XzutilsConan(ConanFile):
    name = "xz-utils"
    version = "5.2"
    license = "LGPL2.1"
    author = "Alexis Lopez Zubieta <contact@azubieta.net>"
    url = "https://github.com/azubieta/conan-xz-utils.git"
    description = "XZ Utils is free general-purpose data compression software with a high compression ratio."
    topics = ("xz",)
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fpic": [True, False]}
    exports_sources = "src/*"

    def source(self):
        git = tools.Git(folder="xz")
        git.clone("https://git.tukaani.org/xz.git", "v5.2.4")


    def config_options(self):
        if self.options.shared == None:
            self.options.shared = False

        if self.options.fpic == None:
            self.options.fpic = True

    def build(self):
        autotools = AutoToolsBuildEnvironment(self)
        autotools.fpic = self.options["fpic"]
        if self.options["shared"] == False:
            autotools.defines.append("--disable-shared --enable-static ")

        env_build_vars = autotools.vars
        self.run("cd xz && ./autogen.sh")
        autotools.configure(configure_dir="xz", vars=env_build_vars)
        autotools.make(vars=env_build_vars)
        autotools.install(vars=env_build_vars)

    def package(self):
        self.copy("*.h", dst="include", src="src")
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["lzma"]
