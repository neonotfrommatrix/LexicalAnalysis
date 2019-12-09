#!/bin/bash/

PASSWORD="neonotfrommatrix"

echo "Enter username: "

read USER_NAME

echo "Enter password: "

read PW

if [ $PASSWORD == $PW ]; then 
    echo "Successful login $USER_NAME!"
else
    echo "Incorrect password for user $USER_NAME"
fi