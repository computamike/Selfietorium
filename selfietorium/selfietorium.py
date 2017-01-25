#!/usr/bin/python
import importlib
import math
import cairo
import pygame
import pygame.display
import rsvg
import PIL.Image
import sys
from libselfietorium import template
from libselfietorium import configuration
from libselfietorium import pygameTextRectangle
from libselfietorium import SendTweet
from libselfietorium import utilities
import datetime
import base64
import StringIO
import os
import traceback

# Constants
WIDTH = 640                     # Width of the window
HEIGHT = 540                    # Height of the window
DPI = 90                        # Recalculate this based on your screen.
SHOOTDIRECTORY = None           # Name of directory to store photographs taken
PHOTOSOUNDEFFECT = None         # Sound effect to play when taking photo
SCREEN_ATTRACT = None           # Attract Screen SVG XML data
CAMERASOUND = None              # Camera noise to play when taking a photo.
SCREEN_FONT = None
FONT_COLOUR = None              # Colour to display updated text to subjects
TWEET_TEXT = ""                 # Default tweet text to use when
                                # tweeting pictures.
mymethod = None

def bgra_rgba(surface):
        img = PIL.Image.frombuffer('RGBA', (surface.get_width(),
              surface.get_height()), surface.get_data(),
              'raw', 'BGRA', 0, 1)
        return img.tobytes('raw', 'RGBA', 0, 1)


