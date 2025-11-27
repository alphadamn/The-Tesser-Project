# The Tesser Project
D0nat10ns are welcome at: tr1qa5u8gjka4pkjhc9zxuxtj6u3fz36qt89vdpjkk or <a href="https://www.buymeacoffee.com/the.tesser.project"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=&slug=the.tesser.project&button_colour=FFDD00&font_colour=000000&font_family=Lato&outline_colour=000000&coffee_colour=ffffff" /></a>

## Bug Bounty
Bugs submitted to the email Oscar.Liu@student.isb.cn or lzh1117@icloud.com are given a incentive of 10000-200000 Tessers respectively, corresponding to the bug submitted. 
### How to
If you find a bug, send an email to one of the two addresses in the format below: 
```
Name: {Your Perfered Name} ({put your github username here inside parentheses })
Bug Description: {Explain what your bug does, its potential, rate the severity of the bug yourself (note that this would not affect the resulting incentive), HOW TO REPRODUCE (must have, BUG MUST BE REPRODUCIBLE, OR ELSE WOULD BE MARKED INVALID)}
Time Found: {YYYY/MM/DD}
Address: {Your tesser address for receiving the rewards}
```
### How long? 
Since we would need to reproduce the bug, note that the reward might take hours or weeks to arrive. 

## Installation
### Building from source
```
git clone https://github.com/alphadamn/The-Tesser-Project.git tesser
cd tesser
```
#### Requirements 
To build from source, you would need to have the required packages installed. 
##### On Mac (requires homebrew to be installed, and assuming that Qt6 libraries are already installed correctly)
```
brew install llvm curl xorgproto libsndfile sqlite jansson jasper jpeg-turbo jpeg-xl openssl openjpeg capnp cmake boost autoconf automake
```
If you want to use the tor/onion interface: 
```
brew install tor
```
##### On other platforms
It's basicly the same packages, but for linux it's lib...-dev for some. 
#### Configuring/Building
To configure the build: `cmake -DCMAKE_BUILD_TYPE=Debug -DBUILD_GUI=ON -S {put your project path here (without brackets) eg. /Users/me/Desktop/tesser} -B {put your project path here (without brackets) eg. /Users/me/Desktop/tesser}/cmake-build-debug`
To build: `cmake --build {put your project path here (without brackets) eg. /Users/me/Desktop/tesser}/cmake-build-debug --target all -j {how much cores your CPU has, eg. 8}`
After the command returns, you should be able to see your binaries located at cmake-build-debug/bin
There might be a case that your binaries are named bitcoin... instead tesser..., if so, just simply rename them with `mv bitcoin... tesser...` for each of them. 

### Download from releases
## Running
Most arguments are the same with Bitcoin Core. 
### Example
```
cd cmake-build-debug/bin
./tesserd #For no gui
or
./tesser-qt #With gui
```
