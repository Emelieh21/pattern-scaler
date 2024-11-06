# Pattern Scaler

## How to use

Install poetry:

```
pip3 install poetry
```

Install the dependencies for the repository:

```
poetry install
```

## Run as API

Launch the API with

```
poetry run ./run.sh
```

You can make a post request to the API with an input file like this with curl:

```
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@sweater-top.png" "http://localhost:8001/scale_pattern?desired_height=46" -o result.pdf
```

In the logs of the API you can see the following information:

```
Current size of image: 6.311912623825248 by 13.385826771653544 cm
Scale factor height: 3.4364705882352937
New size of image: 21.678943357886716 by 45.999491998984 cm
```

With the scale factor height we can scale the bottom part of the pattern the same way by calling:

```
curl -X POST -H "Content-Type: multipart/form-data" -F "file=@sweater-bottom.png" "http://localhost:8001/scale_pattern?scale_factor_height=3.4364705882352937" -o result-bottom.pdf
```

There always needs to be either a `desired_height` (or `desired_weight`) or a `scale_factor_height` (or `scale_factor_weight`) specified for the API call to work. 
