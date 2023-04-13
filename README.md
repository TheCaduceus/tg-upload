<div align="center">
<h1>📦tg-upload</h1>
<b>An open-source python program to upload files/folder to Telegram effortlessly.</b>
</div>

## ⚙️Installation
**1.Install Python & Git:**

For Windows:
```
winget install python3.10
winget install Git.Git
```
For Linux:
```
sudo apt-get update && sudo apt-get install -y python3.10 git
```
For MacOS:
```
brew install python@3.10 git
```
For Termux:
```
pkg install python -y
```

**2.Download Repository:**

```
git clone https://github.com/TheCaduceus/tg-upload.git
```

**3.Change Directory:**

```
cd tg-upload
```

**3.Install requirements:**

```
pip install -r requirements.txt
```

**4.Run the program:**

```
python tg-upload.py --help
```

## 🎮 Options
**tg-upload provides multiple options known as flags to control overall behaviour of the program, flags are categorized as follows:**

**1.LOGIN FLAGS:**

Login flags are responsible for controling behaviour of the program during authentication flow.

```
--profile - Name of your new/existing session.
--api_id - Telegram API ID required to create new session.
--api_hash - Telegram API HASH required to create new session.
--phone - Phone number (international format) required to login as user.
--hide_pswd - Hide 2FA password using getpass.
--bot - Telegram bot token required to login as bot.
--login_string - Session string to login without auth & creating an session file.
--export_string - Generate & display session string using existing session file.
--login_only - Exit immediately after authorization process.
```

**2.FILE FLAGS:**

File flags are used to provide information about file/folder.

```
--path - Path to the file or folder to upload.
--filename - To upload data with custom name.
--thumb - Path of thumbnail image (JPEG format) to be attached with given file.
--caption - Caption text to be attached with file(s), markdown & HTML formatting allowed.
```

**3.BEHAVIOUR FLAGS:**

Behaviour flags controls the behaviour of transmission.

```
--chat_id - Identity of chat to send the file to? can be username, phone number (international format) or ID number. By default to Saved Messages.
--as_photo - Send given file as picture.
--as_video - Send given file as video.
--as_audio - Send given file as audio.
--as_voice - Send given file as voice.
--as_video_note - Send given file as video note.
--disable_stream - Disable streaming for given video.
--spoiler - Send media with spoiler animation.
--delete_on_done - Delete the given file after task completion.
--width - Set custom width for video.
--height - Set custom height for video.
--artist - Set artist name of given audio file.
--title - Set title of given audio file
--silent - Send files silently to given chat.
--recursive - Upload files recursively if path is a folder.
--prefix - Add given prefix text to each filename (prefix + filename) before upload.
--no_warn - Don't show warning messages.
```

## 🕹️ How to use?
**1.Create a Telegram app:**

Go to [My Telegram](https://my.telegram.org/apps) and create an app and get its **API_ID** & **API_HASH** and save it somewhere securely and treat them as you bank password.

**2.Login in tg-upload:**

tg-upload supports login as user (using phone number or session string) or bot (using bot token), you must pass the value of your **API_ID** (`--api_id`) & **API_HASH** (`--api_hash`) and a unique name for your session (`--profile`), to login as user you must pass your phone number (`--phone`) or to login as bot pass bot token (`--bot`).

```
python tg-upload.py --profile VALUE --api_id VALUE --api_hash VALUE --phone VALUE --login_only
```
now from next time whenever you need to perform any task, you just need to pass the profile name (`--profile`) which you used to create your session and you will be logged in without any authentication flow (until you terminate the session from Telegram app).

**3.Get started:**

Hooray! now you are all set to use tg-upload. You can try out some sample commands that will help you to get started quickly:

Get help & options:

```
python tg-upload.py -h
```

Upload files/folder:

```
python tg-upload.py --profile VALUE --path VALUE --OTHER OPTIONAL FLAGS
```

## 🪧 Limits

**1.File size:**

- 2GB for bots & freemium users.
- 4GB for premium users.

**3.Thumbnail:**

- Only JPEG format.
- Size should be 200 KB or below.
- Width & height should not be more than 320 pixels.

**2.Caption:**

- 1024 characters for all files & media.

## ❤️ Credits & Thanks

[**Dr.Caduceus**](https://t.me/TheCaduceusHere): Owner & current maintainer of tg-upload.
