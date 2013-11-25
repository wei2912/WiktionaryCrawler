import time
import sys

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 100. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 100 or bigger represents 100%
def update(finished, total):
    progress = finished*100/total

    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 100:
        progress = 100
        status = "Done...\r\n"
    block = int(round(barLength*progress/100))
    text = "\rPercent: [%s] %d%% %d/%d %s" % ("#"*block + "-"*(barLength - block), round(progress), finished, total, status)
    sys.stdout.write(text)
    sys.stdout.flush()