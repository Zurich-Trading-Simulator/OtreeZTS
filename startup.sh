#!/bin/bash

cd /opt/otree

#otree devserver

#touch /opt/otree/logs/django_debug.log
#tail -F /opt/otree/logs/django_debug.log

touch /django_debug.log
tail -F /django_debug.log