# Facebook Reels Automation Bot

This bot automates the process of scheduling Facebook Reels from multiple folders across different Facebook pages with advanced bot detection avoidance.

## 🚀 Features

- **Multi-Page Support**: Process multiple Facebook pages automatically
- **Multi-Folder Processing**: Handle different video folders for different pages
- **Undetected Chrome**: Uses undetected-chromedriver to avoid bot detection
- **Smart Page Switching**: Automatically switches between Facebook pages
- **Robust Element Detection**: Multiple methods to find and click elements
- **Chrome Focus Protection**: Prevents accidental clicks on other applications
- **Automatic Fallback**: Falls back to regular Chrome if undetected version fails

## Prerequisites

- Windows operating system
- Python 3.8 or newer
- Google Chrome browser
- Facebook account with access to Meta Business Suite

## Setup Instructions

1. **Install Dependencies**:
   ```bash
   pip install selenium webdriver-manager pywinauto pyautogui pyperclip undetected-chromedriver
   ```

2. **Configure the bot**:
   - Open `run_bot.py` in a text editor
   - Update your Facebook credentials:
     ```python
     FACEBOOK_EMAIL = "your_email@gmail.com"
     FACEBOOK_PASSWORD = "your_password"
     ```
   
   - Configure multiple pages and folders in `FOLDER_PAGE_CONFIGS`:
     ```python
     FOLDER_PAGE_CONFIGS = [
         {
             "video_folder_path": "C:/Users/YourName/Videos/Gaming",
             "page_name": "Gaming Channel"
         },
         {
             "video_folder_path": "C:/Users/YourName/Videos/Cooking", 
             "page_name": "Food Recipes"
         },
         {
             "video_folder_path": "C:/Users/YourName/Videos/Travel",
             "page_name": "Travel Adventures"
         }
     ]
     ```

3. **Prepare your videos**:
   - Place your video files (.mp4 or .mov) in the respective folders
   - The filename will be used as the caption for the reel
   - Videos will be moved to a "processed" subfolder after scheduling

## Running the Bot

1. **Execute the bot**:
   ```bash
   python run_bot.py
   ```

2. **Choose execution mode**:
   - **Option 1**: Multi-Page Mode (processes all configured pages automatically)
   - **Option 2**: Single Page Mode (processes one page only - legacy mode)

3. **The bot will**:
   - Initialize undetected Chrome browser
   - Log into Facebook (manual verification may be required)
   - For each page configuration:
     - Navigate to Meta Business Suite home page
     - Switch to the specified Facebook page
     - Upload and schedule videos from the corresponding folder
     - Move processed videos to "processed" subfolder
   - Close browser when all pages are completed

## 🔧 Advanced Features

### **Undetected Chrome**
- Automatically uses undetected-chromedriver to avoid bot detection
- Falls back to regular Chrome if undetected version fails
- Removes automation indicators and webdriver properties

### **Smart Page Switching**
- Uses 10+ different methods to find and click page selector elements
- Handles dynamic Facebook UI changes
- Robust search and selection of target pages

### **Chrome Focus Protection**
- Prevents accidental clicks on other desktop applications
- Allows necessary file explorer interactions for video uploads
- Maintains focus on Chrome browser throughout the process

### **Multi-Method Element Detection**
- Each critical element uses 5-10 different detection methods
- Handles Facebook's frequently changing class names and selectors
- Automatic retry mechanisms with different approaches

## 📁 Folder Structure After Processing

```
Your Video Folder/
├── processed/
│   ├── video1.mp4 (moved after successful scheduling)
│   ├── video2.mp4
│   └── ...
└── (new videos to be processed)
```

## ⚙️ Configuration Options

### **Scheduling Settings**
- **Videos per day**: 3 reels
- **Time slots**: 9:00 AM, 3:00 PM, 9:00 PM
- **Start date**: Next day (tomorrow)

### **Video Requirements**
- **Formats**: .mp4, .mov
- **Caption**: Automatically generated from filename
- **Processing**: Videos moved to "processed" folder after scheduling

## 🛠️ Troubleshooting

### **Common Issues**
- **Bot detection**: The undetected Chrome should handle most detection
- **Element not found**: The bot uses multiple detection methods with automatic fallbacks
- **Page switching fails**: Ensure page names match exactly as they appear in Meta Business Suite
- **Chrome focus issues**: The bot automatically manages Chrome focus

### **Error Handling**
- **Undetected Chrome fails**: Automatically falls back to regular Chrome
- **Page switching fails**: Skips to next page configuration
- **Video upload fails**: Continues with next video
- **Network issues**: Built-in retry mechanisms

### **Debug Features**
- **Screenshots**: Automatically saves debug screenshots
- **Detailed logging**: Comprehensive console output for troubleshooting
- **Error tracebacks**: Full error details for debugging

## 📝 Notes

- **Manual verification**: You may need to complete Facebook login verification steps
- **Page permissions**: Ensure your Facebook account has posting permissions for all configured pages
- **Video compliance**: Videos must meet Facebook's reel requirements
- **Rate limiting**: The bot respects Facebook's rate limits with built-in delays
- **Chrome version**: Undetected Chrome automatically handles version compatibility

## 🔒 Security Features

- **Undetected browsing**: Uses undetected-chromedriver to avoid detection
- **Stealth mode**: Removes automation indicators
- **Human-like behavior**: Includes realistic delays and interactions
- **Focus management**: Prevents suspicious multi-application interactions