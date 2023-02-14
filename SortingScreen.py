"""Module for Sorting screen loop"""

import random
import time
import pygame
from dropdownmenu import dropdownmenu
from button import Button
from theme import Theme
from Column import Column
from Slider import Slider


def sortingScreen(screen) -> bool:
    """Main function of the module. Returns boolean when the loop ends. Returns false if the total program should be closed. Returns true otherwise."""
    running = True
    class sortingScreen:
        def __init__(self):
            self.dragging = False
            self.columns = []
            self.quickSortStarted = False
            self.mergeSortStarted = False
            self.heapSortStarted = False
            self.bubbleSortStarted = False
            self.isVisualStarted = False
            self.done = True

    sortingScreenData = sortingScreen()
    initDone = False
    finish = True
    finIndex = 0

    gui_font = pygame.font.Font(None,30)
    title_font = pygame.font.Font(None,50)
    text_surf = title_font.render("Sorting Visualizer",True,'#FFFFFF')

    shuffle = Button('Shuffle',300,40,(1120,260),5,screen,gui_font)
    theme = Button('sea theme',300,40,(1430,260),5,screen,gui_font)
    algo = Button("Quick Sort",300,40,(810,260),5,screen,gui_font)
    start = Button('Start',300,40,(810,210),5,screen,gui_font)

    shuffleIndex = 500
    otherColumnIndex = 0
    temp = None

    theme1 = Theme(0)
    theme2 = Theme(1)
    theme3 = Theme(2)

    themes = ["sea theme","space theme","pastel theme"]
    algorithms = ["Quick Sort","Heap Sort", "Bubble Sort"]

    themeDropDown = dropdownmenu(themes,(1430,310), screen,40,300,gui_font)
    algoDropDown = dropdownmenu(algorithms,(810,310), screen,40,300,gui_font)

    themeToUse = "sea theme"
    algoToUse = "Quick Sort" # "Merge Sort"
    backgroundToUse = theme1.background

    sortingScreenData.isVisualStarted = False

    menuSurface = pygame.Surface((1860,325), pygame.SRCALPHA)


    slider = Slider(10,500,(260,260,490,20),screen,(255,255,255,150),sortingScreenData)
    oldAmount = 10
    columnColor = (255,255,255)
    chronometer = 0
    backward = Button('',Theme.backwardImg.get_rect().width,Theme.backwardImg.get_rect().height,(200,120),5,screen,gui_font,Theme.backwardImg)
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
            sortingScreenData.columns = []
            oldAmount = columnAmount
            shuffleIndex = columnAmount

        text_surf2 = gui_font.render("Column Amount: {}".format(columnAmount),True,'#FFFFFF')

        if theme.draw():
            themeDropDown.reveal()
        
        if algo.draw():
            algoDropDown.reveal()



        screen.blit(text_surf2,(260,210,400,40))

        columnWidth = 1500/columnAmount
        
        for i in range(columnAmount):
            if len(sortingScreenData.columns) < columnAmount:
                turnOffSorts(sortingScreenData)
                initDone = False
                sortingScreenData.columns.append(Column(screen,(255, 255, 255), 210+i*columnWidth,350,columnWidth,i*(500/(columnAmount-1))+10))
            else: # all sortingScreenData.columns are initilazed and ready to oparate
                initDone = True
            sortingScreenData.columns[i].Draw(columnColor)

        if shuffle.draw() and initDone:
            shuffleIndex = 0
            turnOffSorts(sortingScreenData)
        if shuffleIndex < columnAmount:
            otherColumnIndex = random.randint(0,columnAmount-1)
            replaceColumns(sortingScreenData,shuffleIndex,otherColumnIndex)
            shuffleIndex +=1
        if start.draw() and initDone:
            sortingScreenData.done = False
            sortingScreenData.isVisualStarted = True
            chronometer = time.time()

        if themeDropDown.isOpen:
            themeToUse = themeDropDown.Draw()
            if themeToUse != -1:
                theme.text = themeToUse
                if themeToUse == "sea theme":
                    columnColor = theme1.Color
                    backgroundToUse = theme1.background
                elif themeToUse == "space theme":
                    columnColor =theme2.Color
                    backgroundToUse = theme2.background
                elif themeToUse == "pastel theme":
                    columnColor =theme3.Color
                    backgroundToUse = theme3.background
                themeDropDown.reveal()
        elif algoDropDown.isOpen:
            algoToUsetemp = algoDropDown.Draw()
            if algoToUsetemp != -1:
                algo.text = algoToUsetemp
                algoToUse = algoToUsetemp
                algoDropDown.reveal()
        
        if sortingScreenData.isVisualStarted and initDone:
            if algoToUse == "Quick Sort":
                quick_sorter = quick_sort(sortingScreenData,0,columnAmount-1,columnColor)
                sortingScreenData.quickSortStarted = True
                sortingScreenData.isVisualStarted = False
            elif algoToUse == "Merge Sort":
                mergeSorter = mergeSort(sortingScreenData, 0, columnAmount-1)
                sortingScreenData.mergeSortStarted = True
                sortingScreenData.isVisualStarted = False
            elif algoToUse == "Heap Sort":
                heapSorter = heapSort(sortingScreenData)
                sortingScreenData.heapSortStarted = True
                sortingScreenData.isVisualStarted = False
            elif algoToUse == "Bubble Sort":
                bubbleSorter = bubbleSort(sortingScreenData)
                sortingScreenData.bubbleSortStarted = True
                sortingScreenData.isVisualStarted = False
        


        if sortingScreenData.quickSortStarted:
            try:
                next(quick_sorter)
            except StopIteration:
                finish = True
                sortingScreenData.quickSortStarted = False
                chronometer = time.time() - chronometer
                sortingScreenData.done = True

        if sortingScreenData.mergeSortStarted:
            try:
                next(mergeSorter)
            except StopIteration:
                finish = True
                sortingScreenData.mergeSortStarted = False
                chronometer = time.time() - chronometer
                sortingScreenData.done = True

        if sortingScreenData.heapSortStarted:
            try:
                next(heapSorter)
            except StopIteration:
                finish = True
                sortingScreenData.heapSortStarted = False
                chronometer = time.time() - chronometer
                sortingScreenData.done = True
        
        if sortingScreenData.bubbleSortStarted:
            try:
                next(bubbleSorter)
            except StopIteration:
                finish = True
                sortingScreenData.bubbleSortStarted = False
                chronometer = time.time() - chronometer
                sortingScreenData.done = True

        if finish:
            if finIndex < columnAmount +2:
                initDone = False
                if finIndex < columnAmount:
                    sortingScreenData.columns[finIndex].changeColor((0,255,0))
                if 1<finIndex < columnAmount+1:
                    sortingScreenData.columns[finIndex-1].changeColor((0,255,0))
                if 2<finIndex:
                    sortingScreenData.columns[finIndex-2].changeColor((0,255,0))
                finIndex+= 1
            else:
                initDone = True
                finIndex = 0
                finish = False
        drawTimers(sortingScreenData,chronometer,screen,gui_font)
        pygame.display.update()
    return True

