import subprocess
import time
import pyautogui
import cv2

# Chemin vers l'exécutable de LM Studio
lm_studio_path = "C:\\Users\\x\\AppData\\Local\\LM-Studio\\LM Studio.exe"
# Chemin vers le dossier de ressources contenant les images des boutons
resources_path = "C:\\Users\\x\\Desktop\\NeuroPal_Global\\Base_de_donnees\\00_Resources"

# Démarrer LM Studio
subprocess.Popen(lm_studio_path)
# Attendre que l'application démarre
time.sleep(5)

# Capture de l'écran
screenshot = pyautogui.screenshot()

# Charger les images des boutons depuis le chemin des ressources
local_server_button = cv2.imread(f"{resources_path}\\local_server_button.png")
start_server_button = cv2.imread(f"{resources_path}\\start_server_button.png")

# Fonction pour cliquer sur un bouton en utilisant pyautogui et opencv
def click_button(button_image):
    # Trouver le bouton sur l'écran
    button_location = pyautogui.locateOnScreen(button_image, confidence=0.8)
    if button_location:
        # Obtenir le point central du bouton
        button_center = pyautogui.center(button_location)
        # Cliquer sur le bouton
        pyautogui.click(button_center)
        # Attendre 3 secondes après le clic
        time.sleep(3)
    else:
        print("Bouton non trouvé sur l'écran.")

# Cliquer sur le bouton 'Local Server'
click_button(local_server_button)
# Cliquer sur le bouton 'Start Server'
click_button(start_server_button)

