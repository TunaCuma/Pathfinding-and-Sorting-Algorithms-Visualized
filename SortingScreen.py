from mimetypes import init
import random
import pygame
from dropdownmenu import dropdownmenu

from theme import Theme

dragging = False
columns = []

from button import Button
class SliderBall:
    def __init__(self,x,y,width,screen,color, rect) -> None:
        self.x = x
        self.y = y
        self.startPos = (x,y)
        self.width = width
        self.screen = screen
        self.color = color
        self.dragging = False
        self.rect = pygame.Rect((self.x-15,self.y-15),(30,30))
        self.parentRect = pygame.Rect(rect)
    def Draw(self):
        pygame.draw.circle(self.screen,(180,188,188,150),(self.x,self.y),15)
        pygame.draw.circle(self.screen,self.color,(self.x,self.y),15,2)
        self.rect = pygame.Rect((self.x-15,self.y-15),(30,30))
        self.check_click()

        return (self.x-self.startPos[0])/self.width

    def check_click(self):
        global dragging
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0]:
            if self.parentRect.collidepoint(mouse_pos) and not dragging:
                dragging = True
            elif dragging and self.startPos[0]<mouse_pos[0]<(self.startPos[0] + self.width + 1):
                self.x = mouse_pos[0]
        elif dragging:
            dragging = False
            
class Slider:
    def __init__(self,min,max,rect,screen,color):
        self.min = min
        self.max = max
        self.rect = rect
        self.screen = screen
        self.color = color
        self.value = min
        self.sliderBall = SliderBall(rect[0],rect[1]+(rect[3]/2),rect[2],self.screen,self.color, self.rect)
    def Draw(self):
        pygame.draw.rect(self.screen,self.color,self.rect,2,border_radius = 12)
        self.value = self.min + (self.max-self.min)*(self.sliderBall.Draw())
        return int(self.value)

class Column:
    def __init__(self, screen, color, x,y,width,height):
        self.screen=screen
        self.color=color
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.paintInside = False
    def Draw(self, columnColor):
        if self.paintInside:
            pygame.draw.rect(self.screen, self.color, (self.x,self.y,self.width,self.height))
            self.paintInside = False
        else:
            pygame.draw.rect(self.screen, columnColor, (self.x,self.y,self.width,self.height), 1)

        self.color = (255, 255, 255)
    
    def replace(self, Column):
        self.changeColor((255,0,0))
        tempx = self.x
        tempy = self.y
        self.x = Column.x
        Column.x = tempx
        self.y = Column.y
        Column.y = tempy
    
    def changeColor(self, color):
        self.color = color
        self.paintInside = True



