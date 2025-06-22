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
          config.allowUnfree = true; # если вдруг нужен uv из бинарников
        };

        python = pkgs.python314;

      in {
        devShells.default = pkgs.mkShell {
          name = "python-uv-shell";
          buildInputs = [
            python
            pkgs.uv
          ];

          shellHook = ''
            echo "🐍 Python: $(python --version)"
            echo "🧪 UV: $(uv --version)"
          '';
        };
      });
}
