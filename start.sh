#!/bin/sh

uwsgi --socket 0.0.0.0:5050 --protocol=http -w wsgi:app --logto logfile.log&
