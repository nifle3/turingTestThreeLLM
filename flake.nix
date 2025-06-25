{
  description = "Python 3.14 + uv devShell";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };
      in {
        devShells.default = pkgs.mkShell {
          name = "python-uv-shell";
          buildInputs = [
            pkgs.python313
            pkgs.uv
            pkgs.ruff
          ];

          shellHook = ''
            echo "🐍 Python: $(python --version)"
            echo "🧪 UV: $(uv --version)"
          '';
        };
      });
}
