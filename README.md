# WebAssembly Streaming Experiment

## Overview

This is an experiment to see if `WebAssembly.instantiateStreaming()` can be used
to provide JIT-like capabilities for Wasm with a single module. The idea was to
declare a bunch of functions up front and only send the code for them as needed,
similar to sending `<script>` tags in a never-ending HTML response in HTTP long
polling.

The outcome seems to be that functions cannot be called until the fetch response
is complete, which means that this idea doesn't work in practice. It's possible
that it behaves differently on other browsers (I'm on Firefox 78.10.0 ESR), but
I think this has more to do with the specifications for WebAssembly and its
JavaScript embedding. I'll have to do some research in the specs to see what
exactly "initialization" means in the context of `instantiateStreaming()` and
whether there's any room in the spec for more eager browser behavior.  That
said, I didn't have high hopes or expectations of success for this experiment.

Along the way, I came up with a method for marking locations within the
WebAssembly module in a way that's contained within the module itself and works
with the text format and `wat2wasm`. This has limited use since the information
could be provided in a custom section with custom tooling and would be mostly
discarded by optimization (e.g. `wasm-opt`). Nevertheless, I may expand on it
in the future as a tool for people who write WebAssembly directly in text
format (like me).

## Setup

```
git clone https://github.com/Turtle1331/wasm-stream-test.git
cd wasm-stream-test
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
```

## Running

```
python3 main.py
```

Then, open `http://localhost:8080` in a browser, open the console view, and
refresh.

## License

This project is licensed under the MIT license.
