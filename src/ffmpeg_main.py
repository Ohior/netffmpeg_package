from netffmpeg.net_ffmpeg import NetDrawText, NetFfmpeg
from netffmpeg.net_filter import NetFilter, NetOverlayStyles,NetTextStyles
from netffmpeg.nf_types import MediaCoordinate,NetTimeStamp, InputOverlay

media_path = "C:/Users/HP/Videos/TEST/exampleVideo.mp4"
output_path = "raw/OUT_exampleVideo.mp4"
# create text to be drawn
draw_text = NetDrawText()
draw_text = NetFilter.drawText(
    draw_text=draw_text,
    net_style=NetTextStyles(
        text="Hello, world",
        font_file="Pacifico-Regular.ttf",
        coordinate=MediaCoordinate(100, 20),
        bg_color="black"
    )
)
draw_text = NetFilter.drawText(
    draw_text=draw_text,
    net_style=NetTextStyles(
        text="Hello, world",
        font_file="Pacifico-Regular.ttf",
        coordinate=MediaCoordinate(100, 300),
        bg_color="black"
    )
)

# create files(images, gifs, videos) to be drawn
draw_overlay = InputOverlay()
draw_overlay = NetFilter.drawOverlay(
    input_overlay=draw_overlay,
    net_overlay_style=NetOverlayStyles(
        file_path=NetFilter.addInput(
            media_path="C:/Users/HP/Videos/TEST/image.png", continous=1),
        timestamp=NetTimeStamp(start=0.0, end=10.0),
        coordinate=MediaCoordinate(x=0, y=0, width=200, height=300)
    )
)
draw_overlay = NetFilter.drawOverlay(
    input_overlay=draw_overlay,
    net_overlay_style=NetOverlayStyles(
        file_path=NetFilter.addInput(
            media_path="C:/Users/HP/Videos/TEST/book.gif", continous=-1),
        timestamp=NetTimeStamp(start=0.0, end=10.0),
        coordinate=MediaCoordinate(x=200, y=200, width=200, height=300)
    )
)
draw_overlay = NetFilter.drawOverlay(
    input_overlay=draw_overlay,
    net_overlay_style=NetOverlayStyles(
        file_path=NetFilter.addInput(
            media_path="C:/Users/HP/Videos/TEST/pil.mp4", continous=-1),
        timestamp=NetTimeStamp(start=5.0, end=20.0),
        coordinate=MediaCoordinate(x=500, y=200, width=200, height=300)
    )
)
(
    NetFfmpeg(input_media=NetFilter.addInput(media_path=media_path))
    .addText(net_draw_text=draw_text)
    .addOverlay(input_overlay=draw_overlay)
    .outputInput(media_path=output_path, overwrite=True)
    .execute()
)