#import des bibliothèques
import math
from tkinter import *
from tkinter.filedialog import askopenfilename, SaveAs, SaveFileDialog, asksaveasfile
from PIL import Image, ImageTk, ImageFilter, ImageOps

#déclaration des variables
truc = []
fenetre = Tk()
menufichier = Menu(fenetre)
deroul = Menu(menufichier, tearoff=False, bg='grey')
deral = Menu(menufichier, tearoff=False, bg='grey')
deriol = Menu(menufichier, tearoff=False, bg='grey')
themenb = True
drawing = False
img_width = 0
img_height = 0
taille = 0
couleur = (0,0,0)

#fonctions
def newimage():
    global img_width, img_height, img_edit
    img_new = Image.new(mode='RGB', size=(500, 400), color=(255,255,255))
    img_width = 500
    img_height = 400
    img_edit = img_new.copy()
    editshow(img_edit)

def saveas():
    global img_edit
    image_types = [('jpeg', '*.jpg')]
    saver = asksaveasfile(filetypes=image_types, defaultextension=image_types, initialfile="photo")
    img_edit.save(saver)

def opening():
    global truc, img_height, img_width, img_sized, fichier, img_edit
    fichier = askopenfilename()
    truc = Image.open(fichier)
    img_width, img_height = truc.size
    if img_width > 600:
        img_width = 600
        img_height = math.floor(img_width / truc.width * truc.height)
        img_sized = truc.resize((img_width, img_height))
    elif img_height > 500:
        img_height = 500
        img_width = math.floor(img_height / truc.height * truc.width)
        img_sized = truc.resize((img_width, img_height))
    else:
        img_sized = truc.copy()
    img_edit = img_sized.copy()
    editshow(img_edit)
    nbpixels['text'] = (str(img_width)+" x "+str(img_height))

def editshow(imgshowed):
    global affich
    affich = ImageTk.PhotoImage(imgshowed)
    fond.create_image(math.floor(490 - img_width / 2), math.floor(390 - img_height / 2), anchor=NW, image=affich)
    fond.update()

def effetscouleur():
    global clicked1, img_sized, img_width, img_height, img_edit, img_before
    txtclicked = clicked1.get()
    img_before = img_edit.copy()
    if txtclicked == "inversion des couleurs":
        for i in range(img_width):
            for j in range(img_height):
                px = img_edit.getpixel((i, j))
                img_edit.putpixel((i, j), (255-px[2],255-px[0],255-px[1]))
    elif txtclicked == "noir et blanc":
        for i in range(img_width):
            for j in range(img_height):
                px = img_edit.getpixel((i, j))
                g=int((px[0]+px[1]+px[2])/3)
                img_edit.putpixel((i, j), (g,g,g))
    elif txtclicked == "dessiner les contours":
        img_edit = img_edit.filter(ImageFilter.CONTOUR)
    elif txtclicked == "montrer contrastes":
        img_edit = img_edit.filter(ImageFilter.FIND_EDGES)
    editshow(img_edit)

