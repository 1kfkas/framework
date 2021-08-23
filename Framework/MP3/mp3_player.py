import sys, os, requests, pygame, pytube
from pydub import AudioSegment
from youtubesearchpython import VideosSearch
from pygame.locals import *

###############

img_dir = './Images/';
audio_dir = './Audio/';

if sys.platform.startswith('win32'):
    img_dir = '.\Images\'';
    audio_dir = '.\Audio\'';

###############

searchType = str(input("\nSearch : "))

i = 0
duration = 60*11;
tpe = '';
d = None;
allok = False

while allok is False:
    i += 1;
    print(i);

    if i >= 21:
        customSearch.next();
        i = 1;

    customSearch = VideosSearch(searchType, limit = i);
    d = customSearch.result()['result'][i-1]['duration'];

    tpe = customSearch.result()['result'][i-1]['type'];

    if d != None:
    
        if len(d) <= 4:
            if d[0] == '0':
                duration = 0;
            elif d[0] == '1':
                duration = 60*1;
            elif d[0] == '2':
                duration = 60*2;
            elif d[0] == '3':
                duration = 60*3;
            elif d[0] == '4':
                duration = 60*4;
            elif d[0] == '5':
                duration = 60*5;
            elif d[0] == '6':
                duration = 60*6;
            elif d[0] == '7':
                duration = 60*7;
            elif d[0] == '8':
                duration = 60*8;
            elif d[0] == '9':
                duration = 60*9;

        if len(d) == 5:
            if d[0] == '1' and d[1] == '0' and d[3] == '0' and d[4] == '0':
                duration = 60*10;

    if d != None and tpe == 'video' and duration <=60*10:
        allok = True;

print(tpe)
print(d);

def Get_URL():
    u = customSearch.result()['result'][i-1]['link'];
    return u;

def Get_Title():
    t = customSearch.result()['result'][i-1]['title'];
    ut = t.replace(":", "");
    t = ut.replace(".", "");
    ut = t.replace(",", "");
    t = ut.replace('|', '');
    return t;

def Get_Thumbnail():        
    r = customSearch.result()['result'][i-1]['thumbnails'][0];
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
    stream = yt.streams.get_by_itag(251);
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
