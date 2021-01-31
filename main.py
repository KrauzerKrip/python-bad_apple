from PIL import Image
from time import sleep
import pygame

# ascii characters used to build the output text
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]


# the variable of sleep while prints frames after printing frame.

time_sleep = 0.034444  # for ordinary using
#time_sleep = 0.0330215  # for record
#time_sleep = 0.032333  # for record
#time_sleep = 0.035000  # for ordinary using
#time_sleep = 0.0335  # for record
#time_sleep = 0.03345  # for record

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

    if input("Write the file or play file?\n\n>>> ").lower() == "write":

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

    else:

        # read the frames from the memory file
        with open("memory.txt", "r") as f:
            memory = f.read()


        frames = memory.split("SPLIT")

        # music
        pygame.mixer.init()
        pygame.mixer.music.load("bad_apple.mp3")
        pygame.mixer.music.play()

        # printing the frames        
        for frame in frames:
            print(frame)
            sleep(time_sleep)

        if input("Exit? Yes?") == "Yes":
            raise SystemExit(0)

 
# run program
main()
