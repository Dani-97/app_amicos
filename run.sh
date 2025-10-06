docker run -it --rm --mount type=bind,src=./src,dst=/app/src -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix app_amicos
