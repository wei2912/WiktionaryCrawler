import time
import sys

# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 100. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 100 or bigger represents 100%
def update(progress):
    barLength = 20 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 100:
        progress = 100
        status = "Done...\r\n"
    block = int(round(barLength*progress/100))
    text = "\rPercent: [%s] %d%% %s" % ("#"*block + "-"*(barLength - block), round(progress), status)
    sys.stdout.write(text)
    sys.stdout.flush()