from dataclasses import dataclass
from typing import Optional

from netffmpeg.net_constants import IMAGE, VIDEOS


class NetDrawText(str):
    pass


class NetInputFile(list):
    pass


class NetDrawOverlay(str):
    pass


class NetScaleOverlay(str):
    pass


@dataclass
class InputOverlay:
    net_input_file: Optional[NetInputFile] = None
    net_draw_overlay: Optional[NetDrawOverlay] = None
    net_scale_overlay: Optional[NetScaleOverlay] = None


@dataclass
class MediaCoordinate:
    x: int
    y: int
    width: Optional[int] = None
    height: Optional[int] = None


@dataclass
class NetTimeStamp:
    start: float
    end: float


@dataclass
class NetTextStyles:
    text: str
    font_file: str
    bg_color: Optional[str] = None
    timestamp: Optional[NetTimeStamp] = None
    fg_color: str = "white"
    font_size: int = 20
    weight: int = 3
    coordinate: Optional[MediaCoordinate] = None


@dataclass
class NetOverlayStyles:
    file_path: NetInputFile
    timestamp: Optional[NetTimeStamp] = None
    coordinate: Optional[MediaCoordinate] = None
