VIDEODIR=./videos/episode2.mkv
ffmpeg -copyts -i "$VIDEO_DIR" -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1",subtitles=sub1.ass -frame_pts true -vsync vfr -q:v 5 "Sub_01/%08d.jpg" -r 1000 -vf "mpdecimate=hi=64*12*15:lo=64*5*15:frac=1" -frame_pts true -vsync vfr -q:v 5 "Raw_01/%08d.jpg"
