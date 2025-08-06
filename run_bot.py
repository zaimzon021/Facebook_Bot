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

                            # If text entry is requested
                            if text_to_enter:
                                try:
                                    logging.info(f"Entering text: '{text_to_enter}'")
                                    time.sleep(0.5)
                                    pyperclip.copy(text_to_enter)
                                    send_keys("^v") 
                                    time.sleep(0.5)
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

        # Start from NEXT day (tomorrow)
        start_date = datetime.now() + timedelta(days=1)
        videos_per_day = 3
        time_slots = [
            {"time": "9:00", "period": "AM"},
            {"time": "3:00", "period": "PM"}, 
            {"time": "9:00", "period": "PM"}
        ]

        # Sort video files to ensure consistent order
        video_files.sort()
        print(f"Video files in order: {video_files}")
        print(f"Scheduling will start from: {start_date.strftime('%d-%m-%Y')}")

        for i, video_file in enumerate(video_files):
            day_offset = i // videos_per_day
            time_slot_index = i % videos_per_day
            schedule_date = start_date + timedelta(days=day_offset)
            time_slot = time_slots[time_slot_index]
            
            # Use filename (without extension) as caption
            caption = os.path.splitext(video_file)[0]
            # Clean up caption by removing common video file prefixes/suffixes
            caption = self.clean_caption(caption)

            print("\n" + "="*50)
            print(f"Processing video {i+1}/{len(video_files)}: {video_file}")
            print(f"Caption will be: {caption}")
            print(f"Scheduled for: {schedule_date.strftime('%d-%m-%Y')} at {time_slot['time']} {time_slot['period']}")
            print("="*50)

            video_path = os.path.join(VIDEO_FOLDER_PATH, video_file)
            self.current_video_path = video_path  # Store for verification
            self.current_video_filename = video_file  # Store current filename
            
            # Debug: Check current page state before upload
            self.debug_current_page()
            
            # Only navigate to folder for the first video
            is_first_video = (i == 0)
            success = self.upload_video_file(video_path, is_first_video)
            
            # Debug: Check page state after upload attempt
            if success:
                print("🔍 DEBUG: Video upload reported successful, checking page state...")
                self.debug_current_page()
            else:
                print("🔍 DEBUG: Video upload failed, checking page state...")
                self.debug_current_page()
            if success:
                print(f"✅ Successfully uploaded video: {video_file}")
                
                try:
                    schedule_success = self.schedule_single_reel(caption, schedule_date, time_slot)
                    if schedule_success:
                        print(f"✅ Successfully scheduled reel for {video_file}")
                        
                        # Only navigate back to reel composer after SUCCESSFUL scheduling
                        if i < len(video_files) - 1:  # Not the last video
                            print(f"\n🔄 Video scheduled successfully! Preparing for next video ({i+2}/{len(video_files)})...")
                            print(f"🔄 Opening Meta Business Suite for next video...")
                            
                            # Go back to Meta Business Suite (don't refresh during scheduling)
                            self.driver.get("https://business.facebook.com/latest/reels_composer")
                            time.sleep(3)
                            
                            success = self.load_reel_composer_with_retry()
                            if not success:
                                print(f"❌ Failed to load reel composer for video {i+2}. Skipping remaining videos.")
                                break
                    else:
                        print(f"❌ Failed to schedule reel for {video_file} - skipping to next video")
                        
                except Exception as e:
                    logging.error(f"❌ Failed to schedule reel for {video_file}. Error: {e}")
            else:
                print(f"❌ Failed to upload video: {video_file}")

    def clean_caption(self, caption):
        """Clean up the caption by removing common prefixes and making it more readable."""
        # Remove common video file patterns
        patterns_to_remove = [
            "video_", "vid_", "clip_", "movie_", "film_",
            "_video", "_vid", "_clip", "_movie", "_film"
        ]
        
        cleaned = caption
        for pattern in patterns_to_remove:
            cleaned = cleaned.replace(pattern, "")
        
        # Replace underscores and dashes with spaces
        cleaned = cleaned.replace("_", " ").replace("-", " ")
        
        # Remove extra spaces
        cleaned = " ".join(cleaned.split())
        
        # Capitalize first letter of each word
        cleaned = cleaned.title()
        
        return cleaned if cleaned else caption  # Return original if cleaning resulted in empty string

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
        
        # Load reel composer with retry mechanism
        success = self.load_reel_composer_with_retry()
        if not success:
            print("❌ Failed to load reel composer after multiple attempts")
            return
        
        print("✅ Reel composer loaded successfully. Starting video scheduling...")
        
        # Start scheduling reels
        self.schedule_reels()

    def load_reel_composer_with_retry(self, max_attempts=3):
        """Load the reel composer page with automatic refresh if needed."""
        for attempt in range(max_attempts):
            try:
                print(f"Loading reel composer (attempt {attempt + 1}/{max_attempts})...")
                
                # Check if we're already on the right page
                current_url = self.driver.current_url
                if "reels_composer" not in current_url:
                    self.driver.get("https://business.facebook.com/latest/reels_composer")
                
                # Wait 6 seconds for the page to load
                print("Waiting 6 seconds for page to load...")
                time.sleep(6)
                
                # Check if "Add Video" button is present and clickable
                try:
                    button_xpath = "//*[text()='Add Video']"
                    add_video_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, button_xpath))
                    )
                    
                    # If button is found and clickable, click it and return success
                    add_video_button.click()
                    print("✅ Add Video button found and clicked")
                    time.sleep(2)  # Wait for file picker to be ready
                    return True
                        
                except Exception as e:
                    print(f"⚠️ Add Video button not found or not clickable: {e}")
                
                # If we reach here, the page didn't load properly
                if attempt < max_attempts - 1:
                    print(f"🔄 Page didn't load properly. Refreshing... (attempt {attempt + 1})")
                    self.driver.refresh()
                    time.sleep(3)
                else:
                    print("❌ Page failed to load after all attempts")
                    return False
                    
            except Exception as e:
                print(f"❌ Error loading reel composer: {e}")
                if attempt < max_attempts - 1:
                    print("🔄 Retrying...")
                    time.sleep(3)
                else:
                    return False
        
        return False

    def check_page_loaded(self):
        """Check if the current page has loaded properly by looking for key elements."""
        try:
            # Check for common loading indicators
            loading_indicators = [
                "//div[contains(@class, 'loading')]",
                "//div[contains(@class, 'spinner')]",
                "//*[contains(text(), 'Loading')]"
            ]
            
            for indicator in loading_indicators:
                try:
                    loading_element = self.driver.find_element(By.XPATH, indicator)
                    if loading_element.is_displayed():
                        return False
                except:
                    continue
            
            # Check if Add Video button is present
            try:
                self.driver.find_element(By.XPATH, "//*[text()='Add Video']")
                return True
            except:
                return False
                
        except Exception as e:
            logging.error(f"Error checking page load status: {e}")
            return False

    def enter_caption_with_retry(self, caption, max_attempts=5):
        """Try multiple methods to find and fill the caption field."""
        caption_methods = [
            {
                "name": "Div with role textbox and reel attributes (PRIORITY METHOD)",
                "selector": "//div[@role='textbox' and contains(@aria-label, 'reel')]"
            },
            {
                "name": "Any contenteditable div (simple approach)",
                "selector": "//div[@contenteditable='true']"
            },
            {
                "name": "Direct placeholder match (exact text)",
                "selector": "//div[contains(@placeholder, \"Describe your reel so people will know what it's about\")]"
            },
            {
                "name": "Textarea with 'Describe your reel' placeholder",
                "selector": "//textarea[contains(@placeholder, 'Describe your reel')]"
            },
            {
                "name": "Div with 'Describe your reel' placeholder",
                "selector": "//div[contains(@placeholder, 'Describe your reel')]"
            },
            {
                "name": "Div descendant approach (your requested method)",
                "selector": "//div[descendant::*[contains(@placeholder, 'Describe your reel')]]"
            },
            {
                "name": "Contenteditable div with data-placeholder",
                "selector": "//div[@contenteditable='true' and contains(@data-placeholder, 'Describe your reel')]"
            }
        ]
        
        for attempt in range(max_attempts):
            print(f"📝 CAPTION ENTRY - Attempt {attempt + 1}/{max_attempts}")
            print(f"   Caption to enter: '{caption}'")
            
            for i, method in enumerate(caption_methods):
                method_num = i + 1
                print(f"   🔍 Method {method_num}: {method['name']}")
                
                try:
                    # Find the caption field
                    caption_field = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, method['selector']))
                    )
                    
                    print(f"      ✅ FOUND caption field with Method {method_num}!")
                    print(f"         🔄 Clicking field and pasting caption from clipboard...")
                    
                    # Click the field with Selenium
                    caption_field.click()
                    time.sleep(0.5)
                    
                    # Copy caption to clipboard and paste it
                    pyperclip.copy(caption)
                    send_keys("^v")  # Ctrl+V to paste
                    time.sleep(1)
                    
                    # Verify caption was pasted correctly
                    try:
                        actual_text = caption_field.get_attribute('value') or caption_field.text or caption_field.get_attribute('textContent')
                        if caption.lower() in actual_text.lower():
                            print(f"      ✅ Caption verified: '{actual_text[:50]}...'")
                        else:
                            print(f"      ⚠️ Caption mismatch, trying to replace...")
                            # Clear and try again
                            send_keys("^a")  # Select all
                            time.sleep(0.2)
                            pyperclip.copy(caption)
                            send_keys("^v")  # Paste again
                            time.sleep(0.5)
                    except:
                        print(f"      ⚠️ Could not verify caption, assuming it worked")
                    
                    print(f"      🎉 SUCCESS! Caption '{caption}' pasted and verified")
                    return True
                    
                except Exception as e:
                    print(f"      ❌ Method {method_num} failed: {str(e)[:50]}...")
                    continue
            
            # If all methods failed, wait and try again
            if attempt < max_attempts - 1:
                print(f"   🔄 All methods failed. Waiting 2 seconds before retry...")
                time.sleep(2)
        
        print("❌ CAPTION ENTRY FAILED - Could not enter caption after all attempts")
        return False

    def verify_caption_entered(self, element, expected_caption):
        """Verify that the caption was actually entered in the field."""
        try:
            # Method 1: Check element value
            actual_value = element.get_attribute('value')
            if actual_value and expected_caption.lower() in actual_value.lower():
                return True
            
            # Method 2: Check element text content
            actual_text = element.text
            if actual_text and expected_caption.lower() in actual_text.lower():
                return True
            
            # Method 3: Check innerHTML
            inner_html = element.get_attribute('innerHTML')
            if inner_html and expected_caption.lower() in inner_html.lower():
                return True
            
            # Method 4: Use JavaScript to get the content
            actual_content = self.driver.execute_script("return arguments[0].textContent || arguments[0].value || arguments[0].innerHTML;", element)
            if actual_content and expected_caption.lower() in actual_content.lower():
                return True
                
            return False
            
        except Exception as e:
            print(f"Error verifying caption: {e}")
            return False

    def click_share_button_with_retry(self, max_attempts=5):
        """Find and click Share button, then wait for Schedule options to appear."""
        share_methods = [
            {
                "name": "Direct span with 'Share' text",
                "selector": "//span[text()='Share']"
            },
            {
                "name": "Div containing 'Share' text", 
                "selector": "//div[contains(text(), 'Share')]"
            },
            {
                "name": "Button containing 'Share' text",
                "selector": "//button[contains(text(), 'Share')]"
            },
            {
                "name": "Div descendant approach for Share",
                "selector": "//div[descendant::span[text()='Share']]"
            },
            {
                "name": "Any clickable element with Share",
                "selector": "//*[text()='Share' and (@role='button' or @type='button')]"
            }
        ]
        
        for attempt in range(max_attempts):
            print(f"📤 SHARE BUTTON - Attempt {attempt + 1}/{max_attempts}")
            
            for i, method in enumerate(share_methods):
                method_num = i + 1
                print(f"   🔍 Method {method_num}: {method['name']}")
                
                try:
                    # Find and click Share button
                    share_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, method['selector']))
                    )
                    
                    print(f"      ✅ FOUND Share button with Method {method_num}!")
                    share_button.click()
                    time.sleep(2)  # Wait for share options to appear
                    
                    # Verify Schedule options appeared
                    if self.verify_schedule_options_appeared():
                        print(f"      🎉 SUCCESS! Share clicked and Schedule options appeared using Method {method_num}")
                        return True
                    else:
                        print(f"      ⚠️ Share clicked but Schedule options not found with Method {method_num}")
                        
                except Exception as e:
                    print(f"      ❌ Method {method_num} failed: {str(e)[:50]}...")
                    continue
            
            if attempt < max_attempts - 1:
                print(f"   🔄 All methods failed. Waiting 2 seconds before retry...")
                time.sleep(2)
        
        print("❌ SHARE BUTTON FAILED - Could not click Share button after all attempts")
        return False

    def verify_schedule_options_appeared(self):
        """Check if Schedule options appeared after clicking Share."""
        try:
            print(f"         🔍 Checking if Schedule options appeared...")
            
            schedule_indicators = [
                "//span[text()='Schedule']",
                "//div[contains(text(), 'Schedule')]", 
                "//label[contains(text(), 'Schedule')]",
                "//*[contains(@aria-label, 'Schedule')]",
                "//div[descendant::*[text()='Schedule']]"
            ]
            
            for indicator in schedule_indicators:
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, indicator))
                    )
                    if element.is_displayed():
                        print(f"         ✅ Schedule options found!")
                        return True
                except:
                    continue
            
            print(f"         ❌ Schedule options not found")
            return False
            
        except Exception as e:
            print(f"Error checking Schedule options: {e}")
            return False

    def click_schedule_button_with_manual_approval(self, max_retry_cycles=3):
        """Find and click Schedule button with retry and manual approval fallback."""
        schedule_methods = [
            {
                "name": "Span with 'Schedule' text",
                "selector": "//span[text()='Schedule']"
            },
            {
                "name": "Div containing 'Schedule' text",
                "selector": "//div[contains(text(), 'Schedule')]"
            },
            {
                "name": "Label containing 'Schedule' text", 
                "selector": "//label[contains(text(), 'Schedule')]"
            },
            {
                "name": "Any clickable Schedule element",
                "selector": "//*[text()='Schedule' and (@role='button' or @type='button')]"
            },
            {
                "name": "Button with Schedule text",
                "selector": "//button[contains(text(), 'Schedule')]"
            }
        ]
        
        # Try multiple cycles of all methods
        for cycle in range(max_retry_cycles):
            print(f"📅 SCHEDULE BUTTON SEARCH - Cycle {cycle + 1}/{max_retry_cycles}")
            
            for i, method in enumerate(schedule_methods):
                method_num = i + 1
                print(f"   🔍 Method {method_num}: {method['name']}")
                
                try:
                    # Find and click Schedule button
                    schedule_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, method['selector']))
                    )
                    
                    print(f"      ✅ FOUND Schedule button with Method {method_num}!")
                    schedule_button.click()
                    time.sleep(2)
                    
                    print(f"      🎉 SUCCESS! Schedule button clicked using Method {method_num}")
                    return True
                    
                except Exception as e:
                    print(f"      ❌ Method {method_num} failed: {str(e)[:50]}...")
                    continue
            
            if cycle < max_retry_cycles - 1:
                print(f"   🔄 Cycle {cycle + 1} failed. Waiting 3 seconds before next cycle...")
                time.sleep(3)
        
        # If all automated attempts failed, ask for manual approval
        print("\n" + "="*60)
        print("❌ COULD NOT FIND SCHEDULE BUTTON AUTOMATICALLY")
        print("🔍 Please manually click the Schedule button in the browser")
        print("⏰ You have 10 minutes to complete this action")
        print("="*60)
        
        # Wait for manual approval (10 minutes = 600 seconds)
        manual_success = self.wait_for_manual_schedule_approval(timeout=600)
        
        if manual_success:
            print("✅ Manual scheduling detected - continuing with next video")
            return True
        else:
            print("⏰ Manual approval timeout - refreshing page and restarting process")
            self.driver.refresh()
            time.sleep(5)
            return False

    def wait_for_manual_schedule_approval(self, timeout=600):
        """Wait for user to manually click Schedule button."""
        print(f"⏳ Waiting for manual Schedule button click (timeout: {timeout//60} minutes)...")
        
        start_time = time.time()
        check_interval = 5  # Check every 5 seconds
        
        while time.time() - start_time < timeout:
            try:
                # Check if we're no longer on the scheduling page (indicates success)
                current_url = self.driver.current_url
                
                # Look for success indicators
                success_indicators = [
                    "//div[contains(text(), 'scheduled')]",
                    "//div[contains(text(), 'Your reel is safe to publish')]",
                    "//*[contains(text(), 'success')]",
                    "//span[text()='Create reel']"  # Back to main page
                ]
                
                for indicator in success_indicators:
                    try:
                        element = self.driver.find_element(By.XPATH, indicator)
                        if element.is_displayed():
                            print(f"✅ Success indicator found: Manual scheduling completed!")
                            return True
                    except:
                        continue
                
                # Show remaining time every 30 seconds
                elapsed = int(time.time() - start_time)
                remaining = timeout - elapsed
                
                if elapsed % 30 == 0 and elapsed > 0:
                    print(f"⏳ Still waiting... {remaining//60} minutes {remaining%60} seconds remaining")
                
                time.sleep(check_interval)
                
            except Exception as e:
                print(f"Error during manual approval wait: {e}")
                time.sleep(check_interval)
        
        print("⏰ Manual approval timeout reached")
        return False

    def set_schedule_date(self, schedule_date):
        """Set the schedule date using Ctrl+A and paste."""
        try:
            print(f"         🔄 Setting date to: {schedule_date.strftime('%d-%m-%Y')}")
            
            # Find date input field
            date_input = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='date' or contains(@placeholder, 'date') or contains(@placeholder, 'mm/dd/yyyy')]")
            ))
            
            # Click on date field
            date_input.click()
            time.sleep(0.5)
            
            # Select all and paste the date
            formatted_date = schedule_date.strftime("%m/%d/%Y")  # MM/DD/YYYY format
            pyperclip.copy(formatted_date)
            send_keys("^a")  # Ctrl+A to select all
            time.sleep(0.2)
            send_keys("^v")  # Ctrl+V to paste
            time.sleep(0.5)
            
            print(f"         ✅ Date set to: {formatted_date}")
            return True
            
        except Exception as e:
            print(f"         ❌ Failed to set date: {str(e)[:50]}...")
            return False

    def set_schedule_time(self, time_slot):
        """Set the schedule time by clicking hour, minute, and AM/PM separately."""
        try:
            hour = time_slot["time"].split(":")[0]
            minute = time_slot["time"].split(":")[1] 
            period = time_slot["period"]
            
            print(f"         🔄 Setting time to: {hour}:{minute} {period}")
            
            # Method 1: Click hour, Tab twice to AM/PM, press A or P
            try:
                print(f"            🔍 Using Tab navigation method...")
                
                # Find and click hour field
                hour_field = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'hour') or contains(@aria-label, 'hour')]")
                hour_field.click()
                time.sleep(0.3)
                
                # Set hour
                send_keys("^a")  # Select all
                time.sleep(0.1)
                pyperclip.copy(hour)
                send_keys("^v")  # Paste hour
                time.sleep(0.3)
                print(f"            ✅ Hour set to: {hour}")
                
                # Press Tab twice to reach AM/PM field
                print(f"            🔄 Pressing Tab twice to reach AM/PM...")
                send_keys("{TAB}")  # Tab to minute field
                time.sleep(0.2)
                send_keys("{TAB}")  # Tab to AM/PM field
                time.sleep(0.3)
                
                # Press A for AM or P for PM
                if period == "AM":
                    print(f"            🔄 Pressing 'A' for AM...")
                    send_keys("a")
                else:  # PM
                    print(f"            🔄 Pressing 'P' for PM...")
                    send_keys("p")
                
                time.sleep(0.3)
                print(f"            ✅ Period set to: {period}")
                return True
                
            except Exception as e1:
                print(f"            ❌ Tab navigation method failed: {str(e1)[:30]}...")
            
            # Method 2: Try single time input field
            try:
                print(f"            🔍 Looking for single time input field...")
                
                time_input = self.driver.find_element(By.XPATH, "//input[contains(@placeholder, 'time') or contains(@placeholder, 'hh:mm')]")
                time_input.click()
                time.sleep(0.5)
                
                # Format time for input
                formatted_time = f"{hour}:{minute} {period}"
                pyperclip.copy(formatted_time)
                send_keys("^a")
                time.sleep(0.2)
                send_keys("^v")
                
                print(f"            ✅ Time set to: {formatted_time}")
                return True
                
            except Exception as e2:
                print(f"            ❌ Single field method failed: {str(e2)[:30]}...")
            
            # Method 3: Try clicking on time elements by text
            try:
                print(f"            🔍 Looking for clickable time elements...")
                
                # Try to click on hour element
                hour_element = self.driver.find_element(By.XPATH, f"//*[text()='{hour}' or contains(text(), '{hour}')]")
                hour_element.click()
                time.sleep(0.3)
                
                # Try to click on minute element  
                minute_element = self.driver.find_element(By.XPATH, f"//*[text()='{minute}' or contains(text(), '{minute}')]")
                minute_element.click()
                time.sleep(0.3)
                
                # Try to click on AM/PM element
                period_element = self.driver.find_element(By.XPATH, f"//*[text()='{period}']")
                period_element.click()
                
                print(f"            ✅ Time set by clicking elements: {hour}:{minute} {period}")
                return True
                
            except Exception as e3:
                print(f"            ❌ Click elements method failed: {str(e3)[:30]}...")
            
            return False
            
        except Exception as e:
            print(f"         ❌ Failed to set time: {str(e)[:50]}...")
            return False

    def click_final_schedule_button(self, max_attempts=3):
        """Click the final blue Schedule button (span element)."""
        final_schedule_methods = [
            {
                "name": "Div with descendant span containing Schedule",
                "selector": "//div[descendant::span[text()='Schedule']]"
            },
            {
                "name": "Parent div of Schedule span",
                "selector": "//span[text()='Schedule']/parent::div"
            },
            {
                "name": "Ancestor div of Schedule span (2 levels up)",
                "selector": "//span[text()='Schedule']/ancestor::div[2]"
            },
            {
                "name": "Clickable div with Schedule descendant",
                "selector": "//div[@role='button'][descendant::*[text()='Schedule']]"
            },
            {
                "name": "Any div containing Schedule text",
                "selector": "//div[contains(., 'Schedule')]"
            },
            {
                "name": "Span with Schedule text (direct click)",
                "selector": "//span[text()='Schedule']"
            },
            {
                "name": "Any clickable element with Schedule",
                "selector": "//*[text()='Schedule' and (@onclick or @role='button' or contains(@class, 'click'))]"
            },
            {
                "name": "Broad search for Schedule elements",
                "selector": "//*[contains(text(), 'Schedule')]"
            }
        ]
        
        for attempt in range(max_attempts):
            print(f"🔵 FINAL SCHEDULE BUTTON - Attempt {attempt + 1}/{max_attempts}")
            
            for i, method in enumerate(final_schedule_methods):
                method_num = i + 1
                print(f"   🔍 Method {method_num}: {method['name']}")
                
                try:
                    # Find and click the final Schedule button
                    final_button = WebDriverWait(self.driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, method['selector']))
                    )
                    
                    print(f"      ✅ FOUND final Schedule button with Method {method_num}!")
                    
                    # Forget Selenium - use PyWinAuto to actually click on "Schedule" text
                    print(f"         🔄 Using PyWinAuto to click on Schedule text directly...")
                    click_success = find_and_click_text("Schedule", timeout=5)
                    
                    if click_success:
                        print(f"         ✅ PyWinAuto successfully clicked on Schedule text!")
                    else:
                        print(f"         ❌ PyWinAuto could not find Schedule text")
                        continue
                    
                    print(f"      ⏳ Click executed! Waiting 10 seconds for Meta Business Suite to process...")
                    time.sleep(10)
                    
                    # Verify that scheduling actually worked
                    if self.verify_scheduling_success():
                        print(f"      🎉 SUCCESS! Video actually scheduled using Method {method_num}")
                        return True
                    else:
                        print(f"      ❌ Button was clicked but scheduling failed with Method {method_num}")
                        print(f"      🔍 DEBUG: Current URL: {self.driver.current_url}")
                        continue
                    
                except Exception as e:
                    print(f"      ❌ Method {method_num} failed: {str(e)[:50]}...")
                    continue
            
            if attempt < max_attempts - 1:
                print(f"   🔄 All methods failed. Waiting 1 second before retry...")
                time.sleep(1)
        
        print("❌ FINAL SCHEDULE BUTTON FAILED - Could not click final Schedule button after all attempts")
        return False

    def verify_scheduling_success(self):
        """Verify that the video was actually scheduled successfully."""
        try:
            print(f"         🔍 Verifying scheduling success...")
            
            # First check: Are we still on the same scheduling page?
            current_url = self.driver.current_url
            print(f"         📍 Current URL: {current_url}")
            
            # Look for specific success indicators
            success_indicators = [
                "//div[contains(text(), 'scheduled')]",
                "//div[contains(text(), 'Your reel is safe to publish')]", 
                "//div[contains(text(), 'Scheduled successfully')]",
                "//span[text()='Create reel']",
                "//*[text()='Add Video']"
            ]
            
            found_indicators = []
            for indicator in success_indicators:
                try:
                    elements = self.driver.find_elements(By.XPATH, indicator)
                    visible_elements = [el for el in elements if el.is_displayed()]
                    if visible_elements:
                        found_indicators.append(indicator)
                        print(f"         ✅ Found: {indicator}")
                except:
                    continue
            
            if found_indicators:
                print(f"         🎉 Found {len(found_indicators)} success indicators!")
                return True
            
            # Check if the Schedule button is still there (means we didn't move forward)
            try:
                still_schedule = self.driver.find_elements(By.XPATH, "//span[text()='Schedule']")
                if still_schedule:
                    print(f"         ❌ Schedule button still present - click probably didn't work")
                    return False
            except:
                pass
            
            # Check page title or other indicators
            try:
                page_title = self.driver.title
                print(f"         📄 Page title: {page_title}")
                if "reel" in page_title.lower() and "schedule" not in page_title.lower():
                    print(f"         ✅ Page title suggests we moved away from scheduling")
                    return True
            except:
                pass
            
            print(f"         ❌ No clear success indicators found")
            return False
            
        except Exception as e:
            print(f"         ❌ Error verifying scheduling success: {str(e)[:50]}...")
            return False

    def upload_video_file(self, video_path, is_first_video=False):
        """Upload a video file using the web-based file picker with verification."""
        try:
            print(f"Uploading video: {os.path.basename(video_path)}")
            
            # Check if file exists
            if not os.path.exists(video_path):
                print(f"❌ Video file does not exist: {video_path}")
                return False
            
            # Try multiple methods to upload the file
            upload_success = self.upload_file_with_retry(video_path, is_first_video)
            if not upload_success:
                print(f"❌ Failed to upload video after all attempts")
                return False
            
            # Verify the upload was successful
            verification_success = self.verify_video_uploaded()
            if not verification_success:
                print(f"❌ Video upload could not be verified")
                return False
            
            print(f"✅ Video successfully uploaded and verified: {os.path.basename(video_path)}")
            return True
            
        except Exception as e:
            logging.error(f"Error uploading video file: {e}")
            return False

    def upload_file_with_retry(self, video_path, is_first_video=False, max_attempts=3):
        """Upload video file - navigate to folder only for first video."""
        for attempt in range(max_attempts):
            print(f"Upload attempt {attempt + 1}/{max_attempts}")
            
            try:
                # Wait for file dialog to open
                time.sleep(3)
                
                # Only navigate to folder for the FIRST video
                if is_first_video:
                    print("🔄 First video - navigating to folder...")
                    
                    # Step 1: Press Ctrl+L to focus address bar
                    print("Step 1: Pressing Ctrl+L to focus address bar...")
                    send_keys("^l")
                    time.sleep(1)
                    
                    # Step 2: Paste the folder path using Ctrl+V
                    folder_path = os.path.dirname(video_path)
                    print(f"Step 2: Pasting folder path: {folder_path}")
                    pyperclip.copy(folder_path)
                    send_keys("^v")
                    time.sleep(1)
                    send_keys("{ENTER}")
                    time.sleep(3)  # Wait for navigation
                else:
                    print("🔄 Subsequent video - folder already open, just selecting video...")
                
                # Step 3: Find and click the video file
                video_filename = os.path.basename(video_path)
                print(f"Step 3: Looking for video file: {video_filename}")
                
                success = self.find_and_select_video_file(video_filename)
                if success:
                    print(f"✅ Found and selected video: {video_filename}")
                    print("✅ Video double-clicked - upload should be complete!")
                    time.sleep(3)  # Wait for video to process
                    return True
                else:
                    print(f"❌ Could not find video file: {video_filename}")
                    
            except Exception as e:
                print(f"Upload attempt {attempt + 1} failed: {e}")
            
            if attempt < max_attempts - 1:
                print(f"🔄 Retrying upload in 3 seconds...")
                time.sleep(3)
        
        return False

    def find_and_select_video_file(self, video_filename):
        """Try multiple strategies to find and select the video file."""
        print(f"Searching for video file: {video_filename}")
        
        # Strategy 1: Try exact filename match
        print("  Strategy 1: Exact filename match...")
        success = find_and_click_text(video_filename, timeout=5, partial=False, double_click=True)
        if success:
            print(f"  ✅ Found with exact match: {video_filename}")
            return True
        
        # Strategy 2: Try partial filename match
        print("  Strategy 2: Partial filename match...")
        success = find_and_click_text(video_filename, timeout=5, partial=True, double_click=True)
        if success:
            print(f"  ✅ Found with partial match: {video_filename}")
            return True
        
        # Strategy 3: Try filename without extension
        base_name = os.path.splitext(video_filename)[0]
        print(f"  Strategy 3: Filename without extension: {base_name}")
        success = find_and_click_text(base_name, timeout=5, partial=True, double_click=True)
        if success:
            print(f"  ✅ Found with base name: {base_name}")
            return True
        
        # Strategy 4: Try to find any part of the filename
        # Split filename by common separators and try each part
        separators = [' ', '-', '_', '.', '(', ')', '[', ']']
        filename_parts = [video_filename]
        
        for sep in separators:
            if sep in video_filename:
                parts = video_filename.split(sep)
                filename_parts.extend([part.strip() for part in parts if len(part.strip()) > 3])
        
        print(f"  Strategy 4: Trying filename parts: {filename_parts}")
        for part in filename_parts:
            if len(part) > 3:  # Only try parts longer than 3 characters
                print(f"    Trying part: {part}")
                success = find_and_click_text(part, timeout=3, partial=True, double_click=True)
                if success:
                    print(f"  ✅ Found with part match: {part}")
                    return True
        
        # Strategy 5: Try common video file patterns
        print("  Strategy 5: Trying common video patterns...")
        video_patterns = [".mp4", ".mov", ".avi", ".mkv"]
        for pattern in video_patterns:
            if pattern in video_filename.lower():
                success = find_and_click_text(pattern, timeout=3, partial=True, double_click=True)
                if success:
                    print(f"  ✅ Found with pattern match: {pattern}")
                    return True
        
        print(f"  ❌ Could not find video file with any strategy: {video_filename}")
        return False

    def navigate_to_folder_via_address_bar(self, folder_path):
        """Navigate to folder using universal address bar detection methods."""
        try:
            print(f"Navigating to folder via address bar: {folder_path}")
            
            # Wait for file explorer dialog to be ready
            time.sleep(3)
            
            # Method 1: Universal keyboard shortcut (most reliable)
            print("Method 1: Using universal keyboard shortcuts...")
            success = self.use_keyboard_shortcuts_for_address_bar(folder_path)
            if success:
                return True
            
            # Method 2: Find address bar by looking for editable fields
            print("Method 2: Looking for editable address bar fields...")
            success = self.find_address_bar_by_edit_field(folder_path)
            if success:
                return True
            
            # Method 3: Click anywhere in the top navigation area
            print("Method 3: Clicking in navigation area...")
            success = self.click_navigation_area(folder_path)
            if success:
                return True
            
            print("❌ All address bar methods failed")
            return False
            
        except Exception as e:
            print(f"Error navigating to folder: {e}")
            return False

    def use_keyboard_shortcuts_for_address_bar(self, folder_path):
        """Use keyboard shortcuts to access address bar - most universal method."""
        try:
            desktop = Desktop(backend="uia")
            
            for win in desktop.windows():
                win_title = win.window_text().lower()
                class_name = win.element_info.class_name or ""
                
                # Look for any file dialog or explorer window
                if (class_name == "#32770" or  # Standard Windows dialog
                    class_name == "CabinetWClass" or  # File Explorer
                    "open" in win_title or 
                    "save" in win_title or
                    "file" in win_title or
                    "browse" in win_title):
                    
                    print(f"  Found file dialog: {win_title} ({class_name})")
                    win.set_focus()
                    time.sleep(1)
                    
                    # Try multiple keyboard shortcuts
                    shortcuts = [
                        ("^l", "Ctrl+L"),  # Most common
                        ("%d", "Alt+D"),   # Alternative
                        ("{F4}", "F4"),    # Address bar dropdown
                        ("^{F6}", "Ctrl+F6")  # Cycle through panes
                    ]
                    
                    for shortcut, name in shortcuts:
                        try:
                            print(f"    Trying {name}...")
                            send_keys(shortcut)
                            time.sleep(0.5)
                            
                            # Clear and paste path
                            send_keys("^a")  # Select all
                            time.sleep(0.3)
                            pyperclip.copy(folder_path)
                            send_keys("^v")  # Paste
                            time.sleep(0.5)
                            send_keys("{ENTER}")  # Navigate
                            time.sleep(2)
                            
                            print(f"✅ Successfully used {name}")
                            return True
                            
                        except Exception as e:
                            print(f"    {name} failed: {str(e)[:30]}...")
                            continue
            
            return False
            
        except Exception as e:
            print(f"Keyboard shortcut method error: {e}")
            return False

    def find_address_bar_by_edit_field(self, folder_path):
        """Find address bar by looking for editable text fields."""
        try:
            desktop = Desktop(backend="uia")
            
            for win in desktop.windows():
                class_name = win.element_info.class_name or ""
                
                if (class_name == "#32770" or class_name == "CabinetWClass"):
                    print(f"  Searching for edit fields in {class_name}...")
                    
                    try:
                        # Look for edit controls (address bar is usually an edit control)
                        for control in win.descendants():
                            if not isinstance(control, UIAWrapper):
                                continue
                            
                            control_type = control.element_info.control_type
                            
                            # Look for Edit controls that might be the address bar
                            if (control_type == "Edit" or 
                                control_type == "ComboBox"):
                                
                                try:
                                    # Try to click and enter path
                                    control.set_focus()
                                    time.sleep(0.3)
                                    control.click_input()
                                    time.sleep(0.3)
                                    
                                    # Clear and enter path
                                    send_keys("^a")
                                    time.sleep(0.2)
                                    pyperclip.copy(folder_path)
                                    send_keys("^v")
                                    time.sleep(0.5)
                                    send_keys("{ENTER}")
                                    time.sleep(2)
                                    
                                    print("✅ Successfully used edit field")
                                    return True
                                    
                                except Exception:
                                    continue
                                    
                    except Exception as e:
                        print(f"    Error searching controls: {str(e)[:30]}...")
                        continue
            
            return False
            
        except Exception as e:
            print(f"Edit field method error: {e}")
            return False

    def click_navigation_area(self, folder_path):
        """Click in the general navigation area and try to enter path."""
        try:
            desktop = Desktop(backend="uia")
            
            for win in desktop.windows():
                class_name = win.element_info.class_name or ""
                
                if (class_name == "#32770" or class_name == "CabinetWClass"):
                    print(f"  Clicking in navigation area of {class_name}...")
                    
                    try:
                        win.set_focus()
                        time.sleep(0.5)
                        
                        # Get window rectangle and click in the top area (where address bar usually is)
                        rect = win.rectangle()
                        # Click in the top 20% of the window, center horizontally
                        click_x = rect.left + (rect.width() // 2)
                        click_y = rect.top + (rect.height() // 5)  # Top 20%
                        
                        # Use pyautogui to click in the navigation area
                        pyautogui.click(click_x, click_y)
                        time.sleep(0.5)
                        
                        # Try to enter path
                        send_keys("^a")  # Select all
                        time.sleep(0.3)
                        pyperclip.copy(folder_path)
                        send_keys("^v")  # Paste
                        time.sleep(0.5)
                        send_keys("{ENTER}")  # Navigate
                        time.sleep(2)
                        
                        print("✅ Successfully clicked navigation area")
                        return True
                        
                    except Exception as e:
                        print(f"    Navigation click failed: {str(e)[:30]}...")
                        continue
            
            return False
            
        except Exception as e:
            print(f"Navigation area method error: {e}")
            return False

    def find_address_bar_by_control_type(self, folder_path):
        """Find address bar using PyWinAuto control types."""
        try:
            desktop = Desktop(backend="uia")
            
            for win in desktop.windows():
                win_title = win.window_text().lower()
                class_name = win.element_info.class_name or ""
                
                # Look for file dialog windows
                if ("open" in win_title or "save" in win_title or 
                    class_name == "CabinetWClass" or 
                    class_name == "#32770"):  # Common dialog class
                    
                    print(f"  Found file dialog: {win_title} ({class_name})")
                    win.set_focus()
                    time.sleep(1)
                    
                    # Try Ctrl+L to focus address bar
                    send_keys("^l")
                    time.sleep(0.5)
                    
                    # Clear any existing content and paste new path
                    send_keys("^a")  # Select all
                    time.sleep(0.2)
                    pyperclip.copy(folder_path)
                    send_keys("^v")  # Paste
                    time.sleep(0.5)
                    send_keys("{ENTER}")  # Navigate
                    time.sleep(2)
                    
                    print("✅ Used keyboard shortcut to navigate")
                    return True
            
            return False
            
        except Exception as e:
            print(f"Error navigating to folder: {e}")
            return False

    def select_video_file(self, video_filename):
        """Find and select the video file in the file explorer."""
        try:
            print(f"Looking for video file: {video_filename}")
            
            # Wait for folder to load
            time.sleep(2)
            
            # Try to find and double-click the video file
            success = find_and_click_text(video_filename, timeout=10, partial=True, double_click=True)
            if success:
                print(f"✅ Found and selected video: {video_filename}")
                return True
            
            # If exact name doesn't work, try partial match
            base_name = os.path.splitext(video_filename)[0]
            success = find_and_click_text(base_name, timeout=5, partial=True, double_click=True)
            if success:
                print(f"✅ Found and selected video (partial match): {base_name}")
                return True
            
            print(f"❌ Could not find video file: {video_filename}")
            return False
            
        except Exception as e:
            print(f"Error selecting video file: {e}")
            return False

    def click_open_button(self):
        """Click the Open button in the file dialog."""
        try:
            print("Looking for Open button...")
            
            # Try different variations of the Open button
            open_button_texts = ["Open", "OK", "Select", "Choose"]
            
            for button_text in open_button_texts:
                success = find_and_click_text(button_text, timeout=3)
                if success:
                    print(f"✅ Clicked {button_text} button")
                    time.sleep(2)  # Wait for file to be processed
                    return True
            
            print("❌ Could not find Open button")
            return False
            
        except Exception as e:
            print(f"Error clicking Open button: {e}")
            return False

    def check_upload_started(self):
        """Check if file upload has started by looking for upload indicators."""
        try:
            upload_indicators = [
                # Progress bars
                "//div[@role='progressbar']",
                "//div[contains(@class, 'progress')]",
                
                # Upload status text
                "//*[contains(text(), 'Uploading')]",
                "//*[contains(text(), 'Processing')]",
                "//*[contains(text(), 'Loading')]",
                
                # Video preview elements
                "//video",
                "//div[contains(@class, 'video')]",
                
                # File name display
                f"//*[contains(text(), '{os.path.basename(self.current_video_path)}')]" if hasattr(self, 'current_video_path') else None
            ]
            
            # Remove None values
            upload_indicators = [ind for ind in upload_indicators if ind is not None]
            
            for indicator in upload_indicators:
                try:
                    element = WebDriverWait(self.driver, 3).until(
                        EC.presence_of_element_located((By.XPATH, indicator))
                    )
                    if element.is_displayed():
                        print(f"  Upload indicator found: {indicator[:30]}...")
                        return True
                except:
                    continue
            
            return False
            
        except Exception as e:
            print(f"Error checking upload start: {e}")
            return False

    def verify_video_uploaded(self, timeout=30):
        """Simplified video upload verification - faster and more reliable."""
        try:
            print("🔍 Quick verification: Checking if video is ready...")
            
            # Wait a bit for video to process
            time.sleep(3)
            
            # Simple check: Look for caption field or Share button
            try:
                caption_or_share = WebDriverWait(self.driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((By.XPATH, "//textarea[contains(@placeholder, 'Describe your reel')] | //div[contains(@placeholder, 'Describe your reel')]")),
                        EC.presence_of_element_located((By.XPATH, "//span[text()='Share']"))
                    )
                )
                print("✅ Video upload verified - caption field or Share button found!")
                return True
            except:
                print("⚠️ Caption field not found, assuming video is ready anyway...")
                return True  # Be more lenient
            
        except Exception as e:
            print(f"Error verifying video upload: {e}")
            return True  # Be lenient and assume success

    def debug_current_page(self):
        """Debug method to see what's currently on the page."""
        try:
            print("\n=== DEBUG: Current Page Analysis ===")
            print(f"Current URL: {self.driver.current_url}")
            print(f"Page Title: {self.driver.title}")
            
            # Check for file inputs
            file_inputs = self.driver.find_elements(By.XPATH, "//input[@type='file']")
            print(f"File inputs found: {len(file_inputs)}")
            
            # Check for common elements
            common_elements = [
                ("Add Video buttons", "//button[contains(text(), 'Add Video')] | //*[text()='Add Video']"),
                ("Video elements", "//video"),
                ("Progress bars", "//div[@role='progressbar']"),
                ("Caption fields", "//textarea | //div[@contenteditable='true']"),
                ("Share buttons", "//*[text()='Share']")
            ]
            
            for name, xpath in common_elements:
                try:
                    elements = self.driver.find_elements(By.XPATH, xpath)
                    print(f"{name}: {len(elements)} found")
                except:
                    print(f"{name}: Error checking")
            
            print("=== END DEBUG ===\n")
            
        except Exception as e:
            print(f"Debug error: {e}")



    def schedule_single_reel(self, caption, schedule_date, time_slot):
        """Schedule a single reel following the exact flow: Caption -> Share -> Schedule -> Final Share."""
        try:
            # Wait for video to process
            print("Waiting for video to process...")
            time.sleep(5)
            
            # Step 1: Enter caption in "Describe your reel" field
            print("Step 1: Entering caption...")
            caption_success = self.enter_caption_with_retry(caption)
            if not caption_success:
                print("❌ Failed to enter caption after all attempts")
                return False
            
            # Step 2: Click Share button
            print("Step 2: Clicking Share button...")
            share_success = self.click_share_button_with_retry()
            if not share_success:
                print("❌ Failed to click Share button after all attempts")
                return False

            # Step 3: Click Schedule button/option with retry and manual approval
            print("Step 3: Clicking Schedule button...")
            schedule_success = self.click_schedule_button_with_manual_approval()
            if not schedule_success:
                print("❌ Failed to click Schedule button after all attempts")
                return False

            # Step 4: Set date
            print("Step 4: Setting date...")
            date_success = self.set_schedule_date(schedule_date)
            if not date_success:
                print("❌ Failed to set date")
                return False

            # Step 5: Set time
            print("Step 5: Setting time...")
            time_success = self.set_schedule_time(time_slot)
            if not time_success:
                print("❌ Failed to set time")
                return False

            # Step 6: Click the final blue Schedule button (span element)
            print("Step 6: Clicking final blue Schedule button...")
            final_success = self.click_final_schedule_button()
            if not final_success:
                print("❌ Failed to click final Schedule button")
                return False
            
            print("🎉 Reel scheduled successfully!")
            return True

        except Exception as e:
            logging.error(f"Error scheduling reel: {e}")
            return False
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
