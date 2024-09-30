import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service

class Watcher:
    DIRECTORY_TO_WATCH = r"C:\Users\snoussi\Desktop\folder"  # Change this to your folder path

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    def process(self, event):
        if event.is_directory:
            return
        elif event.event_type == 'created':
            print(f"Received created event - {event.src_path}")
            send_file_to_whatsapp(event.src_path)

    def on_created(self, event):
        self.process(event)

def send_file_to_whatsapp(file_path):
    options = webdriver.ChromeOptions()
    options.add_argument('--user-data-dir=./User_Data')  # To keep the session alive

    # Ensure the path to chromedriver is correct
    service = Service('https://storage.googleapis.com/chrome-for-testing-public/126.0.6478.126/win64/chrome-headless-shell-win64.zip')  # Update this to the actual path of chromedriver if necessary

    driver = webdriver.Chrome(service=service, options=options)
    driver.get("https://web.whatsapp.com")
    
    time.sleep(15)  # Wait for QR code scan

    # Adjusting the XPath to find the search box
    search_box = driver.find_element('xpath', '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.click()
    search_box.send_keys("56046939")
    search_box.send_keys(Keys.RETURN)

    time.sleep(2)  # Wait for chat to open

    attach_button = driver.find_element('xpath', '//span[@data-icon="clip"]')
    attach_button.click()

    time.sleep(1)  # Wait for the attachment menu to open

    file_input = driver.find_element('xpath', '//input[@type="file"]')
    file_input.send_keys(os.path.abspath(file_path))

    time.sleep(1)  # Wait for the file to be attached

    send_button = driver.find_element('xpath', '//span[@data-icon="send"]')
    send_button.click()

    time.sleep(5)  # Wait for the file to be sent
    driver.quit()

if __name__ == '__main__':
    w = Watcher()
    w.run()

