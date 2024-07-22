{
  lib,
  buildPythonPackage,
  setuptools,
  wheel,
}:

let
  pyproject-toml = lib.importTOML ./pyproject.toml;
in
buildPythonPackage {
  pname = "pattern-printer";
  version = pyproject-toml.project.version;
  pyproject = true;

  src = lib.fileset.toSource {
    root = ./.;
    fileset = lib.fileset.gitTracked ./.;
  };

  build-system = [
    setuptools
    wheel
  ];

  pythonImportsCheck = [ "pattern_printer" ];
}
