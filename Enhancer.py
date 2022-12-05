from PIL import Image
from PIL import ImageEnhance
import os
from os import listdir
import matplotlib.pyplot as plt
import multiprocessing
import time

class enhancer(multiprocessing.Process):
    def __init__(self, enh_loc, ctr, queue, remainingItems, brightness = 1.5, sharpness = 1.5, contrast = 1.5):
        multiprocessing.Process.__init__(self)
        self.enh_loc = enh_loc
        self.brightness = brightness
        self.sharpness = sharpness
        self.contrast = contrast
        self.ctr = ctr
        self.queue = queue
        self.remainingItems = remainingItems

    def enhance(self):
        #change brightness first
        # print(self.pid)
        while(self.remainingItems.value > 0):
            img , img_name = self.queue.get()
            newImage = ImageEnhance.Brightness(img).enhance(self.brightness)
            newImage = ImageEnhance.Sharpness(newImage).enhance(self.sharpness)
            newImage = ImageEnhance.Contrast(newImage).enhance(self.contrast)
            newImage.save(self.enh_loc + "/" + img_name, "JPEG")
            with self.ctr.get_lock(): 
                self.ctr.value += 1
            with self.remainingItems.get_lock():
                self.remainingItems.value -= 1
            # print(self.remainingItems.value)
            newImage.show()

            # self.close()

    def run(self):
        self.enhance()
        # print(self.name)

class ImageGetter(multiprocessing.Process):
    def __init__(self, path, queue, flist):
        multiprocessing.Process.__init__(self)
        self.path = path
        self.queue = queue
        self.flist = flist
        # print(self.flist)
    def run(self):
        # time.sleep(5)
        # print(self.pid)
        # print(self.flist)
        while(len(self.flist) > 0):
            fname = self.flist.pop()
            img = Image.open(self.path + '\\' + fname)
            self.queue.put([img,fname])
            print(len(self.flist))
            # print("a")
            # img.show()
        self.close()
        

def main():

    # dirname = os.path.dirname(__file__)

    # Ref_Loc = os.path.join(dirname, 'Reference images\\')
    # Enh_Loc = os.path.join(dirname, 'Enhanced images\\')

    # duration = 5
    # process_count = 3
    # brightness = 1.5
    # sharpness = 1.2
    # contrast = 1.1


    Ref_Loc = input("Location of Images: ")
    Enh_Loc = input("Location of Enhanced Images: ")
    # Enhancing time in units
    duration = int(input("input time: "))
    #Brightness
    brightness= float(input("input brightness: "))
    #sharpness
    sharpness= float (input("input sharpness: "))
    #contrast
    contrast = float(input("input contrast: "))
    process_count = int(input("input process count: "))

    g_processes = []
    e_processes = []
    counter = 0;
    with multiprocessing.Manager() as manager:
        t_start = time.time()
        image_queue = multiprocessing.Queue()
        image_sem = multiprocessing.Semaphore(process_count)

        flist = (listdir(Ref_Loc))
        file_list = manager.list(flist)
        counter = multiprocessing.Value('i', 0)
        remainingItems = multiprocessing.Value('i', len(flist))
        q_done = False
        file_sem = multiprocessing.Semaphore(process_count)
        notDone = True
        print(flist)
        while(time.time() < t_start + duration * 60 and notDone): 
            while(len(file_list) > 0):
                while(len(g_processes) < process_count):
                    file_sem.acquire()
                    p = ImageGetter(path = Ref_Loc, queue= image_queue, flist = file_list)
                    p.start()
                    g_processes.append(p)
                    print("g")
                    file_sem.release()

                # if(len(file_list) == 0):
                #     q_done = True
                # print("Here")

            while(not image_queue.empty()):
                while(len(e_processes) < process_count):
                    image_sem.acquire()
                    p = enhancer(enh_loc= Enh_Loc, ctr = counter, queue= image_queue, remainingItems = remainingItems, brightness= brightness, sharpness= sharpness, contrast= contrast)
                    p.start()
                    e_processes.append(p)
                    print("e")
                    image_sem.release()
                if(image_queue.empty()):
                    # print("here")
                    q_done = False
                    notDone = False

    for process in g_processes:
        process.join()
    # print("G")
    for process in e_processes: 
        process.join()
    # print("E")


    t_end = time.time()
    t_total = t_end - t_start
    # time.sleep(15)

    # print(t_total)
    # print(counter.value)
    with open("log_par.txt", "w") as f:
        f.write("Total time taken : {:.4f} \n".format(t_total))
        f.write("Total number of images enhanced: {0} \n".format(counter.value))
        f.write("Enhanced Images Location : {0}".format(Enh_Loc))
        f.close()

          
          
if __name__ == "__main__":
    main() 




