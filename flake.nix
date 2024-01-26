  {
   description = "A flake for unimatrix";

   inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

   outputs = { self, nixpkgs }: {

    packages.x86_64-linux.unimatrix =
      let
        system = "x86_64-linux";
        pkgs = import nixpkgs { inherit system; };
      in
      import ./default.nix { inherit pkgs; };

    defaultPackage.x86_64-linux = self.packages.x86_64-linux.unimatrix;
 };
}
