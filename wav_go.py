import pygame

# function that loads the passed filename and plays it
def say(filename):
    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue   

# play a song
def main():
    say("wav1.wav")

if __name__ == '__main__':
    main()
