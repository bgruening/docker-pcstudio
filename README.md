
# Docker image for PhysiCell Studio - constructed for the use as Galaxy IT

[QuPath](https://qupath.github.io) Bioimage Analysis is now available in [Galaxy](https://usegalaxy.eu/root?tool_id=interactive_tool_qupath).


### Run the image

You can start the container outside of Galaxy with:

```bash
docker run -i -t --rm -v /path/to/infile.tiff:/opt/qupath/infile.tiff -p 8080:5800 quay.io/galaxy/qupath-headless:0.4.3 bash
```

Once you are in the container you can start the application with:

```bash
/init
```

### Configuration

This image is based on top of the fantastic work of Jocelyn Le Sage [base GUI image](https://github.com/jlesage/docker-baseimage-gui). Please consult the documentation of the [upstream container](https://github.com/jlesage/docker-baseimage-gui).

### Galaxy integration

Galaxy can run arbitrary Virtual Research Environments (VREs). In Galaxy terms, such VRE's are called "Interactive Tools", as they are using the same subsystem then normal Galaxy tools.
The only requirement is that those tools needs to run in containers and expose a port(s) to which Galaxy can redirect users. The Docker image for QuPath you can find in this repository.
The Galaxy tool defintion for the QuPath Interactive tool can be found [here](https://github.com/usegalaxy-eu/galaxy/blob/release_23.0_europe/tools/interactive/interactivetool_qupath.xml).
