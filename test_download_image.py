import unittest
from unittest.mock import patch, mock_open
from download_images import download_the_image

class TestDownloadImage(unittest.TestCase):

    @patch('download_images.requests.get')
    @patch('download_images.open', new_callable=mock_open)
    @patch('download_images.os.path.exists')
    @patch('download_images.shutil.copyfileobj')
    def test_download_image(self, mock_copyfileobj, mock_exists, mock_open, mock_get):
        mock_exists.return_value = False
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.raw = 'image data'

        download_the_image('test_keyword', 'http://example.com/image.jpg', 'test_title')

        mock_open.assert_called_once_with('./images/test_keyword/test_title.jpg', 'wb')
        mock_copyfileobj.assert_called_once()

if __name__ == '__main__':
    unittest.main()