
import subprocess
from typing import Optional
from netffmpeg.nf_types import InputOverlay, NetDrawText, NetInputFile


class NetFfmpeg:
    def __init__(self, input_media: NetInputFile):
        self._commands = []
        self._inputs = ["ffmpeg", ]+input_media
        self._draw_text = ""
        self._draw_overlay = ""
        self._scale = ""

    def addText(self, net_draw_text: NetDrawText):
        self._draw_text = net_draw_text
        return self

    def addOverlay(self, input_overlay: InputOverlay):
        self._inputs.extend(input_overlay.net_input_file)
        self._draw_overlay = input_overlay.net_draw_overlay
        self._scale = input_overlay.net_scale_overlay
        print("******", self._scale)
        return self

    def outputInput(self, media_path: str, overwrite: bool = False, duration: Optional[float] = None):
        """
        Configures the output settings for the ffmpeg command.

        Parameters:
        media_path (str): The path where the output media file will be saved.
        overwrite (bool): If True, the output file will be overwritten if it already exists. Defaults to False.
        duration (Optional[float]): The duration of the output media file in seconds. If None, the duration is not limited.
        this is important when using continious  = -1 

        Returns:
        NetFfmpeg: The instance of the NetFfmpeg class with the updated output settings.
        """
        command = "[0:v]scale=1280:720[scaled];"
        if len(self._scale) > 0:
            command += f"{self._scale}"
        command += "[scaled]"
        if len(self._draw_text) > 0:
            command += f"{self._draw_text}"
        if len(self._draw_overlay) > 0:
            count = self._draw_text.count("drawtext=")
            if count > 0:
                command += f"[text{count}];[text{count}]"
            command += f"{self._draw_overlay}"
        self._commands.extend([
            # "-filter_complex", f_complex
            "-filter_complex", f"{command}[final]",
            "-map", "[final]",
            "-map", "0:a",
            "-c:a", "copy",
        ])
        if duration is not None:
            self._commands.extend([
                "-t", str(duration),
                "-r", "10",
                "-vcodec", "libx264",
                "-pix_fmt", "yuv420p"
            ])
        if overwrite:
            self._commands.append("-y")
        self._commands.append(media_path)
        self._commands = self._inputs+self._commands
        print(self._commands)
        return self

    def execute(self):
        subprocess.run(self._commands, shell=True)
