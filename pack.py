import subprocess
import sys
import os
import zipfile
from pathlib import Path

PROJECT_DIR = Path(__file__).parent
CSPROJ = PROJECT_DIR / "Alba.Spolszczenie.csproj"
DLL_NAME = "Alba.Spolszczenie.dll"
BUILD_CONFIG = "Release"
BUILD_OUTPUT = PROJECT_DIR / "bin" / BUILD_CONFIG / "netstandard2.0"
INJECTION_DIR = PROJECT_DIR / "Injection"
TRANSLATION_FILE = PROJECT_DIR / "alba.pl.jsonl"
OUTPUT_ZIP = PROJECT_DIR / "Alba.Spolszczenie.zip"


def build():
    print("Building project...")
    result = subprocess.run(
        ["dotnet", "build", str(CSPROJ), "-c", BUILD_CONFIG],
        cwd=str(PROJECT_DIR),
    )
    if result.returncode != 0:
        print("Build failed.", file=sys.stderr)
        sys.exit(1)
    print("Build succeeded.")


def pack():
    dll_path = BUILD_OUTPUT / DLL_NAME
    if not dll_path.exists():
        print(f"DLL not found at {dll_path}", file=sys.stderr)
        sys.exit(1)

    print(f"Creating {OUTPUT_ZIP.name}...")
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add Injection files at root level
        for file in INJECTION_DIR.rglob("*"):
            if file.is_file():
                arcname = file.relative_to(INJECTION_DIR)
                zf.write(file, arcname)
                print(f"  + {arcname}")

        # Add DLL to BepInEx/plugins/
        plugin_arcname = Path("BepInEx") / "plugins" / DLL_NAME
        zf.write(dll_path, plugin_arcname)
        print(f"  + {plugin_arcname}")

        # Add translation file at root level
        if TRANSLATION_FILE.exists():
            zf.write(TRANSLATION_FILE, TRANSLATION_FILE.name)
            print(f"  + {TRANSLATION_FILE.name}")

    print(f"Done. Created {OUTPUT_ZIP.name}")


if __name__ == "__main__":
    build()
    pack()
