#!/bin/bash

exit | sqlplus system/test @/vol/test.sql
date --rfc-3339=s >> /vol/clear_res.txt
cat /vol/res.txt | grep Elapsed >> /vol/clear_res.txt
echo "-----" >> /vol/clear_res.txt