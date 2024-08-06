from pathlib import Path


ROOT_PATH = Path(__file__).parent.parent.parent.parent
RESOURCES_PATH = ROOT_PATH / "resources"


if __name__ == "__main__":
    print(f"ROOT_PATH: {ROOT_PATH}")