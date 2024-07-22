{
  description = "Compatibility module of Python imp";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.05";
    nixpkgs-lib.url = "github:NixOS/nixpkgs/nixos-24.05?dir=lib";
    devshell.url = "github:numtide/devshell";
    devshell.inputs.nixpkgs.follows = "nixpkgs";
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixfmt.url = "github:NixOS/nixfmt";
    treefmt-nix.url = "github:numtide/treefmt-nix";
    treefmt-nix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs =
    inputs@{ self, flake-parts, ... }:
    let
      inherit (inputs.nixpkgs-lib) lib;
    in
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        inputs.devshell.flakeModule
        inputs.treefmt-nix.flakeModule
      ];
      # # flake-parts would error out if elements in sytems are not provided by
      # # the Nixpkgs flake as a system attribute.
      # systems = lib.platforms.all;
      systems = lib.attrNames inputs.nixpkgs.legacyPackages;
      flake = {
        lib.pythonPackagesExtensions.default = import ./python-packages-extensions.nix;
      };
      perSystem =
        {
          config,
          pkgs,
          system,
          ...
        }:
        let
          pythons = {
            inherit (pkgs)
              python3
              python310
              python311
              python312
              python313
              pypy3
              pypy39
              pypy310
              ;
          };
          pythonsOkay = lib.filterAttrs (
            pythonName: pythonPackage:
            lib.all (packageName: (builtins.tryEval pythonPackage.pkgs.${packageName}.drvPath).success) [
              "setuptools"
              "wheel"
              "six"
            ]
          ) pythons;
          siblings = lib.mapAttrs' (
            pythonName: pythonPackage:
            (lib.nameValuePair "pattern-printer_${pythonName}"
              (pythonPackage.override (previousArgs: {
                packageOverrides =
                  final: prev:
                  self.lib.pythonPackagesExtensions.default final (previousArgs.packageOverrides final prev);
              })).pkgs.pattern-printer
            )
          ) pythonsOkay;
          defaultPython = pkgs.python3;
          defaultSibling = siblings.pattern-printer_python3;
        in
        {
          packages = siblings;
          checks =
            siblings
            // lib.listToAttrs (
              lib.concatMap (
                name:
                (map (nv: nv // { name = "${name}-tests-${nv.name}"; }) (
                  lib.attrsToList siblings.${name}.tests or { }
                ))
              ) (lib.attrNames siblings)
            );
          devshells.default = {
            packages = with pkgs; [
              ruff # Python formatter and linter
            ];
            packagesFrom = [ defaultSibling ];
          };
          treefmt.projectRootFile = ".git/config";
          treefmt.programs.ruff.check = true;
          treefmt.programs.ruff.format = true;
          treefmt.programs.nixfmt.enable = true;
          treefmt.programs.nixfmt.package = inputs.nixfmt.packages.${system}.default;
        };
    };
}
