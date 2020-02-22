import logging

console = logging.getLogger("fast")
console.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
console.addHandler(ch)
