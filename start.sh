#! /bin/sh

source ./.venv/bin/activate
uvicorn src.main:app --host "0.0.0.0" --port 8910