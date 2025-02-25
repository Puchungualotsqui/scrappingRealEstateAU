import pyautogui
import time


def moveToNormalize(x, y):
    local_x = pyautogui.size()[0] * x
    local_y = pyautogui.size()[1] * y
    pyautogui.moveTo(local_x, local_y)
    return


def openProgram(name, timeWait):
    pyautogui.press('win')
    time.sleep(timeWait)
    pyautogui.write(name, interval=0.1)
    pyautogui.press('enter')
    return

def getHTML(url, folderLocation, newFileName):

    time.sleep(0.1)

    openProgram('Opera', 0.5)
    time.sleep(1)

    pyautogui.write(url, interval=0.01)
    pyautogui.press('enter')
    time.sleep(3)

    # Open inspect element
    pyautogui.hotkey('ctrl', 'shift', 'c')
    time.sleep(0.5)

    moveToNormalize(0.9, 0.19)
    time.sleep(0.1)

    pyautogui.click(button='right')
    time.sleep(0.5)

    # Copy HTML
    pyautogui.press('down', presses=6, interval=0.1)
    pyautogui.press('enter', presses=2, interval=0.1)
    time.sleep(0.1)

    moveToNormalize(0.98, 0.02)
    pyautogui.click()
    time.sleep(0.1)

    # Open program to page HTML
    openProgram('Sublime Text', 0.5)
    time.sleep(0.1)

    pyautogui.hotkey('ctrl', 'n')
    time.sleep(1)

    pyautogui.hotkey('ctrl', 'v')

    # Starts to save the fileD:\Documentos\SPJain\Term2\Intro\Project\html
    pyautogui.hotkey('ctrl', 'shift', 's')
    time.sleep(0.1)

    pyautogui.write(newFileName)
    time.sleep(0.2)

    # Move to change folder location
    pyautogui.press('tab', presses=6, interval=0.1)
    pyautogui.press('enter')
    pyautogui.write(folderLocation)
    pyautogui.press('enter')
    time.sleep(0.1)

    pyautogui.press('tab', presses=9, interval=0.1)
    pyautogui.press('enter')
    time.sleep(0.2)

    moveToNormalize(0.98, 0.02)
    pyautogui.click()
    time.sleep(0.1)

# If you apply filters in the scrapping you need to split the URL
folder = r'D:\Documentos\SPJain\Term2\Intro\Project\html'
url = 'https://www.realestate.com.au/buy/in-{},+nsw/list-{}?misc=ex-no-display-price&source=refinement'
suburb = 'Zetland'

newFileName = 'page'
pages = 12
numberOfFiles = 1051

for i in range(1, pages+1):
    print(i)
    getHTML(url.format(suburb,i), folder, newFileName + str(i+numberOfFiles) + str('.txt'))
