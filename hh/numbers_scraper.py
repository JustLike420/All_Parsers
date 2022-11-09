from bs4 import BeautifulSoup


def main(path: str):
    output_list = []
    with open(f'{path}', 'r', encoding='utf-8') as file:
        src = file.read()
        soup = BeautifulSoup(src, 'lxml')
        items = soup.find_all('div', class_='serp-item')
        for item in items:
            name = item.find('div', class_='resume-search-item__fullname').text.split(',')[0]
            phone = item.find('span', class_='resume__contacts-phone-hidden')
            if phone is not None:
                phone = phone.find('span').text
                if '...' in phone:
                    ...
                else:
                    output_list.append(name + ' ' + phone)
            else:
                continue
    with open('output.txt', 'w', encoding='utf-8') as file:
        for line in output_list:
            file.write(line + '\n')
    print("Работа завершена, проверьте файл output.txt")



if __name__ == "__main__":
    path = input("Введите название файла (например file.html): ")
    main(path)
