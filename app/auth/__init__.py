# -*- coding: utf-8 -*-
from flask import Blueprint
#蓝图

auth = Blueprint('auth', __name__)

import  forms, views