## Run with Docker
docker run --rm -d -p 80:80 -v <some_folder>:/mnt/input -v<some_folder>:/mnt/output liorbarakprivate/uveye-cars

## Usage 

the server runs on port 80 and accepts get requests to http://0.0.0.0:80/process
they must contain the following json:
{
"InputImage”: "/path/to/image”,
"DiagOutput:”: true/false
}



## expected output 
{
    "Result”: "SUCCESS”/”FAILURE”,
    "Error”: null/”failure details”,
    "DetectedCars”:
    [
        {
        "Confidence”: 0.8,
        "BoundingBox”: [x1, y1, x2, y2]
        }
        ...
        ...
    ],
    "DiagOutput”: "/path/to/diag/output”
}