def sortingScreen(screen):
    global columns
    running = True
    initDone = False
    finish = False
    finIndex = 0

    backwardImg = pygame.image.load('assets/backwards.png')
    background4 = pygame.image.load('assets/background4.png')
    background2 = pygame.image.load('assets/background2.png')
    background3 = pygame.image.load('assets/background3.png')
    gui_font = pygame.font.Font(None,30)
    title_font = pygame.font.Font(None,50)
    text_surf = title_font.render("Sorting Visualizer",True,'#FFFFFF')

    shuffle = Button('Shuffle',300,40,(1120,260),5,screen,gui_font)
    theme = Button('theme 1',300,40,(1430,260),5,screen,gui_font)
    algo = Button("Merge Sort",300,40,(810,260),5,screen,gui_font)
    start = Button('Start',300,40,(810,210),5,screen,gui_font)

    shuffleIndex = 500
    otherColumnIndex = 0
    temp = None

    theme1 = Theme(background2, (255,255,255))
    theme2 = Theme(background4, (30,30,160))
    theme3 = Theme(background3, (180,188,188))

    themeDropDown = dropdownmenu(["theme 1","theme 2","theme 3"],(1430,310), screen,40,300,gui_font)
    algoDropDown = dropdownmenu(["Merge Sort","Quick Sort","Heap Sort", "Bubble Sort"],(810,310), screen,40,300,gui_font)

    themeToUse = "theme 1"
    algoToUse = "Merge Sort"
    backgroundToUse = background2

    themeMenu = False
    algoMenu = False
    quickSortStarted = False
    mergeSortStarted = False
    heapSortStarted = False
    bubbleSortStarted = False

    isVisualStarted = False

    menuSurface = pygame.Surface((1860,325), pygame.SRCALPHA)


    slider = Slider(10,500,(260,260,490,20),screen,(255,255,255,150))
    oldAmount = 10
    columns = []
    columnColor = (255,255,255)
    
    backward = Button('',backwardImg.get_rect().width,backwardImg.get_rect().height,(200,120),5,screen,gui_font,backwardImg)
    while running:
        
        
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(backgroundToUse, (0, 0))
        pygame.draw.rect(menuSurface,(180,188,188,150),(180,0,1860,325))
        pygame.draw.rect(menuSurface,(250,245,245,190),(180,0,1860,325),2)
        screen.blit(menuSurface, (0,0))
        screen.blit(text_surf,(810,140,400,40))
        #pygame.draw.rect(screen, (255, 255, 255), (210,350,1500,600), 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False
        if backward.draw():
            running = False
            return True

        columnAmount = slider.Draw()
        if columnAmount != oldAmount:
            columns = []
            oldAmount = columnAmount
            shuffleIndex = columnAmount

        text_surf2 = gui_font.render("Column Amount: {}".format(columnAmount),True,'#FFFFFF')

        if theme.draw():
            themeMenu = not themeMenu
            algoMenu = False
        
        if algo.draw():
            algoMenu = not algoMenu
            themeMenu = False



        screen.blit(text_surf2,(260,210,400,40))

        columnWidth = 1500/columnAmount
        
        for i in range(columnAmount):
            if len(columns) < columnAmount:
                initDone = False
                columns.append(Column(screen,(255, 255, 255), 210+i*columnWidth,350,columnWidth,i*(500/(columnAmount-1))+10))
            else: # all columns are initilazed and ready to oparate
                initDone = True
            columns[i].Draw(columnColor)

        if shuffle.draw() and initDone:
            shuffleIndex = 0
        if shuffleIndex < columnAmount:
            otherColumnIndex = random.randint(0,columnAmount-1)
            replaceColumns(columns,shuffleIndex,otherColumnIndex)
            shuffleIndex +=1
        if start.draw() and initDone:
            isVisualStarted = True

        if themeMenu:
            themeToUsetemp = themeDropDown.Draw()
            if themeToUsetemp != -1:
                theme.text = themeToUsetemp
                themeToUse = themeToUsetemp
                if themeToUse == "theme 1":
                    columnColor = theme1.Color
                    backgroundToUse = theme1.background
                if themeToUse == "theme 2":
                    columnColor =theme2.Color
                    backgroundToUse = theme2.background
                if themeToUse == "theme 3":
                    columnColor =theme3.Color
                    backgroundToUse = theme3.background
                themeMenu = False
        if algoMenu:
            algoToUsetemp = algoDropDown.Draw()
            if algoToUsetemp != -1:
                algo.text = algoToUsetemp
                algoToUse = algoToUsetemp
                algoMenu = False
        
        if isVisualStarted and initDone:
            if algoToUse == "Quick Sort":
                a = quick_sort(columns,0,columnAmount-1,columnColor)
                quickSortStarted = True
                isVisualStarted = False
            if algoToUse == "Merge Sort":
                mergeSort(columns, 0)
                mergeSortStarted = True
                isVisualStarted = False
            if algoToUse == "Heap Sort":
                c = heapSort(columns)
                heapSortStarted = True
                isVisualStarted = False
            if algoToUse == "Bubble Sort":
                d = bubbleSort(columns)
                bubbleSortStarted = True
                isVisualStarted = False
        

        if quickSortStarted:
            try:
                next(a)
            except StopIteration:
                finish = True
                quickSortStarted = False

        if mergeSortStarted and False:
            try:
                next(b)
            except StopIteration:
                finish = True
                mergeSortStarted = False

        if heapSortStarted:
            try:
                next(c)
            except StopIteration:
                finish = True
                heapSortStarted = False
        
        if bubbleSortStarted:
            try:
                next(d)
            except StopIteration:
                finish = True
                bubbleSortStarted = False

        if finish:
            if finIndex < columnAmount +2:
                initDone = False
                if finIndex < columnAmount:
                    columns[finIndex].changeColor((0,255,0))
                if 1<finIndex < columnAmount+1:
                    columns[finIndex-1].changeColor((0,255,0))
                if 2<finIndex:
                    columns[finIndex-2].changeColor((0,255,0))
                finIndex+= 1
            else:
                initDone = True
                finIndex = 0
                finish = False

        pygame.display.update()



