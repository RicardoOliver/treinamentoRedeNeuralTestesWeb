import tensorflow as tf
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tensorflow.keras.callbacks import Callback

import time



# URL do site a ser testado
url = "https://www.magazineluiza.com.br/"

# Seletor do campo de busca
search_box_selector = "input[id='input-search']"

# Seletor dos resultados de busca
search_results_selector = "img[loading='lazy']"

# Seletor dos botões de adicionar ao carrinho
add_to_cart_button_selector = "button[data-testid='bagButton']"

# Tempo de espera máximo para o carregamento dos elementos
wait_time = 10

driver = webdriver.Firefox()
driver.get(url)


def search(query):
    # Encontre o campo de busca e insira o termo da busca
    search_box = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, search_box_selector)))
    search_box.clear()
    search_box.send_keys(query)
    search_box.send_keys(Keys.RETURN)

    # Espere pelos resultados da busca e retorne-os
    search_results = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, search_results_selector)))
    return search_results


def add_to_cart():
    # Encontre o botão de adicionar ao carrinho e clique nele
    add_to_cart_button = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, add_to_cart_button_selector)))
    add_to_cart_button.click()

    # Espere pelo carrinho aparecer na página e clique nele
    cart_button = WebDriverWait(driver, wait_time).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/carrinho']")))
    cart_button.click()

    # Espere pelo carrinho carregar e retorne o número de itens no carrinho
    cart_count = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, "span[data-testid='cart-products-count']"))).text
    return cart_count


def capture_data():
    # Implemente aqui a lógica para capturar os dados que você quer utilizar como entrada para o modelo
    # Por exemplo, você pode extrair informações do HTML dos resultados de busca para determinado produto
    return [1, 2, 3, 4, 5]


# Crie um conjunto de treinamento com dados de 10 buscas diferentes
training_data = []
for i in range(10):
    query = " {}".format(i)
    search(query)
    time.sleep(2)
    training_data.append(capture_data())

# Crie um modelo de rede neural simples com TensorFlow
model = tf.keras.Sequential([
    tf.keras.layers.Dense(128, activation="relu"),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
])
model.compile(loss="binary_crossentropy",
optimizer="adam", metrics=["accuracy"])

x_train = tf.stack(training_data)
y_train = tf.constant([1, 0, 1, 0, 1, 0, 1, 0, 1, 0])
model.fit(x_train, y_train, epochs=10, batch_size=1)

query = "produto aleatorio"
search(query)
class MyCallback(Callback):
    def on_epoch_end(self, epoch, logs=None):
        if logs.get('accuracy') > 0.9:
            print("\nReached 90% accuracy so cancelling training!")
            self.model.stop_training = True

callbacks = MyCallback()
model.fit(x_train, y_train, epochs=10, callbacks=[callbacks])

quit()