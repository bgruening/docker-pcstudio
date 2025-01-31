
# Docker image for PhysiCell Studio - constructed for the use as Galaxy IT


### Build and (attempt to) run the image locally; upload it

```bash
# "name-of-image" that I used was "physicell-studio". I uploaded to my (heiland) Docker Hub
# and it is referenced in the "interactivetool_physicell_studio.xml" file (below)
docker build -t name-of-image .

# after it builds, can see it listed via:
docker images

# can attempt to run it and display the Studio on your desktop
# (may depend on your OS; need XQuartz running on OSX; need "xhost +")
docker run -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix  name-of-image  /usr/local/pcstudio-venv/bin/python3 /opt/pcstudio/bin/studio.py -c /opt/pcstudio/config/PhysiCell_settings.xml

# prepare your Docker repository for this image (e.g., create name first; login from cmd line),
# then push (upload) it
docker push heiland/name-of-image
```

### Galaxy integration

Galaxy can run arbitrary Virtual Research Environments (VREs). In Galaxy terms, such VRE's are called "Interactive Tools", as they are using the same subsystem then normal Galaxy tools.
The only requirement is that those tools needs to run in containers and expose a port(s) to which Galaxy can redirect users. 

This repo provides sample files needed by a Galaxy server to be aware of this interactive tool:
* [job_conf.yml](./job_conf.yml) - put in /config
* [tool_conf.xml](./tool_conf.xml) - put in /config
* [interactivetool_physicell_studio.xml](./interactivetool_physicell_studio.xml) - put in /tools/interactive
