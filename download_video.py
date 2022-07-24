from pytube import YouTube as Video
from argparse import ArgumentParser
from sys import exit

def __retrieve_formats(video: Video) -> list[dict]:
    return video.vid_info['streamingData']['formats']

def __retrieve_available_resolutions(formats: list[dict]) -> list[str]:
    resolutions = list()
    for fm in formats:
        resolutions.append(fm['qualityLabel'])
    return resolutions

def download_video(video: Video, output_dir: str | None = None) -> None:
    formats = __retrieve_formats(video)
    res = __retrieve_available_resolutions(formats).pop()
    video.register_on_complete_callback(
        lambda _1, _2: print('Done: ', video.title)
    )
    print('Fetching: ', video.title, res)
    video.streams.filter(
        progressive=True,
        file_extension='mp4',
        res=res
    )   .first() \
        .download(output_dir)

def main():
    try:
        parser = ArgumentParser()
        parser.add_argument('url', help='Video link')
        args = parser.parse_args()

        video = Video(args.url)
        download_video(video)
    except Exception as e:
        print(e)
        exit(1)

    exit(0)

if __name__ == '__main__':
    main()
