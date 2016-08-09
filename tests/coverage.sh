#!/bin/bash
coverage erase
coverage run --source azurepy/ -m pytest tests/test_queues.py tests/test_vm.py
coverage html
open htmlcov/index.html
