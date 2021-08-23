import sys, os, requests, pygame, pytube
from pydub import AudioSegment
from youtubesearchpython import *
from pygame.locals import *

###############

img_dir = './Images/';
audio_dir = './Audio/';

if sys.platform.startswith('win32'):
    img_dir = '.\Images\'';
    audio_dir = '.\Audio\'';

###############

def CheckPosMouse(x, y, w, h):
    if pygame.mouse.get_pos()[0] >= x and pygame.mouse.get_pos()[0] <= x+w and pygame.mouse.get_pos()[1] >= y and pygame.mouse.get_pos()[1] <= y+h:
        return True
    else:
        return False

###############

searchType = str(input("\nSearch : "))

customSearch = VideosSearch(searchType, limit = 1);

def Get_URL():
    u = customSearch.result()['result'][0]['link'];
    return u;

def Get_Title():
    t = customSearch.result()['result'][0]['title'];
    ut = t.replace(":", "");
    t = ut.replace(".", "");
    ut = t.replace(",", "");
    t = ut.replace('|', '');
    return t;

def Get_Thumbnail():        
    r = customSearch.result()['result'][0]['thumbnails'][0];
    return r;

def Download_Thumbnail():
    print('\nBaixando Thumbnail...');
    response = requests.get(Get_Thumbnail()['url']);
    file = open(img_dir+"image.png", "wb");
    file.write(response.content);
    file.close();
    print('Thumbnail Baixada!\n');

def Download_Music():
    print('Baixando Música...');
    yt = pytube.YouTube(Get_URL());
    stream = yt.streams.get_by_itag(249);
    stream.download(audio_dir);
    print('Música Baixada!\n\nConvertendo Música...');
    webm_audio = AudioSegment.from_file(audio_dir+Get_Title()+'.webm', format="webm");
    webm_audio.export(audio_dir+Get_Title()+'.ogg', format="ogg");
    os.remove(audio_dir+Get_Title()+'.webm');
    print('Música Convertida!');

###########################

Download_Thumbnail();
Download_Music();

pygame.mixer.init();

sound = pygame.mixer.music.load(audio_dir+Get_Title()+'.ogg');

pause = False;

pygame.mixer.music.play();

def Set_Pause(bol):
    pause = bol;

def Get_Pause():
    return pause;

def PauseMusic():
    pygame.mixer.music.pause();
    
def ResumeMusic():
    pygame.mixer.music.unpause();
    
def StopMusic():
    pygame.mixer.music.stop();

def Load():
    spr = pygame.image.load(img_dir+'image.png').convert();
    pl = pygame.image.load(img_dir+'play.png').convert_alpha();
    pa = pygame.image.load(img_dir+'pause.png').convert_alpha();
    display.blit(spr, (64, 0));

    if Get_Pause():
        display.blit(pl, (64+w/2-24, h+16));
    else:
        display.blit(pa, (64+w/2-24, h+16));

###############################

pygame.init();
pygame.display.init();

w = Get_Thumbnail()['width'];
h = Get_Thumbnail()['height'];

display = pygame.display.set_mode((w+128, h+64));
clock = pygame.time.Clock();
pygame.display.set_caption(Get_Title());

print('\nPronto para iniciar!\n')

while True:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            os.remove(img_dir+"image.png");
            os.remove(audio_dir+Get_Title()+".ogg");
            pygame.mixer.quit();
            pygame.display.quit();
            pygame.quit();
            sys.exit();

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Get_Pause():
                    pause = False;
                    ResumeMusic();
                else:
                    pause = True;
                    PauseMusic();

    clock.tick(60);

    display.fill((102, 102, 102));

    Load();
    
    pygame.display.flip();
