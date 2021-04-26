#!/bin/bash

echo "http://127.0.0.1:8888/"

exec jupyter notebook --no-browser --allow-root --ip=0.0.0.0 --port=8888