def effetspixel():
    global clicked2, img_sized, img_width, img_height, img_edit, img_before
    txtclicked = clicked2.get()
    img_before = img_edit.copy()
    if txtclicked == "quadrillage de pixels":
        for i in range(0,img_width,2):
            for j in range(0,img_height,2):
                img_edit.putpixel((i,j),(255,255,255))
    elif txtclicked == "pixel mix":
         for i in range(0,img_width-1,2):
            for j in range(0,img_height-1,2):
                px1 = img_edit.getpixel((i, j))
                px2 = img_edit.getpixel((i+1, j+1))
                px3 = img_edit.getpixel((i+1, j))
                px4 = img_edit.getpixel((i, j+1))
                pxm = ((px1[0]+px2[0]+px3[0]+px4[0])//2,(px1[1]+px2[1]+px3[1]+px4[1])//2,(px1[2]+px2[2]+px3[2]+px4[2])//2)
                img_edit.putpixel((i,j),pxm)
                img_edit.putpixel((i+1,j),pxm)
                img_edit.putpixel((i,j+1),pxm)
                img_edit.putpixel((i+1,j+1),pxm)
    elif txtclicked == "augmenter netteté":
        img_edit = img_edit.filter(ImageFilter.SHARPEN)
    elif txtclicked == "mirroir":
        img_edit = ImageOps.flip(img_edit)
        img_edit = img_edit.rotate(180)
    elif txtclicked == "tourner l'image":
        img_edit = img_edit.rotate(90, Image.BILINEAR, expand = 1)
    nbpixels['text'] = (str(img_width)+" x "+str(img_height))
    editshow(img_edit)

def effetsrogner():
    global clicked3, img_sized, img_width, img_height, img_edit, img_before
    txtclicked = clicked3.get()
    img_before = img_edit.copy()
    if txtclicked == "en haut à droite":
        img_edit = img_edit.crop((math.floor(img_width/2),0,img_width,math.floor(img_height/2)))
    elif txtclicked == "en haut à gauche":
        img_edit = img_edit.crop((0,0,math.floor(img_width/2),math.floor(img_height/2)))
    elif txtclicked == "en bas à droite":
        img_edit = img_edit.crop((math.floor(img_width/2),math.floor(img_height/2),img_width,img_height))
    elif txtclicked == "en bas à gauche":
        img_edit = img_edit.crop((0,math.floor(img_height/2),math.floor(img_width/2),img_height))
    elif txtclicked == "au centre":
        img_edit = img_edit.crop((math.floor(img_width/4),math.floor(img_height/4),math.floor(3*img_width/4),math.floor(3*img_height/4)))
    img_width, img_height = img_edit.size
    nbpixels['text'] = (str(img_width)+" x "+str(img_height))
    editshow(img_edit)

def colorchange():
    global clicked4, couleur
    txtclicked = clicked4.get()
    if txtclicked == "noir":
        couleur = (0,0,0)
    elif txtclicked == "blanc":
        couleur = (255,255,255)
    elif txtclicked == "bleu":
        couleur = (0,0,255)
    elif txtclicked == "rouge":
        couleur = (255,0,0)
    elif txtclicked == "jaune":
        couleur = (255,255,0)
    draw

def drawtaille1():
    global taille
    taille = 1
    draw
def drawtaille2():
    global taille
    taille = 2
    draw
def drawtaille0():
    global taille
    taille = 0
    draw
def drawtaille3():
    global taille
    taille = 3
    draw
def drawtaille4():
    global taille
    taille = 4
    draw

def draw(valeur_souris):
    global img_edit, taille, img_before, couleur
    img_before = img_edit.copy()
    xmouse = valeur_souris.x
    ymouse = valeur_souris.y
    if taille == 1:
        img_edit.putpixel((xmouse-math.floor(490 - img_width / 2), ymouse-math.floor(390 - img_height / 2)),couleur)
    elif taille == 2:
        for i in range(xmouse-math.floor(490 - img_width / 2)-1,xmouse-math.floor(490 - img_width / 2)+1):
            for j in range(ymouse-math.floor(390 - img_height / 2)-1,ymouse-math.floor(390 - img_height / 2)+1):
                img_edit.putpixel((i,j),couleur)
    elif taille == 3:
        for i in range(xmouse-math.floor(490 - img_width / 2)-3,xmouse-math.floor(490 - img_width / 2)+3):
            for j in range(ymouse-math.floor(390 - img_height / 2)-3,ymouse-math.floor(390 - img_height / 2)+3):
                img_edit.putpixel((i,j),couleur)
    elif taille == 4:
        for i in range(xmouse-math.floor(490 - img_width / 2)-5,xmouse-math.floor(490 - img_width / 2)+5):
            for j in range(ymouse-math.floor(390 - img_height / 2)-5,ymouse-math.floor(390 - img_height / 2)+5):
                img_edit.putpixel((i,j),couleur)
    editshow(img_edit)

def doubleimg():
    global img_edit, img_width, img_height, img_before
    img_before = img_edit.copy()
    img_width *= 2
    img_height *= 2
    imdouble = Image.new(mode='RGB', size=(img_width, img_height), color=(255,255,255))
    for i in range(math.floor(img_width/2)):
            for j in range(math.floor(img_height/2)):
                px = img_edit.getpixel((i, j))
                imdouble.putpixel((i*2,j*2),px)
                imdouble.putpixel((i*2+1,j*2+1),px)
                imdouble.putpixel((i*2+1,j*2),px)
                imdouble.putpixel((i*2,j*2+1),px)
    img_edit = imdouble.copy()
    editshow(img_edit)
    nbpixels['text'] = (str(img_width)+" x "+str(img_height))

def halfimg():
    global img_edit, img_width, img_height, img_before
    img_before = img_edit.copy()
    imx = img_width
    imy = img_height
    img_width = math.floor(img_width/2)
    img_height = math.floor(img_height/2)
    imhalf = Image.new(mode='RGB', size=(img_width, img_height), color=(255,255,255))
    for i in range(math.floor(imx)):
            for j in range(math.floor(imy)):
                px = img_edit.getpixel((i, j))
                imhalf.putpixel((math.floor(i/2),math.floor(j/2)),px)
    img_edit = imhalf.copy()
    editshow(img_edit)
    nbpixels['text'] = (str(img_width)+" x "+str(img_height))

def controlz():
    global img_edit, img_before
    editshow(img_before)
    img_edit = img_before.copy()

def theme():
    global fond, fenetre, themenb
    if themenb == True:
        fenetre.config(bg="#EFEFEF")
        fond.config(bg="#EFEFEF")
        bt1.config(bg="#EFEFEF",fg="black")
        bt2.config(bg="#EFEFEF",fg="black")
        bt3.config(bg="#EFEFEF",fg="black")
        bt4.config(bg="#EFEFEF",fg="black")
        bt5.config(bg="#EFEFEF",fg="black")
        bt6.config(bg="#EFEFEF",fg="black")
        bt7.config(bg="#EFEFEF",fg="black")
        bt8.config(bg="#EFEFEF",fg="black")
        bt9.config(bg="#EFEFEF",fg="black")
        bt10.config(bg="#EFEFEF",fg="black")
        bt11.config(bg="#EFEFEF",fg="black")
        coloureffectsmenu.config(bg="#EFEFEF",fg="black")
        pixeleffectsmenu.config(bg="#EFEFEF",fg="black")
        cropeffectsmenu.config(bg="#EFEFEF",fg="black")
        colorsmenu.config(bg="#EFEFEF",fg="black")
        effetcolourtxt.config(bg="#EFEFEF",fg="black")
        effetpixeltxt.config(bg="#EFEFEF",fg="black")
        effetcroptxt.config(bg="#EFEFEF",fg="black")
        drawtxt.config(bg="#EFEFEF",fg="black")
        nbpixels.config(bg="#EFEFEF",fg="black")
        colorc.config(bg="#EFEFEF",fg="black")
        fenetre,fond.update()
        themenb = False
    elif themenb == False:
        fenetre.config(bg="#3C3C3C")
        fond.config(bg="#3C3C3C")
        bt1.config(bg="#3C3C3C",fg="white")
        bt2.config(bg="#3C3C3C",fg="white")
        bt3.config(bg="#3C3C3C",fg="white")
        bt4.config(bg="#3C3C3C",fg="white")
        bt5.config(bg="#3C3C3C",fg="white")
        bt6.config(bg="#3C3C3C",fg="white")
        bt7.config(bg="#3C3C3C",fg="white")
        bt8.config(bg="#3C3C3C",fg="white")
        bt9.config(bg="#3C3C3C",fg="white")
        bt10.config(bg="#3C3C3C",fg="white")
        bt11.config(bg="#3C3C3C",fg="white")
        coloureffectsmenu.config(bg="#3C3C3C",fg="white")
        pixeleffectsmenu.config(bg="#3C3C3C",fg="white")
        cropeffectsmenu.config(bg="#3C3C3C",fg="white")
        colorsmenu.config(bg="#3C3C3C",fg="white")
        effetcolourtxt.config(bg="#3C3C3C",fg="white")
        effetpixeltxt.config(bg="#3C3C3C",fg="white")
        effetcroptxt.config(bg="#3C3C3C",fg="white")
        drawtxt.config(bg="#3C3C3C",fg="white")
        nbpixels.config(bg="#3C3C3C",fg="white")
        colorc.config(bg="#3C3C3C",fg="white")
        fond,fenetre.update()
        themenb = True

#Tkinter
fenetre.geometry('1100x800')
fond = Canvas(fenetre, width = 1080, height = 786, bg = "#3C3C3C")
fond.place(x=8, y=4)
fond.create_line(900,0,900,790, fill="white")

effetcolourtxt=Label(fenetre,text="Choisir un effet de couleur :",font=("@Yu Gothic UI Semibold", 10),fg="white",bg="#3C3C3C")
effetcolourtxt.place(x=910, y=10)
effetpixeltxt=Label(fenetre,text="Choisir un effet de pixel :",font=("@Yu Gothic UI Semibold", 10),fg="white",bg="#3C3C3C")
effetpixeltxt.place(x=910, y=110)
effetcroptxt=Label(fenetre,text="Rogner l'image :",font=("@Yu Gothic UI Semibold", 10),fg="white",bg="#3C3C3C")
effetcroptxt.place(x=910, y=210)
drawtxt=Label(fenetre,text="Crayons :",font=("@Yu Gothic UI Semibold", 10),fg="white",bg="#3C3C3C")
drawtxt.place(x=910, y=310)
nbpixels=Label(fenetre,text=(str(img_width)+" x "+str(img_height)),font=("@Yu Gothic UI Semibold", 10),fg="white",bg="#3C3C3C")
nbpixels.place(x=15,y=766)
colorc=Label(fenetre,text="Couleur du crayon :",font=("@Yu Gothic UI Semibold", 10),fg="white",bg="#3C3C3C")
colorc.place(x=910, y=530)

coloureffects = ["aucun effet","inversion des couleurs","noir et blanc","dessiner les contours","montrer contrastes"]
pixeleffects =["aucun effet","quadrillage de pixels","pixel mix","augmenter netteté","mirroir","tourner l'image"]
cropeffects = ["aucune zone","en haut à droite","en haut à gauche","en bas à droite","en bas à gauche","au centre"]
colorspencil = ["noir","blanc","bleu","rouge","jaune"]
clicked1 = StringVar(fenetre)
clicked1.set(coloureffects[0])
clicked2 = StringVar(fenetre)
clicked2.set(pixeleffects[0])
clicked3 = StringVar(fenetre)
clicked3.set(cropeffects[0])
clicked4 = StringVar(fenetre)
clicked4.set(colorspencil[0])
coloureffectsmenu = OptionMenu(fenetre, clicked1, *coloureffects)
coloureffectsmenu.config(bg="#3C3C3C", fg="white")
coloureffectsmenu.place(x=920,y=32)
pixeleffectsmenu = OptionMenu(fenetre, clicked2, *pixeleffects)
pixeleffectsmenu.config(bg="#3C3C3C", fg="white")
pixeleffectsmenu.place(x=920,y=132)
cropeffectsmenu = OptionMenu(fenetre, clicked3, *cropeffects)
cropeffectsmenu.config(bg="#3C3C3C", fg="white")
cropeffectsmenu.place(x=920,y=232)
colorsmenu = OptionMenu(fenetre, clicked4, *colorspencil)
colorsmenu.config(bg="#3C3C3C", fg="white")
colorsmenu.place(x=920,y=562)

bt1=Button(fenetre, text="Appliquer effet", command=effetscouleur, bg="#3C3C3C", fg="white")
bt1.place(x=922,y=70)
bt4=Button(fenetre, text="Appliquer effet", command=effetspixel, bg="#3C3C3C", fg="white")
bt4.place(x=922,y=170)
bt5=Button(fenetre, text="Rogner", command=effetsrogner, bg="#3C3C3C", fg="white")
bt5.place(x=922,y=270)
bt2=Button(fenetre, text="agrandir l'image X 2", command=doubleimg, bg="#3C3C3C", fg="white")
bt2.place(x=930,y=720)
bt3=Button(fenetre, text="réduire l'image X 2", command=halfimg, bg="#3C3C3C", fg="white")
bt3.place(x=930,y=752)
bt6=Button(fenetre, text="crayon fin", command=drawtaille1, bg="#3C3C3C", fg="white")
bt6.place(x=922,y=340)
bt7=Button(fenetre, text="crayon moyen", command=drawtaille2, bg="#3C3C3C", fg="white")
bt7.place(x=922,y=370)
bt9=Button(fenetre, text="crayon épais", command=drawtaille3, bg="#3C3C3C", fg="white")
bt9.place(x=922,y=400)
bt10=Button(fenetre, text="crayon très épais", command=drawtaille4, bg="#3C3C3C", fg="white")
bt10.place(x=922,y=430)
bt8=Button(fenetre, text="désactiver crayon", command=drawtaille0, bg="#3C3C3C", fg="white")
bt8.place(x=940,y=460)
bt11=Button(fenetre, text="Changer couleur", command=colorchange, bg="#3C3C3C", fg="white")
bt11.place(x=922,y=600)

menufichier.add_cascade(label="Fichier", menu=deroul)
deroul.add_command(label="Nouveau", accelerator="CTRL+N", command=newimage)
deroul.bind_all("<Control-n>", lambda x: newimage())
deroul.add_command(label="Ouvrir", accelerator="CTRL+O", command=opening)
deroul.bind_all("<Control-o>", lambda x: opening())
deroul.add_separator()
deroul.add_command(label="Enregistrer sous", accelerator="CTRL+S", command=saveas)
deroul.bind_all("<Control-s>", lambda x: saveas())
menufichier.add_cascade(label="Affichage", menu=deral)
deral.add_command(label="Changer de thème", accelerator="F4", command=theme)
deral.bind_all("<F4>", lambda x: theme())
menufichier.add_cascade(label="Options", menu=deriol)
deriol.add_command(label="Retour", accelerator="CTRL+Z", command=controlz)
deriol.bind_all("<Control-z>", lambda x: controlz())
deriol.add_command(label="Mise à jour", accelerator="F5", command=fond.update)
deriol.bind_all("<F5>", lambda x: fond.update())
deriol.add_separator()
deriol.add_command(label="Quitter", accelerator="ALT+F4", command=fenetre.destroy)
deriol.bind_all("<Alt-F4>", lambda x: fenetre.destroy())

fenetre.focus_force()
fenetre.title("Photocheap")
fenetre.config(menu=menufichier, bg="#3C3C3C")
fenetre.bind('<B1-Motion>', draw)
fenetre.iconbitmap('iconetoshop.ico')

#demarrage fenetre
fenetre.mainloop()

#créer une fonction pour agrandir, réduire la taille de l'image et mettre la taille de l'image en bas à gauche 400x256