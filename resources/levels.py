"""
	Contains level design and definition
	Square types :
	- 0 -> wall
	- 1 -> walking
	- 2 -> start
	- 3 -> end
"""


LEVELS = [

{	

	"id" : 0,

	"name" : "Ossirian's tomb",
	
	"design" : [[0,0,0,0,0,0,1,1,1,3],
				[0,0,1,1,1,0,0,1,0,0],
				[0,0,0,1,0,0,0,1,0,0],
				[0,0,0,1,0,1,1,1,0,0],
				[0,1,1,1,1,1,0,1,1,1],
				[0,0,1,0,0,0,1,0,1,0],
				[1,0,1,0,1,0,1,0,1,1],
				[1,0,1,1,1,1,1,0,1,0],
				[2,1,1,0,1,0,0,0,0,0],
				[1,0,0,0,0,0,0,0,0,0]],

	"start" : (8, 0),
	"end" : (0, 9),

	"background_music" : "C:\Users\Smau\My Documents\GitHub\pyramos-game\\resources\\audio\0.mp3",
	"top_score" : 18, 

},


]