docker run -it --rm --mount type=bind,src=.,dst=/app -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix app_amicos
