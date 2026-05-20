{
  description = "A flake for unimatrix";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
  let
    forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;
  in
  {
    packages = forAllSystems (system:
    let
      pkgs = import nixpkgs { inherit system; };
      unimatrix = import ./default.nix { inherit pkgs; };
    in
    {
      inherit unimatrix;
      default = unimatrix;
    });
  };
}
