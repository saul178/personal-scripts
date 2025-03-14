import subprocess


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


def download_video(url, browser, is_playlist=False):
    base_command = [
        "yt-dlp",
        "-f",
        "bv*[ext=mp4]+ba[ext=m4a]/b[ext=mp4]",
        "--merge-output-format",
        "mp4",
    ]

    if browser:
        base_command.extend(["--cookies-from-browser", browser])
    if is_playlist:
        output_format = "%(playlist_index)s - %(title)s.%(ext)s"
    else:
        output_format = "%(title)s.%(ext)s"

    base_command.extend(["-o", output_format])
    base_command.append(url)

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
            download_video(url, browser, is_playlist=False)
            break
        elif choice == "2":
            url = get_video_url(choice)
            browser = grab_supported_browser()
            download_video(url, browser, is_playlist=True)
            break
        elif choice == "3":
            print("exiting script, good bye!")
            break
        else:
            print("ERROR: invalid input try again or exit the script!")


if __name__ == "__main__":
    main()
