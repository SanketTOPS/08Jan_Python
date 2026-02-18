import qrcode

url="https://www.tops-int.com/"

qr=qrcode.make(url)
qr.save("tops.png")