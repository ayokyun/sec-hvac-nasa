from NasaSignal import NasaSignal


def hexify(buf):
    return '-'.join('%02X' % b for b in buf)


data = '0c823f00c8800100800301808d00803f008243000082350000805e0080310082480006801700801a00aaa434e6cce6cce6'
# data = '01400001'
buf = [int(data[i] + data[i + 1], 16) for i in range(0, len(data), 2)]

offset = 0

# 패킷 개수 읽는다
numCommands = buf[offset]
offset += 1

print(f'ncount = {numCommands}')

for i in range(numCommands):
    # 헤더 읽고 파싱
    payload, offset = NasaSignal.deserialize(buf, offset)

    print(
        f'Header = {payload.header:04X} (state = {payload.is_state}, command = {payload.is_command}, data_type = {payload.data_type}, signal = {payload.signal:02X})')
    print(f'Data = {payload.value:X}')
    print()

if offset != len(buf):
    print(f'cannot read the whole packet, offset = {offset}, len = {len(buf)}')
    print(hexify(buf[offset:]))
