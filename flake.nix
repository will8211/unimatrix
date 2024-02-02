{
  description = "A flake for unimatrix";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
  let
    systems = [ "x86_64-linux" "aarch64-linux" "i686-linux" "x86_64-darwin" ];
    systemPackageBuilder = system:
      let
        pkgs = import nixpkgs { inherit system; };
      in
      {
        ${system} = {
          unimatrix = import ./default.nix { inherit pkgs; };
          default = self.packages.${system}.unimatrix;
        };
      };
    systemPackages = builtins.map systemPackageBuilder systems;
  in
  {
    packages = builtins.foldl' (a: b: a // b) {} systemPackages;
  };
}
