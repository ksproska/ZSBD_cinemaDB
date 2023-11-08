#!/bin/bash

exit | sqlplus system/test @/vol/create_user.sql
sh /vol/import.sh
