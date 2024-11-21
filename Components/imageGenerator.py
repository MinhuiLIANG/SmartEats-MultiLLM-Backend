from openai import OpenAI
import sys

sys.path.append("..")
from Components import entityExtractor
from DAO import dbops


def imageGenerate(food):
    client = OpenAI(api_key="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")
    # foods = entityExtractor.extractor_interface(passage=passage)
    prompt = '''
    Generate one image according to the following *food description* below. The image must be complete without any empty spaces. The image must be highly realistic, and should not resemble artwork in any way. The colors should be balanced, and the saturation should be natural. Use a natural background, such as a luminous kitchen or a dining table, instead of a whiteboard.
    *food description*: {food}
    '''.format(food=food)

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1792x1024",
        quality="standard",
        style="natural",
        n=1,
    )
    image_url = response.data[0].url
    # url = dbops.upload_image_to_firebase(uid, round + 'food' + order, image_url)

    return image_url

# text = 'Boiled shrimp dumplings with side of mixed vegetables'
# url = imageGenerate(text)
# url_pls = stops.upload_image_to_firebase('bcd', 'food1', url)
# print(url_pls)