def drawTimers(sortingScreenData,chronometer,screen,gui_font):
    if sortingScreenData.done:
        executionTime = gui_font.render("timer: " + str(round(chronometer,3)),True,'#FFFFFF')
    else:
        executionTime = gui_font.render("timer: " + str(round(time.time()-chronometer,3)),True,'#FFFFFF')

    screen.blit(executionTime,(380,140,400,40))

def turnOffSorts(sortingScreenData):
    sortingScreenData.quickSortStarted = False
    sortingScreenData.mergeSortStarted = False
    sortingScreenData.heapSortStarted = False
    sortingScreenData.bubbleSortStarted = False

def replaceColumns(sortingScreenData,firstIndex,secondIndex):
    sortingScreenData.columns[firstIndex].replace(sortingScreenData.columns[secondIndex])
    replaceIndex(sortingScreenData,firstIndex,secondIndex)

def replaceIndex(sortingScreenData,firstIndex,secondIndex):
    temp =sortingScreenData.columns[firstIndex]
    sortingScreenData.columns[firstIndex] = sortingScreenData.columns[secondIndex]
    sortingScreenData.columns[secondIndex] = temp

def partition(sortingScreenData, start, end, columnColor):
    pivot = sortingScreenData.columns[start]
    low = start + 1
    high = end

    while True:
        while low <= high and sortingScreenData.columns[high].height >= pivot.height:
            high = high - 1

        while low <= high and sortingScreenData.columns[low].height <= pivot.height:
            low = low + 1

        if low <= high:
            yield
            replaceColumns(sortingScreenData,low,high)
        else:
            break

    replaceColumns(sortingScreenData,start,high)
    yield high