def load_svg_string(svg_data):
    svg = rsvg.Handle(data=svg_data)
    img_w, img_h = svg.props.width, svg.props.height
    scale_factorx = float(WIDTH) / float(img_w)
    scale_factory = float(HEIGHT) / float(img_h)
    surface = cairo.ImageSurface(cairo. FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(scale_factorx, scale_factory)
    svg.render_cairo(ctx)
    return pygame.image.frombuffer(bgra_rgba(surface), (WIDTH, HEIGHT), 'RGBA')


def load_svg(filename):
    """Render SVG as Pygame image"""
    svg = rsvg.Handle(filename)
    img_w, img_h = svg.props.width, svg.props.height
    scale_factorx = float(WIDTH) / float(img_w)
    scale_factory = float(HEIGHT) / float(img_h)
    surface = cairo.ImageSurface(cairo. FORMAT_ARGB32, WIDTH, HEIGHT)
    ctx = cairo.Context(surface)
    ctx.scale(scale_factorx, scale_factory)

    svg.render_cairo(ctx)
    return pygame.image.frombuffer(bgra_rgba(surface), (WIDTH, HEIGHT), 'RGBA')


# This is a poor state implementation - a better implementation will be
#worked out in due course
#Valid States are :
#
# ATTRACT
# PREEN
# PHOTO
# COMPOSITE
# PRINT
#


#def picam_get_photo(cam):
#    img = cam.get_image()
#    return img


def convert_surface_to_image(surface):
    width = surface.get_width() # 640
    height = surface.get_height() # 480
    pil = pygame.image.tostring(surface, "RGBA", False)
    img = PIL.Image.frombytes("RGBA", (width, height), pil)
    return img


def savephoto(mydir, img_photo, filename):
    """Saves a photo as filename in the folder specified"""
    try:
        os.makedirs(mydir)
    except OSError, e:
        if e.errno != 17:
            raise     # This was not a "directory exist" error..
    img_photo = convert_surface_to_image(img_photo)
    img_photo.save(os.path.join(mydir, filename), format="PNG")



def layout(tplate, photos, outputdir):
    """Layout template and save to Directory"""
    update_node = tplate
    for shot in photos:
        imgPhoto = convert_surface_to_image(shot.photo)
        output = StringIO.StringIO()
        imgPhoto.save(output, format="PNG")
        contents = output.getvalue()
        output.close()
        base64data = base64.b64encode(contents)
        str_b64 = "data:image/png;base64," + base64data
        update_node = template.updateNodeAttrib(update_node, shot.imageID,
            "{http://www.w3.org/1999/xlink}href", str_b64)
    text_file = open(os.path.join(outputdir, "Output.svg"), "w")
    text_file.write(update_node)
    text_file.close()
    save_svg_to_img(update_node, outputdir, "Composite.png")
    return os.path.join(outputdir, "Composite.png")

# Screen methods


def save_svg_to_img(svg, outputdir, filename):
    IMG = load_svg_string(svg)
    screen.blit(cbackground, (0, 0))
    screen.blit(IMG, (0, 0))
    pygame.display.flip()
    pygame.time.delay(5000)
    savephoto(outputdir, IMG, filename)

def load_image_from_url_as_B64(source):
    from urllib2 import urlopen
    import io
    image_str = urlopen(source).read()
    image_file = io.BytesIO(image_str)
    avatar = pygame.image.load(image_file)
    result = convert_surface_to_image(avatar)
    output = StringIO.StringIO()
    result.save(output, format="PNG")
    contents = output.getvalue()
    output.close()
    base64data = base64.b64encode(contents)
    str_b64 = "data:image/png;base64," + base64data
    return str_b64

def twitter_latest(svg, imagesvg):
    svg_loaded = rsvg.Handle(data=svg)
    img_w, img_h = svg_loaded.props.width, svg_loaded.props.height
    scale_factorx = float(WIDTH) / float(img_w)
    scale_factory = float(HEIGHT) / float(img_h)
    latest_tweet = SocialMedia.latest_Tweet

    if latest_tweet != None:
        print "Screen Name : "+latest_tweet.user.name
        print "Handle      : "+latest_tweet.user.screen_name
        print "Avatar URL  : "+latest_tweet.user.profile_image_url
        print "Tweet Text  : "+latest_tweet.text
        # load avatar
        from HTMLParser import HTMLParser
        h = HTMLParser()
        str_b64 = load_image_from_url_as_B64(latest_tweet.user.profile_image_url)
        #Update Avatar
        svg = template.updateNodeAttrib(svg, "twitter_avatar",
            "{http://www.w3.org/1999/xlink}href", str_b64)
        #Update Twitter name
        svg = template.updateNode(svg, 'twitter_name',latest_tweet.user.name)
        #Update Twitter handle
        svg = template.updateNode(svg, 'twitter_handle','@'+latest_tweet.user.screen_name)
        #Update Twitter handle
        #svg = template.updateNode(svg, 'twitter_tweet',the_dict['text'])
        #update Tweet
        screenGeometry = template.findGeometry(svg)
        scaleWidth = float(float(WIDTH) / float(screenGeometry[0]))
        scaleHeight = float(float(HEIGHT) / float(screenGeometry[1]))
        prompt = template.findNode(svg, '//svg:rect[@id="twitter_tweet_region"]')
        promptFont = template.findNode(svg, '//svg:text[@id="twitter_tweet_region_font"]')

        # what does this do?

        #s = promptFont.attrib['style']
        #s = s.rstrip(';')
        #styles = dict(item.split(":") for item in s.split(";"))
        #SCREEN_FONT = styles["font-family"]
        styles = template.get_Element_Styles(promptFont)
        SCREEN_FONT = styles["font-family"]
        SCREEN_FONT_SIZE = int(''.join(c for c in styles["font-size"] if c.isdigit()))

        print str(SCREEN_FONT_SIZE)
        print str(scale_factorx)
        print str(scale_factory)
        SCREEN_FONT_SIZE = int(round((float(SCREEN_FONT_SIZE)) * float(scale_factorx)))
        #points = (pixels / 150) * 72
        SCREEN_FONT_COLOUR = styles["fill"][1:]
        SCREEN_FONT_COLOUR  = util.hex_to_rgb(SCREEN_FONT_COLOUR)
        svg = template.deleteNode(svg, '//svg:rect[@id="twitter_tweet_region"]')
        promptx = int(math.floor(float(prompt.attrib['x']) * scaleWidth))
        prompty = int(math.floor(float(prompt.attrib['y']) * scaleHeight))
        promptWidth = int(math.ceil(float(prompt.attrib['width']) * scaleWidth))
        promptHeight = int(math.ceil(float(prompt.attrib['height']) * scaleHeight))
        twitter_rect = pygame.Rect((promptx, prompty, promptWidth, promptHeight))
        my_font = pygame.font.SysFont(SCREEN_FONT, SCREEN_FONT_SIZE)
        prompt = pygameTextRectangle.render_textrect(h.unescape(latest_tweet.text), my_font, twitter_rect, SCREEN_FONT_COLOUR, (0, 0, 0, 0), 0)
        IMG = load_svg_string(svg)
        screen.blit(background, (0, 0))
        screen.blit(IMG, (0, 0))
        screen.blit(prompt, (promptx, prompty))
        pygame.display.flip()
        pygame.time.delay(5000)

        if 'media' in latest_tweet.entities:
            for image in latest_tweet.entities['media']:
                print 'Photo found @ : ' + image['media_url']
                imagesvg = template.updateNodeAttrib(imagesvg, "twitter_avatar","{http://www.w3.org/1999/xlink}href", str_b64)
                imagesvg = template.updateNode(imagesvg, 'twitter_name',latest_tweet.user.name)

                photo_b64 = load_image_from_url_as_B64(image['media_url'])
                imagesvg = template.updateNodeAttrib(imagesvg, "twitter_photo","{http://www.w3.org/1999/xlink}href", photo_b64)
                IMG = load_svg_string(imagesvg)
                screen.blit(IMG, (0, 0))
                pygame.display.flip()
                pygame.time.delay(5000)


def preen_screen(photoshoot, svg_data, preentime=10):
    ShootTime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    SHOOTDIRECTORY = os.path.join(SHOOTPHOTOSTORE, ShootTime)
    screenGeometry = template.findGeometry(svg_data)
    scaleWidth = float(float(WIDTH) / float(screenGeometry[0]))
    scaleHeight = float(float(HEIGHT) / float(screenGeometry[1]))
    picam = template.findNode(svg_data, '//svg:rect[@id="picam"]')
    pcamWidth = int(math.ceil(float(picam.attrib['width']) * scaleWidth))
    pcamHeight = int(math.ceil(float(picam.attrib['height']) * scaleHeight))
    picamx = int(math.floor(float(picam.attrib['x']) * scaleWidth))
    picamy = int(math.floor(float(picam.attrib['y']) * scaleHeight))

    prompt = template.findNode(svg_data, '//svg:rect[@id="prompt"]')

    svg_data = template.deleteNode(svg_data, '//svg:rect[@id="prompt"]')
    svg_data = template.deleteNode(svg_data, '//svg:text[@id="promptfont"]')

    promptx = int(math.floor(float(prompt.attrib['x']) * scaleWidth))
    prompty = int(math.floor(float(prompt.attrib['y']) * scaleHeight))
    promptWidth = int(math.ceil(float(prompt.attrib['width']) * scaleWidth))
    promptHeight = int(math.ceil(float(prompt.attrib['height']) * scaleHeight))

    for shot in photoshoot:
        #photo = mymethod.GetPhoto()
        #photo = picam_get_photo(cam) # we might not need this one.
        my_font = pygame.font.SysFont(SCREEN_FONT, SCREEN_FONT_SIZE)
        my_string = str(shot.title) or config.prePhotoPhrase
        my_rect = pygame.Rect((promptx, prompty, promptWidth, promptHeight))
        prompt = pygameTextRectangle.render_textrect(my_string, my_font,
            my_rect, SCREEN_FONT_COLOUR, (0, 0, 0, 0), 1)
        start = datetime.datetime.now()
        end = datetime.datetime.now()

        preentimeSpent = (end - start).seconds
        while preentime - preentimeSpent > 0:
            photo = mymethod.GetPhoto()
            #photo = picam_get_photo(cam)
            end = datetime.datetime.now()
            preentimeSpent = (end - start).seconds
            if preentime - preentimeSpent == 0:
                break
            svg_data = template.updateNode(svg_data, 'countDown',
                                               str(preentime - preentimeSpent))
            IMG = load_svg_string(svg_data)
            screen.blit(background, (0, 0))
            screen.blit(IMG, (0, 0))
            screen.blit(pygame.transform.scale(photo,
                             (pcamWidth, pcamHeight)), (picamx, picamy))
            shot.image = photo
            screen.blit(prompt, (promptx, prompty))
            pygame.display.flip()
            pygame.time.delay(25)
        CAMERASOUND.play()
        shot.photo = photo
        savephoto(SHOOTDIRECTORY, photo, shot.imageID + ".png")
        pygame.time.delay(500)
        screen.blit(background, (0, 0))
        screen.blit(pygame.transform.scale(photo, (WIDTH, HEIGHT)), (0, 0))
        pygame.display.flip()
        pygame.time.delay(2000)

    # Cache this...
    tphotoshoot = svg_data = open(config.layout).read()
    composite = layout(tphotoshoot, photoshoot, SHOOTDIRECTORY)
    print('Composite png located at ' + composite)
    SocialMedia.tweetPhoto(TWEET_TEXT, composite)
    PRINTER.print_photo(composite, 'test-' + ShootTime)
    #//c.print_photo('output.svg','test')
    return "ATTRACT"


def attract_screen(attract_svg_data):
    IMG = load_svg_string(attract_svg_data)
    screen.blit(background, (0, 0))
    screen.blit(IMG, (0, 0))
    pygame.display.flip()


def error_screen(error_svg_data, xception):

    my_font = pygame.font.SysFont(ERROR_FONT, SCREEN_FONT_SIZE)
    my_string = "an error has occured"
    screenGeometry = template.findGeometry(error_svg_data)
    scaleWidth = float(float(WIDTH) / float(screenGeometry[0]))
    scaleHeight = float(float(HEIGHT) / float(screenGeometry[1]))
    prompt = template.findNode(error_svg_data, '//svg:rect[@id="ErrorMessage"]')
    error_svg_data = template.deleteNode(error_svg_data, '//svg:rect[@id="ErrorMessage"]')

    IMG = load_svg_string(error_svg_data)

    promptx = int(math.floor(float(prompt.attrib['x']) * scaleWidth))
    prompty = int(math.floor(float(prompt.attrib['y']) * scaleHeight))
    promptWidth = int(math.ceil(float(prompt.attrib['width']) * scaleWidth))
    promptHeight = int(math.ceil(float(prompt.attrib['height']) * scaleHeight))
    my_rect = pygame.Rect((promptx, prompty, promptWidth, promptHeight))
    prompt = pygameTextRectangle.render_textrect(my_string, my_font, my_rect, ERROR_FONT_COLOUR, (0, 0, 0, 0), 1)
    screen.blit(background, (0, 0))
    screen.blit(IMG, (0, 0))
    screen.blit(prompt, (promptx, prompty))
    pygame.display.flip()
    pygame.time.delay(1000)
    print ('Error :')
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_template = '''Traceback (most recent call last):
      File "%(filename)s", line %(lineno)s, in %(name)s %(type)s: %(message)s\n'''
    traceback_details = {
                         'filename': exc_traceback.tb_frame.f_code.co_filename,
                         'lineno'  : exc_traceback.tb_lineno,
                         'name'    : exc_traceback.tb_frame.f_code.co_name,
                         'type'    : exc_type.__name__,
                         'message' : exc_value.message, # or see traceback._some_str()
                        }
    print()
    print(traceback.format_exc())
    print()
    print(traceback_template % traceback_details)
    print()


def debug_print_configuration(config, photoshoot):
    """Prints configuration to console."""
    print("Starting selfietorium...")
    print("------------------------")
    print()
    print("Configuration :")
    print()
    print("Template        : " + config.layout)
    print("Pre-PhotoPhrase : " + config.prePhotoPhrase)
    print("Preen Time      : " + str(config.preenTime) + " seconds.")
    print("Shutter Sound   : " + config.shutterSound)
    print("Photo store     : " + config.photostore)
    print("Pre-PhotoPhrase : " + config.prePhotoPhrase)
    print("Update Font     : " + config.Font)
    print("Update Font Size: " + str(config.Size))
    print("Update Font Colour: " + str(config.FontColour))
    print("Printer Name     :" + str(config.PrinterName))
    print("Twitter Screen Name:" + str(config.TweetAuthor))
    print("Twitter Hashtag     :" + str(config.TweetHashTag))

    print()
    print()

if __name__ == '__main__':
    #Set up configuration
    print "WIDTH " + str(WIDTH)
    config = configuration.ConfigFile("boothsettings.json")
    print "WIDTH " + str(WIDTH)
    print "CP1"
    config.Load()
    print "WIDTH " + str(WIDTH)

    debug_print_configuration(config, None)
    #Set up variables
    SHOOTPHOTOSTORE = config.photostore
    SHOOTDIRECTORY = os.path.join(SHOOTPHOTOSTORE,
                         datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
    SCREEN_FONT = config.Font
    SCREEN_FONT_SIZE = config.Size
    SCREEN_FONT_COLOUR = config.FontColour
    PHOTOSOUNDEFFECT = config.shutterSound
    TWEET_TEXT = config.TweetPhrase
    photoshoot = template.LoadPhotoShoot(config.layout)
    debug_print_configuration(config, photoshoot)
    PRINTERNAME = str(config.PrinterName)
    PRINTER = getattr(importlib.import_module("libselfietorium.Printer"), "Printer")(PRINTERNAME)


    #Set Up Screens
    SCREEN_ATTRACT = open('Screens/Attract.svg').read()
    SCREEN_PREEN = open('Screens/Instructions2.svg').read()
    SCREEN_ERROR = open('Screens/Error.svg').read()
    SCREEN_TWITTER = open('Screens/Tweet.svg').read()
    SCREEN_TWITTER_IMAGE =open('Screens/TweetImage.svg').read()
    ERROR_FONT = config.ErrorFont
    ERROR_FONT_SIZE = config.ErrorFontSize
    ERROR_FONT_COLOUR = config.ErrorFontColour

    ACCESS_TOKEN = config.ACCESS_TOKEN
    ACCESS_SECRET = config.ACCESS_SECRET
    CONSUMER_KEY = config.CONSUMER_KEY
    CONSUMER_SECRET = config.CONSUMER_SECRET
    TWITTERAUTHOR = config.TweetAuthor
    HASHTAG = config.TweetHashTag

    util = utilities.utilities()

    SocialMedia = SendTweet.selfie_Tweet(
        CONSUMER_KEY,
        CONSUMER_SECRET,
        ACCESS_TOKEN,
        ACCESS_SECRET,
        HASHTAG,
        TWITTERAUTHOR)

    CamerObject = importlib.import_module("libselfietorium.USBCamera")
    mymethod = getattr(importlib.import_module("libselfietorium.USBCamera"), "USBCamera")()

    state = "ATTRACT"
    pygame.init()
    pygame.mixer.init(48000, -16, 1, 1024)
    CAMERASOUND = pygame.mixer.Sound(PHOTOSOUNDEFFECT)
    print "WIDTH " + str(WIDTH)
    print "HEIGHT " + str(HEIGHT)
    print(pygame.display.Info())
    #pygame.display.set_mode((WIDTH,HEIGHT),0,16)
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.mouse.set_visible(False)
    background = pygame.Surface((WIDTH, HEIGHT))
    background = background.convert()
    background.fill((0, 0, 0))

    cbackground = pygame.Surface((WIDTH, HEIGHT))
    cbackground = cbackground.convert()
    cbackground.fill((200, 255, 255))


    c = pygame.time.Clock()
    while True:
        try:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key == pygame.K_p:
                        if state == "ATTRACT":
                            state = "PREEN"
                    elif event.key == pygame.K_s:
                        CAMERASOUND.play()
                    elif event.key == pygame.K_t:
                        twitter_latest(SCREEN_TWITTER,SCREEN_TWITTER_IMAGE)
                    elif event.key == pygame.K_e:
                        #ErrorScreen(SCREEN_ERROR)
                        raise ValueError('A very specific bad thing happened')
                if state == "ATTRACT":
                    attract_screen(SCREEN_ATTRACT)
                if state == "PREEN":
                    state = preen_screen(photoshoot, SCREEN_PREEN,
                                        config.preenTime)
        except Exception as e:
            error_screen(SCREEN_ERROR, e)


    # c.tick(1)