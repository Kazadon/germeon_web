import segno
import qrcode_artistic
from ....config.env_config import WebConfig

print('hello')
base_url = WebConfig().BASE_SITE

print('Making qr...')
qrcode = segno.make(f'{base_url}greetings', error='h')
qrcode_artistic.write_artistic(qrcode, scale=6, background='./app/core/features/qr_maker/pasha_face.jpg', target='qrnew.png')
print('Done')