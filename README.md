# Network Congestion Control Emulator

The Pantheon contains wrappers for many popular practical and research
congestion control schemes. The Pantheon enables them to run on a common
interface, and has tools to benchmark and compare their performances.
Pantheon tests can be run locally over emulated links using
[mahimahi](http://mahimahi.mit.edu/) or over the Internet to a remote machine.

## Disclaimer
This repo was forked from [Pantheon of Congestion Control](https://github.com/StanfordSNR/pantheon)

## Installation
Follow the guidelines from the original repo

```
git clone https://github.com/oss-slu/Congestion-control-emulator.git
```

Add submodules after cloning by running:

```
git submodule update --init --recursive  # or tools/fetch_submodules.sh
```

Follow the remaining of the set-up guidelines [here](https://github.com/StanfordSNR/pantheon)

## How to fix common errors

### 1. Unable to run verus, quic, copa, and taova
I ran into the following error for verus. Similar errors occur for quic, copa, and taova. This happens because the set-up failed for each of these protocols. As such, the needed folders were not created. They are currently disabled in [src/config.yml](src/config.yml)

```python
Traceback (most recent call last):
  File "/home/pokorie/Documents/repos/pantheon/src/wrappers/verus.py", line 42, in <module>
    main()
  File "/home/pokorie/Documents/repos/pantheon/src/wrappers/verus.py", line 32, in main
    check_call(cmd, cwd=utils.tmp_dir)
  File "/usr/lib/python2.7/subprocess.py", line 185, in check_call
    retcode = call(*popenargs, **kwargs)
  File "/usr/lib/python2.7/subprocess.py", line 172, in call
    return Popen(*popenargs, **kwargs).wait()
  File "/usr/lib/python2.7/subprocess.py", line 394, in __init__
    errread, errwrite)
  File "/usr/lib/python2.7/subprocess.py", line 1047, in _execute_child
    raise child_exception
OSError: [Errno 2] No such file or directory
```

### Docker Usage
Getting the right environment for Pantheon can be tricky. So as of now (2/23/23), we have a docker image that holds the dependencies.
Get yourself familiar with [Docker](https://docs.docker.com/config/daemon/start/)
Start a docker daemon
Then,
```bash
docker pull a8nguyen/oss-slu-congestion:mahimahi
```
Once you download the image, you can run with. To learn more about the arguments used, refer to [Docker's documentation](https://docs.docker.com/engine/reference/run/) 
```
docker run --privileged \
--device /dev/net/tun -it \
-v /this/project/on/your/local/machine:/working/dir/inside/docker \
a8nguyen/oss-slu-congestion:mahimahi
```
Once inside the container, please change into a non-root sudo user. I have created one living inside the docker machine with `su a8nguyen`
Voila, now you can run pantheon inside the container!

### Pantheon Testing


Some pantheon testing and analysis commands
```bash
$ src/experiments/test.py local --all -f=20 --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/att.lte.driving' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving.down'
$ src/experiments/test.py local --all -f=1 -t=600 --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/att.lte.driving.2016' --uplink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving-2016.up' --downlink-trace='/usr/share/mahimahi/traces/ATT-LTE-driving-2016.down'
$ src/experiments/test.py local --all -f=1 -t=600 --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/tm.lte.driving' --uplink-trace='/usr/share/mahimahi/traces/TMobile-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/TMobile-LTE-driving.down '
$ src/experiments/test.py local --all -f=1 -t=600 --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/tm.lte.short' --uplink-trace='/usr/share/mahimahi/traces/TMobile-LTE-short.up' --downlink-trace='/usr/share/mahimahi/traces/TMobile-LTE-short.down'
$ src/experiments/test.py local --all -f=1 -t=600 --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/tm.umts.driving' --uplink-trace='/usr/share/mahimahi/traces/TMobile-UMTS-driving.up' --downlink-trace='/usr/share/mahimahi/traces/TMobile-UMTS-driving.down'
$ src/experiments/test.py local --all -f=1 -t=600 --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/vz.evdo.driving' --uplink-trace='/usr/share/mahimahi/traces/Verizon-EVDO-driving.up' --downlink-trace='/usr/share/mahimahi/traces/Verizon-EVDO-driving.down'
$ src/experiments/test.py local --all -f=1 -t=600 --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/vz.lte.driving' --uplink-trace='/usr/share/mahimahi/traces/Verizon-LTE-driving.up' --downlink-trace='/usr/share/mahimahi/traces/Verizon-LTE-driving.down' 
$ src/experiments/test.py local --all -f=1 -t=600 --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/vz.lte.short' --uplink-trace='/usr/share/mahimahi/traces/Verizon-LTE-short.up' --downlink-trace='/usr/share/mahimahi/traces/Verizon-LTE-short.down' 
```

### Pantheon Analysis

Some pantheon analysis commands
```bash
$ src/analysis/analyze.py --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/att.lte.driving'
$ src/analysis/analyze.py --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/att.lte.driving.2016'
$ src/analysis/analyze.py --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/tm.lte.driving'
$ src/analysis/analyze.py --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/tm.lte.short'
$ src/analysis/analyze.py --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/tm.umts.driving'
$ src/analysis/analyze.py --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/vz.evdo.driving'
$ src/analysis/analyze.py --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/vz.lte.driving'
$ src/analysis/analyze.py --data-dir='/home/pokorie/Documents/repos/mimic/log/pantheon/vz.lte.short'
```
