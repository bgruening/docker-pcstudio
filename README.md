
# Docker image for PhysiCell Studio - constructed for the use as Galaxy IT


### Build and run the image locally

```bash
docker build -t docker-pcstudio .
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix docker-pcstudio python3 /opt/pcstudio/bin/studio.py -c /opt/pcstudio/config/PhysiCell_settings.xml
```

### Galaxy integration

Galaxy can run arbitrary Virtual Research Environments (VREs). In Galaxy terms, such VRE's are called "Interactive Tools", as they are using the same subsystem then normal Galaxy tools.
The only requirement is that those tools needs to run in containers and expose a port(s) to which Galaxy can redirect users. 
