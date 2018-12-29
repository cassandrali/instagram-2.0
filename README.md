# instagram-2.0

Instagram 2.0 is a Flask app that allows you to upload images with captions, ultmately creating an image feed. Hashtags are automatically generated for each image using TensorFlow's [Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection). 

## Getting Started

To run the application, cd to the project directory and run the following commands from the command line. 

```
pip install -r requirements.txt
python run.py
```

Navigate to `localhost:5000`.

## Built With
* [Flask](http://flask.pocoo.org/)
* [Bootstrap](https://getbootstrap.com/)
* [TensorFlow](https://www.tensorflow.org/)
