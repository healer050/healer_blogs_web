# coding: utf-8

import os
import logging
from config import LOG_DIR, LOG_FILE

if not os.path.exists(LOG_DIR + '/' + LOG_FILE):
    if not os.path.exists(LOG_DIR):
        os.mkdir(LOG_DIR)
    os.mknod(LOG_DIR + '/' + LOG_FILE)

log_config = dict(
    level=logging.WARNING,
    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=LOG_DIR + '/' + LOG_FILE,
    filemode='a'
)

logging.basicConfig(**log_config)

