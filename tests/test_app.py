from io import BytesIO
from urllib.parse import urlencode
import unittest
from app import application
class AppTests(unittest.TestCase):
    def test_pasted_html_is_escaped(self):
        data=urlencode({'ticket':'Site: <script>alert(1)</script>'}).encode()
        env={'REQUEST_METHOD':'POST','CONTENT_LENGTH':str(len(data)),'wsgi.input':BytesIO(data)}
        statuses=[]
        result=b''.join(application(env,lambda status,headers:statuses.append(status))).decode()
        self.assertEqual(statuses,['200 OK'])
        self.assertNotIn('<script>',result)
        self.assertIn('&lt;script&gt;',result)
if __name__=='__main__': unittest.main()
