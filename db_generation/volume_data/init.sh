#!/bin/bash

exit | sqlplus system/test @create_user.sql
sh import.sh
