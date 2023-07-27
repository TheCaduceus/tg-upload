<div align="center">
<h1>📦tg-upload</h1>
<b>An open-source Python program or a CLI Tool to upload/download files/folders to/from Telegram effortlessly.</b>
</div><br>

<div align="center">
<i>Transform your Telegram account into personal cloud storage with tg-upload.</i>
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
  * [Download](#flag-5)
  * [Utility](#flag-6)
  * [Misc](#flag-7)
* [**📝 ENV Variables**](#env)
* [**🕹️ How to use?**](#how-to-use)
  * [Get API ID & HASH](#htu-1)
  * [Authorization](#htu-2)
  * [Get Started](#htu-3)
  * [Caption](#htu-4)
    * [Dynamic Caption](#htu4.1)
      * [Variables](#htu4.1.1)
      * [Path Methods](#htu4.1.2)
      * [Time Index](#htu4.1.3)
      * [Decimal Places](#htu4.1.4)
    * [Formatting Modes](#htu-4.2)
    * [Caption Templates](#htu-4.3)
  * [Using Proxy](#htu-5)
* [**🪧 Limits**](#limits)
  * [File Size](#l-1)
  * [Thumbnail](#l-2)
  * [Caption](#l-3)
* [**❓ FAQ**](#faq)
* [**⚒️ Contribution**](#contribution)
* [**⛑️ Need help!**](#help)
* [**❤️ Credits & Thanks**](#credits)

<a name="installation"></a>

## ⚙️ Installation
Git installation is optional if you prefer downloading tg-upload as zip file using the [releases](https://github.com/TheCaduceus/tg-upload/releases) section.
<a name="i-1"></a>

**1.Install Python & Git:**

For Windows:
```
winget install Python.Python.3.11
winget install Git.Git
```
For Linux:
```
sudo apt-get update && sudo apt-get install -y python3.11 git pip
```
For macOS:
```
brew install python@3.11 git
```
For Termux:
```
pkg install python -y
pkg install git -y
```

<a name="i-2"></a>

**2.Download tg-upload:**

- Download as zip from [here](https://github.com/TheCaduceus/tg-upload/releases).

- Use Git:
```
git clone https://github.com/TheCaduceus/tg-upload.git
```

> Starting from release [v1.0.1](https://github.com/TheCaduceus/tg-upload/releases/tag/v1.0.1), tg-upload no longer supports Termux due to the absence of some required dependencies. You may try an older [release](https://github.com/TheCaduceus/tg-upload/releases/tag/v1.0.0) to enjoy the basic functionalities offered by tg-upload. Hence, any issue related to Termux will be rejected without any further investigation.

**3.Change Directory:**

```
cd tg-upload
```

<a name="i-3"></a>

**4.Install requirements:**

If your device already has the required dependencies installed, verify if their version matches the version mentioned in 'requirements.txt'. Otherwise, upgrade them. You can see their version by using the tg-upload's `-v` flag.

```
pip install -r requirements.txt
```

**5.Run the program:**

```
python tg-upload.py -h
```

<a name="options"></a>

## 🚩 Options
**tg-upload provides multiple options known as flags to control the overall behaviour of the program. These flags are categorized as follows:**

<a name="flag-1"></a>

**1.CONNECTIVITY FLAGS:**

Connectivity flags control how the program should establish a connection to Telegram servers, thus allowing users to use proxies and IPV6.

How to configure proxies? [[Learn here](#htu-5)]

```
--ipv6 - Connect to Telegram using your device’s IPv6, by default IPv4.
--proxy - The name of the proxy (in proxy.json) to use for connecting to Telegram.
```

<a name="flag-2"></a>

**2.LOGIN FLAGS:**

Login flags are responsible for controlling the behaviour of the program during the authentication flow.

```
-p,--profile - The name of your new or existing session.
--info - Show your Telegram account details as JSON.
--api_id - Telegram API ID, required to create new session.
--api_hash - Telegram API HASH, required to create new session.
--phone - Phone number (in international format), required to login as user.
--hide_pswd - Hide 2FA password using getpass.
--bot - Telegram bot token, required to login as bot.
--logout - Revoke current session and delete session file.
--login_string - Session string to login without auth & creating session file.
--export_string - Generate & display session string using existing session file.
--tmp_session - Don't create session file for this login.
--login_only - Exit immediately after authorization process.
```

<a name="flag-3"></a>

**3.FILE FLAGS:**

File flags are used to provide information about files/folders.

```
-l,--path - Path to the file or folder to upload.
-n,--filename - To upload data with custom name.
-i,--thumb - Path of thumbnail image to be attached with given file. Pass "auto" for random frame or particular frame time (in seconds) to attach it with video as thumbnail.
-z,--caption - Caption text to be attached with file, markdown & HTML formatting allowed.
--duration - Duration of audio/video in seconds. Pass "-1" for automatic detection.
--capjson - Caption name (in caption.json) to attach with given file.
```

<a name="flag-4"></a>

**4.BEHAVIOUR FLAGS:**

Behaviour flags control the transmission’s behaviour.

```
-c,--chat_id - The identity of the chat to upload the file to can be the username, phone number (in international format), or ID number. By default, Saved Messages.
--as_photo - Send given file as picture.
--as_video - Send given file as video.
--as_audio - Send given file as audio.
--as_voice - Send given file as voice.
--as_video_note - Send given file as video note.
--split - Split file in given bytes and upload.
--replace - Replace given character or keyword in filename. Requires two arguments including "text to replace" "text to replace from".
--reply_to - Send file as reply to given message id.
--disable_stream - Disable streaming for given video.
-b,--spoiler - Send media with spoiler animation.
-y,--self_destruct - Number of seconds (60 or below) after which photo/video will self destruct once seen by receiver.
--protect - Protect uploaded file from getting forwarded & saved.
--parse_mode - Set custom formatting mode for caption.
-d,--delete_on_done - Delete the given file after task completion.
-w,--width - Set custom width for video, by default to original video width.
-e,--height - Set custom height for video, by default to original video height.
-a,--artist - Set artist name of given audio file.
-t,--title - Set title of given audio file.
-s,--silent - Send files silently to given chat.
-r,--recursive - Upload files recursively if path is a folder.
--prefix - Add given prefix text to filename (prefix + filename).
--hash_memory_limit - Limit how much memory should be used to calculate hash in bytes, by default to 1 MB.
--combine_memory_limit - Limit how much memory should be used to combine files in bytes, by default to 1 MB.
--split_dir - Set custom directory for saving splitted files.
--combine_dir - Set custom directory for saving combined files.
--thumb_dir - Set custom directory for saving thumbnails.
--no_warn - Don't show warning messages. (DEPRECATED)
--no_update - Disable checking for updates.
```
<a name="flag-5"></a>

**5.DOWNLOAD FLAGS:**

List of flags that are usable with tg-upload's download module, while flags with "(common)" tag are usable with both upload & download task.

```
--dl - Enable download module of tg-upload.
--links - Telegram file links to be downloaded (separated with space).
--txt_file - .txt file path containing Telegram file links to be downloaded (1 link / line).
-j,--auto_combine - Automatically start combining part files after download.
--range - Find and download messages in between of two given links or message IDs of same chat.
--chat_id (common) - The identity of the chat to download the file from can be the username, phone number (in international format), or ID number. By default, Saved Messages.
--msg_id - Identity number of messages to be downloaded (separated with space).
--filename (common) - To download data with custom name.
--replace (common) - Replace given character or keyword in filename. Requires two arguments including "text to replace" "text to replace from".
--prefix (common) - Add given prefix text to filename (prefix + filename).
--dl_dir - Change the download directory, by default "downloads" in current working directory.
```

<a name="flag-6"></a>

**6.UTILITY FLAGS:**

Utility flags provide an easy way to directly use internal functions used by tg-upload without starting the main client. Therefore, there is no need to create or use an existing session (`--profile`) to use these flags.

```
--env - Display environment variables, their current value and default value in tabular format.
--file_info - Show basic file information.
--hash - Calculate & display hash of given file.
--split_file - Split file in given bytes, accepts only size & requires path using path flag.
--combine - Restore original file using part files produced by tg-upload. Accepts one or more paths.
--convert - Convert any image into JPEG format.
--frame - Capture a frame from a video file at given time & save as .jpg file, accepts only time (in seconds) & video file path using path flag.
```

<a name="flag-7"></a>

**7.MISC FLAGS:**

Flags that do not fit in the above categories are listed in this category:

```
-h, --help - To get help message as well as availabe options.
--device_model - Overwrite device model before starting client, by default "tg-upload".
--system_version - Overwrite system version before starting client, by default installed python version.
-v,--version - Display current tg-upload & dependencies version.
```

<a name="how-to-use"></a>

<a name="env"></a>

## 📝 ENV Variables

**Tired of passing values each time using flags? Set flag values in system environment, each flag has its own unique system variable name from which it retrieves the value once detected. The table below shows the variable name, flag it is associated with, and the value it expects.**

|Variable                        |Flag                    |Value           |
|:------------------------------:|:----------------------:|:--------------:|
|`TG_UPLOAD_IPV6`                |`--ipv6`                |True or False   |
|`TG_UPLOAD_PROXY`               |`--proxy`               |Same as flag    |
|`TG_UPLOAD_PROFILE`             |`--profile`             |Same as flag    |
|`TG_UPLOAD_INFO`                |`--info`                |True or False   |
|`TG_UPLOAD_API_ID`              |`--api_id`              |Same as flag    |
|`TG_UPLOAD_API_HASH`            |`--api_hash`            |Same as flag    |
|`TG_UPLOAD_PHONE`               |`--phone`               |Same as flag    |
|`TG_UPLOAD_HIDE_PSWD`           |`--hide_pswd`           |True or False   |
|`TG_UPLOAD_BOT_TOKEN`           |`--bot`                 |Same as flag    |
|`TG_UPLOAD_LOGOUT`              |`--logout`              |True or False   |
|`TG_UPLOAD_SESSION_STRING`      |`--login_string`        |Same as flag    |
|`TG_UPLOAD_EXPORT_STRING`       |`--export_string`       |True or False   |
|`TG_UPLOAD_TMP_SESSION`         |`--tmp_session`         |True or False   |
|`TG_UPLOAD_LOGIN_ONLY`          |`--login_only`          |True or False   |
|`TG_UPLOAD_PATH`                |`--path`                |Same as flag    |
|`TG_UPLOAD_FILENAME`            |`--filename`            |Same as flag    |
|`TG_UPLOAD_THUMB`               |`--thumb`               |Same as flag    |
|`TG_UPLOAD_CAPTION`             |`--caption`             |Same as flag    |
|`TG_UPLOAD_DURATION`            |`--duration`            |Same as flag    |
|`TG_UPLOAD_CAPJSON`             |`--capjson`             |Same as flag    |
|`TG_UPLOAD_CHAT_ID`             |`--chat_id`             |Same as flag    |
|`TG_UPLOAD_AS_PHOTO`            |`--as_photo`            |True or False   |
|`TG_UPLOAD_AS_VIDEO`            |`--as_video`            |True or False   |
|`TG_UPLOAD_AS_AUDIO`            |`--as_audio`            |True or False   |
|`TG_UPLOAD_AS_VOICE`            |`--as_voice`            |True or False   |
|`TG_UPLOAD_AS_VIDEO_NOTE`       |`--as_video_note`       |True or False   |
|`TG_UPLOAD_SPLIT`               |`--split`               |Same as flag    |
|`TG_UPLOAD_REPLACE`             |`--replace`             |Separate both values using "," (comma).|
|`TG_UPLOAD_REPLY_TO`            |`--reply_to`            |Same as flag    |
|`TG_UPLOAD_DISABLE_STREAM`      |`--disable_stream`      |True or False   |
|`TG_UPLOAD_SPOILER`             |`--spoiler`             |True or False   |
|`TG_UPLOAD_SELF_DESTRUCT`       |`--self_destruct`       |Same as flag    |
|`TG_UPLOAD_PROTECT`             |`--protect`             |True or False   |
|`TG_UPLOAD_PARSE_MODE`          |`--parse_mode`          |Same as flag    |
|`TG_UPLOAD_DELETE_ON_DONE`      |`--delete_on_done`      |True or False   |
|`TG_UPLOAD_WIDTH`               |`--width`               |Same as flag    |
|`TG_UPLOAD_HEIGHT`              |`--height`              |Same as flag    |
|`TG_UPLOAD_ARTIST`              |`--artist`              |Same as flag    |
|`TG_UPLOAD_TITLE`               |`--title`               |Same as flag    |
|`TG_UPLOAD_SILENT`              |`--silent`              |True or False   |
|`TG_UPLOAD_RECURSIVE`           |`--recursive`           |True or False   |
|`TG_UPLOAD_PREFIX`              |`--prefix`              |Same as flag    |
|`TG_UPLOAD_HASH_MEMORY_LIMIT`   |`--hash_memory_limit`   |Same as flag    |
|`TG_UPLOAD_COMBINE_MEMORY_LIMIT`|`--combine_memory_limit`|Same as flag    |
|`TG_UPLOAD_SPLIT_DIR`           |`--split_dir`           |Same as flag    |
|`TG_UPLOAD_COMBINE_DIR`         |`--combine_dir`         |Same as flag    |
|`TG_UPLOAD_THUMB_DIR`           |`--thumb_dir`           |Same as flag    |
|`TG_UPLOAD_NO_WARN`             |`--no_warn`             |True or False   |
|`TG_UPLOAD_NO_UPDATE`           |`--no_update`           |True or False   |
|`TG_UPLOAD_DL`                  |`--dl`                  |True or False   |
|`TG_UPLOAD_LINKS`               |`--links`               |Separate both values using "," (comma).|
|`TG_UPLOAD_TXT_FILE`            |`--txt_file`            |Same as flag    |
|`TG_UPLOAD_AUTO_COMBINE`        |`--auto_combine`        |True or False   |
|`TG_UPLOAD_RANGE`               |`--range`               |True or False   |
|`TG_UPLOAD_MSG_ID`              |`--msg_id`              |Separate both values using "," (comma).|
|`TG_UPLOAD_DL_DIR`              |`--dl_dir`              |Same as flag    |
|`TG_UPLOAD_DEVICE_MODEL`        |`--device_model`        |Same as flag    |
|`TG_UPLOAD_SYSTEM_VERSION`      |`--system_version`      |Same as flag    |

Users can set as many variables as they want in any order and can temporarily overwrite a variable’s value by passing the new value using its associated flag.

## 🕹️ How to use?
For running python commands we can either use 'python' or 'py', in below examples we will use 'py'.

<a name="htu-1"></a>

**1.Create a Telegram app:**

Go to [My Telegram](https://my.telegram.org/apps), create an app, and get its **API_ID** & **API_HASH**. Save them somewhere secure and treat them as you would your bank password.

<a name="htu-2"></a>

**2.Login in tg-upload:**

tg-upload supports logging in as a user (using a phone number or session string) or bot (using a bot token or session string). You must pass the value of your **API_ID** (`--api_id`) & **API_HASH** (`--api_hash`) and a unique name for your session (`--profile`). To log in as a user, you must pass your phone number (--phone), or to log in as a bot, pass the bot token (--bot).

```
py tg-upload.py --profile VALUE --api_id VALUE --api_hash VALUE --phone VALUE --login_only
```
From now on, whenever you need to perform any task, you just need to pass the profile name (--profile) that you used to create your session. You will be logged in without any authentication flow until you terminate the session from the Telegram app.

<a name="htu-3"></a>

**3.Get Started:**

Hooray! Now you’re all set to use tg-upload. You can try out some sample commands that will help you get started quickly:

Get help & options:

```
py tg-upload.py -h
```

Upload files/folders:

```
py tg-upload.py --profile VALUE --path VALUE --OTHER OPTIONAL FLAGS
```

Download files:

*1.From private/public chats:*

```
py tg-upload.py --profile VALUE --dl --links LINK...  --OTHER OPTIONAL FLAGS
```

*2.From Saved Messages:*

```
py tg-upload.py --profile VALUE --dl --msg_id VALUE --OTHER OPTIONAL FLAGS
```

*3.From personal chats or by manually providing `chat_id` & `msg_id`:*

```
py tg-upload.py --profile VALUE --dl --chat_id phone/username/id --msg_id VALUE --OTHER OPTIONAL FLAGS
```
How to get `chat_id` and `msg_id`? [[Learn here](#faq-8)]

Check versions:

```
py tg-upload.py -v
```

<a name="htu-4"></a>

<a name="htu4.1"></a>

**4.Dynamic Caption:**

tg-upload provides variables that users can place in a file’s caption to make it dynamic. These variables are automatically replaced with their expected values. Users must place the variable name between {} to define it as a variable in the string. Here is the list of variables that tg-upload offers:

<a name="htu4.1.1"></a>

* `{file_name}` - Name of file without its format.
* `{file_format}` - Format of given file including '.'.
* `{height}` - Height of video file. *(--as_video only)*
* `{width}` - Width of video file. *(--as_video only)*
* `{duration}` - Duration of video or audio file in seconds. *(--as_audio & --as_video only)*
* `{path}` - Retrive particular value from path or exact path. *(for advanced users)*
* `{creation_time[indice]}` - File's creation time.
* `{modification_time[indice]}` - File's last modification time.
* `{file_sha256}` - Given file's SHA256.
* `{file_md5}` - Given file's MD5.
* `{file_size_b}` - Size of file in bytes.
* `{file_size_kb}` - Size of file in KB.
* `{file_size_mb}` - Size of file in MB.
* `{file_size_gb}` - Size of file in GB.

<a name="htu4.1.2"></a>

File's source variable `{path}` is both a variable and a function. Calling it directly will simply return the full path of the file, while calling it with a given method will return the value associated with that method. Below are the methods that you can call with path:
* `{path}` - Return exact path of file.
* `{path.parts}` - A tuple giving access to the path’s various components. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parts)]
* `{path.drive}` - A string representing the drive letter or name, if any. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.drive)]
* `{path.root}` - A string representing the (local or global) root, if any. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.root)]
* `{path.anchor}` - The concatenation of the drive and root. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.anchor)]
* `{path.parents}` - An immutable sequence providing access to the logical ancestors of the path. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parents)]
* `{path.parent}` - The logical parent of the path. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.parent)]
* `{path.name}` - A string representing the final path component, excluding the drive and root, if any. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.name)]
* `{path.suffix}` - The file extension of the final component, if any. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.suffix)]
* `{path.suffixes}` - A list of the path’s file extensions. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.suffixes)]
* `{path.stem}` - The final path component, without its suffix. [[example](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.stem)]

For more detailed methods, click [here](https://docs.python.org/3/library/pathlib.html#pathlib.PurePath.as_posix). Some methods requires newer Python version.

<a name="htu4.1.3"></a>

The file’s creation/modification time variables `{creation_time}` and `{modification_time}` store multiple values like year, month, day, hour, minute, and second of creation/modification. They all have their own index value inside the variable and should be passed with the variable to get a specific value. If the creation time is unknown, then the last modification time will be passed or vice versa. It also depends on your operating system:
* `0` - Year of creation/modification.
* `1` - Month of creation/modification.
* `2` - Day of creation/modification.
* `3` - Hour of creation/modification.
* `4` - Minute of creation/modification.
* `5` - Second of creation/modification.

<a name="htu4.1.4"></a>

Additionally, we can also limit the number of decimal places to be shown in the file size. For example, to limit the number of decimal places to 2, we need to pass `:.2f` with a variable like `{file_size_mb:.2f}`.
<div align="center">

<img src="https://user-images.githubusercontent.com/87380104/233824278-eed11926-1748-4455-8cb0-cb2cf1ebcdbd.png">

</div>
Just like plain text, you can also apply the same formatting on variables. Make sure you put all formatting tags outside of {} brackets to prevent any error.

One variable can be called multiple times in the same caption, and users must prevent writing any other keyword between {} brackets; otherwise, tg-upload will raise a KeyError indicating that the given variable is not yet defined.

<a name="htu-4.2"></a>

**5.Formatting Modes:**

Formatting and making captions attractive is cool! But sometimes the filename or output of any variable can mess up our caption by injecting the same tags that are used to format our plain text. To tackle this error, tg-upload provides an option to switch between different formatting modes to prevent the misinterpretation of some tags in our caption.

* `DEFAULT` - Interpret both markdown & HTML tags in caption.
* `MARKDOWN` - Interpret only markdown tags and ignore HTML tags in caption.
* `HTML` - Interpret only HTML tags and ignore markdown tags in caption.
* `DISABLED` - Interpret nothing, keep caption as it is.

If you are using the `--caption` flag, then you can switch modes using the `--parse_mode` flag. Otherwise, just change the ‘mode’ key value in ‘caption.json’ in case of `--capjson`.

<a name="htu-4.3"></a>

**6.Caption Templates:**

We can make and save our static and dynamic caption format in ‘caption.json’ with a name (required) and description (optional) so we don’t have to write it again.

1.Open 'caption.json' file and edit it as following:

```json
{
  "captionTemplateName": {
    "text" : "main caption text",
    "mode" : "DEFAULT",
    "description" : "An optional description to make recall easy."
  },
  ...more caption templates 
}
```

2.When needed, just mention the caption template name using `--capjson` flag.

Just like the `--caption` flag, the caption template also supports formatting using HTML or markdown. I have already provided some general caption templates to make your work easy! :)

<a name="htu-5"></a>

**7.Using Proxy**

Using a proxy is a completely optional step and can be used to bypass bans imposed by local authorities or for increasing transfer speed.

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
  ...more proxies
}
```

3.While running tg-upload, just mention the proxy name using `--proxy`.

<a name="limits"></a>

## 🪧 Limits

<a name="l-1"></a>

**1.File size:**

*Upload Limit:*

- 2GB for bots & freemium users.
- 4GB for premium users.

*Download Limit:*

- 4GB for all users & bots.

To upload larger files, use the `--split` flag and tg-upload will automatically split all files into the given size. To restore the original file out of part files, simply use the `--combine` flag and tg-upload will restore the original file for you (remember to provide part file paths in ordered form 0,1,2,3…).

<a name="l-2"></a>

**2.Thumbnail:**

- ~~Only JPEG format.~~
- Size should be 200 KB or below.
- Width & height should not be more than 320 pixels.

Starting from v1.0.5, tg-upload will automatically convert any other image format into JPEG format. You can also use the `--convert` flag to do it manually and without starting the main client.

<a name="l-3"></a>

**3.Caption:**

- 1024 characters for all files & media.

<a name="faq"></a>

## ❓FAQ

**1.Getting `socket.send()`, `OSError()`, `TimeoutError()`, Connection lost/reset…?**

Such network related issues are most likely a result of a temporarily slow or inconsistent network connection and will eventually disappear automatically.

**2.Can split or combine flags cause file corruption?**

No, the split and combine flags NEVER cause file corruption unless it’s a user-side mistake like not providing .part file paths in the correct format (0,1,2,3…). tg-upload follows commonly used and trusted techniques to split or combine data.

**3.Files are still usable/accessible in their splitted form?**

Yes, some file extensions like .txt, .csv, .json etc. are still usable in their split forms while some file extensions like .mkv, .exe, .mp3 etc. are NOT usable until we combine them back.

**4.For me upload/download speed is slow?**

In many cases, users expect speed in Mbps while tg-upload shows upload/download speed in MB/s where MB/s > Mbps and this is where users get confused.

In fact, tg-upload has nothing to do with upload/download speed and it totally depends upon Telegram servers (generally 5-7 MB/s) and your internet connection including proxy. Check the code to understand it in a better way.

To increase download speed, you must subscribe to Telegram premium to remove the speed limit imposed by Telegram for freemium users.

**5.How tg-upload able to upload/download larger files (upto 2GB & 4GB) using bot profiles while Bot API limit it to just 50MB & 20MB?**

It’s simple! tg-upload never makes use of the Bot API server which works as an intermediate server to communicate with Telegram’s MTProto. Instead, tg-upload directly uses the MTProto API, making it even faster.

**i.Generally:🐢**

You (JSON/HTTP) -> Bot API (MTProto) -> Telegram = Smaller & slower data transfer.

**ii.tg-upload:⚡**

You (MTProto) -> Telegram = Larger & direct data transfer.

**6.I don't want to login again and again in different devices! is there any way to use existing session in different devices?**

Yes, there are mainly two ways to do the same:

**i.Generate & use session string:**

tg-upload supports the generation of a session string and login through it. To generate a session string, you can use the `--export_string` flag with the `--profile` flag to mention the profile for which the session string should be generated. Also, upon using a session string, tg-upload never creates a new .session file.

**ii.Carry .session files:**

For every profile, tg-upload generates a .session file which is the main file that helps you log in to your Telegram account without following the auth flow. Place the .session file in tg-upload’s working directory.

**7.Feels like my .session file or session string is leaked! how I can revoke it to prevent unauthorized usage?**

Use the `--logout` flag of tg-upload to revoke the specified session and omit it from your Telegram Account’s active sessions list. Simply mention the session name using the `--profile` flag and pass the `--logout` flag.

```
py tg-upload.py --profile xyz --logout
```

<a name="faq-8"></a>

**8.How to get `chat_id` & `msg_id` to use with tg-upload?**

You can use third-party Telegram clients that let users to see more details (<a href="https://github.com/TheCaduceus/tg-upload/assets/87380104/6aa76de6-14ec-4a5f-b889-186aeb2e175b">see image</a>) of a given message like [OctoGram](https://github.com/OctoGramApp/OctoGram).

**9.Can I send files to a particular topic inside a Telegram community?**

To do this, you just need to pass the topic identity or identity of any message inside of that topic with the `--reply_to` flag.

**Getting topic identity:**

Copy link of any message inside the topic you want identity of and the link will be in this format `https://t.me/username/topic_id/msg_id` or in case of private chats link will be in this format `https://t.me/c/chat_id/topic_id/msg_id`.

**10.Is `--replace` flag case-sensitive? can it also manipulate file format?**

Be aware that the replace flag is case-sensitive and has full access to the filename, including its format. This means that it can manipulate the file format and even your filename prefix. During download, you should use replace more carefully because if the file is a part file containing `.partX` (an extension allotted by tg-upload) where `X` is any number starting from 0, then replace can even manipulate it.

However, it is not going to damage your file content. If you have replaced some unexpected words, you can always rename your file.

<a name="contribution"></a>

## ⚒️ Contribution

Feel free to create a PR (to dev branch) if you have any valuable changes like adding new features or fixing bugs and not only limited to:

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

[**Dr.Caduceus**](https://github.com/TheCaduceus): Owner & developer of tg-upload.<br>
[**Bing AI**](https://bing.com/chat): For ~~documentaion~~ documentation improvements.
