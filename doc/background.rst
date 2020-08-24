Background
==========

What is Janken?
---------------

*Janken* (or じゃんけん) is the Japanese term for the familiar game of
"rock paper scissors"! Since our tool is meant to classify images of hand
gestures indicating one of rock, paper, or scissors, we've borrowed the
name! Want to teach a computer how to understand *Janken*? Try Janken!

How does Janken work?
---------------------

Janken is built around a trained convolutional neural network, or CNN,
specifically intended to classify images of hand gestures as being either
rock, paper, or scissors.

When applying CNNs to image classification problems, a common technique is
to employ a pre-trained model: an existing model architecture--as opposed to
a new design--already trained on a large dataset, typically for a large-scale
classification task. This technique is called *transfer learning*, based on
the idea that, for models trained on large and general datasets, the features
learned by those models will be general to images of the visual world, and
therefore *transferable* to other problems and applications.

The model behind Janken was trained this way, using the
`VGG16 Model <https://www.tensorflow.org/api_docs/python/tf/keras/applications/VGG16>`_
built into TensorFlow's high-level modeling API, Keras. Its weights were
pre-trained on `ImageNet <www.image-net.org>`_, a project and image database
used by researchers around the world.

Janken uses its underlying model to predict the classification of any new
hand gesture image you show it! Technically, its model will predict
*the probabilities* of an image being rock, paper, or scissors. Janken
reports those probabilities, and the label it would assign--the most probable
of the three. For example, given input image ``testpaper01-00.png``:

.. figure:: /images/testpaper01-00.png
   :alt: picture of rock-paper-scissors "paper" gesture

   Example hand gesture image ``testpaper01-00.png``, a player using "paper".

Janken will output the following::

   +----------------------+-------------+----------+-------------+---------+
   | image                |        rock |    paper |    scissors | label   |
   +======================+=============+==========+=============+=========+
   | .\testpaper01-00.png | 3.96574e-06 | 0.98432  | 0.015676    | paper   |
   +----------------------+-------------+----------+-------------+---------+
