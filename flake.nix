{
  description = "Coral";

  # Pinning to a specific nixpkgs commit for reproducibility. Last updated: 2024-12-14.
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?rev=a0f3e10d94359665dba45b71b4227b0aeb851f8e";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      devShells.${system}.default = pkgs.mkShell {
        packages = [
          (pkgs.python3.withPackages (python-pkgs: with python-pkgs; [ pygame pyinstaller ]))
        ];
      };
    };
}
