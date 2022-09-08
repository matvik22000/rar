# import logging
#
# # add filemode="w" to overwrite
#
# log = logging.getLogger("test_logger")
# log.setLevel(logging.INFO)
#
# file = logging.FileHandler("sample.log")
# formatter = logging.Formatter('%(asctime)s %(levelname)s [%(name)s]: %(message)s')
# file.setFormatter(formatter)
#
# log.addHandler(file)
#
# log.debug("This is a debug message")
# log.info("Informational message")
# log.error("An error has happened!")

for x in range(2):
    for y in range(2):
        for w in range(2):
            for z in range(2):
                f = (x and (not y)) or (y == z) or w
                if not f:
                    print(x, y, w, z, int(f))