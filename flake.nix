{
  description = "barebones python runner";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs";

  outputs = { nixpkgs, ... }: let
    system = "x86_64-linux";
    pkgs = import nixpkgs { inherit system; };
  in
  {
    apps.${system}.default = {
      type = "app";
      program = "${pkgs.python3}/bin/python";
      args = [ "${./py/main.py}" ];
      # optional: make print() unbuffered so output shows immediately
      env = { PYTHONUNBUFFERED = "1"; };
    };
  };
}
