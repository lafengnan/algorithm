from datetime import datetime

def debug(msg, level, **kwargs):
    print("anan: [{ts} {lv}] --- {msg} {karg}"\
          .format(ts=datetime.utcnow(), lv=level, \
                  msg=msg, karg=kwargs))
