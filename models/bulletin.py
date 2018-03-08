# -*- coding: utf-8 -*-

from libs.motor.base import BaseMotor
from config import MongoBasicInfoDb, BULLETIN_INFOS

class Bulletin_info():
    def __init__(self):
        self.coll = BaseMotor().client[MongoBasicInfoDb][BULLETIN_INFOS]
