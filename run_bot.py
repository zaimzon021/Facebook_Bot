import os
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from pywinauto.application import Application
from pywinauto.keyboard import send_keys
import pyautogui
import pyperclip
import logging
from pywinauto import Desktop
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.keyboard import send_keys

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def find_and_click_text(search_text: str, timeout: int = 10, partial: bool = False, text_to_enter: str = None, double_click: bool = False) -> bool:
    """
    Searches for a UI element with the specified text, clicks it, and optionally enters text.

    Args:
        search_text (str): The exact text to search for.
        timeout (int): How long to keep searching (in seconds).
        partial (bool): If True, matches any element containing the text (case-insensitive).
        text_to_enter (str, optional): Text to enter after clicking. Defaults to None.

    Returns:
        bool: True if element was found, clicked, and text entered (if applicable); False otherwise.
    """
    logging.info(f"Searching for text: '{search_text}' (partial match: {partial}, double click: {double_click})")

    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            desktop = Desktop(backend="uia")
            all_windows = desktop.windows()

            # Filter: Include Chrome or active File Explorer; exclude VS Code
            filtered_windows = []
            for win in all_windows:
                    win_title = win.window_text().lower()
                    class_name = win.element_info.class_name or ""

                    if "chrome" in win_title:
                             filtered_windows.append(win)
                    elif class_name == "CabinetWClass" and win.is_active():  # File Explorer (active only)
                             filtered_windows.append(win)
                    elif "visual studio code" in win_title:
                            continue  # Skip VS Code

            for win in filtered_windows:
                try:
                    for el in win.descendants():
                        if not isinstance(el, UIAWrapper):
                            continue

                        el_text = el.window_text().strip().lower()
                        search = search_text.strip().lower()

                        if (partial and search in el_text) or (not partial and el_text == search):
                            logging.info(f"Found element with text: '{el_text}', clicking...")
                            el.set_focus()
                            if double_click:
                                print("Performing double click...")
                                logging.info("Performing double click...")
                                el.double_click_input()
                            else:
                                logging.info("Performing single click...")
                                el.click_input()
                                time.sleep(0.3)
                                rect = el.rectangle()
                                click_x = rect.width() + 10
                                click_y = 0
                                el.click_input(coords=(click_x, click_y))

                            # If text entry is requested
                            if text_to_enter:
                                try:
                                    logging.info(f"Entering text: '{text_to_enter}'")
                                    pyperclip.copy(text_to_enter)
                                    send_keys("^v") 
                                    send_keys("{ENTER}")
                                    logging.info("Text entry successful.")
                                except Exception as typing_error:
                                    logging.error(f"Text entry failed: {typing_error}")
                                    return False

                            return True
                except Exception:
                    continue  # Skip this window on error

        except Exception as e:
            logging.error(f"Failed to enumerate desktop windows: {e}")

        time.sleep(0.5)

    logging.error(f"Text '{search_text}' not found on screen after {timeout} seconds.")
    return False


# ———- CONFIGURATION ———-
# Your Facebook login credentials
FACEBOOK_EMAIL = "zaimzon134@gmail.com"
FACEBOOK_PASSWORD = "zaim.com123*"


PAGE_NAME_TO_SWITCH_TO = "true hearted"


# Use forward slashes (/).
VIDEO_FOLDER_PATH = "C:/Users/Zaim Iftikhar/Downloads/Video/Aismr"


BUSINESS_SUITE_URL = "https://business.facebook.com/latest/content/posts"



