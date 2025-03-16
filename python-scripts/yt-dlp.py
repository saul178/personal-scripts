#!/usr/bin/env python3
import subprocess
import sys

WARNING_MSG = """\nWARNING: This option will grab the cookies from your browser if it's supported!
Using cookies may result in a temporary ban from sites like YouTube if abused too much!
You've been warned!!!\n"""


def get_video_url(choice):
    while True:
        if choice == "1":
            url = input("Enter the url for the video: ").strip()
        else:
            url = input("Enter the url for the playlist: ").strip()

        if url:
            return url
        else:
            print("ERROR: URL cannot be empty! Enter a valid URL!")


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
    display_supported_browsers = "Supported browsers are: " + ", ".join(
        supported_browsers
    )

    while True:
        print(display_supported_browsers)
        get_browser = input("Enter your supported browser: ").strip().lower()

        if get_browser in supported_browsers:
            return get_browser
        else:
            print("\nERROR: The browser you entered is not supported.")
            print(display_supported_browsers)
            retry = input("\nDo you want to retry? (y/n): ").strip().lower()
            if retry not in ["y", "yes"]:
                print(
                    "\nExiting script... A supported browser is requied for paid content downloads\n "
                )
                sys.exit(1)


def yt_dlp_command():
    base_command = [
        "yt-dlp",
        "-f",
        "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "--merge-output-format",
        "mp4",
    ]
    return base_command


def download_video(url, is_playlist=False):
    base_command = yt_dlp_command()

    if is_playlist:
        output_format = "%(playlist_index)s - %(title)s.%(ext)s"
    else:
        output_format = "%(title)s.%(ext)s"

    base_command.extend(["-o", output_format])
    base_command.append(url)

    print(base_command)
    subprocess.run(base_command)


def download_paid_video(browser, url, is_playlist=False, is_paid_content=False):
    base_command = yt_dlp_command()

    # brave browser is weird on linux, requires gnomekeyring to grab cookies from the browser.
    # set warning that by using cookies you may end up ip banned for a bit.
    # so far edge and chrome just work, brave is the weird one here even though it's chromium based.
    if browser != "brave" and is_paid_content:
        base_command.extend(["--cookies-from-browser", browser])
    else:
        base_command.extend(["--cookies-from-browser", browser + "+gnomekeyring"])

    if is_playlist:
        output_format = "%(playlist_index)s - %(title)s.%(ext)s"
    else:
        output_format = "%(title)s.%(ext)s"

    base_command.extend(["-o", output_format])
    base_command.append(url)

    print(base_command)
    subprocess.run(base_command)


def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).strip().lower()
        if user_input in valid_options:
            return user_input
        else:
            print("ERROR: invalid input try again or exit the script!")


def prompt():
    try:
        while True:
            print(
                """
            What video are we downloading?
                Enter [1] for a single video
                Enter [2] for a playlist
                Enter [3] to exit
            """
            )
            choice = get_valid_input("Enter: ", ["1", "2", "3"])
            if choice == "3":
                print("Exiting script, good bye!")
                break

            is_paid_content = get_valid_input(
                "Is this paid content? (y/n): ", ["y", "yes", "n", "no"]
            )

            if is_paid_content == "y" or is_paid_content == "yes":
                print(WARNING_MSG)
                browser = grab_supported_browser()
                url = get_video_url(choice)
                download_paid_video(
                    browser, url, is_playlist=(choice == "2"), is_paid_content=True
                )
                break
            else:
                url = get_video_url(choice)
                download_video(url, is_playlist=(choice == "2"))
                break
    except KeyboardInterrupt:
        print("\nCanceled script... \nExiting...")
        sys.exit(0)
    finally:
        print("Script finished.")


def main():
    prompt()


if __name__ == "__main__":
    main()
