"""Pure-Python LZO1X decompressor (the variant BI's ODOL uses for arrays >= 1024 bytes).

decompress(buf, start, out_len) -> (bytes, bytes_consumed)   raises ValueError on any inconsistency.
Port of minilzo's lzo1x_decompress_safe control flow.
"""


class LzoError(ValueError):
    pass


def decompress(buf, start, out_len):
    ip = start
    n = len(buf)
    out = bytearray()

    def need(k):
        if ip + k > n:
            raise LzoError("input overrun")

    def copy_match(m_pos, length):
        if m_pos < 0:
            raise LzoError("lookbehind overrun")
        if len(out) + length > out_len:
            raise LzoError("output overrun")
        for i in range(length):
            out.append(out[m_pos + i])

    def copy_lit(length):
        nonlocal ip
        if ip + length > n:
            raise LzoError("input overrun")
        if len(out) + length > out_len:
            raise LzoError("output overrun")
        out.extend(buf[ip:ip + length])
        ip += length

    state = "loop"
    t = 0
    need(1)
    if buf[ip] > 17:
        t = buf[ip] - 17
        ip += 1
        if t < 4:
            state = "match_next"
        else:
            copy_lit(t)
            state = "first_literal_run"
    while True:
        if state == "loop":
            need(1)
            t = buf[ip]; ip += 1
            if t >= 16:
                state = "match"
                continue
            if t == 0:
                while True:
                    need(1)
                    if buf[ip] != 0:
                        break
                    t += 255; ip += 1
                t += 15 + buf[ip]; ip += 1
            copy_lit(t + 3)
            state = "first_literal_run"
            continue
        if state == "first_literal_run":
            need(1)
            t = buf[ip]; ip += 1
            if t >= 16:
                state = "match"
                continue
            need(1)
            m_pos = len(out) - (1 + 0x0800) - (t >> 2) - (buf[ip] << 2)
            ip += 1
            copy_match(m_pos, 3)
            state = "match_done"
            continue
        if state == "match":
            if t >= 64:
                need(1)
                m_pos = len(out) - 1 - ((t >> 2) & 7) - (buf[ip] << 3)
                ip += 1
                t = (t >> 5) - 1
                copy_match(m_pos, t + 2)
                state = "match_done"
                continue
            elif t >= 32:
                t &= 31
                if t == 0:
                    while True:
                        need(1)
                        if buf[ip] != 0:
                            break
                        t += 255; ip += 1
                    t += 31 + buf[ip]; ip += 1
                need(2)
                m_pos = len(out) - 1 - ((buf[ip] >> 2) + (buf[ip + 1] << 6))
                ip += 2
                copy_match(m_pos, t + 2)
                state = "match_done"
                continue
            elif t >= 16:
                m_pos = len(out) - ((t & 8) << 11)
                t &= 7
                if t == 0:
                    while True:
                        need(1)
                        if buf[ip] != 0:
                            break
                        t += 255; ip += 1
                    t += 7 + buf[ip]; ip += 1
                need(2)
                m_pos -= (buf[ip] >> 2) + (buf[ip + 1] << 6)
                ip += 2
                if m_pos == len(out):
                    # end of stream
                    if len(out) != out_len:
                        raise LzoError("eof with %d of %d bytes" % (len(out), out_len))
                    return bytes(out), ip - start
                m_pos -= 0x4000
                copy_match(m_pos, t + 2)
                state = "match_done"
                continue
            else:
                need(1)
                m_pos = len(out) - 1 - (t >> 2) - (buf[ip] << 2)
                ip += 1
                copy_match(m_pos, 2)
                state = "match_done"
                continue
        if state == "match_done":
            t = buf[ip - 2] & 3
            if t == 0:
                state = "loop"
                continue
            state = "match_next"
            continue
        if state == "match_next":
            copy_lit(t)
            need(1)
            t = buf[ip]; ip += 1
            state = "match"
            continue
