let
  unstable = import 
    (builtins.fetchTarball "https://github.com/nixos/nixpkgs/tarball/063dece00c5a77e4a0ea24e5e5a5bd75232806f8")
    # reuse the current configuration
    { config = {allowUnfree=true;}; };
in 
{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShellNoCC {

  # LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";

  packages = with pkgs; [ 
    unstable.go
    unstable.gopls
    unstable.golangci-lint
    unstable.golangci-lint-langserver
    sqlite
    air
    gcc
    nodePackages.typescript-language-server
    vscode-langservers-extracted
    just
    tree
  ];

}
