import requests
import hashlib
import sys

def request_api_data(char_for_query):
    url = 'https://api.pwnedpasswords.com/range/' + char_for_query
    response = requests.get(url)
    response.raise_for_status()
    return response

def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    #check password if it exists in API response
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    print(response)
    return get_password_leaks_count(response, tail)


def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was fount {count} times. Please change your password!')
        else:
            print(f'{password} was Not found. Good choice!')

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))

