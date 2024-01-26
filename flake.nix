{
 description = "A flake for unimatrix";

 inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

 outputs = { self, nixpkgs }: {

  packages.x86_64-linux.unimatrix =
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
    in
    pkgs.stdenv.mkDerivation rec {
      pname = "unimatrix";
      version = "1.0.0";

      src = self;

      phases = "installPhase";

      installPhase = ''
        mkdir -p $out/bin
        cp ${./unimatrix.py} $out/bin/unimatrix
        chmod +x $out/bin/unimatrix
      '';

      meta = with pkgs.lib; {
        description = "Python script to simulate the display from \"The Matrix\" in terminal. Uses half-width katakana unicode characters by default, but can use custom character sets. Accepts keyboard controls while running";
        homepage = https://github.com/will8211/unimatrix;
        license = licenses.gpl3;
        maintainers = [ maintainers.will8211 ];
        platforms = platforms.all;
      };
    };

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.unimatrix;
 };
}
