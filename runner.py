import time
import find_get_image
import translater
import gen_qrcode
import docx_save_print


def main():
    # Проверка наличия папок
    results, images = 'Results', 'Images'
    if not os.path.exists(results):
        os.mkdir(results)
        os.mkdir(f"{results}/{images}")
        print("Все необходимые папки созданы")

    find_get_image.Find_Get()
    translater.Translate()
    with open('Results/translate.txt', 'r', encoding='utf-8') as translate:
        url_list = []
        for stroke in translate.read().split('\n'):
            if len(stroke) > 0:
                word, translate, transcription, url = stroke.split(',')
                url_list.append(str(url).strip())
        print(*url_list, sep='\n')

    gen_qrcode.Generate_QR(url_list)
    docx_save_print.Save_Print()


if __name__ == "__main__":
    main()
