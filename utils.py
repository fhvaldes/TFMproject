import json

from PIL import Image
from robobopy.utils.BlobColor import BlobColor

from behaviour_mod.sharedclass import SharedClass


# Leer de un archivo json
def update_dict(key, value, path='data.json'):
    with open(path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Actualizar el valor de una clave
    data[key] = value

    # Escribir en un archivo json
    with open(path, 'w', encoding='utf-8') as file:
        json.dump(data, file)

    return data


def read_dict():
    path = 'data.json'
    with open(path, 'r', encoding='utf-8') as file:
        try:
            data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Error: File {path} not found.")
            return {}  # Return an empty dictionary
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {}  # Return an empty dictionary
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {}  # Return an empty dictionary   


def str_to_blob(obj_string):
    obj_name, attr_name = obj_string.split('.')
    return getattr(BlobColor, attr_name)


import base64

import pyautogui
import os
from PIL import ImageGrab


def take_screenshot_sim():
    # Capture the current region under the mouse cursor

    # Save the screenshot to a file
    current_dir = os.getcwd()

    # screenshot a part of the screen

    # Obtener las dimensiones de la pantalla
    screen_width, screen_height = pyautogui.size()

    # Definir las coordenadas de la esquina inferior izquierda para una captura de 500x500
    left = 0
    top = screen_height - 524
    width = 382
    height = 524

    # Tomar la captura de pantalla de la región especificada
    screenshot = ImageGrab.grab(bbox=(left, top, left + width, top + height))

    files = os.listdir(current_dir)
    png_files = [file for file in files if file.endswith(".png")]
    screenshot.save(f"images/screenshot{len(png_files) + 1}.png")

    # Leer la imagen original
    # imagen_original = cv2.imread("screenshot.png")

    # Redimensionar la imagen a 512x512
    # imagen_redimensionada = cv2.resize(imagen_original, (512, 512))

    # Guardar la imagen redimensionada
    # cv2.imwrite("screenshot.png", imagen_redimensionada)


def take_screenshot():
    print("Showing images")
    # rob.setLaneColorInversion(False)
    i = 0
    last_ts = 0
    current_dir = os.getcwd()
    width = 365
    height = 365
    frame, timestamp, sync_id, frame_id = SharedClass.videoStream.getImageWithMetadata()
    files = os.listdir(current_dir)
    png_files = [file for file in files if file.endswith(".png")]
    frame = Image.fromarray(frame)
    frame = frame.resize((width, height))
    frame.save(f"images/screenshot{len(png_files) + 1}.png")


def delete_png_files():
    # Save the screenshot to a file
    folder_path = "images/"
    # Walk through the directory tree
    for root, _, files in os.walk(folder_path):
        for file in files:
            # Check if the file is a PNG file
            if file.endswith(".png"):
                # Get the full path to the file
                file_path = os.path.join(root, file)
                # Try to delete the PNG file
                try:
                    os.remove(file_path)
                except PermissionError:
                    print(f"Could not delete file {file_path} because it is being used by another process.")


def load_image():
    # Load the image from the file
    img_list = []
    current_dir = os.getcwd()
    for root, _, files in os.walk(current_dir):
        for file in files:
            # Check if the file is a PNG file
            if file.endswith(".png"):
                # Get the full path to the file
                file_path = os.path.join(root, file)
                img_list.append(encode_image(file_path))
    img_list = sorted(img_list, reverse=True)[0:10] if img_list else []
    return sorted(img_list, reverse=True)


# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        image = base64.b64encode(image_file.read()).decode('utf-8')
        image_file.close()
        return image
