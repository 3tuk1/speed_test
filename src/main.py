

import logging
import sys

from src.create_popup import create_popup
from src.no_gui_do import  no_gui_do

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def main():
    boot = sys.argv
    # 引数があるかどうかをチェック
    if len(boot) > 1 and boot[1] == "no_GUI":
        try:
            no_gui_do()
        except Exception as e:
            logger.exception("An error has occurred.")
            raise
    else:
        try:
            create_popup()
        except Exception as e:
            logger.exception("An error has occurred.")
            raise


if __name__ == "__main__":
    main()
