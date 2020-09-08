"""The Janken package!

Functions
---------

.. autofunction:: janken.predict

"""

import itertools
import pathlib

from typing import List, Tuple

import pandas as pd
import tensorflow as tf


def predict(
    images: List[str],
    labels: Tuple[str, str, str] = ('rock', 'paper', 'scissors')):
    """Handle prediction for a list of input `images`.

    Arguments:
        images: The input images to classify.
        labels: The labels to apply as part of classification. Optionally
            modifiable to support other expressions of equivalent meaning
            to rock, paper, and scissors (e.g. guu, paa, choki).

    """

    tf.config.set_visible_devices([], 'GPU')
    tf.get_logger().setLevel('WARNING')

    model = pathlib.Path(__file__).parent.joinpath('data', 'janken_take_10.h5')
    model = tf.keras.models.load_model(model)

    batch_size = 16
    batches = 1 + len(images) // batch_size

    def batcher(iterable, batch_size=batch_size, fillvalue=None):
        args = [iter(iterable)] * batch_size
        return itertools.zip_longest(*args, fillvalue=fillvalue)

    predictions = []
    for batch_num, batch in enumerate(batcher(images)):
        image_pngs = []
        for image in batch:
            if not image:
                continue
            with open(image, 'rb') as imgf:
                image_tensor = tf.convert_to_tensor(imgf.read())
            image_png = tf.io.decode_png(image_tensor, channels=3)
            image_png = tf.cast(image_png, tf.float32) / 255.
            image_pngs.append(tf.expand_dims(image_png, axis=0))

        image_pngs = tf.concat(image_pngs, axis=0)

        print(f'Running batch {batch_num + 1} of {batches}')
        predictions.append(model.predict(image_pngs))

    predictions = tf.concat(predictions, axis=0)
    predicted_labels = [
        labels[idx] for idx in tf.math.argmax(predictions, axis=1)
    ]
    data = {'image': images}
    data.update({labels[idx]: predictions[:, idx] for idx in range(3)})
    data['label'] = predicted_labels
    df = pd.DataFrame(data=data)
    print(df.to_markdown(tablefmt='grid', index=False))
