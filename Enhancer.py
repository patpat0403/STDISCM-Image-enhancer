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
        print(self.pid)
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
            print(self.remainingItems.value)
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
            img = Image.open(self.path + fname)
            self.queue.put([img,fname])
            print("a")
            # img.show()
        self.close()
        

def main():

    dirname = os.path.dirname(__file__)

    Ref_Loc = os.path.join(dirname, 'Reference images\\')
    Enh_Loc = os.path.join(dirname, 'Enhanced images\\')

    process_count = 2
    #Enhancing time in units
    # time = int(input("input time: "))
    #Brightness
    # brightness= float(input("input brightness: "))
    #sharpness
    # sharpness= float (input("input sharpness: "))
    #contrast
    # contrast = float(input("input contrast: "))
    g_processes = []
    e_processes = []
    counter = 0;
    with multiprocessing.Manager() as manager:
        image_queue = multiprocessing.Queue()
        t_start = time.time()
        image_sem = multiprocessing.Semaphore(process_count)
        flist = (listdir(Ref_Loc))
        counter = multiprocessing.Value('i', 0)
        remainingItems = multiprocessing.Value('i', len(flist))
        file_list = manager.list(flist)
        q_done = False
        # file_list.append(flist)
        file_sem = multiprocessing.Semaphore(process_count)
        while(len(file_list) > 0):
            while(len(g_processes) < process_count):
                file_sem.acquire()
                p = ImageGetter(path = Ref_Loc, queue= image_queue, flist = file_list)
                p.start()
                g_processes.append(p)
                print("g")
                file_sem.release()
            if(len(file_list) == 0):
                q_done = True

        while(q_done):
            while(len(e_processes) < process_count):
                image_sem.acquire()
                p = enhancer(enh_loc= Enh_Loc, ctr = counter, queue= image_queue, remainingItems = remainingItems)
                p.start()
                e_processes.append(p)
                print("e")
                image_sem.release()
                print(image_sem)
                if(image_queue.empty()):
                    q_done = False
            


        print("X")


        # while not empty
            # while # process <= process
                # add process
            # else ;

    for process in g_processes:
        process.join()
    print("G")
    print(image_queue.empty())
    for process in e_processes: # TODO: fix
        process.join()
    print("E")


    t_end = time.time()
    t_total = t_end - t_start
    # time.sleep(15)

    print(t_total)
    # print(counter.value)

          
          
if __name__ == "__main__":
    main() 




