{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  buildInputs = [
    pkgs.python3
    pkgs.python3Packages.pip

    pkgs.gcc-unwrapped
    pkgs.stdenv.cc.cc.lib

    pkgs.openblas
    pkgs.lapack
    pkgs.zlib
  ];

  shellHook = ''
    export LD_LIBRARY_PATH=${pkgs.zlib}/lib:${pkgs.gcc-unwrapped.lib}/lib:${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
  '';
}
