{ pkgs ? import <nixpkgs> {} }:
pkgs.mkShellNoCC {

  LD_LIBRARY_PATH = "${pkgs.stdenv.cc.cc.lib}/lib";

  packages = with pkgs; [ 
    gcc
    just
    rust-analyzer
    rustup
  ];

}
