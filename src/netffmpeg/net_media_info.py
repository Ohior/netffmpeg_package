from dataclasses import dataclass
from json import loads
import subprocess
from typing import Optional


@dataclass
class Tags:
    major_brand: Optional[str]
    minor_version: Optional[str]
    compatible_brands: Optional[str]
    encoder: Optional[str]

    def __init__(self, kwargs: dict):
        self.major_brand = kwargs.get('major_brand', None)
        self.minor_version = kwargs.get('minor_version', None)
        self.compatible_brands = kwargs.get('compatible_brands', None)
        self.encoder = kwargs.get('encoder', None)


@dataclass
class MediaFormat:
    filename: Optional[str]
    nb_streams: Optional[int]
    nb_programs: Optional[int]
    nb_stream_groups: Optional[int]
    format_name: Optional[str]
    format_long_name: Optional[str]
    start_time: Optional[str]
    duration: Optional[str]
    size: Optional[str]
    bit_rate: Optional[str]
    probe_score: Optional[int]
    tags: Optional[Tags]

    def __init__(self, kwargs: dict):
        self.filename = kwargs.get('filename', None)
        self.nb_streams = kwargs.get('nb_streams', None)
        self.nb_programs = kwargs.get('nb_programs', None)
        self.nb_stream_groups = kwargs.get('nb_stream_groups', None)
        self.format_name = kwargs.get('format_name', None)
        self.format_long_name = kwargs.get('format_long_name', None)
        self.start_time = kwargs.get('start_time', None)
        self.duration = kwargs.get('duration', None)
        self.size = kwargs.get('size', None)
        self.bit_rate = kwargs.get('bit_rate', None)
        self.probe_score = kwargs.get('probe_score', None)
        self.tags = Tags(kwargs.get('tags', {}))


@dataclass
class MediaInfo:
    media_type: Optional[str]
    channels: Optional[int]
    bits_per_sample: Optional[int]
    sample_rate: Optional[int]
    nb_frames: Optional[str]
    channel_layout: Optional[str]
    width: Optional[int]
    height: Optional[int]
    media_format: Optional[MediaFormat]

    def __init__(self, kwargs: dict):
        self.media_type = kwargs.get('codec_type', None)
        self.channels = kwargs.get('channels', None)
        self.bits_per_sample = kwargs.get('bits_per_sample', None)
        self.sample_rate = kwargs.get('sample_rate', None)
        self.nb_frames = kwargs.get('nb_frames', None)
        self.channel_layout = kwargs.get('channel_layout', None)
        self.width = kwargs.get('width', 0)
        self.height = kwargs.get('height', 0)
        self.media_format = MediaFormat(kwargs.get('format', None))

    @staticmethod
    async def getMediaInfo(file_path) -> dict:
        try:
            # Run the ffprobe command to get media information in JSON format
            result = subprocess.run(
                [
                    "ffprobe",
                    "-v", "quiet",
                    "-print_format", "json",
                    "-show_format",
                    "-show_streams",
                    file_path
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            # Parse the JSON output
            info = loads(result.stdout)
            for stream in info['streams']:
                media_type = stream.get('codec_type', None)
                channels = stream.get('channels', None)
                bits_per_sample = stream.get('bits_per_sample', None)
                sample_rate = stream.get('sample_rate', None)
                nb_frames = stream.get('nb_frames', None)
                channel_layout = stream.get('channel_layout', None)
                width = stream.get('width', 0)
                height = stream.get('height', 0)
            media_format = info['format']
            return {
                "media_type": media_type,
                "channels": channels,
                "bits_per_sample": bits_per_sample,
                "sample_rate": sample_rate,
                "nb_frames": nb_frames,
                "format": media_format,
                "channel_layout": channel_layout,
                "width": width,
                "height": height
            }
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
