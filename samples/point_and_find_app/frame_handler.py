import cv2 as cv

class FrameHandler:

    def __init__(self, img_files):
        self.img_files = img_files

        self.current_img_file_point = 0

    def show_next(self):
        self.current_img_file_point += 1
        self.current_img_file_point %= len(self.img_files)

        return self.get_current_img()

    def show_previous(self):
        self.current_img_file_point -= 1

        if self.current_img_file_point < 0:
            self.current_img_file_point += len(self.img_files)

        return self.get_current_img()

    def get_current_img(self):
        file_name = self.img_files[self.current_img_file_point]
        return file_name, cv.imread(file_name, 1)





