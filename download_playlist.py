from argparse import ArgumentParser
from threading import Thread
from os import path, mkdir
from shutil import rmtree
from sys import exit
from pytube import Playlist
from download_video import download_video

def __complete_threads(threads: list[Thread]) -> None:
    for thread in threads:
        thread.join()

def download_playlist(pl: Playlist, output_dir: str | None = None) -> None:
    threads = list()
    for video in pl.videos:
        thread = Thread(
            target=download_video,
            args=(video, output_dir)
        )
        threads.append(thread)
        thread.start()
    __complete_threads(threads)

def main():
    try:
        parser = ArgumentParser()
        parser.add_argument('url', help='A link to the playlist')
        args = parser.parse_args()

        pl = Playlist(args.url)
        output_dir = pl.title
        try:
            if path.exists(output_dir):
                rmtree(output_dir)
            mkdir(output_dir)
            download_playlist(pl, output_dir)
        except:
            print('Failed to create the ' + output_dir + ' directory')
            print('Using the "output" directory')
            output_dir = 'output'
            if path.exists(output_dir):
                rmtree(output_dir)
            mkdir(output_dir)
            download_playlist(pl, output_dir)
    except Exception as e:
        print(e)
        exit(1)

    exit(0)
if __name__ == '__main__':
    main()
