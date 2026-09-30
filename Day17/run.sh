#!/bin/bash
export DYLD_LIBRARY_PATH="/opt/homebrew/opt/libpq/lib:$DYLD_LIBRARY_PATH"
source venv/bin/activate
uvicorn main:app --reload
