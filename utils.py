def hexify(buf):
    return '-'.join('%02X' % b for b in buf)
