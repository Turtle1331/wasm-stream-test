from flask import Flask, Response
import time
import os
import re
import binascii


TAG = "marks"
WASM_SRC_PATH = "static/index.wasm"
WASM_OUT_DIR = "static/wasm"

app = Flask(__name__)


def streaming(*args, **kwargs):
    def outer(func):
        def inner():
            return Response(func(), *args, **kwargs)
        return inner
    return outer


@app.route("/")
def index():
    return app.send_static_file("index.html")


@app.route("/index.wasm")
@streaming(mimetype="application/wasm")
def index_wasm():
    i = 0
    while True:
        i += 1
        try:
            with open(os.path.join(WASM_OUT_DIR, f"part{i}.wasm"), "rb") as f:
                part = f.read()
                print(f"Loaded part{i}.wasm ({len(part)} bytes)")
                yield part
                time.sleep(1)
        except FileNotFoundError:
            print(f"Loaded {i-1} parts")
            break


def prepare_wasm():
    with open(WASM_SRC_PATH, "rb") as f:
        src = f.read()

    tag_start = f"<{TAG}>".encode()
    tag_end = f"</{TAG}>".encode()
    starts = [m.start() for m in re.finditer(tag_start, src)]
    ends = [m.start() for m in re.finditer(tag_end, src)]
    tag_start_pos = None
    tag_end_pos = None

    if len(starts) == len(ends) == 1:
        tag_start_pos = starts[0]
        tag_end_pos = ends[0]
    else:
        raise NotImplemented()

    marks = src[tag_start_pos+len(tag_start):tag_end_pos]
    marks = set(marks.strip(b"\r\n").splitlines())

    marks_stops = {}
    for mark_hex in marks:
        mark_hex = mark_hex.lower()
        if mark_hex in marks_stops:
            print(f"skipping duplicate mark {mark_hex!r}")
            continue

        try:
            mark = binascii.a2b_hex(mark_hex)
        except binascii.Error:
            print(f"error: could not decode mark {mark_hex!r}")
            continue

        mark_all_pos = [m.start() for m in re.finditer(re.escape(mark), src)]
        if len(mark_all_pos) != 1:
            print(f"error: found multiple matches for mark {mark_hex.decode()}")
            continue

        mark_pos = mark_all_pos[0]
        if mark_pos in marks_stops.values():
            other_mark_hex = marks_stops[mark_hex]
            print(f"warning: stop at byte {mark_pos} for mark {mark_hex.decode()} already added from mark {other_mark_hex.decode()}")
            continue

        print(f"added stop at byte {mark_pos} for mark {mark_hex.decode()}")
        marks_stops[mark_hex] = mark_pos

    stops = sorted(marks_stops.values())
    stops.append(len(src))

    for fname in os.listdir(WASM_OUT_DIR):
        os.remove(os.path.join(WASM_OUT_DIR, fname))

    prev_stop = 0
    for i, stop in enumerate(stops):
        with open(os.path.join(WASM_OUT_DIR, f"part{i+1}.wasm"), "wb") as f:
            f.write(src[prev_stop:stop])
        prev_stop = stop

    num_stops = len(stops)
    assert num_stops == i + 1
    print(f"{num_stops} parts written")


if __name__ == "__main__":
    prepare_wasm()
    app.run(host="localhost", port=8080)
