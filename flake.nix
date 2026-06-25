{
  description = "Markdown to Instagram Carousel Environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAllSystems = nixpkgs.lib.genAttrs supportedSystems;
    in
    {
      devShells = forAllSystems (system:
        let
          pkgs = nixpkgs.legacyPackages.${system};

          pythonEnv = pkgs.python3.withPackages (ps: with ps; [
            markdown
            weasyprint
            pymupdf
          ]);

          # WeasyPrint needs fonts to render the PDF.
          # This guarantees it has access to standard fonts even in an isolated Nix shell.
          fonts = pkgs.makeFontsConf {
            fontDirectories = [
              pkgs.dejavu_fonts
              pkgs.ubuntu-classic
            ];
          };
        in
        {
          default = pkgs.mkShell {
            packages = [
              pythonEnv
            ];

            FONTCONFIG_FILE = fonts;

            shellHook = ''
              echo "🚀 Carousel Generator Environment Ready"
              echo "Run the script using: python auto_carousel.py"
            '';
          };
        });
    };
}