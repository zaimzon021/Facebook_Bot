# Facebook Reels Automation Bot

This bot automates the process of scheduling Facebook Reels from a local folder.

## Prerequisites

- Windows operating system
- Python 3.8 or newer
- Google Chrome browser
- Facebook account with access to Meta Business Suite

## Setup Instructions

1. **Run the setup script**:
   - Double-click on `setup.bat` to install all required dependencies
   - If you encounter any errors, make sure Python is installed and added to your PATH

2. **Configure the bot**:
   - Open `run_bot.py` in a text editor
   - Update the following variables:
     - `FACEBOOK_EMAIL`: Your Facebook login email
     - `FACEBOOK_PASSWORD`: Your Facebook login password
     - `PAGE_NAME_TO_SWITCH_TO`: The name of your Facebook page
     - `VIDEO_FOLDER_PATH`: Path to the folder containing your videos (use forward slashes)

3. **Prepare your videos**:
   - Place your video files (.mp4 or .mov) in the folder specified in `VIDEO_FOLDER_PATH`
   - The filename will be used as the caption for the reel

## Running the Bot

1. Run the bot by executing:
   ```
   python run_bot.py
   ```

2. The bot will:
   - Open Chrome and log into Facebook
   - Navigate to Meta Business Suite
   - Upload and schedule your videos as reels
   - Move processed videos to a subfolder named "uploaded"

3. **Important**: You may need to manually complete any verification steps during the first login

## Troubleshooting

- If the bot fails to find elements on the page, try increasing the timeout values
- Make sure your Facebook account has the necessary permissions to post reels
- Check that your video files meet Facebook's requirements for reels

## Notes

- The bot schedules 3 reels per day at 10:00, 16:00, and 22:00
- You may need to adjust these times in the code if needed