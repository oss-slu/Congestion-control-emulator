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

### LSTM Analysis

To use the LSTM feature run through the emulation and analysis described above. Then cd to the LSTM folder, if you did the other steps correctly there should be a data.csv file in that folder 

Run: 
```bash
$ /Congestion-control/LSTM python3 lstm_network_emulator.py

```
