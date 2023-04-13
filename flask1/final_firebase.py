import random
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import time
# Khởi tạo Firebase App và Database Reference
cred = credentials.Certificate("filedatabase.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://argon-radius-377619-default-rtdb.firebaseio.com/'
})
ref = db.reference('random_number')
# Định nghĩa callback function
def on_update(event):
    print('New value:', event.data)
# Đăng ký callback function với database reference
ref.listen(on_update)
# Tạo số ngẫu nhiên từ 1 đến 10 và cập nhật liên tục lên Firebase
while True:
    rand_num = random.randint(0, 100)
    ref.set(rand_num)
    time.sleep(2)