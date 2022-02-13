from PIL import Image
from time import sleep
import pygame

# ascii characters used to build the output text
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]
MEMORY_FPS = 24

# resize image according to a new width
def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height/width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return(resized_image)

# convert each pixel to grayscale
def grayify(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)
    
# convert pixels to a string of ascii characters
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel//25] for pixel in pixels])
    return(characters)    

# the main
def main(new_width=100):

    input_str = input("Write the file or play file? Type 'write' or 'play [FPS] [START TIME IN SECONDS] ' (e.g: 'play 24 10'). \n\n>>> ").lower()

    if input_str == "write":

       write(new_width)

    else:

        tokens = input_str.split(" ")

        token_FPS = tokens[1]
        token_time = tokens[2]

        time = int(token_time)
        FPS = int(token_FPS)

        play(time, FPS)

        if input("Exit?"):
            raise SystemExit(0)

def write(new_width: int):

        frames = []
        
        # from 1st to 5257th frame
        for frameNumb in range(1, 5258):

            # make the number of image to open like in the folder 
            if frameNumb < 10:
                frameNumb = "000" + str(frameNumb)
            elif (frameNumb < 100) and (frameNumb > 9):
                frameNumb = "00" + str(frameNumb)
            elif (frameNumb < 1000) and (frameNumb > 99):
                frameNumb = "0" + str(frameNumb)

            # open image
            try:
                image = Image.open(rf'Frames\bad_apple3 {frameNumb}.jpg')
            except:
                print("It isn`t a valid pathname to an image.")
                return
        
            # convert image to ascii    
            new_image_data = pixels_to_ascii(grayify(resize_image(image)))
        
            # format
            pixel_count = len(new_image_data)  
            frame = "\n".join([new_image_data[index:(index+new_width)] for index in range(0, pixel_count, new_width)])
        
            # put the frames into the list
            frames.append(frame)

            print(f"The frame bad_apple{frameNumb}.jpg processed successfully.")
            
        
        # save result to file
        with open("memory.txt", "w") as f:
            for frame in frames:
                print("Frame writed!")
                f.write(str(frame) + "SPLIT")


def play(start_time: int, FPS: int):

        # read the frames from the memory file
        with open("memory.txt", "r") as f:
            memory = f.read()

        frames = memory.split("SPLIT")

        framesNew = []

        frame_time = 1 / FPS

        start_frame = start_time / frame_time

        i = 0

        if (FPS > MEMORY_FPS):
            raise ValueError("FPS can`t be more than MEMORY_FPS")

        ratio = MEMORY_FPS / FPS

        for frame in frames:
            i = i + 1
            i2 = int(i / ratio)
            if (i % ratio) == 0:
                if (i2 >= start_frame):
                    frame = frame.replace(".", " ")
                    framesNew.append(frame)

        clock = pygame.time.Clock()

        # music
        pygame.mixer.init()
        pygame.mixer.music.load("bad_apple.mp3")
        pygame.mixer.music.play(start=start_time)

        # printing the frames        
        for frame in framesNew:
            print(frame)
            clock.tick(FPS)

 
# run program
main()
