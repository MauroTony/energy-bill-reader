import json
import os
from io import BytesIO
import cv2
import numpy as np
from pdf2image import convert_from_path
import camelot
import matplotlib.pyplot as plt
from PIL import Image
from PyPDF2 import PdfFileWriter, PdfFileReader
import img2pdf
def teste1(path_img):
    img2 = cv2.imread(path_img)
    img = cv2.imread(path_img)
    img = img[470:1475, 60:2270]
    # converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # aplica um filtro para remover ruído
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # detecta as bordas na imagem
    edges = cv2.Canny(blur, 100, 500, L2gradient=False, apertureSize=7)

    # encontra os contornos na imagem
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # percorre todos os contornos encontrados
    for contour in contours:
        # encontra o perímetro do contorno
        perimeter = cv2.arcLength(contour, True)

        # aproxima o contorno com um polígono
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)

        # verifica se o polígono tem quatro lados
        if len(approx) == 4 or len(approx) == 3 or len(approx) == 2:
            # desenha o retângulo encontrado na imagem original
            cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)

    # cria uma janela com um nome específico e tamanho ajustável
    cv2.namedWindow('Imagem', cv2.WINDOW_NORMAL)

    # redimensiona a janela para ocupar a largura e altura da tela
    cv2.resizeWindow('Imagem', 1920, 1080)
    # exibe a imagem com os retângulos encontrados
    cv2.imshow('Imagem', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def teste2(path_img):
    img = cv2.imread(path_img)
    # ["25,421,820,55"]
    # img = img[470:1475, 60:2270]

    # converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # aplica um filtro de suavização
    blur = cv2.medianBlur(gray, 5)

    # aplica um filtro de binarização
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # encontra os contornos presentes na imagem binarizada
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # percorre os contornos encontrados
    foto = 1
    for c in contours:
        # calcula o retângulo delimitador do contorno
        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = float(w) / h
        # print(aspect_ratio)
        # if aspect_ratio > 0.1 and aspect_ratio < 10.6:
        # calcula a área do retângulo
        area = w * h
        # Cacula perimetro
        perimeter = cv2.arcLength(c, True)
        # verifica se o retângulo tem uma área suficientemente grande
        if area > 1000:
            # desenha um retângulo verde em volta do retângulo encontrado
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            teste = img[y:y + h, x:x + w]
            #foto_nome = "foto" + str(foto) + ".png"
            #cv2.imwrite(foto_nome, teste)
            #nome_pdf = cast_img_to_pdf(foto_nome)
            #foto = foto + 1
            #teste_camelot(nome_pdf)
            exibe_imagem(teste)
            # escreve a área do retângulo na imagem
            cv2.putText(img, str(area), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    # exibe a imagem com os contornos dos retângulos desenhados
    # cria uma janela com um nome específico e tamanho ajustável
    cv2.namedWindow('Imagem', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagem', 1920, 1080)
    cv2.imshow('Imagem', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # salva imagem

    # deleta_temporarios()

def cast_img_to_pdf(path_img):
    pdf_path = path_img.replace("png", "pdf")
    image = Image.open(path_img)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(pdf_path, "wb")
    file.write(pdf_bytes)
    image.close()
    file.close()
    print("Successfully made pdf file")

    return pdf_path

def deleta_temporarios():
    os.remove('temp.png')
    os.remove('temp.pdf')
def teste3(path_img):
    # Lê a imagem
    img = cv2.imread(path_img)
    img = img[470:1475, 60:2270]
    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplica um filtro de suavização
    blur = cv2.medianBlur(gray, 5)

    # Aplica um filtro de binarização
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Procura por retângulos com títulos
    rects = []
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        # Calcula o retângulo delimitador
        x, y, w, h = cv2.boundingRect(c)
        # Verifica se a área do retângulo é maior que 1000
        if w * h > 1000:
            print(x, y, w, h)
            # Verifica se a linha de interrupção está presente
            if (gray[y, x:x + w] == 0).sum() > w / 2 or (gray[y + h - 1, x:x + w] == 0).sum() > w / 2 or (
                    gray[y:y + h, x] == 0).sum() > h / 2 or (gray[y:y + h, x + w - 1] == 0).sum() > h / 2:
                rects.append((x, y, w, h))

    # Desenha os retângulos na imagem
    for rect in rects:
        x, y, w, h = rect
        area = w * h
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, f'{area} px²', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Exibe a imagem
    cv2.namedWindow('Imagem', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagem', 1920, 1080)
    cv2.imshow('Imagem', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def teste4(path_img):
    # Leitura da imagem
    img = cv2.imread(path_img)
    img = img[470:1475, 60:2270]
    # Conversão para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detecção de bordas usando a função Canny
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detecção de linhas usando a transformada de Hough
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, minLineLength=100, maxLineGap=10)

    # Criação de uma imagem preta para desenhar os retângulos
    rect_img = np.zeros_like(img)

    # Loop para desenhar os retângulos
    for line in lines:
        x1, y1, x2, y2 = line[0]

        # Verificação de linhas horizontais
        if abs(y2 - y1) < abs(x2 - x1) / 2:
            # Cálculo das coordenadas do retângulo
            x = min(x1, x2)
            y = min(y1, y2)
            w = abs(x2 - x1)
            h = abs(y2 - y1)

            # Desenho do retângulo na imagem preta
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Conversão da imagem preta para escala de cinza
    rect_gray = cv2.cvtColor(rect_img, cv2.COLOR_BGR2GRAY)

    # Limiarização da imagem para criar uma máscara
    _, mask = cv2.threshold(rect_gray, 10, 255, cv2.THRESH_BINARY)

    # Aplicação da máscara na imagem original para exibir apenas os retângulos
    masked = cv2.bitwise_and(img, img, mask=mask)

    # Exibição da imagem com os retângulos
    cv2.namedWindow('Imagem', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagem', 1920, 1080)
    cv2.imshow('Imagem', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def teste5(path_img):
    # Lê a imagem
    img = cv2.imread(path_img)
    img = img[470:1475, 60:2270]

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplica um filtro de suavização
    blur = cv2.medianBlur(gray, 5)

    # Aplica um filtro de binarização
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Detecta as linhas na imagem utilizando a Transformada de Hough
    lines = cv2.HoughLinesP(thresh, 1, np.pi / 180, 100, minLineLength=50, maxLineGap=5)

    # Identifica os pontos de intersecção entre as linhas
    intersections = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            x1, y1, x2, y2 = lines[i][0]
            x3, y3, x4, y4 = lines[j][0]
            # Calcula o ponto de intersecção entre as linhas
            d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
            if d != 0:
                xi = int(((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / d)
                yi = int(((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / d)
                intersections.append((xi, yi))

    # Identifica os retângulos a partir dos pontos de intersecção
    rects = []
    for i in range(len(intersections)):
        for j in range(i + 1, len(intersections)):
            xi, yi = intersections[i]
            xj, yj = intersections[j]
            # Calcula a distância entre os pontos
            dist = np.sqrt((xi - xj) ** 2 + (yi - yj) ** 2)
            if dist > 100 and dist < 500:
                # Verifica se os pontos formam um retângulo
                for k in range(len(intersections)):
                    if k != i and k != j:
                        xk, yk = intersections[k]
                        if np.abs((xi - xj) * (yk - yj) - (yi - yj) * (xk - xj)) < 500:
                            # Os pontos formam um retângulo
                            x = min(xi, xj, xk)
                            y = min(yi, yj, yk)
                            w = max(xi, xj, xk) - x
                            h = max(yi, yj, yk) - y
                            area = w * h
                            rects.append((x, y, w, h, area))

    # Desenha os retângulos na imagem e exibe a área
    for rect in rects:
        x, y, w, h, area = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, str(area), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Exibe a imagem com os retângulos desenhados
    cv2.namedWindow('Imagem', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagem', 1920, 1080)
    cv2.imshow('Imagem', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def teste6(path_img):
    # Lê a imagem
    img = cv2.imread(path_img)
    img = img[470:1475, 60:2270]

    # Converte a imagem para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplica um filtro de suavização
    blur = cv2.medianBlur(gray, 5)

    # Aplica um filtro de binarização
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Encontra os contornos na imagem
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Filtra os contornos que são retângulos
    rects = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        # print("perimeter: ", perimeter)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        if len(approx) == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            aspect_ratio = float(w) / h
            if aspect_ratio > 0.5 and aspect_ratio < 1.6:
                area = w * h
                rects.append((x, y, w, h, area))

    # Desenha os retângulos na imagem e exibe a área
    for rect in rects:
        x, y, w, h, area = rect
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(img, str(area), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Exibe a imagem com os retângulos desenhados
    cv2.namedWindow('Imagem', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagem', 1920, 1080)
    cv2.imshow('Imagem', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def exibe_imagem(img):
    cv2.namedWindow('Imagem', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Imagem', 1920, 1080)
    cv2.imshow('Imagem', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def recorta_parte_em_branco1(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar uma limiarização para separar o fundo da imagem
    _, thresh = cv2.threshold(gray, 220, 255, cv2.THRESH_BINARY)

    # Inverter a imagem para que o fundo seja preto e as informações sejam brancas
    inv = cv2.bitwise_not(thresh)
    #exibe_imagem(inv)
    # Encontrar os contornos na imagem
    contours, _ = cv2.findContours(inv, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontrar o maior contorno que está na parte inferior da imagem
    largest_contour = None
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if y > img.shape[0] * 0.7 and w > img.shape[1] * 0.9:
            if largest_contour is None or cv2.contourArea(contour) > cv2.contourArea(largest_contour):
                largest_contour = contour

    # Cortar a imagem na posição do maior contorno encontrado
    if largest_contour is not None:
        x, y, w, h = cv2.boundingRect(largest_contour)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        img = img[0:y, 0:img.shape[1]]
    return img

def recorta_parte_em_branco2(img):
    # Inverter as cores da imagem
    inv = cv2.bitwise_not(img)

    # Identificar a posição do y que contém a última parte branca da imagem
    y_last_white = None
    for y in range(inv.shape[0] - 1, 0, -1):
        if 255 in inv[y, :]:
            y_last_white = y
            break

    # Exibir a posição do y que contém a última parte branca da imagem
    print('A última parte branca da imagem está na posição y =', y_last_white)
    img = img[0:y_last_white, :]
    return img
def cria_img_unica(path_pdf):
    # Converter o arquivo PDF em uma lista de imagens
    pages = convert_from_path(path_pdf, dpi=300)

    # Converter cada imagem em um array do OpenCV
    images = []
    qtd_pages = len(pages)
    page_atual = 1
    for page in pages:
        image = cv2.cvtColor(np.array(page), cv2.COLOR_RGB2BGR)
        exibe_imagem(image)
        if page_atual == 1:
            image = image[750:2200, 115:3392]
        elif page_atual == qtd_pages:
            image = image[750:1850, 115:3392]
        else:
            #print("page_atual: ", page_atual)
            image = image[750:2200, 115:3392]

        #image1 = recorta_parte_em_branco1(image)
        #exibe_imagem(image1)
        image2 = recorta_parte_em_branco2(image)
        #exibe_imagem(image2)
        #exibe_imagem(image)
        images.append(image2)
        page_atual += 1

    # Juntar as imagens verticalmente
    result_img = cv2.vconcat(images)

    # Salvar a imagem resultante
    cv2.imwrite('result2.png', result_img)

def teste_camelot(path_img, x_pdf, y_pdf, x_final, y_final, pagina):

    tables = camelot.read_pdf(
        path_img,
        pages=str(pagina),
        flavor='stream',
        edge_tol=50,
        row_tol=10,
        #columns=ref_colunas_model1,
        #table_areas=[f"{int(122/4.216346154)},{int((2475 - 826) / 4.274611399)},{int(3385/4.216346154)},{int((2475 - 1281) / 4.274611399)}"]
        table_areas=[
            f"{int(x_pdf / 4.216346154)},{int((2475 - y_pdf) / 4.274611399)},{int(x_final / 4.216346154)},{int((2475 - y_final) / 4.274611399)}"]
    )
    # plota tabela
    print(tables)
    camelot.plot(tables[0], kind='contour')
    plt.show(block=True)
    table_df = tables[0].df
    dict_data = table_df.to_dict()
    json_data = json.dumps(dict_data, indent=4, ensure_ascii=False)
    print(json_data)


def teste_cast_coordenadas(path_pdf):
    pagina = 5
    pages = convert_from_path(path_pdf, dpi=300)
    print("pages: ", len(pages))
    image = cv2.cvtColor(np.array(pages[pagina-1]), cv2.COLOR_RGB2BGR)
    img = image[750:2200, 115:3392]

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # aplica um filtro de binarização
    thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # encontra os contornos presentes na imagem binarizada
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # percorre os contornos encontrados
    foto = 1
    ultimo_x = -1
    for c in contours:
        # calcula o retângulo delimitador do contorno
        x, y, w, h = cv2.boundingRect(c)
        aspect_ratio = float(w) / h
        # print(aspect_ratio)
        # if aspect_ratio > 0.1 and aspect_ratio < 10.6:
        # calcula a área do retângulo
        area = w * h
        # Cacula perimetro
        perimeter = cv2.arcLength(c, True)
        # verifica se o retângulo tem uma área suficientemente grande
        if area > 352000:
            # desenha um retângulo verde em volta do retângulo encontrado
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print("x: ", x, "y: ", y, "w: ", w, "h: ", h)
            teste = img[y:y + h, x:x + w]
            exibe_imagem(teste)
            if x != 0 and x != ultimo_x:
                x_pdf = x + 115
                y_pdf = y + 718
                x_final = x_pdf + w
                y_final = y_pdf + h
                teste_camelot(path_pdf, x_pdf, y_pdf, x_final, y_final, pagina)
                ultimo_x = x
            #teste = img[y:y + h, x:x + w]
            # foto_nome = "foto" + str(foto) + ".png"
            # cv2.imwrite(foto_nome, teste)
            # nome_pdf = cast_img_to_pdf(foto_nome)
            # foto = foto + 1
            # teste_camelot(nome_pdf)
            #exibe_imagem(teste)
            # escreve a área do retângulo na imagem
            cv2.putText(img, str(area), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

        #exibe_imagem(img)
# carrega a imagem
"""for imgs in os.listdir('pdfs/pages'):
    path_img = 'pdfs/pages/' + imgs
    print(path_img)
    teste2(path_img)"""
path_img = 'result2.png'
#cria_img_unica('pdfs/Extrato Girlene.pdf')
# teste1(path_img)
#teste2(path_img)
# teste3(path_img)
# teste4(path_img)
# teste5(path_img)
# teste6(path_img)
#teste_camelot("pdfs/Extrato Girlene.pdf")
teste_cast_coordenadas("../pdfs/relacoes_prev.pdf")