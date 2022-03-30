# Pantheon of Congestion Control [![Build Status](https://travis-ci.org/StanfordSNR/pantheon.svg?branch=master)](https://travis-ci.org/StanfordSNR/pantheon)
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
git clone https://github.com/Principe92/pantheon.git
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

### 2. C++ errors during src/experiments/setup.py
Some of the warnings were marked as errors during some set ups. So, I manually edited some of the third_party files as follows:

In [third_party/pantheon-tunnel/configure.ac](third_party/pantheon-tunnel/configure.ac) change line 12 to:
```text
PICKY_CXXFLAGS="-pedantic -Wall -Wextra -Weffc++ -Wno-error"
```

In [third_party/genericCC/makefile](third_party/genericCC/makefile) change line 4 to:
```text
CXXFLAGS := -DHAVE_CONFIG_H -std=c++11 -pthread -pedantic -Wall -Wextra -Weffc++ -Wno-error -fno-default-inline -g -O2 -fPIC
```

In [third_party/verus/src/verus_server.cpp](third_party/verus/src/verus_server.cpp) change line 187 to:
```cplusplus
timer.expires_from_now (boost::posix_time::milliseconds(int(timeouttimer)));
```

Also on line 649, set it to:
```cplusplus
timer.expires_from_now (boost::posix_time::milliseconds(int(timeouttimer)));
```

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