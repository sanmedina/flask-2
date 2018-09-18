#!/bin/bash
venv/bin/python -m coverage run --source=../flask-ws --omit=app_tests.py,run.py,venv/*,setup.py app_tests.py
venv/bin/python -m coverage report