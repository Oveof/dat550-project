{
  description = "Your jupyenv project";

  nixConfig.extra-substituters = [
    "https://tweag-jupyter.cachix.org"
  ];
  nixConfig.extra-trusted-public-keys = [
    "tweag-jupyter.cachix.org-1:UtNH4Zs6hVUFpFBTLaA4ejYavPo5EFFqgd7G7FxGW9g="
  ];

  inputs.flake-compat.url = "github:edolstra/flake-compat";
  inputs.flake-compat.flake = false;
  inputs.flake-utils.url = "github:numtide/flake-utils";
  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";
  inputs.jupyenv.url = "github:tweag/jupyenv";

  outputs = {
    self,
    flake-compat,
    flake-utils,
    nixpkgs,
    jupyenv,
    ...
  } @ inputs:
    flake-utils.lib.eachSystem
    [
      flake-utils.lib.system.x86_64-linux
    ]
    (
      system: let
        inherit (jupyenv.lib.${system}) mkJupyterlabNew;
        jupyterlab = mkJupyterlabNew ({...}: {
          nixpkgs = inputs.nixpkgs;
          imports = [(import ./kernels.nix)];
        });
        pkgs = inputs.nixpkgs.legacyPackages.${system};
      in rec {
        packages = {
          inherit jupyterlab;
          merge = pkgs.writeShellApplication {
            name = "merge";

            runtimeInputs = with pkgs; [
              findutils
              pandoc

              texliveFull
              python311Packages.nbmerge
            ];

            text = ''
              dir=$(realpath "$1");
              find . -type f -not -path "$dir/.*" -name '*.ipynb' -print0 | xargs -0 nbmerge --output "$dir"/"$(basename "$dir")"_merged.ipynb
            '';
          };
        };
        packages.default = jupyterlab;
        apps.default.program = "${jupyterlab}/bin/jupyter-lab";
        apps.default.type = "app";

        devShells.default = pkgs.mkShell {
          buildInputs = with pkgs; [
            python311
          ] ++ (with pkgs.python311Packages; [
            flask
            python-lsp-server
            pylint
            pyflakes
            pycodestyle
            pydocstyle
            
            (torch.override {
              # rocmSupport = true;
              # cudaSupport = true;
            })
            faiss
            datasets
            torchvision
            transformers
            pandas
            pillow
            requests
            numpy
            scikit-learn
          ]);
        };
      }
    );
}
