import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")

OUTPUT_DIR = "output"
INPUT_DIR = "input"

DROPSHIP_DIR = os.path.join(DATA_DIR,
"dropship")

def mkdir_if_not_exists(dir):
    if not os.path.exists(dir):
        os.mkdir(dir)
        print(f"Created: {dir}")

mkdir_if_not_exists(ABS_PATH)
mkdir_if_not_exists(BASE_DIR)
#mkdir_if_not_exists(DATA_DIR)
mkdir_if_not_exists(INPUT_DIR)
mkdir_if_not_exists(OUTPUT_DIR)
#PROMO_DIR = os.path.join(DATA_DIR, "promo")

PROMO_DIR = r"C:\Users\Professor\Documents\PlatformIO\Projects\url test\data\dropship\promos"