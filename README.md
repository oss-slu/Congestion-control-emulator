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

To use the LSTM feature run through the emulation and analysis described above. Then cd to the LSTM folder, if you did the other steps correctly there should be a data.csv file in that folder. You can specify the amount of epochs and how many predictions you want the LSTM to make past the emulation runtime

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



