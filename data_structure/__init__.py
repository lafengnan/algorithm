from datetime import datetime

def debug(msg, level, *args, **kwargs):
    print("anan: [{ts} {lv}] --- {msg} {arg} {karg}"\
          .format(ts=datetime.utcnow(), lv=level, \
                  msg=msg, arg=args, karg=kwargs))
