import pygame
import random
from colors import *
from settings import *

pygame.init()

FONT_BIG = pygame.font.SysFont('comicsans', 40)
FONT_MEDIUM = pygame.font.SysFont('comicsans', 30)
FONT_SMALL = pygame.font.SysFont('comicsans', 20)

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Sorting visualizer')

name = FONT_MEDIUM.render('VISUALIZER', 1,LIGHT_GREEN)
project = FONT_BIG.render('SORTING', 1, LIGHT_GREEN)
sorting = [FONT_SMALL.render('1. Selection Sort', 1, LIGHT_GREEN),
           FONT_SMALL.render('2. Bubble Sort', 1, LIGHT_GREEN),
           FONT_SMALL.render('3. Merge Sort', 1, LIGHT_GREEN),
           FONT_SMALL.render('4. Quick Sort', 1, LIGHT_GREEN),
           FONT_SMALL.render('5. Heap Sort', 1, LIGHT_GREEN),
           FONT_SMALL.render('6. Insertion Sort', 1, LIGHT_GREEN)]
reset = FONT_SMALL.render('0. Reset', 1, LIGHT_GREEN)


class Bar:
    def __init__(self, x, y, width, height, value):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = LIGHT_YELLOW
        self.value = value

    def reset(self, num):
        self.x = BORDER + num * SPACE
        return self

    def draw(self, win):
        pygame.draw.rect(
            win, self.color, (self.x, self.y, self.width, self.height))

    def check(self):
        self.color = RED

    def done(self):
        self.color = GREEN

    def match(self):
        self.color = L_BLUE

    def back(self):
        self.color = LIGHT_YELLOW


sort = [x for x in range(1, NUM_BAR + 2)]
random.shuffle(sort)
bar = [Bar((BORDER + i * SPACE), (HEIGHT - DOWN - (BAR_HEIGHT * sort[i])),
           BAR_WIDTH, BAR_HEIGHT * sort[i], sort[i]) for i in range(NUM_BAR)]


def main(win):
    clock = pygame.time.Clock()

    global RUN
    global bar
    global SORTED
    while RUN:

        clock.tick(FPS)
        draw(win, bar)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                break

        keys = pygame.key.get_pressed()

        if keys[pygame.K_0]:
            random.shuffle(sort)
            bar = [Bar((BORDER + i * SPACE), (HEIGHT - DOWN - (BAR_HEIGHT * sort[i])), BAR_WIDTH, BAR_HEIGHT * sort[i],
                       sort[i]) for i in range(NUM_BAR)]
            SORTED = False
        if keys[pygame.K_1]:
            check()
            selection(bar, win)
        if keys[pygame.K_2]:
            check()
            bubble(bar, win)
        if keys[pygame.K_3]:
            check()
            merge_sort(bar, 0, len(bar) - 1, win)
        if keys[pygame.K_4]:
            check()
            quick_sort(bar, 0, len(bar) - 1, win)
        if keys[pygame.K_5]:
            check()
            heap_sort(bar, win)
        if keys[pygame.K_6]:
            check()
            insertion(bar, win)

    pygame.quit()


def check():
    global SORTED
    global bar
    if SORTED:
        SORTED = False
        random.shuffle(sort)
        bar = [Bar((BORDER + i * SPACE), (HEIGHT - DOWN - (BAR_HEIGHT * sort[i])),
                   BAR_WIDTH, BAR_HEIGHT * sort[i], sort[i]) for i in range(NUM_BAR)]

# draw function for the screen


def draw(win, bar):
    global reset
    global name
    global sorting
    global project

    win.fill(BLUE)

    pygame.draw.rect(win, DARK_BLUE, (0, 0, 800, 180))
   

    win.blit(project, (30, 20))

    win.blit(name, (40, 90))

    pygame.draw.rect(win, BLUE, (250, 15, 5, 150))

    for i in range(len(sorting)):
        win.blit(sorting[i], (270, 13 + (25 * i)))
    win.blit(reset, (460, 13))

    for i in bar:
        i.draw(win)
    pygame.time.wait(6)

    pygame.display.update()


def selection(bar, win):
    global SORTED
    SORTED = True
    global RUN

    for i in range(len(bar)):
        if not RUN:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                break
        min = i
        for u in range(i + 1, len(bar)):

            bar[min].match()
            bar[u].check()
            draw(win, bar)
            bar[u].back()

            if bar[u].y > bar[min].y:
                bar[min].back()
                min = u

        bar[len(bar) - 1].back()
        temp = bar[min]
        bar[min] = bar[i]
        bar[i] = temp
        bar[min].reset(min)
        bar[i].reset(i).done()


