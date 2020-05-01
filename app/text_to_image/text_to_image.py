import requests
import w3lib.url


class TextToImageEngine:
    GENERATE_OPTIONS = {
        'maxWidth': 1280,
        'fontFamily': 'Consolas',
        'fontSize': 16,
        'lineHeight': 18,
        'margin': 20,
        'bgColor': '#2b3e50',
        'textColor': '#f8f8f2'
    }

    def __init__(self, service_url, service_port):
        self.service_url = service_url
        self.service_port = service_port

    def text_to_image_bytes(self, text):
        payload = {
            'text': text,
            'options': self.GENERATE_OPTIONS
        }

        endpoint = f'http://{self.service_url}:{self.service_port}/api/text-to-image'

        try:
            request = requests.post(endpoint, json=payload)
        except Exception:
            return None, 'error request to text to image API'
        else:
            response = request.json()

        if response['status'] == 'success':
            image_bytes = w3lib.url.parse_data_uri(response['dataURI']).data
            return image_bytes, response['message']
        elif response['status'] == 'fail':
            return None, response['errorMessage']
        else:
            return None, 'unknown response status'
