import subprocess
import browser_cookie3 as bc
import tempfile
from urllib.parse import urlparse


def get_video_url(choice):
    if choice == "1":
        return input("Enter the url for the video: ").strip()
    else:
        return input("Enter the url for the playlist: ").strip()


def grab_supported_browser():
    supported_browsers = [
        "brave",
        "chrome",
        "edge",
        "firefox",
        "opera",
        "safari",
        "vivaldi",
        "whale",
    ]
    print("Supported browsers are: ", ", ".join(supported_browsers))

    get_browser = input("Enter your supported browser: ").strip().lower()
    if get_browser in supported_browsers:
        return get_browser
    else:
        print(
            """
            WARNING: the browser you put in is not supported, this script will continue without extracting your browsers cookies! Which means that membership content that you are subribed to will be ignored!"
            """
        )


def get_domain(url):
    try:
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        return domain
    except Exception as e:
        print(f"ERROR: failed to extract domain from URL: {e}")
        return None


# this function can be refactored
def get_cookies(browser, domain):
    try:
        match browser.lower().strip():
            case "chrome":
                cookies = bc.chrome()
            case "brave":
                print("found brave!!")
                cookies = bc.brave()
            case "edge":
                cookies = bc.edge()
            case "firefox":
                cookies = bc.firefox()
            case "operagx":
                cookies = bc.opera_gx()
            case "vivaldi":
                cookies = bc.vivaldi()
            case "safari":
                cookies = bc.safari()
            case "w3m":
                cookies = bc.w3m()
            case "lynx":
                cookies = bc.lynx()
            case "opera":
                cookies = bc.opera()
            case "librewolf":
                cookies = bc.librewolf()
            case _:
                print("Unsupported browser, defaulting to no authentication!")
                return None

        cookie_str = ""
        normailized_domain = domain.lstrip("www.")
        cookie_file = tempfile.NamedTemporaryFile(
            delete=True,
            mode="w",
            newline="",
            dir="./",
            prefix="cookies_",
            suffix=".txt",
        )
        cookie_file_path = cookie_file.name

        for cookie in cookies:
            cookie_domain = cookie.domain.lstrip("www.")
            if normailized_domain in cookie_domain:
                cookie_str += f"{cookie.name}={cookie.value}"

        cookie_file.write(cookie_str)
        cookie_file.close()

        return cookie_file_path

    except Exception as e:
        print(f"ERROR: failed to extract cookies {e}")
        return None


def download_video(url, browser, cookies, is_playlist=False):
    base_command = [
        "yt-dlp",
        "-f",
        "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "--merge-output-format",
        "mp4",
    ]

    if browser and cookies:
        base_command.extend(["--cookies", cookies])

    if is_playlist:
        output_format = "%(playlist_index)s - %(title)s.%(ext)s"
    else:
        output_format = "%(title)s.%(ext)s"

    base_command.extend(["-o", output_format])
    base_command.append(url)

    print(base_command)
    subprocess.run(base_command)


def main():
    print(
        """
    What video are we downloading?
    Enter [1] for a single video
    Enter [2] for a playlist
    Enter [3] to exit
    """
    )

    while True:
        choice = input("Enter: ").strip()
        if choice == "1":
            url = get_video_url(choice)
            browser = grab_supported_browser()
            domain = get_domain(url)
            cookies = get_cookies(browser, domain)
            download_video(url, browser, cookies, is_playlist=False)
            break
        elif choice == "2":
            url = get_video_url(choice)
            browser = grab_supported_browser()
            domain = get_domain(url)
            cookies = get_cookies(browser, domain)
            download_video(url, browser, cookies, is_playlist=True)
            break
        elif choice == "3":
            print("exiting script, good bye!")
            break
        else:
            print("ERROR: invalid input try again or exit the script!")


if __name__ == "__main__":
    main()