def bubble(bar, win):
    global RUN
    global SORTED
    SORTED = True

    for i in range(len(bar)):
        if not RUN:
            break
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                break

        for j in range(len(bar) - 1 - i):

            bar[j].check()
            draw(win, bar)
            bar[j].back()

            if bar[j].value > bar[j + 1].value:
                temp = bar[j]
                bar[j] = bar[j + 1]
                bar[j + 1] = temp
                bar[j].reset(j)
                bar[j + 1].reset(j + 1)

        bar[len(bar) - 1 - i].done()


def merge(bar, left, mid, right, win):
    temp = []
    i = left
    j = mid + 1

    while i <= mid and j <= right:
        bar[i].check()
        bar[j].check()
        draw(win, bar)
        bar[i].back()
        bar[j].back()
        if bar[i].value < bar[j].value:
            temp.append(bar[i])
            i += 1
        else:
            temp.append(bar[j])
            j += 1
    while i <= mid:
        bar[i].check()
        draw(win, bar)
        bar[i].back()
        temp.append(bar[i])
        i += 1
    while j <= right:
        bar[j].check()
        draw(win, bar)
        bar[j].back()
        temp.append(bar[j])
        j += 1
    k = 0
    for i in range(left, right + 1):
        bar[i] = temp[k]
        bar[i].reset(i)
        bar[i].check()
        draw(win, bar)
        if right - left == len(bar) - 1:
            bar[i].done()
        else:
            bar[i].back()
        k += 1


def merge_sort(bar, left, right, win):
    global SORTED
    SORTED = True
    global RUN

    mid = left + (right - left) // 2
    if left < right:
        merge_sort(bar, left, mid, win)
        merge_sort(bar, mid + 1, right, win)
        if not RUN:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                break
        merge(bar, left, mid, right, win)


def quick_sort(bar, low, high, win):
    global RUN
    global SORTED
    SORTED = True

    if len(bar) == 1:
        return bar
    if low < high:

        pi = partition(bar, low, high, win)

        draw(win, bar)

        quick_sort(bar, low, pi - 1, win)

        if not RUN:
            return
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False
                break

        for i in range(pi + 1):
            bar[i].done()

        quick_sort(bar, pi, high, win)


def partition(bar, low, high, win):
    i = low
    pivot = bar[high]
    pivot.color = ORANGE
    for j in range(low, high):

        bar[j].check()
        bar[i].check()
        draw(win, bar)
        bar[j].back()
        bar[i].back()
        if bar[j].value < pivot.value:

            bar[i], bar[j] = bar[j], bar[i]
            bar[i].reset(i)
            bar[j].reset(j)
            i += 1

    bar[i], bar[high] = bar[high], bar[i]
    bar[i].reset(i)
    pivot.back()
    draw(win, bar)
    bar[high].reset(high)
    return i


def insertion(bar, win):
    global RUN
    global SORTED
    SORTED = True

    for i in range(1, len(bar)):
        bar[i].check()
        draw(win, bar)
        bar[i].back()
        j = i
        while j > 0 and bar[j].value < bar[j - 1].value:
            if not RUN:
                return
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    RUN = False
                    break
            bar[i].check()
            draw(win, bar)
            bar[i].back()
            bar[j], bar[j - 1] = bar[j - 1], bar[j]
            bar[j].reset(j)
            bar[j - 1].reset(j - 1)
            j -= 1
    for i in range(len(bar)):
        bar[i].done()
        pygame.time.delay(1)
        draw(win, bar)


def heap_sort(bar, win):
    global RUN
    global SORTED
    SORTED = True
    n = len(bar)
    for i in range(n // 2 - 1, -1, -1):
        heapify(bar, n, i, win)

    for i in range(n - 1, 0, -1):
        bar[i], bar[0] = bar[0], bar[i]
        bar[i].reset(i)
        bar[0].reset(0)
        bar[i].done()
        draw(win, bar)
        heapify(bar, i, 0, win)


def heapify(bar, n, i, win):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and bar[left].value > bar[largest].value:
        largest = left
    if right < n and bar[right].value > bar[largest].value:
        largest = right
    if largest != i:
        bar[i].check()
        bar[largest].check()
        draw(win, bar)

        bar[i], bar[largest] = bar[largest], bar[i]

        bar[i].reset(i)
        bar[largest].reset(largest)

        bar[i].back()
        bar[largest].back()
        draw(win, bar)

        heapify(bar, n, largest, win)


if __name__ == "__main__":
    main(win)
