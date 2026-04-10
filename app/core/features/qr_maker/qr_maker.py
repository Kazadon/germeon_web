import segno
import qrcode_artistic
from ....config.env_config import WebConfig

print('hello')
url = WebConfig().BASE_SITE

qrcode = segno.make(url, error='h')
qrcode_artistic.write_artistic(qrcode, scale=6, background='./app/core/features/qr_maker/catmeme.jpg', target='qr.png')
