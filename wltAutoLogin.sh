#!/bin/bash
username="None"
type=9
while getopts "u:t:" arg
do
	case $arg in
		u)
		username=$OPTARG;;
		t)
		type=$OPTARG;;
		?)
		echo "Unknow argument"
		exit 1;;
	esac
done
if [ $username == "None" ]
then
	echo "Please enter your wlt username:"
	read username
fi

unset PASSWORD
unset CHARCOUNT

echo "Please enter your password:"

stty -echo

CHARCOUNT=0
while IFS= read -p"$PROMPT" -r -s -n 1 CHAR
do
    # Enter - accept password
    if [[ $CHAR == $'\0' ]] ; then
        break
    fi
    # Backspace
    if [[ $CHAR == $'\177' ]] ; then
        if [ $CHARCOUNT -gt 0 ] ; then
            CHARCOUNT=$((CHARCOUNT-1))
            PROMPT=$'\b \b'
            PASSWORD="${PASSWORD%?}"
        else
            PROMPT=''
        fi
    else
        CHARCOUNT=$((CHARCOUNT+1))
        PROMPT='*'
        PASSWORD+="$CHAR"
    fi
done

stty echo

#echo "Please enter your password:"
#read -s password
#echo "wt=$waittime"
#echo "rt=$retrytime"
#echo "$stuid"
#echo "$password"
python3 wlt.py -u $username -p $PASSWORD -t $type
