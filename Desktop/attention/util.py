import time
import math

import konlpy
from konlpy.tag import Hannanum, Okt
from konlpy.utils import pprint

Hannanum = Hannanum()
Okt = Okt()
SOS_token = 0
EOS_token = 1


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)

def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))