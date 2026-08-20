{
  pkgs ? import <nixpkgs> { },
}:

let
  python = pkgs.python313;
  gcc_lib_path = "${pkgs.stdenv.cc.cc.lib}/lib";
in

pkgs.mkShell {
  buildInputs = with pkgs; [
    gcc
    #python
    #python3Packages.pip
  ];

  shellHook = ''
    # Explicitly set the LD_LIBRARY_PATH
    rm -rf .venv
    export LD_LIBRARY_PATH=${gcc_lib_path}:$LD_LIBRARY_PATH

    # Ensure the correct python is in PATH for venv activation
    export PATH=${python}/bin:$PATH


    if [ ! -d ".venv" ]; then
        python3 -m venv .venv
    fi
    source .venv/bin/activate
    pip install git+https://github.com/jarlrobin/django_cli_sessions.git@main
  '';
}
