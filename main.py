from openai import OpenAI
from openai import RateLimitError
import datetime
from PIL import Image
import requests
from io import BytesIO

from keys import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def is_room_description(description):
    # Use GPT to verify the description is of a room
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Does the following description generally describe, talk about, or ask to be shown a room? Yes or no."},
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
    modified_prompt = prompt + " --photorealistic"
    # Call the DALL-E API (simulation since actual DALL-E API might differ)
    response = client.images.generate(
        prompt=modified_prompt,
        n=1,
        size="1024x1024"
    )
    image_data = response.data[0]["url"]
    return image_data


def save_image(url, file_path):
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(file_path)


def main():
    while True:
        try:
            room_description = input("Please describe a simple room: ")
            if is_room_description(room_description):
                break
            else:
                print("That doesn't seem to describe a room. Please try again.")
        except RateLimitError as e:
            print("You've exceeded your API call quota. Please check your OpenAI account and try again later.")
            break  # Exit the loop and the program since you can't proceed without API access

    # image_url = generate_room_image(room_description)
    # timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # file_path = f"room_image_{timestamp}.png"
    # save_image(image_url, file_path)
    # print(f"Image saved as {file_path}")


if __name__ == "__main__":
    main()
