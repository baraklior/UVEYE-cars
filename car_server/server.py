from flask import Flask, request, jsonify
from car_finder import CarFinder

app = Flask(__name__)

print("creating local cache")
cache_tester = CarFinder()


@app.route('/')
def hello():
    return "Hello UVEye!"


@app.route("/process", methods=['GET'])
def process():
    try:
        content = request.json
        print("processing request made: {}".format(content))
        car_finder = CarFinder()
        detected_cars, output_path = car_finder.process_one_photo(
            image_path=content["InputImage"], save_to_disk=content["DiagOutput"])
        
        print("--result--")
        result = {
            "Result": "SUCCESS",
            "Error": None,
            "DetectedCars": detected_cars,
            "DiagOutput": output_path
        }
        print(result)
        return jsonify(result)

    except Exception as e:
        # this is unsafe - must be changed in a production environment
        # and in general not a good idea
        result = {
            "Result": "FAILURE",
            "Error": e.__repr__(),
            "DetectedCars": None,
            "DiagOutput": None
        }
        return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, threaded=True)
