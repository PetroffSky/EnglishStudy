import qrcode
import os, os.path


class Generate_QR:
    def __init__(self, url_list):
        with open('words.txt', 'r', encoding='utf-8') as words:
            self.word_list = list(filter(lambda a: len(a) > 0, words.read().split('\n')))
            print(f"Переводим следующие слова: {self.word_list}")

        self.url_list = url_list
        self.generator()


    def generator(self):
        for word, url in zip(self.word_list, self.url_list):
            self.path = f'Results/Images/QR_{word}.png'
            if os.path.isfile(self.path): os.remove(self.path)
            print("Генерируем QR-code")
            print(word, url)
            qr_code = qrcode.make(url)
            type(qr_code)
            qr_code.save(self.path)

        return "QR-codes is Done"