def quick_sort(sortingScreenData, start, end, columnColor):
    if start >= end:
        return
    run = True
    p = partition(sortingScreenData, start, end, columnColor)

    while run:
        try:
            yield
            a = next(p)
            if a != None:
                funcs = [quick_sort(sortingScreenData, start, a-1, columnColor),quick_sort(sortingScreenData, a+1, end, columnColor)]

                for func in funcs:
                    try:
                        yield from func
                    except StopIteration:
                        pass
        except StopIteration:
            run = False

def merge(sortingScreenData, start, mid, end):
    start2 = mid + 1
    # If the direct merge is already sorted
    if (sortingScreenData.columns[mid].height <= sortingScreenData.columns[start2].height):
        return
    # Two pointers to maintain start
    # of both columnsays to merge
    while (start <= mid and start2 <= end):
        # If element 1 is in right place
        if (sortingScreenData.columns[start].height <= sortingScreenData.columns[start2].height):
            start += 1
        else:
            #value = sortingScreenData.columns[start2].height
            index = start2
            while (index != start):
                #sortingScreenData.columns[index].height = sortingScreenData.columns[index - 1].height
                replaceColumns(sortingScreenData,index,index-1)
                index -= 1
            #sortingScreenData.columns[start].height = value
            replaceColumns(sortingScreenData,start2,start)
            start += 1
            mid += 1
            start2 += 1

def mergeSort(sortingScreenData, l, r):
    if (l < r):
        # Same as (l + r) / 2, but avoids overflow
        # for large l and r
        m = l + (r - l) // 2
        # Sort first and second halves
        m1 = mergeSort(sortingScreenData, l, m)
        try:
            next(m1)
        except StopIteration:
            pass
        m2 = mergeSort(sortingScreenData, m + 1, r)
        try:
            next(m2)
        except StopIteration:
            pass
        merge(sortingScreenData, l, m, r)
    yield

def heapify(sortingScreenData, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2

    if l < n and sortingScreenData.columns[i].height < sortingScreenData.columns[l].height:
        largest = l

    if r < n and sortingScreenData.columns[largest].height < sortingScreenData.columns[r].height:
        largest = r

    if largest != i:
        yield
        replaceColumns(sortingScreenData,i,largest)
        try:
            yield from heapify(sortingScreenData, n, largest)
        except StopIteration:
            pass

def heapSort(sortingScreenData):
    n = len(sortingScreenData.columns)

    funcs = []

    for i in range(n//2, -1, -1):
        funcs.append(heapify(sortingScreenData, n, i))
    for func in funcs:
        try:
            yield from func
        except StopIteration:
            funcs.remove(func)
    funcs = []
    for i in range(n-1, 0, -1):
        funcs.append(i)
        funcs.append(heapify(sortingScreenData, i, 0))
    
    for func in funcs:
        try:
            yield from func
        except StopIteration:
            funcs.remove(func)
        except TypeError:
            replaceColumns(sortingScreenData,func,0)

def bubbleSort(sortingScreenData):
    n = len(sortingScreenData.columns)
    for i in range(n-1):
        for j in range(0, n-i-1):
            if sortingScreenData.columns[j].height > sortingScreenData.columns[j+1].height:
                yield
                replaceColumns(sortingScreenData,j,j+1)

if __name__ == '__main__':
    #initilaze the pygame
    pygame.init()

    # Creating the screen
    screen = pygame.display.set_mode((1920, 1080), pygame.HWSURFACE)

    # Setting title and icon
    pygame.display.set_caption("Visualized Algorithms")
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)

    sortingScreen(screen)