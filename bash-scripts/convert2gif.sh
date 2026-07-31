#!/bin/bash
function usage() {
    cat << EOF
conver2gif Usage:
	convert2gif [video file] Converts a video to GIF (default)
	convert2gif -s [seconds] [video file] Slices a video by nth seconds
	convert2gif -w [video file] Converts a video to an animated webp

Options:
    -s, --slice     Slice video
    -w, --wallpaper Covert video to animated webp wallpaper
    -h, --help      Display this help message
EOF
}

function sliceVideo() {
	defaultSlice=5
	slice="$1"
	if [[ ! "$slice" =~ ^-?[0-9]+$ ]]; then 
		slice="$defaultSlice"
		printf "\n\e[0;33m[WARN]\e[0m Invalid choice defaulting to $defaultSlice seconds\n"
	fi
	videoFile="$2"

	if [[ -z "$videoFile" || ! -f "$videoFile" ]]; then 
		printf "\n\e[0;31m[ERROR]\e[0m missing video file or video file doesn't exist\n"
		usage
		exit 1
	fi

	ffmpeg -i "$videoFile" -c copy -map 0 -f segment -segment_time "$slice" output_%03d.mp4
}

function convertVideoToGif() {
	if [[ -z "$1" ]]; then
		printf "\n\e[0;31m[ERROR]\e[0m $0 missing video file \n"
		usage
		exit 1
	fi

	videoTitle="$1"
	if [[  ! -f "$videoTitle"  ]]; then 
		printf "\n\e[0;31m[ERROR]\e[0m video \"$videoTitle\" does not exist \n"
		usage 
		exit 1
	fi


	defaultScale="480"
	printf "\nOptions: [1] 240px (lowest), [2] 360px, [3] 600px, [4] 720px (highest)\n"
	read -rp "Choose max width/height or enter for default (default=480px): " choice

	case "$choice" in
		"")
			scale="$defaultScale"
			;;
		1)
			scale="240"
			;;
		2)
			scale="360"
			;;
		3)
			scale="600"
			;;
		4)
			scale="720"
			;;
		*)
			printf "\n\e[0;33m[WARN]\e[0m Invalid choice defaulting to $defaultScale\n"
			scale="$defaultScale"
			;;
	esac

	read -rp "Set fps (default=24fps): " fps

	if [[ -z "$fps" || ! "$fps" =~ ^-?[0-9]+$ ]]; then
		fps=24
		printf "\n\e[0;33m[WARN]\e[0m Invalid choice defaulting to $fps fps\n"
	fi

	read -rp "Enter output gif name: " videoName

	if [[ -z "$videoName" ]]; then
		videoName="$(basename "$videoTitle")"
		videoName="${videoName%.*}"
	fi


	ffmpeg -i "$videoTitle" -r "$fps" -filter_complex \
	"scale='if(gt(iw/ih,1),min($scale,iw),-1)':'if(gt(iw/ih,1),-1,min($scale,ih))':flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse" \
	-loop 0 \
	"$videoName.gif"
}

#TODO: extend script so that it does animated wallpapers
function convertToWallpaper() {
	if [[ -z "$1" ]]; then
		printf "\n\e[0;31m[ERROR]\e[0m $0 missing video file \n"
		usage
		exit 1
	fi

	videoTitle="$1"
	if [[  ! -f "$videoTitle"  ]]; then 
		printf "\n\e[0;31m[ERROR]\e[0m video \"$videoTitle\" does not exist \n"
		usage 
		exit 1
	fi

	printf "\n
libwebp encoder tends to fix blockiness and grid artifacting on red/yellow colors but usually results in a bigger file size. 
75 quality with the libwebp encoder can sometimes be better than 95-100 quality and give a smaller file size. 
Start with 75 quality when using the libwebp encoder.
\n"

	defaultQuality=75
	printf "\nOptions: [1] 75 (lowest), [2] 80, [3] 85 (recommended), [4] 90 (recommended), [5] 95, [6] 100\n"
	read -rp "Choose quality of animated wallpaper (default=75): " choice
	case "$choice" in 
		""|1)
			quality="$defaultQuality"
			;;
		2)
			quality=80
			;;
		3)
			quality=85
			;;
		4)
			quality=90
			;;
		5)
			quality=95
			;;
		6)
			quality=100
			;;
		*)
			printf "\n\e[0;33m[WARN]\e[0m Invalid choice defaulting to $defaultQuality\n"
			quality="$defaultQuality"
			;;
	esac

	videoName="$(basename "$videoTitle")"
	videoName="${videoName%.*}"

	ffmpeg -i "$videoTitle" -c libwebp -quality "$quality" -loop 0 -preset photo "$videoName".webp
}

case "$1" in
	-h|--help)
		usage
		;;
	-s|--slice)
		sliceVideo "$2" "$3"
		;;
	-w|--wallpaper)
		convertToWallpaper "$2"
		;;
	*)
		convertVideoToGif "$1"
		;;


esac
