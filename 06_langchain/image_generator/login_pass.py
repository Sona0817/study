import yaml
import bcrypt

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')

# 사용자 정보 및 기타 정보 생성
credentials = {
    'credentials': {
        'usernames': {
            'user1': {
                'name': 'user1',
                'password': hash_password('pass1234')
            },
            'admin': {
                'name': 'admin',
                'password': hash_password('admin1234')
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'random_signature_key',
        'name': 'random_cookie_name'
    }
}

# YAML 파일로 저장
with open('credentials.yaml', 'w') as file:
    yaml.dump(credentials, file)
