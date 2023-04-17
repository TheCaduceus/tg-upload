<div align="center">
<h1>📦tg-upload</h1>
<b>An open-source Python program to upload files/folder to Telegram effortlessly.</b>
</div>

## **📑 INDEX**

* [**⚙️ Installation**](#installation)
  * [Python & Git](#i-1)
  * [Download](#i-2)
  * [Requirements](#i-3)
* [**🚩 Options**](#options)
  * [Connectivity](#flag-1)
  * [Login](#flag-2)
  * [File](#flag-3)
  * [Behaviour](#flag-4)
  * [Misc](#flag-5)
* [**🕹️ How to use?**](#how-to-use)
  * [Get API ID & HASH](#htu-1)
  * [Authorization](#htu-2)
  * [Get Started](#htu-3)
  * [Using Proxy](#htu-4)
* [**🪧 Limits**](#limits)
  * [File Size](#l-1)
  * [Thumbnail](#l-2)
  * [Caption](#l-3)
* [**⚒️ Contribution**](#contribution)
* [**⛑️ Need help!**](#help)
* [**❤️ Credits & Thanks**](#credits)

<a name="installation"></a>

## ⚙️ Installation

<a name="i-1"></a>

**1.Install Python & Git:**

For Windows:
```
winget install python3.10
winget install Git.Git
```
For Linux:
```
sudo apt-get update && sudo apt-get install -y python3.10 git pip
```
For MacOS:
```
brew install python@3.10 git
```
For Termux:
```
pkg install python -y
pkg install git -y
```

<a name="i-2"></a>

**2.Download tg-upload:**

- For stable releases, download zip from [here](https://github.com/TheCaduceus/tg-upload/releases) and unzip. (Recommended)

- To download beta releases, use git:
```
git clone https://github.com/TheCaduceus/tg-upload.git
```
**3.Change Directory:**

```
cd tg-upload
```

<a name="i-3"></a>

**4.Install requirements:**

```
pip install -r requirements.txt
```

**5.Run the program:**

```
python tg-upload.py --help
```

<a name="options"></a>

## 🚩 Options
**tg-upload provides multiple options known as flags to control overall behaviour of the program, flags are categorized as follows:**

<a name="flag-1"></a>

**1.CONNECTIVITY FLAGS:**

Connectivity flags controls how the program should establish connection to Telegram servers, helpful for those uses proxies to bypass ban imposed on Telegram by their ISP (or for increasing transfer speed) or for those prefer IPv6 to establish connection.

Learn here, how to configure proxies?

```
--ipv6 - Connect Telegram using device's IPv6. By default IPv4.
--proxy - Proxy name (in proxy.json) to use for connecting Telegram.
```

<a name="flag-2"></a>

**2.LOGIN FLAGS:**

Login flags are responsible for controling behaviour of the program during authentication flow.

```
-p,--profile - Name of your new/existing session.
--api_id - Telegram API ID required to create new session.
--api_hash - Telegram API HASH required to create new session.
--phone - Phone number (international format) required to login as user.
--hide_pswd - Hide 2FA password using getpass.
--bot - Telegram bot token required to login as bot.
--login_string - Session string to login without auth & creating an session file.
--export_string - Generate & display session string using existing session file.
--tmp_session - Don't create session file for this login.
--login_only - Exit immediately after authorization process.
```

<a name="flag-3"></a>

**3.FILE FLAGS:**

File flags are used to provide information about file/folder.

```
-l,--path - Path to the file or folder to upload.
-n,--filename - To upload data with custom name.
-i,--thumb - Path of thumbnail image (JPEG format) to be attached with given file.
-z,--caption - Caption text to be attached with file(s), markdown & HTML formatting allowed.
```

<a name="flag-4"></a>

**4.BEHAVIOUR FLAGS:**

Behaviour flags controls the behaviour of transmission.

```
-c,--chat_id - Identity of chat to send the file to? can be username, phone number (international format) or ID number. By default to Saved Messages.
--as_photo - Send given file as picture.
--as_video - Send given file as video.
--as_audio - Send given file as audio.
--as_voice - Send given file as voice.
--as_video_note - Send given file as video note.
--disable_stream - Disable streaming for given video.
-b,--spoiler - Send media with spoiler animation.
-d,--delete_on_done - Delete the given file after task completion.
-w,--width - Set custom width for video.
-e,--height - Set custom height for video.
-a,--artist - Set artist name of given audio file.
-t,--title - Set title of given audio file
-s,--silent - Send files silently to given chat.
-r,--recursive - Upload files recursively if path is a folder.
--prefix - Add given prefix text to each filename (prefix + filename) before upload.
--no_warn - Don't show warning messages.
```

<a name="flag-5"></a>

**5.MISC FLAGS:**

Flags that does not fit in above categories are listed in this category:

```
-h, --help - To get help message as well as availabe options.
--device_model - Overwrite device model before starting client, by default 'tg-upload', can be anything like your name or 'My Device'.
--system_version - Overwrite system version before starting client, by default installed python version, can be anything like 'Windows 11'.
-v,--version - Display current tg-upload & dependencies version.
```

<a name="how-to-use"></a>

## 🕹️ How to use?

<a name="htu-1"></a>

**1.Create a Telegram app:**

Go to [My Telegram](https://my.telegram.org/apps) and create an app and get its **API_ID** & **API_HASH** and save it somewhere securely and treat them as your bank password.

<a name="htu-2"></a>

**2.Login in tg-upload:**

tg-upload supports login as user (using phone number or session string) or bot (using bot token), you must pass the value of your **API_ID** (`--api_id`) & **API_HASH** (`--api_hash`) and a unique name for your session (`--profile`), to login as user you must pass your phone number (`--phone`) or to login as bot pass bot token (`--bot`).

```
python tg-upload.py --profile VALUE --api_id VALUE --api_hash VALUE --phone VALUE --login_only
```
now from next time whenever you need to perform any task, you just need to pass the profile name (`--profile`) which you used to create your session and you will be logged in without any authentication flow (until you terminate the session from Telegram app).

<a name="htu-3"></a>

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

Check versions:

```
python tg-upload.py -v
```

<a name="htu-4"></a>

**4.Using proxy:**

Using proxy is completely optional step and can be used to bypass ban imposed by local authorities or for increasing transfer speed:

1.Rename 'proxy-sample.json' to 'proxy.json'

2.Fill the proxy details:

```json
{
  "proxyName": {
    "scheme": "proxyScheme", # like socks5
    "hostname": "proxyHostname", # like 192.168.1.1
    "port": 1234, # like 8080, should be integer.
    "username": "proxyUsername", # optional, omit or keep empty if not required.
    "password": "proxyPassword" # optional, omit or keep empty if not required.
  },

  ... more proxies
}
```

3.While running tg-upload, just mention the proxy name using `--proxy`.

<a name="limits"></a>

## 🪧 Limits

<a name="l-1"></a>

**1.File size:**

- 2GB for bots & freemium users.
- 4GB for premium users.

<a name="l-2"></a>

**2.Thumbnail:**

- Only JPEG format.
- Size should be 200 KB or below.
- Width & height should not be more than 320 pixels.

<a name="l-3"></a>

**3.Caption:**

- 1024 characters for all files & media.

<a name="contribution"></a>

## ⚒️ Contribution

Feel free to create a PR (to dev branch) if you have any valueable changes like adding new features or fixing bugs and not only including (but not limited to):

- Changing print statements' string.
- Refactoring code using AI tools.
- Typos in README.
- File rename.
- Changing default values unless it causing problems.
- Deleting existing features.

<a name="help"></a>

## ⛑️ Need help!

- Create an [issue](https://github.com/TheCaduceus/tg-upload/issues) on GitHub.
- [Subscribe](https://t.me/TheCaduceusOfficial) Telegram channel.
- Ask questions or doubts [here](https://t.me/DrDiscussion).
- Send a [personal message](https://t.me/TheCaduceusHere) to developer on Telegram.
- Tag on [Twitter](https://twitter.com/BeingDrCaduceus).

<a name="credits"></a>

## ❤️ Credits & Thanks

[**Dr.Caduceus**](https://t.me/TheCaduceusHere): Owner & current maintainer of tg-upload.
