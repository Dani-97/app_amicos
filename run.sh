docker run -it --rm \
           --mount type=bind,src=./src,dst=/home/user/app/src \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -e DISPLAY=$DISPLAY \
        app_amicos
