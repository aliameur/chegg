import env
import random
from urllib.parse import urlparse


def get_proxy_and_account() -> tuple[str, tuple[str, str]]:
    """
    Randomly choose 1 of available proxy & email pair to use with homeworkify.
    :return: tuple of proxy details and account details
    """
    i = random.randint(0, len(env.PROXY_LIST) - 1)
    return env.PROXY_LIST[i], env.ACCOUNT_LIST[i]


def convert_proxy(proxy: str) -> str:
    """
    Format proxy correctly for use with rest of program.
    :param proxy: proxy in ip:port:user:pass format
    :return: proxy in http://user:pass@ip:port format
    """
    ip, port, username, password = proxy.split(':')
    return f"http://{username}:{password}@{ip}:{port}"


def convert_account(account: str) -> tuple[str, str]:
    """
    Format account correctly for use with rest of program.
    :param account: account in email:pass format
    :return: tuple of email and password
    """
    email, password = account.split(':')
    return email, password


def check_domain(link: str, domain: str) -> bool:
    """
    Check if link has a given domain and return True or False
    :param link: link to check
    :param domain: domain to check against (can have www. or not)
    :return: True or False
    """
    parsed_url = urlparse(link)
    if parsed_url.netloc == domain:
        return True
    else:
        return False


def main():
    choice = int(input("Proxy env formatter (1)\n"
                       "Account env formatter (2)\n"))
    # format proxy
    if choice == 1:
        proxy_list = []
        while True:
            pre = input("Input proxy: ")
            if pre == "":
                break
            try:
                post = convert_proxy(pre)
                proxy_list.append(post)
            except Exception as e:
                print(f"Exception: {e} \n"
                      f"Most likely wrongly pasted proxy")
        print(proxy_list)
    # format account
    if choice == 2:
        account_list = []
        while True:
            pre = input("Input account: ")
            if pre == "":
                break
            try:
                post = convert_account(pre)
                account_list.append(post)
            except Exception as e:
                print(f"Exception: {e} \n"
                      f"Most likely wrongly pasted account")
        print(account_list)


if __name__ == "__main__":
    main()
