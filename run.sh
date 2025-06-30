#!/bin/bash

# Run scraper in background
python scraper.py &

# Run Flask server
python server.py
