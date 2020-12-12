import logging


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)-15s %(levelname)8s %(name)s %(message)s'
)


for name in ('meshstats'):
    logging.getLogger(name).setLevel(logging.DEBUG)


def register():
    pass
