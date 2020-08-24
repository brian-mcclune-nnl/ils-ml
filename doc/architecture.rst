The Janken model architecture
=============================

Janken does not feature a custom model architecture; instead, it uses
TensorFlow's
`VGG16 Model <https://www.tensorflow.org/api_docs/python/tf/keras/applications/VGG16>`_
as a convolutional base, excluding the three fully-connected layers at the top
of the complete network. Its classifier head is composed of two dense layers: a
Rectified Linear Unit (ReLU) activation layer, and a softmax activation layer which
outputs a probability distribution over its different classes, with a dropout layer
between:

.. code-block:: python

   # VGG16 convolutional base
   conv_base = tf.keras.applications.VGG16(
       weights='imagenet',
       include_top=False,
       input_shape=(300, 300, 3),
   )

   model = models.Sequential()
   model.add(conv_base)

   # Custom classification layers
   model.add(tf.keras.layers.Flatten())
   model.add(tf.keras.layers.Dense(
       128,
       activation='relu',
       kernel_regularizer=tf.keras.regularizers.l2(0.001),
   ))
   model.add(tf.keras.layers.Dropout(0.5))
   model.add(tf.keras.layers.Dense(3, activation='softmax'))

The dropout layer randomly sets input units to 0 with a frequency of ``0.5``
at each step during training, which helps prevent overfitting. It only applies
when training; no values are dropped during inference.

Ultimately this means that, for every image, the Janken network will output
a length-3 vector whose elements are the probabilities that the image
belongs to each of the "rock", "paper", and "scissors" classes. The three
scores will add up to 1.