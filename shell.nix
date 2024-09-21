let
  unstable = import 
    (builtins.fetchTarball "https://github.com/nixos/nixpkgs/tarball/71e91c409d1e654808b2621f28a327acfdad8dc2")
    # reuse the current configuration
    { config = {allowUnfree=true;}; };
in 
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShellNoCC {

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";

  packages = with pkgs; [ 
    unstable.go
    unstable.gopls
    sqlite
    air
    gcc
    nodePackages.typescript-language-server
    vscode-langservers-extracted
    tree
  ];

}
