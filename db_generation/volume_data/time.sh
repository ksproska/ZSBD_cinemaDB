#!/bin/bash

exit | sqlplus test/test @test.sql
cat res.txt | grep Elapsed >> clear_res.txt
echo "-----" >> clear_res.txt