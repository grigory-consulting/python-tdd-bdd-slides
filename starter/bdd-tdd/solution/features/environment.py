import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"


def use_src_on_path() -> None:
    src = str(SRC_DIR)
    if src not in sys.path:
        sys.path.insert(0, src)


use_src_on_path()


def before_all(context):
    use_src_on_path()


def before_scenario(context, scenario):
    context.customer_type = None
    context.subtotal = None
    context.discount = None
    context.total = None
    context.coupon = None
