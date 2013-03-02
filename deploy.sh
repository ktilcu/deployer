#!/bin/bash
# The purpose of this script is to receive the folder and branch from the python server, cd to the right folder, checkout a branch, pull any changes and use the prestool to upload them.
set -e

echo `whoami` >>/home/trike/log.txt
exec > >(tee logfile.txt)

# Without this, only stdout would be captured - i.e. your
# log file would not contain any error messages.
# SEE answer by Adam Spiers, which keeps STDERR a seperate stream -
# I did not want to steal from him by simply adding his answer to mine.
exec 2>&1
ahhh(){
    folder="$1"
    branch="$2"
    repo="$3"

    cd "/home/trike/update/$folder"

    currentdir=`pwd`
    dir=${currentdir##*/}
    destination=""
    fold=""
    echo "c $currentdir d $dir" >> /home/trike/log.txt
    checkout(){
        git fetch origin
        git reset --hard origin/$branch
        git clean -df
        git media sync
        echo "End checkout" >> /home/trike/log.txt
        deploy   
    }

    setDestination(){
        if [ "$1" == "master" ]; then
            destination="/home/trike/update/$dir"
            fold="$dir"       
        else
            destination="/home/trike/update/$dir-$1"
            fold="$dir-$1"
        fi

        if [ ! -d "$destination" ]; then
            mkdir "$destination"
        fi
    }

    deploy(){
        cd ..
        echo "Start Deploy" >> /home/trike/log.txt
        setDestination $branch
        echo "Destination Set" >> /home/trike/log.txt
        rsync -av --exclude='.git/' "$dir/"  "$destination/"
        
        cd /home/trike/update

        /home/trike/server/JonPresTool.py -f $fold
        echo "Finished Deploy" >> /home/trike/log.txt
    }

    # Check for remote and add if not present
    echo "$folder $branch $repo" >> /home/trike/log.txt

    if !(git remote | grep -q origin); then
        git remote add --track $branch origin git@github.com:TricycleStudios/$repo.git
    fi

    echo "Start Checkout" >> /home/trike/log.txt

    checkout
}

export -f ahhh
su trike -c "ahhh $1 $2 $3"