#!/bin/bash
coverage erase
coverage run --source azurepy/ -m pytest tests/test_queues.py
coverage run --source azurepy/ -m pytest tests/test_vm.py
coverage html
open htmlcov/index.html