def replaceColumns(columns,firstIndex,secondIndex):
    columns[firstIndex].replace(columns[secondIndex])
    replaceIndex(columns,firstIndex,secondIndex)

def replaceIndex(columns,firstIndex,secondIndex):
    temp =columns[firstIndex]
    columns[firstIndex] = columns[secondIndex]
    columns[secondIndex] = temp

def partition(columns, start, end, columnColor):
    pivot = columns[start]
    low = start + 1
    high = end

    while True:
        while low <= high and columns[high].height >= pivot.height:
            high = high - 1

        while low <= high and columns[low].height <= pivot.height:
            low = low + 1

        if low <= high:
            replaceColumns(columns,low,high)
        else:
            break

    replaceColumns(columns,start,high)
    return high

def quick_sort(columns, start, end, columnColor):
    if start >= end:
        return

    p = partition(columns, start, end, columnColor)

    yield

    funcs = [quick_sort(columns, start, p-1, columnColor),quick_sort(columns, p+1, end, columnColor)]

    for func in funcs:
        try:
            yield from func
        except StopIteration:
            pass

def mergeSort(arr, plus):#it doesnt work for now
    global columns
    print(len(arr))
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]

        mergeSort(L, plus)
        mergeSort(R, plus+mid)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i].height < R[j].height:
                #columns[k] = L[i]
                #replaceColumns(orginalColumns,k+plus,i+plus)
                i += 1
            else:
                #columns[k] = R[j]
                for a in range(j-k):
                    replaceColumns(columns,(j+plus+mid)-a,(j+plus+mid)-a-1)
                    
                j += 1
            k += 1
        
        while i < len(L):
            #columns[k] = L[i]
            #replaceColumns(orginalColumns,k+plus,i+plus)
            i += 1
            k += 1
        
        while j < len(R):
            #columns[k] = R[j]
            for a in range(j-k):
                replaceColumns(columns,(j+plus+mid)-a,(j+plus+mid)-a-1)
                
            j += 1
            k += 1
        

def heapify(columns, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and columns[i].height < columns[l].height:
        largest = l

    if r < n and columns[largest].height < columns[r].height:
        largest = r

    if largest != i:
        yield
        replaceColumns(columns,i,largest)
        try:
            yield from heapify(columns, n, largest)
        except StopIteration:
            pass


def heapSort(columns):
    n = len(columns)

    funcs = []

    for i in range(n//2, -1, -1):
        funcs.append(heapify(columns, n, i))
    for func in funcs:
        try:
            yield from func
        except StopIteration:
            funcs.remove(func)
    funcs = []
    for i in range(n-1, 0, -1):
        funcs.append(i)
        funcs.append(heapify(columns, i, 0))
    
    for func in funcs:
        try:
            yield from func
        except StopIteration:
            funcs.remove(func)
        except TypeError:
            replaceColumns(columns,func,0)

def bubbleSort(columns):
    n = len(columns)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if columns[j].height > columns[j+1].height:
                yield
                replaceColumns(columns,j,j+1)