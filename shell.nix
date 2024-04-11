{ pkgs ? import <nixpkgs> {} }:
  pkgs.mkShell {
    nativeBuildInputs = with pkgs.buildPackages; [ 
      python311
      python311Packages.pip
      (python311.withPackages(ps: with ps; [ 
        notebook
        jupyter-core
        pandas
        matplotlib
        scikit-learn
	pynvim
	jupyter-client
	cairosvg
	pnglatex
	plotly
	pyperclip
	nbformat
      ]))
    ];
}


