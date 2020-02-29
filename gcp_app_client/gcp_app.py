import os
import warnings
warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)
import tensorflow as tf
import numpy as np
from pathlib import Path
from oauth2client.client import GoogleCredentials
import googleapiclient

PROJECT_ID = 'speero-268500'
MODEL_NAME = 'sound_repetition_model'

BATCH_SIZE = 1
imgs_per_seq = 39
img_h = 172
img_w = 128
img_c = 1

AUTOTUNE = tf.data.experimental.AUTOTUNE
CLASS_NAMES = np.array(["no_stutter", "sound_repetition"])
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'speero-aiplatform-service-account.json')
def predict_json(project, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the AI Platform Model is deployed.
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    # Create the AI Platform service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
    service = googleapiclient.discovery.build('ml', 'v1')
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

def get_label(file_path):
    parts = tf.strings.split(file_path, os.path.sep)
    return parts[-2] == CLASS_NAMES

def decode_img(file_path):
    img = tf.io.read_file(file_path)
    # convert the compressed string to a 3D uint8 tensor
    img = tf.image.decode_jpeg(img, channels=1)
    # Use `convert_image_dtype` to convert to floats in the [0,1] range.
    img = tf.image.convert_image_dtype(img, tf.float32)
    # resize the image to the desired size.
    img = tf.reshape(img, (1, imgs_per_seq, img_w, img_h, img_c))
    return img

def process_path(file_path):
    label = get_label(file_path)
    img = decode_img(file_path)
    return img, label

def main():

    data_dir = "data/*/*"

    list_ds = tf.data.Dataset.list_files(data_dir)
    labeled_ds = list_ds.map(process_path, AUTOTUNE)

    for img, label in labeled_ds.take(1):
        print(img.numpy().tolist())
        # # print(img)
        # instances = img.numpy().tolist()
        # predictions = predict_json(PROJECT_ID, MODEL_NAME, instances)
        # print(predictions)

if __name__ == "__main__":
    main()