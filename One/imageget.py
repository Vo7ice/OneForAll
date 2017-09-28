import requests
from PIL import Image
from io import BytesIO

img_src = 'http://image.wufazhuce.com/Fn8Zgp3FBOKd8X-2A_cKoU9sCRzK'

SUCCESS = 200


def main():
    response = requests.get(img_src)
    print('response:', response.status_code)
    if response.status_code == SUCCESS:
        image = Image.open(BytesIO(response.content))
        image.save('D:/Git/OneForAll/Fn8Zgp3FBOKd8X-2A_cKoU9sCRzK.jpg')


main()
