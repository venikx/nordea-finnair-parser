{ pkgs ? import <nixpkgs> {} }:

with pkgs;

poetry2nix.mkPoetryApplication {
  projectDir = ./.;
}
