from random import choice
from PIL import Image
import moviepy.editor as mp
from cv import LOGOS, width_scale


def watermark_pic():
	logo = Image.open('files/'+choice(LOGOS))
	logo_width, logo_height = logo.size

	to_watermark = Image.open("files/to_watermark_pic.png")
	width, height = to_watermark.size


	resized_logo_size = ( int(width/width_scale), int(logo_height*(width/width_scale)/logo_width) )
	resized_logo = logo.resize(resized_logo_size)

	#Saved in the same relative location 
	# img.save("resized_.jpg")  
	# img2 = Image.open("Capture.PNG")
	# img = Image.open("out.png")  
	offset = int(width/(width_scale*2.7))
	to_watermark.paste(resized_logo, (offset, height-resized_logo_size[1]-offset), resized_logo) 
	to_watermark.save("files/watermarked_pic.png") 


def watermark_vid():

	# myClip.resize( (460,720) ) # New resolution: (460,720)

	video = mp.VideoFileClip("files/to_watermark_vid.mp4")
	# print(video.duration)
	logo_path = 'files/'+choice(LOGOS)

	logo_width, logo_height = Image.open(logo_path).size
	width, height = video.size
	offset = int(width/(width_scale*2.7))
	resized_logo_size = ( int(width/width_scale), int(logo_height*(width/width_scale)/logo_width) )

	logo = (mp.ImageClip(logo_path)
	      .set_duration(video.duration)
	      .resize(width=resized_logo_size[0], height=resized_logo_size[1]) # if you need to resize...
	      .margin(left=offset, bottom=offset, opacity=0) # (optional) logo-border padding
	      .set_pos(("left","bottom")))

	final = mp.CompositeVideoClip([video, logo])
	final.subclip(0,video.duration).write_videofile("files/watermarked_vid.mp4")
	return video.duration, video.size[0], video.size[1]


if __name__ == '__main__':
	watermark_vid()
	watermark_pic()
