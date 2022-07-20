{ pkgs ? import <nixpkgs> {} }:

let
  mach-nix = import (builtins.fetchGit {
    url = "https://github.com/DavHau/mach-nix";
    ref = "refs/tags/3.5.0";
  }) {
    python = "python39";
  };
in
mach-nix.buildPythonApplication {
  pname = "nordea-finnair-parser";
  version = "1.0.0";
  requirements = builtins.readFile ./requirements.txt;
  src = ./.;
}
