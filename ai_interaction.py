import datetime
import requests
import os

from io import BytesIO
from openai import OpenAI
from openai import RateLimitError
from PIL import Image
from typing import Optional

from keys import OPENAI_API_KEY


client = OpenAI(api_key=OPENAI_API_KEY)

IMAGE_PATH: str = "dalle_generated_images"

def save_image(url, file_path):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(file_path)


def save_image(url, directory="dalle_generated_images") -> Optional[str]:
    if not os.path.exists(directory):
        os.makedirs(directory)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"room_image_{timestamp}.png"
    file_path = os.path.join(directory, file_name)
    try:
        response = requests.get(url)
        image = Image.open(BytesIO(response.content))
        image.save(file_path)
        print(f"Image saved as {file_path}")
        return file_path
    except Exception as e:
        print(f"An error occurred while saving the image: {e}")
        return None



def is_room_description(description):
    # Use GPT to verify the description is of a room
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[
                {"role": "system", "content": "Does the following description generally describe, talk about, or ask to be shown a room? It's ok if you are asked to show the room, or if the room is in the style of someone. Yes or no."},
                {"role": "user", "content": description}
            ],
            max_tokens=10
        )
        return "yes" in response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"An error occurred: {e}")
        return False



def generate_room_image(prompt):
    # Append "--photorealistic" to the prompt
    modified_prompt = prompt + "The room should be photorealistic yet simple, and there should be no text shown."
    # Call the DALL-E API (simulation since actual DALL-E API might differ)
    response = client.images.generate(
        model="dall-e-3",
        prompt=modified_prompt,
        size="1024x1024",
        quality="standard",
        n=1
    )
    image_data = response.data[0].url
    return image_data

def generate_image_path() -> str:
    """
    Asks the user to describe a room, then returns the image path to resulted generated room image
    """
    while True:
        try:
            room_description = input("Please describe a simple room: ")
            if is_room_description(room_description):
                print("A room is described, proceeding to image generation")
                break
            else:
                print("That doesn't seem to describe a room. Please try again.")
        except RateLimitError as e:
            print("You've exceeded your API call quota. Please check your OpenAI account and try again later.")
            break  # Exit the loop and the program since you can't proceed without API access

    image_url = generate_room_image(room_description)
    file_path = save_image(image_url, IMAGE_PATH)
    return file_path


if __name__ == "__main__":
    image_path = generate_image_path()
    print(image_path)