class FacebookBot:
    """
    A robust bot that logs into Facebook, handles verification, switches to a 
    specific page, and automates Reel scheduling.
    """
    def __init__(self):
        print("Initializing a new Chrome browser...")
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
        self.wait = WebDriverWait(self.driver, 60)
        print("✅ Browser initialized.")
    
    
    def schedule_reels(self):
        """Main loop to find videos and schedule them."""
        print(f"\nStarting reel scheduling process...")
        try:
            video_files = [f for f in os.listdir(VIDEO_FOLDER_PATH) if f.endswith(('.mp4', '.mov'))]
            if not video_files:
                print("No video files (.mp4, .mov) found in the specified folder.")
                return
        except FileNotFoundError:
            print(f"Error: The folder '{VIDEO_FOLDER_PATH}' was not found. Please check the path.")
            return

        print(f"Found {len(video_files)} videos to schedule.")

        start_date = datetime.now()
        videos_per_day = 3
        time_slots = ["10:00", "16:00", "22:00"]

        for i, video_file in enumerate(video_files):
            day_offset = i // videos_per_day
            time_slot_index = i % videos_per_day
            schedule_date = start_date + timedelta(days=day_offset)
            schedule_time = time_slots[time_slot_index]
            caption = os.path.splitext(video_file)[0]

            print("\n" + "="*50)
            print(f"Processing video {i+1}/{len(video_files)}: {video_file}")
            print(f"Scheduled for: {schedule_date.strftime('%Y-%m-%d')} at {schedule_time}")
            print("="*50)

            success = find_and_click_text(video_file[i], timeout=10, partial=True, double_click=True)
            if success:
                print(f"Found and clicked on video: {video_file[i]}")
    
    # ADD THESE 3 LINES:
                logging.info("Re-focusing on browser and waiting for editor to load...")
            try:
                Schedule_Reels_After_Opening_Video(caption,)
            

            except Exception as e:
                logging.error(f"❌ Failed to find the reel editor after uploading. Skipping video. Error: {e}")

    def login_and_navigate(self):
        
        print("Navigating to facebook.com...")
        self.driver.get("https://www.facebook.com/")

        print("Entering login credentials...")
        email_field = self.wait.until(EC.presence_of_element_located((By.ID, "email")))
        password_field = self.wait.until(EC.presence_of_element_located((By.ID, "pass")))
        
        email_field.send_keys(FACEBOOK_EMAIL)
        password_field.send_keys(FACEBOOK_PASSWORD)
        
        login_button = self.wait.until(EC.element_to_be_clickable((By.NAME, "login")))
        login_button.click()
        print("Login request submitted.")


        print("\n--- ⚠️ ACTION REQUIRED ⚠️ ---")
        input("Please complete any login verification steps in the browser window, then press Enter here to continue...")


        print("\nVerification complete. Forcing navigation to the main Facebook homepage...")
        self.driver.get("https://www.facebook.com/")
        

        print("Waiting for the homepage to be ready...")
        feed_ready_xpath = "//span[contains(text(), \"What's on your mind\")]"
        self.wait.until(EC.presence_of_element_located((By.XPATH, feed_ready_xpath)))
        print("✅ Homepage is ready.")

        print(f"Opening Meta Reel Composer")

        self.driver.get("https://business.facebook.com/latest/reels_composer")

        print("Opened Reel Composer")

        button_xpath = "//*[text()='Add Video']"
        button_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, button_xpath)))
        button_element.click()


        success = find_and_click_text("Zaim Iftikhar", text_to_enter= VIDEO_FOLDER_PATH )
        if success:
            print("Automation completed successfully.")
        else:
            print("Automation failed.")
        
        reels_scheduler_variable = self.schedule_reels()
    def Schedule_Reels_After_Opening_Video((text_to_enter: str = None, timeout: int = 10, partial: bool = False, text_to_enter: str = None, double_click: bool = False)):
        
    end_time = time.time() + timeout
    while time.time() < end_time:
        try:
            desktop = Desktop(backend="uia")
            all_windows = desktop.windows()

            # Filter: Include Chrome or active File Explorer; exclude VS Code
            filtered_windows = []
            for win in all_windows:
                    win_title = win.window_text().lower()
                    class_name = win.element_info.class_name or ""

                    if "chrome" in win_title:
                             filtered_windows.append(win)
                    elif class_name == "CabinetWClass" and win.is_active():  # File Explorer (active only)
                             filtered_windows.append(win)
                    elif "visual studio code" in win_title:
                            continue  # Skip VS Code
                for win in filtered_windows:
                    try:
                        for el in win.descendants():
                            if not isinstance(el, UIAWrapper):
                                continue
                            el_text = el.window_text().strip().lower()
                            search_text = "Describe your reel"
                            search = search_text.strip().lower()
                            if (partial and search in el_text) or (not partial and el_text == search):
                            logging.info(f"Found element with text: '{el_text}', clicking...")
                            el.set_focus()
                            el.click_input()
                            time.sleep(0.3)
                            text_to_enter = 
                            if text_to_enter:
                                try:
                                    logging.info(f"Entering text: '{text_to_enter}'")
                                    pyperclip.copy(text_to_enter)
                                    send_keys("^v") 
                                    send_keys("{ENTER}")
                                    logging.info("Text entry successful.")
                                except Exception as typing_error:
                                    logging.error(f"Text entry failed: {typing_error}")
                            search_text_2 = "Share"
                            search_2 = search.strip().lower()
                            if (partial and search in el_text) or (not partial and el_text == search):
                                try:
                                    logging.info(f"Found element with text: '{search_2}', clicking...")
                                    el.set_focus()        
                                    el.click_input()
                                    time.sleep(0.3)
                                except:
                                    logging.error(f"Could not found Share")
                            el_text_Share_Screen = el.window_text().strip().lower()
                            search_text_3 = "Schedule"
                            search_3 = search_text_3.strip().lower()
                            if (partial and search in el_text) or (not partial and el_text == search):
                                try:
                                    logging.info(f"Found element with text: '{search_3}', clicking...")
                                    el.set_focus()        
                                    el.click_input()
                                    time.sleep(0.3)
                                except:
                                    logging.error(f"Could not found Schedule")


        if(reels_scheduler_variable):
            
             print(f"Scheduling reel: {reels_scheduler_variable.video_file} for {reels_scheduler_variable.schedule_date} at {reels_scheduler_variable.schedule_time}");

             self.driver.switch_to.window(self.driver.current_window_handle)
             try:
                 create_button = self.driver.find_element(By.XPATH, "//span[text()='Create reel' or text()='Create Reel']")
                 create_button.click()
             except:
                 logging.info("Already in reel creation mode or button not found.")
                 pass

    #       -- MINOR FIX FOR IFRAME HANDLING ---
    #       he logic here is more robust for finding the caption field inside a frame.

             # We need to switch out of any frame we might be in before starting
                 self.driver.switch_to.default_content()

             iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
             for frame in iframes:
                 try:
                     self.driver.switch_to.frame(frame)
                     caption_field = self.driver.find_element(
                         By.XPATH, "//textarea[contains(@placeholder, \"Describe your reel\")]"
                     )
                     caption_field.click()
                     caption_field.send_keys(reels_scheduler_variable.video_file)
                     print("✅ Caption entered")
                     break
                 except Exception:
                     self.driver.switch_to.window(self.driver.current_window_handle)
                     continue

             if not reels_scheduler_variable.video_file:
                     print("❌ Could not find caption field in any iframe.")
                     return


    #       ✅ Step 2: Click on "Share"
             try:
                 share_label = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Share')]")))
                 share_label.click()
                 print("✅ Clicked 'Share'")
             except Exception as e:
                 print(f"❌ Could not click 'Share': {e}")
                 return

    #       ✅ Step 3: Click on "Schedule"
             try:
                 schedule_label = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//label[contains(text(), 'Schedule')]")))
                 schedule_label.click()
                 print("✅ Clicked 'Schedule'")
             except Exception as e:
                 print(f"❌ Could not click 'Schedule': {e}")
                 return

    #       ✅ Step 4: Set the Date
             try:
                 date_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='date']")))
                 date_input.click()
                 time.sleep(0.5)
                 date_input.clear()
                 date_input.send_keys(reels_scheduler_variable.schedule_date)
                 print(f"✅ Date set to {reels_scheduler_variable.schedule_date}")
             except Exception as e:
                 print(f"❌ Could not set date: {e}")
                 return

    #       ✅ Step 5: Set the Time
             try:
               time_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='hh:mm am/pm']")))
               time_input.clear()
               time_input.send_keys(reels_scheduler_variable.schedule_time)
               print(f"✅ Time set to {reels_scheduler_variable.schedule_time}")
             except Exception as e:
               print(f"❌ Could not set time: {e}")
               return

    #       ✅ Step 6: Click the Schedule Button
             try:
                 schedule_button = self.wait.until(EC.element_to_be_clickable(
                 (By.XPATH, "//div[@aria-label='Schedule' and @role='button']")))
                 schedule_button.click()
                 print("✅ Reel scheduled successfully.")
             except Exception as e:
                 print(f"❌ Could not click Schedule button: {e}")
        else:
            print("Could Not Find")
    def _upload_and_schedule_single_reel(self, video_path, caption, schedule_date, schedule_time):
        """Handles the UI interaction for a single reel."""
        try:
            print("Clicking 'Create reel' button...")
            create_reel_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Create reel' or text()='Create Reel']")))
            create_reel_button.click()

            print("Uploading video...")
            file_input = self.wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='file']")))
            file_input.send_keys(video_path)

            print("Waiting for video upload to complete...")
            self.wait.until(EC.invisibility_of_element_located((By.XPATH, "//div[@role='progressbar']")))
            print("Video uploaded successfully.")

            print("Adding caption...")
            caption_area = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Reel details']//div[@role='textbox']")))
            caption_area.click()
            caption_area.send_keys(caption)

            next_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']")))
            next_button.click()
            
            print("Setting schedule...")
            schedule_radio_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Schedule']")))
            schedule_radio_button.click()

            date_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='mm/dd/yyyy']")))
            date_input.click(); time.sleep(0.5)
            date_input.clear()
            date_input.send_keys(schedule_date.strftime("%m/%d/%Y"))
            self.driver.find_element(By.TAG_NAME, 'body').click(); time.sleep(1)

            time_input = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='hh:mm am/pm']")))
            time_input.clear()
            time_input.send_keys(schedule_time)
            self.driver.find_element(By.TAG_NAME, 'body').click(); time.sleep(1)

            print("Clicking final 'Schedule' button...")
            final_schedule_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@aria-label='Schedule' and @role='button']")))
            final_schedule_button.click()

            self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Create reel' or text()='Create Reel']")))
            print(f"✅ Successfully scheduled '{caption}'.")
            
            processed_folder = os.path.join(VIDEO_FOLDER_PATH, "uploaded")
            if not os.path.exists(processed_folder):
                os.makedirs(processed_folder)
            os.rename(video_path, os.path.join(processed_folder, os.path.basename(video_path)))
            print(f"Moved video to '{processed_folder}'.")

        except Exception as e:
            print(f"\n--- ❌ An Error Occurred ---")
            print(f"Could not schedule the video: {os.path.basename(video_path)}")
            print(f"Error details: {e}")
            print("Skipping this video and attempting to reset...")
            self.driver.get(BUSINESS_SUITE_URL)
            self.wait.until(EC.presence_of_element_located((By.XPATH, "//span[text()='Create reel' or text()='Create Reel']")))


    def close(self):
        """Keeps the browser open for inspection before closing."""
        print("\nAll tasks completed. The browser will close in 30 seconds.")
        time.sleep(30)
        self.driver.quit()


if __name__ == "__main__":
    bot = None
    try:
        bot = FacebookBot()
        bot.login_and_navigate()
        bot.schedule_reels()
    except Exception as e:
        print(f"\n--- ❌ AN ERROR OCCURRED ❌ ---")
        print(f"Error details: {e}")
        input("Press Enter to exit.")
    finally:
        if bot:
            bot.close()
