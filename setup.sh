#!/bin/bash

set -e

[ ! -z `which virtualenv` ] || pip install -U virtualenv

ls virtualenv &>/dev/null || virtualenv --setuptools --no-site-packages -p python2.7 virtualenv
[ -z "${VIRTUAL_ENV:-}" ] && . virtualenv/bin/activate

pip install -r requirements.txt