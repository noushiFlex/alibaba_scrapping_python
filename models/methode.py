import time,os,requests
def scroll_to_bottom(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
def download_image(img_url, img_name, images_dir_path):
    try:
        if not os.path.exists(images_dir_path):
            os.makedirs(images_dir_path)
            print(f'Dossier d\'images créé: {images_dir_path}')
        
        response = requests.get(img_url)
        if response.status_code == 200:
            img_data = response.content
            img_path = os.path.join(images_dir_path, img_name)
            with open(img_path, 'wb') as img_file:
                img_file.write(img_data)
            print(f"Image téléchargée et sauvegardée à: {img_path}")
            return img_path  # Return path of downloaded image
        else:
            print(f"Échec du téléchargement de l'image : {img_url}")
            return ''
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image: {e}")
        return ''
