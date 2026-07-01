import argparse
import shutil
from pathlib import Path


def copytree(src: Path, dst: Path, overwrite: bool) -> None:
    if dst.exists():
        if not overwrite:
            raise SystemExit(f"Target already exists: {dst}. Pass --overwrite to replace it.")
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a local 仿药速探 V1 platform from the bundled template.")
    parser.add_argument("--target", required=True, help="Directory where the platform should be created.")
    parser.add_argument("--overwrite", action="store_true", help="Replace the target directory if it already exists.")
    args = parser.parse_args()

    skill_root = Path(__file__).resolve().parents[1]
    template = skill_root / "assets" / "platform-template"
    target = Path(args.target).resolve()

    if not template.exists():
        raise SystemExit(f"Template not found: {template}")

    copytree(template, target, args.overwrite)
    app_dir = target / "app"
    print(f"Created platform at: {target}")
    print(f"Run: python {app_dir / 'server.py'}")
    print("Open: http://127.0.0.1:8790/")


if __name__ == "__main__":
    main()
