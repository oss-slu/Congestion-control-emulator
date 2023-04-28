# ⚙️ Network Congestion Control Emulator
1. [Software Overview](#software-overview)
2. [Disclaimer](#disclaimer)
3. [Installation](#installation)
    1. [Operating System Prerequesites](#operating-system-prerequesites)
    2. [Clone the Project](#clone-the-project)
    3. [Evaluation Module](#install-evaluation-module)
    4. [Emulation Moddule](#install-emulation-module)
    5. [Docker Usage](#docker-usage)
    <!--6. [Kernel Configuration Notes](#kernel-configuration)-->
4. [Usage](#usage)
   
----
## Software Overview

Congestion Control (CC) Emulator is the CLI (command-line interface) application that allows users to define network conditions with (network delays, losses and links) to emulate and run congestion control algorithms in such user-defined environment. The software will output analytics that summarize the performance of all tested algorithms. The software supports real-time kernel tracing with eBPF/XDP and traffic prediction (right now based on throughput variable using Long Short Term Memory (LSTM) architecture).


## Disclaimer
- The benchmarking system is forked from [Pantheon](https://github.com/StanfordSNR/pantheon).
- The emulation system is based on [mahimahi](http://mahimahi.mit.edu/).

---
## Installation

### Operating System Prerequesites
To utilize the emulation and real-time traacing features, a Linux kernel version >= 4.1 is required.
- Follow this [guide](https://github.com/iovisor/bcc/blob/master/INSTALL.md) to configure your kernel and environments for eBPF [^1]
- The current emulation system is supported by Debian and Fedora. Please consult the [Docker section](#docker-usage) for full list of dependedencies.
[^1]: As of now 04/27/2023 we recommend you build from source instead of using binary releases

### Clone the Project
```
git clone https://github.com/oss-slu/Congestion-control-emulator.git
```
### Install evaluation module
```
cd Congestion-control-emulator/src/
```
#### Link CC schemes to your project
We use source implementations of the congestion control algorithms. Please link the submodules once you clone our project. Learn more about submodule [here](https://github.blog/2016-02-01-working-with-submodules/)
```
git submodule update --init --recursive 
```
#### Global Installation
If you are uncomfortable with global installation, we provide Docker images for you to use. Please consult the [Docker section](#docker-usage) 
Some dependencies require global installations to your system. You can do so with (*note well this script is Debian-based*):
```
sh tools/install_deps.sh
```
#### Set up Dependencies for CC schemes
If you use our Docker image, please skip this step
```
src/experiments/setup.py --install-deps (--all | --schemes "<cc1> <cc2> ...")
```

#### Set up CC schemes in your system
If you use our Docker image, please skip this step
```
src/experiments/setup.py [--setup] [--all | --schemes "<cc1> <cc2> ..."]
```

### Install emulation module
If you use our Docker please skip this step.
```
cd shell
```

#### Build emulation shells
```
[path_of_the_shell]
./autogen.sh
./configure
make
sudo make install
```

### Docker Usage
Getting the right environment for Pantheon can be tricky. So as of now (2/23/23), we have a docker image that holds all dependencies. Any contributions to make more docker images so our application can be supported in many Linux-based platforms is appreciated.

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
Once inside the container, please change into a non-root sudo user. I have created one living inside the docker machine with `su nonroot`
Voila, now you can run pantheon inside the container!

<!--### Kernel Configuration
If you can't configure the kernel yourself and run into problem installing eBPF on your system. Please let me know, we have an OS image (Fedora).-->
---
## Usage
### Run Experiment [^2]
You can run CLI arguments or use a config files to run the program. `src/experiments/test.py -h`. When you run the program, kernel tracing will log in text files [^3]. Summary of full local options is below:
[^2]: As of now (4/27/23) kernel tracing only supports local mode.
[^3]: As of now (4/27/23) TCP information is logged in `tcp_trace.txt`

```src/experiments/test.py (local|remote) -f=<flow-rate-int> (default 1) -t=<duration-int>(default 30) --interval=<interval-between-flows-int>(default 0) --run-times=<int> (default 1) --start-run-id=<int> --random-order --data-dir=<output/path/for/results> --uplink-trace=<uplink/trace/path> --downlink-trace=<downlink/trace/path> (--all | --schemes "<cc1> <cc2> ...")```

To run analysis
```
src/analysis/analyze.py --data-dir <directory/specified/in/last/step>
```

### LSTM Analysis

To use the LSTM feature run through the emulation and analysis described above, cd to the LSTM folder, if you did the other steps correctly there should be a data.csv file in that folder. You can specify the amount of epochs and how many predictions you want the LSTM to make past the emulation runtime

make sure you have python libraries pandas and scikit-learn installed

Run: 
```bash
$ /Congestion-control/LSTM python3 lstm_network_emulator.py --epochs "# of epochs" --predictions "# of predictions" 

```

## Metrics 

Three metrics are used to test the accuracy of the model: 

1. Mean Squared Error (MSE):
MSE measures the average squared difference between the predicted values and the actual values. A lower MSE indicates better model performance. However, since the errors are squared, MSE is sensitive to outliers and larger errors have a disproportionally larger impact on the overall metric.
Formula: MSE = (1/n) * Σ(actual_i - predicted_i)^2

2. Root Mean Squared Error (RMSE):
RMSE is the square root of MSE. It is also a measure of the average difference between predicted and actual values, but it is in the same unit as the target variable, making it more interpretable. Like MSE, a lower RMSE value indicates better model performance. RMSE is sensitive to outliers, similar to MSE.
Formula: RMSE = √(MSE)

3. Mean Absolute Error (MAE):
MAE is the average of the absolute differences between the predicted and actual values. It measures the average magnitude of the errors in the predictions without considering their direction. Unlike MSE and RMSE, MAE is not sensitive to outliers, as it does not square the errors. A lower MAE value indicates better model performance.

All 3 are printed at the end of the script

## State of the LSTM 

At present, the LSTM model performs well on a limited number of trace files, such as Verizon LTE and T-Mobile LTE. To improve the model's performance, several adjustments have been experimented with, including:

1. n_input: Increasing the n_input value provides the LSTM's short-term memory with more data to work with. This value should be adjusted depending on the network emulation runtime (e.g., for a 60-second runtime, use n_input = 10).

3. epochs: Adjusting the number of epochs can be time-consuming but is essential for determining the model's accuracy. Adjust the epoch count to best fit your emulation data.

4. batch_size: batch_size can be modified to help the model fit your data more effectively (optimal results are typically found between 30 and 100).

5. dropout: Adding dropout layers was attempted, but it resulted in constant predictions.

6. activation function: Both tanh and sigmoid activation functions work well for LSTM models. However, the tanh function seems to yield better results with our current model and data.

7. Multiple RNN Layers: My attempt to add more LSTM layers were unsuccessful in improving predictions. Future exploration could involve using other types of RNN layers, such as GRU, or even combining LSTM and GRU layers.

There is still much more work to be done to improve the LSTM's accuracy and make it compatible with all trace files and various emulation runtimes. The most successful model so far has been for the T-Mobile LTE trace file with an emulation runtime of 60 seconds. The corresponding data is saved in TMobile60Data.csv. By changing the file path from data.csv to TMobile60Data.csv and running the model with 120 epochs, a relatively accurate model can be obtained. Below is an example output from these settings:

<img width="613" alt="image" src="https://user-images.githubusercontent.com/115129576/234693822-b9899b70-767f-4c19-a5c1-40ea2b52385d.png">



