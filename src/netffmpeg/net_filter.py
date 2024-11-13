from netffmpeg.net_constants import IMAGE
from netffmpeg.nf_types import InputOverlay, NetDrawText, NetInputFile, NetOverlayStyles, NetTextStyles


class NetFilter:
    @staticmethod
    def addInput(media_path: str, continous: int = 0) -> NetInputFile:
        m_format = f".{media_path.split('/')[-1].split(".")[-1]}"
        if m_format in IMAGE:
            return NetInputFile((
                "-loop", str(1),
                "-i", media_path
            ))
        return NetInputFile((
            "-stream_loop", str(continous),
            "-i", media_path
        ))

    @staticmethod
    def drawOverlay(
        input_overlay: InputOverlay,
        net_overlay_style: NetOverlayStyles,
    ) -> InputOverlay:
        inputs = input_overlay.net_input_file
        overlay = input_overlay.net_draw_overlay
        scale = input_overlay.net_scale_overlay
        if overlay is None:
            overlay = ""
        if inputs is not None:
            inputs.extend(net_overlay_style.file_path)
        else:
            inputs = net_overlay_style.file_path
        if net_overlay_style.coordinate is not None:
            count_overlay = 1
            if overlay.__contains__("overlay="):
                count_overlay = input_overlay.net_draw_overlay.count(
                    "overlay")+1
            if scale is not None:
                scale += f"[{count_overlay}:v]scale={net_overlay_style.coordinate.width}:\
{net_overlay_style.coordinate.height}[scaled{count_overlay}];"
            else:
                scale = f"[{count_overlay}:v]scale={net_overlay_style.coordinate.width}:\
{net_overlay_style.coordinate.height}[scaled{count_overlay}];"

        if overlay.__contains__("overlay="):
            count_overlay = input_overlay.net_draw_overlay.count("overlay")
            overlay += f"[bg{count_overlay}];[bg{count_overlay}]"
            overlay += f"[scaled{count_overlay+1}]"
            overlay += f"overlay={net_overlay_style.coordinate.x}:{net_overlay_style.coordinate.y}:\
shortest=1:\
enable='between(t,{net_overlay_style.timestamp.start},{net_overlay_style.timestamp.end})'"
        else:
            if scale is not None:
                overlay += f"[scaled{1}]"
            overlay += f"overlay={net_overlay_style.coordinate.x}:{net_overlay_style.coordinate.y}:\
shortest=1:\
enable='gte(t,{net_overlay_style.timestamp.start},{net_overlay_style.timestamp.end})'"
        return InputOverlay(
            net_input_file=inputs,
            net_draw_overlay=overlay,
            net_scale_overlay=scale
        )

    @staticmethod
    def drawText(
        draw_text: NetDrawText,
        net_style: NetTextStyles
    ) -> NetDrawText:
        dt_count = draw_text.count("drawtext")
        dt = ""
        if dt_count > 0:
            dt += f"[text{dt_count}];[text{dt_count}]"
        dt += f"drawtext=text='{net_style.text}':\
fontsize={net_style.font_size}:\
fontcolor={net_style.fg_color}:\
font={net_style.font_file}"
        if net_style.coordinate is not None:
            dt += f":x={net_style.coordinate.x}:y={net_style.coordinate.y}"
        if net_style.bg_color is not None:
            dt += f":box={True}:boxcolor={net_style.bg_color}:\
boxborderw={net_style.weight}"
            if net_style.coordinate.height is not None:
                dt += f":boxh={net_style.coordinate.height + net_style.weight}"
        if net_style.timestamp is not None:
            dt += f":enable='between(t,{net_style.timestamp.start},{
                net_style.timestamp.end})'"
        return NetDrawText(draw_text+dt)
