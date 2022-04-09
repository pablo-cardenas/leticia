# Leticia

Leticia is a python package that run the model. The slow functions (such us
dijkstra) are located in the c++ library
[libleticia](https://github.com/pablo-cardenas/libleticia).


## Installation

This package can be installed using pip and git.

```bash
$ pip install git+https://github.com/pablo-cardenas/leticia.git
```

Note: You have to install
[libleticia](https://github.com/pablo-cardenas/libleticia) to run this package.


## Usage

### Run the model

This package install a console script named `leticia`. Use the following
command to run the model:

```bash
leticia run $nrow $ncol $params $seed $output
```

For example

```bash
leticia run 20 20 "[-0,0.5,-0.5,-0.5]" 42 output.json
```

This command create a json file at `$output` (`output.json`) that can be
[uploaded to the server](#upload-to-the-server).

Note: You have to install
[libleticia](https://github.com/pablo-cardenas/libleticia) to run the `leticia`
command.


### Upload to the server

To upload the simulation to to the server, send the json by an HTTP POST
request to `https://leticia.pcardenasb.com/api/question/create`. With
[curl](https://curl.se), run the following command:

``` bash
curl \
  --request POST \
  --header "Content-Type: application/json"\
  --data @$output \
  "https://leticia.pcardenasb.com/api/question/create"
```


### Automate running and uploading

In addition, you can run a bash script to automate running the model and
uploading the simulation to the server.


```bash
#!/bin/bash
nrow=20
ncol=20
list_params=(
	"[-0,0.1,-0.1,-0.1]"
	"[-0,0.2,-0.2,-0.2]"
	"[-0,0.3,-0.3,-0.3]"
	"[-0,0.4,-0.4,-0.4]"
)

for params in ${list_params[@]}; do
    for seed in $(seq 42 44); do
        filename=${nrow}x${ncol}-${params}-${seed}.json
        echo $filename

        [ ! -f $filename ] && leticia run $nrow $ncol $params $seed $filename

        curl \
            --request POST \
            --header "Content-Type: application/json"\
            --data @$filename \
            "https://leticia.pcardenasb.com/api/question/create"
    done
done
```
