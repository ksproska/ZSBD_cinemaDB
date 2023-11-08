#!/bin/bash

exit | sqlplus test/test @/vol/test.sql
cat /vol/res.txt | grep Elapsed >> /vol/clear_res.txt
echo "-----" >> /vol/clear_res.txt