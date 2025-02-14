{ pkgs ? import <nixpkgs> {} }:

pkgs.stdenv.mkDerivation rec {
  pname = "unimatrix";
  version = "1.0.0";

  src = ./.;

  buildInputs = with pkgs; [
    python3
  ];

  phases = "installPhase";

  installPhase = ''
    mkdir -p $out/bin
    cp $src/unimatrix.py $out/bin/unimatrix
    chmod +x $out/bin/unimatrix
  '';

  meta = with pkgs.lib; {
    description = "Python script to simulate the display from \"The Matrix\" in terminal. Uses half-width katakana unicode characters by default, but can use custom character sets. Accepts keyboard controls while running";
    homepage = https://github.com/will8211/unimatrix;
    license = licenses.gpl3;
    maintainers = [ maintainers.will8211 ];
    platforms = platforms.all;
  };
}

