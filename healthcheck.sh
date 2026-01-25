#!/bin/bash
supervisorctl status | grep -q RUNNING
exit $?
