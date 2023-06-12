from pathlib import Path, PurePath
from sys import version_info as py_ver
from pkg_resources import get_distribution as get_dist
from time import time
from json import load as json_load
from PIL import Image
from datetime import datetime
from httpx import get as get_url
from os import environ as env
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from math import floor

import argparse
import hashlib

tg_upload = "1.1.0"
versions = f"tg-upload: {tg_upload} \
Python: {py_ver[0]}.{py_ver[1]}.{py_ver[2]} \
Pyrogram: {get_dist('pyrogram').version} \
Prettytable: {get_dist('prettytable').version} \
Pillow: {get_dist('pillow').version} \
httpx: {get_dist('httpx').version} \
TgCrypto: {get_dist('tgcrypto').version} \
moviepy {get_dist('moviepy').version} \
"
json_endpoint = "https://cdn.thecaduceus.eu.org/tg-upload/release.json"

parser = argparse.ArgumentParser(
  prog="tg-upload.py",
  usage="To perform any task listed below, you will need to create or use a new/existing session.\nEach new/existing session can be accessed by its name provided using the --profile flag.\n\nYou don't need to provide API_ID, API_HASH, phone number or bot token etc to perform any task again & again!\nOnce you successfully login & created a session then you just need to provide its name using --profile flag and you will be logged in without any authentication flow (until you terminate the session using Telegram).",
  description="An open-source Python program to upload/download files/folder to/from Telegram effortlessly.",
  epilog="An open-source program developed by Dr.Caduceus (GitHub.com/TheCaduceus)"
  )

# CONNECTIVITY FLAGS
parser.add_argument("--ipv6", default=env.get("TG_UPLOAD_IPV6", "False").lower() in {"true", "t", "1"}, action="store_true", help="Connect Telegram using device's IPv6. By default IPv4")
parser.add_argument("--proxy", metavar="TG_UPLOAD_PROXY", default=env.get("TG_UPLOAD_PROXY", None), help="Proxy name (in proxy.json) to use for connecting Telegram.")

# LOGIN FLAGS
parser.add_argument("-p","--profile", metavar="TG_UPLOAD_PROFILE", default=env.get("TG_UPLOAD_PROFILE", None), help="Name of your new/existing session.")
parser.add_argument("--info", default=env.get("TG_UPLOAD_INFO", "False").lower() in {"true", "t", "1"}, action="store_true", help="Show your Telegram account details as JSON.")
parser.add_argument("--api_id", metavar="TG_UPLOAD_API_ID", default=int(env.get("TG_UPLOAD_API_ID", 12345)), type=int, help="Telegram API ID required to create new session.")
parser.add_argument("--api_hash", metavar="TG_UPLOAD_API_HASH", default=env.get("TG_UPLOAD_API_HASH", None), help="Telegram API HASH required to create new session.")
parser.add_argument("--phone", metavar="TG_UPLOAD_PHONE", default=env.get("TG_UPLOAD_PHONE", None), help="Phone number (international format) required to login as user.")
parser.add_argument("--hide_pswd", default=env.get("TG_UPLOAD_HIDE_PSWD", "False").lower() in {"true", "t", "1"}, action="store_true", help="Hide 2FA password using getpass.")
parser.add_argument("--bot", metavar="TG_UPLOAD_BOT_TOKEN", default=env.get("TG_UPLOAD_BOT_TOKEN", None), help="Telegram bot token required to login as bot.")
parser.add_argument("--logout", default=env.get("TG_UPLOAD_LOGOUT", "False").lower() in {"true", "t", "1"}, action="store_true", help="Revoke current session and delete session file.")
parser.add_argument("--login_string", metavar="TG_UPLOAD_SESSION_STRING", default=env.get("TG_UPLOAD_SESSION_STRING", None), help="Session string to login without auth & creating a session file.")
parser.add_argument("--export_string", default=env.get("TG_UPLOAD_EXPORT_STRING", "False").lower() in {"true", "t", "1"}, action="store_true", help="Generate & display session string using existing session file.")
parser.add_argument("--tmp_session", default=env.get("TG_UPLOAD_TMP_SESSION", "False").lower() in {"true", "t", "1"}, action="store_true", help="Don't create session file for this login.")
parser.add_argument("--login_only", default=env.get("TG_UPLOAD_LOGIN_ONLY", "False").lower() in {"true", "t", "1"}, action="store_true", help="Exit immediately after authorization process.")

# FILE FLAGS
parser.add_argument("-l","--path", metavar="TG_UPLOAD_PATH", default=env.get("TG_UPLOAD_PATH", None), help="Path to the file or folder to upload.")
parser.add_argument("-n","--filename", metavar="TG_UPLOAD_FILENAME", default=env.get("TG_UPLOAD_FILENAME", None), help="To upload/download data with custom name.")
parser.add_argument("-i","--thumb", metavar="TG_UPLOAD_THUMB", default=env.get("TG_UPLOAD_THUMB", None), help="Path of thumbnail image to be attached with given file. Pass 'auto' for random frame or particular frame time (in seconds) to attach it with video as thumbnail.")
parser.add_argument("-z","--caption", metavar="TG_UPLOAD_CAPTION", default=env.get("TG_UPLOAD_CAPTION", ""), help="Caption text to be attached with file(s), markdown & HTML formatting allowed.")
parser.add_argument("--duration", metavar="TG_UPLOAD_DURATION", default=int(env.get("TG_UPLOAD_DURATION", 0)), type=int, help="Duration of audio/video in seconds. Pass '-1' for automatic detection.")
parser.add_argument("--capjson", metavar="TG_UPLOAD_CAPJSON", default=env.get("TG_UPLOAD_CAPJSON", None), help="Caption name (in caption.json) to attach with given file(s).")

# BEHAVIOUR FLAGS
parser.add_argument("-c","--chat_id", metavar="TG_UPLOAD_CHAT_ID", default=env.get("TG_UPLOAD_CHAT_ID", "me") , help="Identity of chat to send/download the file to/from? can be username, phone number (international format) or Identity number, by default to Saved Messages.")
parser.add_argument("--as_photo", default=env.get("TG_UPLOAD_AS_PHOTO", "False").lower() in {"true", "t", "1"}, action="store_true", help="Send given file as picture.")
parser.add_argument("--as_video", default=env.get("TG_UPLOAD_AS_VIDEO", "False").lower() in {"true", "t", "1"}, action="store_true", help="Send given file as video.")
parser.add_argument("--as_audio", default=env.get("TG_UPLOAD_AS_AUDIO", "False").lower() in {"true", "t", "1"}, action="store_true", help="Send given file as audio.")
parser.add_argument("--as_voice", default=env.get("TG_UPLOAD_AS_VOICE", "False").lower() in {"true", "t", "1"}, action="store_true", help="Send given file as voice.")
parser.add_argument("--as_video_note", default=env.get("TG_UPLOAD_AS_VIDEO_NOTE", "False").lower() in {"true", "t", "1"}, action="store_true", help="Send given file as video note.")
parser.add_argument("--split", metavar="TG_UPLOAD_SPLIT", type=int, default=int(env.get("TG_UPLOAD_SPLIT", 0)), help="Split files in given bytes and upload.")
parser.add_argument("--replace", metavar="TG_UPLOAD_REPLACE", type=str, default=env.get("TG_UPLOAD_REPLACE", ",").split(","), nargs=2, help="Replace given character or keyword in filename. Requires two arguments including 'text to replace' 'text to replace from'.")
parser.add_argument("--disable_stream", default=env.get("TG_UPLOAD_DISABLE_STREAM", "True").lower() in {"true", "t", "1"}, action="store_false", help="Disable streaming for given video.")
parser.add_argument("-b","--spoiler", default=env.get("TG_UPLOAD_SPOILER", "False").lower() in {"true", "t", "1"}, action="store_true", help="Send media with spoiler animation.")
parser.add_argument("--parse_mode", metavar="TG_UPLOAD_PARSE_MODE", default=env.get("TG_UPLOAD_PARSE_MODE", "DEFAULT"), help="Set custom formatting mode for caption.")
parser.add_argument("-d","--delete_on_done", default=env.get("TG_UPLOAD_DELETE_ON_DONE", "False").lower() in {"true", "t", "1"}, action="store_true", help="Delete the given file after task completion.")
parser.add_argument("-w","--width", metavar="TG_UPLOAD_WIDTH", type=int, default=int(env.get("TG_UPLOAD_WIDTH", 0)), help="Set custom width for video, by default to original video width.")
parser.add_argument("-e","--height", metavar="TG_UPLOAD_HEIGHT", type=int, default=int(env.get("TG_UPLOAD_HEIGHT", 0)), help="Set custom height for video, by default to original video height.")
parser.add_argument("-a","--artist", metavar="TG_UPLOAD_ARTIST", default=env.get("TG_UPLOAD_ARTIST", None), help="Set artist name of given audio file.")
parser.add_argument("-t","--title", metavar="TG_UPLOAD_TITLE", default=env.get("TG_UPLOAD_TITLE", None), help="Set title of given audio file.")
parser.add_argument("-s","--silent", default=env.get("TG_UPLOAD_SILENT", "False").lower() in {"true", "t", "1"}, action="store_true", help="Send files silently to given chat.")
parser.add_argument("-r","--recursive", default=env.get("TG_UPLOAD_RECURSIVE", "False").lower() in {"true", "t", "1"}, action="store_true", help="Upload files recursively if path is a folder.")
parser.add_argument("--prefix", metavar="TG_UPLOAD_PREFIX", default=env.get("TG_UPLOAD_PREFIX", None), help="Add given prefix text to each filename (prefix + filename).")
parser.add_argument("-g","--hash_memory_limit", metavar="TG_UPLOAD_HASH_MEMORY_LIMIT", type=int, default=int(env.get("TG_UPLOAD_HASH_MEMORY_LIMIT", 1000000)), help="Limit how much memory should be used to calculate hash in bytes, by default to 1 MB.")
parser.add_argument("-f","--combine_memory_limit", metavar="TG_UPLOAD_COMBINE_MEMORY_LIMIT", type=int, default=int(env.get("TG_UPLOAD_COMBINE_MEMORY_LIMIT", 1000000)), help="Limit how much memory should be used to combine files in bytes, by default to 1 MB.")
parser.add_argument("--no_warn", default=env.get("TG_UPLOAD_NO_WARN", "False").lower() in {"true", "t", "1"}, action="store_true", help="Don't show warning messages.")
parser.add_argument("--no_update", default=env.get("TG_UPLOAD_NO_UPDATE", "False").lower() in {"true", "t", "1"}, action="store_true", help="Disable checking for updates.")

# DOWNLOAD FLAGS
parser.add_argument("--dl", default=env.get("TG_UPLOAD_DL", "False").lower() in {"true", "t", "1"}, action="store_true", help="Enable download module of tg-upload.")
parser.add_argument("--links", metavar="TG_UPLOAD_LINKS", nargs="+", type=str, default=env.get("TG_UPLOAD_LINKS", "").split(","), help="Telegram file links to be downloaded (separated with space).")
parser.add_argument("--txt_file", metavar="TG_UPLOAD_TXT_FILE", default=env.get("TG_UPLOAD_TXT_FILE", None), help=".txt file path containing telegram file links to be downloaded (1 link / line).")
parser.add_argument("--range", default=env.get("TG_UPLOAD_RANGE", "False").lower() in {"true", "t", "1"}, action="store_true", help="Find and download messages in between of two given links or message ids of same chat.")
parser.add_argument("--msg_id", nargs="+", metavar="TG_UPLOAD_MSG_ID", type=int, default=env.get("TG_UPLOAD_MSG_ID", "").split(","), help="Identity number of messages to be downloaded.")
parser.add_argument("--dl_dir", metavar="TG_UPLOAD_DL_DIR", default=env.get("TG_UPLOAD_DL_DIR", None), help="Change the download directory, by default 'downloads' in current working directory.")

# UTILITY FLAGS
parser.add_argument("--env", action="store_true", help="Display environment variables, their current value and default value in tabular format.")
parser.add_argument("--file_info", help="Show basic file information.")
parser.add_argument("--hash", help="Calculate & display hash of given file.")
parser.add_argument("--split_file", type=int, help="Split file in given byte, accepts only size & requires path using path flag.")
parser.add_argument("--combine", nargs="+", type=str, help="Restore original file using part files produced by tg-upload. Accepts one or more paths.")
parser.add_argument("--frame", type=int, help="Capture a frame from a video file at given time & save as .jpg file, accepts only time (in seconds) & video file path using path flag.")
parser.add_argument("--convert", help="Convert any image into JPEG format.")

# MISC FLAGS
parser.add_argument("--device_model", metavar="TG_UPLOAD_DEVICE_MODEL", default=env.get("TG_UPLOAD_DEVICE_MODEL", "tg-upload"), help="Overwrite device model before starting client, by default 'tg-upload', can be anything like your name.")
parser.add_argument("--system_version", metavar="TG_UPLOAD_SYSTEM_VERSION", default=env.get("TG_UPLOAD_SYSTEM_VERSION", f"{py_ver[0]}.{py_ver[1]}.{py_ver[2]}"), help="Overwrite system version before starting client, by default installed python version, can be anything like 'Windows 11'.")
parser.add_argument("-v","--version", action="version", help="Display current tg-upload version.", version=versions)

args = parser.parse_args()

# Check version
if not args.no_update:
  try:
    release_json = get_url(json_endpoint).json()
    if tg_upload != release_json["latestRelease"]["version"]:
      print(f"[UPDATE] - A new release v{release_json['latestRelease']['version']} is availabe.\n")
      if release_json["latestRelease"]["showNotLatestMSG"] == "1":
        print(f"\n[NEWS] - {release_json['release']['notLatestMSG']}\n")
    elif release_json["latestRelease"]["showLatestMSG"] == "1":
      print(f"[NEWS] - {release_json['latestRelease']['latestMSG']}\n")

    if tg_upload in list(release_json["releaseSpecificNotice"].keys()):
      print(f"[NOTICE] - {release_json['releaseSpecificNotice'][tg_upload]}\n")
  except Exception:
    print("[UPDATE] - Failed to check for latest version.")

def validate_link(link):
	link_parts = link.replace(" ", "").split('/')
	if 'https:' not in link_parts and 'http:' not in link_parts:
		exit("Error: Link should contain 'https://' or 'http://'.")
	elif "t.me" not in link_parts:
		exit("Error: Link should use t.me as domain.")
	chat_id = int(f"-100{link_parts[4]}") if 'c' in link_parts else link_parts[3]
	msg_id = int(link_parts[-1])
	
	return chat_id, msg_id

def msg_info(message):
  if message.video:
    filename = message.video.file_name
    filesize = message.video.file_size
    if filename is None:
      if message.video.mime_type == 'video/x-matroska':
        filename = f"VID_{message.id}_{message.video.file_unique_id}.mkv"
      else:
        filename = f"VID_{message.id}_{message.video.file_unique_id}.{message.video.mime_type.split('/')[-1]}"
  elif message.document:
    filename = message.document.file_name
    filesize = message.document.file_size
  elif message.sticker:
    filename = message.sticker.file_name
    filesize = message.sticker.file_size
  elif message.animation:
    filename = message.animation.file_name
    filesize = message.animation.file_size
  elif message.audio:
    filename = message.audio.file_name
    filesize = message.audio.file_size
  elif message.photo:
    filename = f"IMG_{message.id}_{message.photo.file_unique_id}.jpg"
    filesize = message.photo.file_size
  else:
    filename = f"unknown_{message.id}"
    filesize = 0

  if args.filename:
    filename = args.filename
  if args.prefix:
    filename = args.prefix + filename
  if args.replace:
    filename = filename.replace(args.replace[0], args.replace[1])
  if args.dl_dir:
    dl_dir = PurePath(args.dl_dir)
    filename = f"{dl_dir}/{filename}"

  return filename, filesize / 1024 / 1024 if filesize != 0 else 0

def file_info(file_path, caption_text):
  file_size = Path(file_path).stat().st_size

  if '{file_sha256}' in caption_text and '{file_md5}' in caption_text:
    with open(file_path, "rb") as f:
      bytes_read = 0
      file_sha256 = hashlib.sha256()
      file_md5 = hashlib.md5()
      while True:
        chunk = f.read(args.hash_memory_limit)
        if not chunk:
          break
        file_sha256.update(chunk)
        file_md5.update(chunk)
        bytes_read += len(chunk)
        progress = bytes_read / file_size * 100
        print(f"\rCalculating SHA256 & MD5 - {progress:.2f}%", end="")
    file_sha256 = file_sha256.hexdigest()
    file_md5 = file_md5.hexdigest()
  elif '{file_sha256}' in caption_text:
    with open(file_path, "rb") as f:
      bytes_read = 0
      file_sha256 = hashlib.sha256()
      while True:
        chunk = f.read(args.hash_memory_limit)
        if not chunk:
          break
        file_sha256.update(chunk)
        bytes_read += len(chunk)
        progress = bytes_read / file_size * 100
        print(f"\rCalculating SHA256 - {progress:.2f}%", end="")
    file_sha256 = file_sha256.hexdigest()
    file_md5 = None
  elif '{file_md5}' in caption_text:
    with open(file_path, "rb") as f:
      bytes_read = 0
      file_md5 = hashlib.md5()
      while True:
        chunk = f.read(args.hash_memory_limit)
        if not chunk:
          break
        file_md5.update(chunk)
        bytes_read += len(chunk)
        progress = bytes_read / file_size * 100
        print(f"\rCalculating MD5 - {progress:.2f}%", end="")
    file_sha256 = None
    file_md5 = file_md5.hexdigest()
  else:
    file_sha256 = None
    file_md5 = None

  creation_time, modification_time = [], []
  ct = Path(file_path).stat().st_ctime
  mt = Path(file_path).stat().st_mtime
  ct, mt = datetime.fromtimestamp(ct), datetime.fromtimestamp(mt)
  creation_time.extend(
    (ct.year, ct.month, ct.day, ct.hour, ct.minute, ct.second))
  modification_time.extend(
    (mt.year, mt.month, mt.day, mt.hour, mt.minute, mt.second))
  return file_size, file_sha256, file_md5, creation_time, modification_time

def split_file(file_path, chunk_size, file_name):

  file_size = Path(file_path).stat().st_size
  num_chunks = file_size // chunk_size + \
    (1 if file_size % chunk_size != 0 else 0)
  Path("tmp").mkdir(exist_ok=True)
  with open(file_path, 'rb') as f:
    for i in range(num_chunks):
      chunk_file_name = f"{file_name}.part{i}"
      chunk_file_path = f"tmp/{chunk_file_name}"
      with open(chunk_file_path, 'wb') as cf:
        cf.write(f.read(chunk_size))
      progress = (i + 1) / num_chunks * 100
      print(f"\rSPLIT: [{file_name}] - {progress:.2f}%", end="")
      yield chunk_file_path, chunk_file_name

def download_progress(current,total):
	elapsed_time = time() - start_time
	dl_speed = current / elapsed_time / 1024 / 1024
	print(f"\rDL: [{filename}] - {filesize:.2f}MB | {current/total*100:.2f}% | {dl_speed:.2f}MB/s", end="")

def upload_progress(current,total):
  elapsed_time = time() - start_time
  upload_speed = current / elapsed_time / 1024 / 1024
  print(f"\rUP: [{filename}] - {current/total*100:.2f}% | {upload_speed:.2f}MB/s", end="")

def get_chatid(raw_id):
  raw_id = raw_id.replace(" ", "")
  if raw_id[0] == '-' and raw_id[1:].isdigit():
    return int(raw_id)
  elif raw_id.isdigit():
    return int(raw_id)
  else:
    return raw_id

if args.combine:
  output_file_name = args.filename or Path(args.combine[0]).stem
  with open(output_file_name, 'wb') as f:
    file_size = sum(Path(file_path).stat().st_size for file_path in args.combine)
    bytes_written = 0
    for file_path in args.combine:
      with open(file_path, 'rb') as cf:
        while True:
          chunk = cf.read(args.combine_memory_limit)
          if not chunk:
            break
          f.write(chunk)
          bytes_written += len(chunk)
          progress = (bytes_written / file_size) * 100
          print(f"\rCOMBINE: [{output_file_name}] - {progress:.2f}%", end="")
      if args.delete_on_done:
        Path(file_path).unlink() 
  exit()
elif args.hash:
  _, file_sha256, file_md5,_,_ = file_info(args.hash,"{file_sha256},{file_md5}")
  print(f"\nFile Name:\n{Path(args.hash).name}\nSHA256:\n{file_sha256}\nMD5:\n{file_md5}")
  exit()
elif args.split_file:
  if not args.path:
    raise ValueError("Path not defined, use --path to define.")
  elif Path(args.path).stat().st_size < args.split_file:
    raise ValueError("Split size is larger than file size.")
  filename = args.filename or Path(args.path).name
  for _ in split_file(args.path, args.split_file, filename):
    pass
  exit()
elif args.convert:
  filename = args.filename or PurePath(args.convert).stem
  jpg_path = f"{filename}.jpg"
  print(f"CONVERT: {PurePath(args.convert).name} -> {jpg_path}")
  Image.open(args.convert).convert('RGB').save(jpg_path)
  exit()
elif args.file_info:
  file_size,_,_, creation_time, modification_time = file_info(args.file_info, "")
  print(f"File Name:\n{PurePath(args.file_info).name}\n\nSize(s):\n{file_size / (1024 * 1024 * 1024):.2f}GB\n{file_size / (1024 * 1024):.2f}MB\n{file_size / 1024 :.2f}KB\n{file_size}B\n\nCreation Date (Time):\n{creation_time[2]}.{creation_time[1]}.{creation_time[0]} ({creation_time[3]}:{creation_time[4]}:{creation_time[5]})\n\nModification Date (Time):\n{modification_time[2]}.{modification_time[1]}.{modification_time[0]} ({modification_time[3]}:{modification_time[4]}:{modification_time[5]})")
  exit()
elif args.env:
  from prettytable import PrettyTable
  table = PrettyTable(["ENV VARIABLE", "FLAG","CURRENT VALUE", "DEFAULT VALUE"])
  table.add_row(["TG_UPLOAD_IPV6", "--ipv6", env.get("TG_UPLOAD_IPV6"), False])
  table.add_row(["TG_UPLOAD_PROXY", "--proxy", env.get("TG_UPLOAD_PROXY"), None])
  table.add_row(["TG_UPLOAD_PROFILE", "--profile", env.get("TG_UPLOAD_PROFILE"), None])
  table.add_row(["TG_UPLOAD_INFO", "--info", env.get("TG_UPLOAD_INFO"), False])
  table.add_row(["TG_UPLOAD_API_ID", "--api_id", env.get("TG_UPLOAD_API_ID"), None])
  table.add_row(["TG_UPLOAD_API_HASH", "--api_hash", env.get("TG_UPLOAD_API_HASH"), None])
  table.add_row(["TG_UPLOAD_PHONE", "--phone", env.get("TG_UPLOAD_PHONE"), None])
  table.add_row(["TG_UPLOAD_HIDE_PSWD", "--hide_pswd", env.get("TG_UPLOAD_HIDE_PSWD"), False])
  table.add_row(["TG_UPLOAD_BOT_TOKEN", "--bot", env.get("TG_UPLOAD_BOT_TOKEN"), None])
  table.add_row(["TG_UPLOAD_LOGOUT", "--logout", env.get("TG_UPLOAD_LOGOUT"), False])
  table.add_row(["TG_UPLOAD_SESSION_STRING", "--login_string", env.get("TG_UPLOAD_SESSION_STRING"), None])
  table.add_row(["TG_UPLOAD_EXPORT_STRING", "--export_string", env.get("TG_UPLOAD_EXPORT_STRING"), False])
  table.add_row(["TG_UPLOAD_TMP_SESSION", "--tmp_session", env.get("TG_UPLOAD_TMP_SESSION"), False])
  table.add_row(["TG_UPLOAD_LOGIN_ONLY", "--login_only", env.get("TG_UPLOAD_LOGIN_ONLY"), False])
  table.add_row(["TG_UPLOAD_PATH", "--path", env.get("TG_UPLOAD_PATH"), None])
  table.add_row(["TG_UPLOAD_FILENAME", "--filename", env.get("TG_UPLOAD_FILENAME"), None])
  table.add_row(["TG_UPLOAD_THUMB", "--thumb", env.get("TG_UPLOAD_THUMB"), None])
  table.add_row(["TG_UPLOAD_CAPTION", "--caption", env.get("TG_UPLOAD_CAPTION"), None])
  table.add_row(["TG_UPLOAD_DURATION", "--duration", env.get("TG_UPLOAD_DURATION"), 0])
  table.add_row(["TG_UPLOAD_CAPJSON", "--capjson", env.get("TG_UPLOAD_CAPJSON"), None])
  table.add_row(["TG_UPLOAD_CHAT_ID", "--chat_id", env.get("TG_UPLOAD_CHAT_ID"), "me"])
  table.add_row(["TG_UPLOAD_AS_PHOTO", "--as_photo", env.get("TG_UPLOAD_AS_PHOTO"), False])
  table.add_row(["TG_UPLOAD_AS_VIDEO", "--as_video", env.get("TG_UPLOAD_AS_VIDEO"), False])
  table.add_row(["TG_UPLOAD_AS_AUDIO", "--as_audio", env.get("TG_UPLOAD_AS_AUDIO"), False])
  table.add_row(["TG_UPLOAD_AS_VOICE", "--as_voice", env.get("TG_UPLOAD_AS_VOICE"), False])
  table.add_row(["TG_UPLOAD_AS_VIDEO_NOTE", "--as_video_note", env.get("TG_UPLOAD_AS_VIDEO_NOTE"), False])
  table.add_row(["TG_UPLOAD_SPLIT", "--split", env.get("TG_UPLOAD_SPLIT"), 0])
  table.add_row(["TG_UPLOAD_REPLACE", "--replace", env.get("TG_UPLOAD_REPLACE"), None])
  table.add_row(["TG_UPLOAD_DISABLE_STREAM", "--disable_stream", env.get("TG_UPLOAD_DISABLE_STREAM"), False])
  table.add_row(["TG_UPLOAD_SPOILER", "--spoiler", env.get("TG_UPLOAD_SPOILER"), False])
  table.add_row(["TG_UPLOAD_PARSE_MODE", "--parse_mode", env.get("TG_UPLOAD_PARSE_MODE"), "DEFAULT"])
  table.add_row(["TG_UPLOAD_DELETE_ON_DONE", "--delete_on_done", env.get("TG_UPLOAD_DELETE_ON_DONE"), False])
  table.add_row(["TG_UPLOAD_WIDTH", "--width", env.get("TG_UPLOAD_WIDTH"), 0])
  table.add_row(["TG_UPLOAD_HEIGHT", "--height", env.get("TG_UPLOAD_HEIGHT"), 0])
  table.add_row(["TG_UPLOAD_ARTIST", "--artist", env.get("TG_UPLOAD_ARTIST"), None])
  table.add_row(["TG_UPLOAD_TITLE", "--title", env.get("TG_UPLOAD_TITLE"), None])
  table.add_row(["TG_UPLOAD_SILENT", "--silent", env.get("TG_UPLOAD_SILENT"), False])
  table.add_row(["TG_UPLOAD_RECURSIVE", "--recursive", env.get("TG_UPLOAD_RECURSIVE"), False])
  table.add_row(["TG_UPLOAD_PREFIX", "--prefix", env.get("TG_UPLOAD_PREFIX"), None])
  table.add_row(["TG_UPLOAD_HASH_MEMORY_LIMIT", "--hash_memory_limit", env.get("TG_UPLOAD_HASH_MEMORY_LIMIT"), 1000000])
  table.add_row(["TG_UPLOAD_COMBINE_MEMORY_LIMIT", "--combine_memory_limit", env.get("TG_UPLOAD_COMBINE_MEMORY_LIMIT"), 1000000])
  table.add_row(["TG_UPLOAD_NO_WARN", "--no_warn", env.get("TG_UPLOAD_NO_WARN"), False])
  table.add_row(["TG_UPLOAD_NO_UPDATE", "--no_update", env.get("TG_UPLOAD_NO_UPDATE"), False])
  table.add_row(["TG_UPLOAD_DL", "--dl", env.get("TG_UPLOAD_DL"), False])
  table.add_row(["TG_UPLOAD_LINKS", "--links", env.get("TG_UPLOAD_LINKS"), None])
  table.add_row(["TG_UPLOAD_TXT_FILE", "--txt_file", env.get("TG_UPLOAD_TXT_FILE"), None])
  table.add_row(["TG_UPLOAD_RANGE", "--range", env.get("TG_UPLOAD_RANGE", False)])
  table.add_row(["TG_UPLOAD_MSG_ID", "--msg_id", env.get("TG_UPLOAD_MSG_ID"), None])
  table.add_row(["TG_UPLOAD_DL_DIR", "--dl_dir", env.get("TG_UPLOAD_DL_DIR"), None])
  table.add_row(["TG_UPLOAD_DEVICE_MODEL", "--device_model", env.get("TG_UPLOAD_DEVICE_MODEL"), "tg-upload"])
  table.add_row(["TG_UPLOAD_SYSTEM_VERSION", "--system_version", env.get("TG_UPLOAD_SYSTEM_VERSION"), f"{py_ver[0]}.{py_ver[1]}.{py_ver[2]}"])
  exit(table)
elif args.frame:
  if not args.path:
    exit("Error: Video file path is not provided.")
  print("Capturing frame...")
  with VideoFileClip(args.path) as video:
    Path("thumb").mkdir(exist_ok=True)
    thumb = f"thumb/THUMB_{PurePath(args.path).stem}.jpg"
    video.save_frame(thumb, t=args.frame)
  exit(f"Saved at {thumb}")

elif not args.profile:
  exit("Error: No session name (--profile) passed to start client with.")

if args.proxy:
  if not Path("proxy.json").exists():
    raise FileNotFoundError("Not found: proxy.json [file].")
  with open("proxy.json", "r") as proxy:
    try:
      proxy_json = json_load(proxy)[args.proxy]
      print(f"Connecting to {args.proxy}...")
    except KeyError:
      exit(f"Error: Unable to load {args.proxy}, please check proxy.json and ensure that everything is in correct format.")
else:
  proxy_json = None

if args.api_id and args.api_hash:
  if args.phone and args.bot:
    exit("Error: Both phone number and bot token cannot be passed at the same time.")
  elif not args.phone and not args.bot:
    if not Path(f"{args.profile}.session").exists():
      raise ValueError ("Given profile is not yet initialized! provide phone number or bot token to initialize.")
elif not args.api_id or not args.api_hash:
  if not Path(f'{args.profile}.session').exists() and not args.login_string:
    raise ValueError("Given profile is not yet initialized! provide API_ID and API_HASH to initialize.")

from pyrogram import Client, enums, errors

if args.phone:
  client = Client(
    args.profile,
    api_id=args.api_id,
    api_hash=args.api_hash,
    phone_number=args.phone,
    hide_password=args.hide_pswd,
    app_version=tg_upload,
    device_model=args.device_model,
    system_version=args.system_version,
    ipv6=args.ipv6,
    in_memory=args.tmp_session,
    proxy=proxy_json
  )
elif args.bot:
  client = Client(
    args.profile,
    api_id=args.api_id,
    api_hash=args.api_hash,
    bot_token=args.bot,
    ipv6=args.ipv6,
    in_memory=args.tmp_session,
    proxy=proxy_json
  )
elif args.login_string:
  client = Client(
    args.profile,
    session_string=args.login_string,
    ipv6=args.ipv6,
    proxy=proxy_json
  )
else:
  client = Client(
    args.profile,
    ipv6=args.ipv6,
    proxy=proxy_json
  )

with client:
  if args.login_only:
    exit("Authorization completed!")
  elif args.export_string:
    exit(f"Your session string:\n{client.export_session_string()}")
  elif args.logout:
    client.log_out()
    exit(f"Terminated [{args.profile}]")
  elif args.info:
    try:
      print(client.get_me())
    except Exception as error_code:
      print(f"\nAn error occured!\n{error_code}")
  elif args.dl:
    if args.txt_file:
      if not Path(args.txt_file).exists() or not Path(args.txt_file).is_file():
        exit("Error: Given txt file path is invalid.")
      with open(args.txt_file, 'r') as txt_file:
        args.links = txt_file.readlines()

    if len(args.links) != 0 and args.links[0]:
      if args.range:
        if not len(args.links) >= 2:
          exit("Error: Using --range flag requires two different links of same chat.")
        
        _chat_id , _message_id = validate_link(args.links[0])
        __chat_id, __message_id = validate_link(args.links[1])

        if _chat_id != __chat_id:
          exit("Error: Chat ID of both the links should be same.")
        elif _message_id == __message_id:
          exit("Error: Message ID of both links should be different.")
        message_ids = range(_message_id,__message_id+1) if _message_id < __message_id else range(__message_id,_message_id+1)

        for message_id in message_ids:
          try:
            message = client.get_messages(_chat_id, message_id)
          except ValueError: # Chat ID or Message ID is not valid
            print(f"\nMessage ID not found: {message_id}")
            continue

          filename, filesize = msg_info(message)
          start_time = time()

          try:
            client.download_media(message, progress=download_progress, file_name=filename)
          except ValueError: # No downloadable file in message
            print(f"\nNo Media: MSG_{message_id}")
          except Exception as error_code:
            print(f"\n{error_code}")
      else:
        for link in args.links:
          chat_id, message_id = validate_link(link)
          try:
            message = client.get_messages(chat_id, message_id)
          except errors.exceptions.bad_request_400.ChannelInvalid:
            print(f"Error: No access to {link}")
            continue
          except ValueError as error_code:
            print(f"\n{error_code} - {link}")
            continue

          filename, filesize = msg_info(message)
          start_time = time()
      
          try:
            client.download_media(message, progress=download_progress, file_name=filename)
          except ValueError as error_code:
            print(f"\n{error_code}  - {link}")
    elif args.chat_id and len(args.msg_id) != 0 and args.msg_id[0]:
      args.chat_id = get_chatid(args.chat_id)

      if args.range:
        if not len(args.msg_id) >= 2:
          exit("Error: Using --range requires two different MSG IDs of same chat.")
        elif args.msg_id[0] == args.msg_id[1]:
          exit("Error: MSG_IDs should be different.")

        message_ids = range(args.msg_id[0], args.msg_id[1]+1) if args.msg_id[0] < args.msg_id[1] else range(args.msg__id[1], args.msg_id[0]+1)

        for message_id in message_ids:
          try:
            message = client.get_messages(args.chat_id, message_id)
          except ValueError:
            print(f"\nMessage ID not found: {message_id}")
            continue

          filename, filesize = msg_info(message)
          start_time = time()
          
          try:
            client.download_media(message, progress=download_progress, file_name=filename)
          except ValueError:
            print(f"\nNo Media: MSG_{message_id}")
          except Exception as error_code:
            print(f"\n{error_code}")
            
      else:
        for msg_id in args.msg_id:
          try:
            message = client.get_messages(args.chat_id, args.msg_id)
          except errors.exceptions.bad_request_400.ChannelInvalid:
            exit(f"Error: No access to {args.chat_id}.")
          except ValueError as error_code:
            exit(f"\n{error_code} - {args.chat_id}")
          
          filename, filesize = msg_info(message)
          start_time = time()

          try:
            client.download_media(message, progress=download_progress, file_name=filename)
          except ValueError:
            exit(f"\nError: No downloadable media found - {msg_id}")
    else:
      exit("Error: No link or message id provided to download.")
  else:
    if not args.path:
      exit("Error: Path is not provided.")

    chat_id = get_chatid(args.chat_id)

    if not args.as_video and args.thumb == 'auto':
      args.thumb = None
    elif args.thumb and PurePath(args.thumb).suffix not in ['.jpg','jpeg'] and args.thumb != 'auto':
      thumbname = PurePath(args.thumb).stem
      jpg_path = f"{thumbname}.jpg"
      print(f"CONVERT: {PurePath(args.thumb).name} -> {jpg_path}")
      Image.open(args.thumb).convert('RGB').save(jpg_path)
      args.thumb = jpg_path

    parse_mode = enums.ParseMode.DEFAULT

    if args.capjson:
      if not Path("caption.json").exists():
        raise FileNotFoundError("Not found: caption.json [file].")
      with open("caption.json", "r") as caption_json:
        try:
          _caption = json_load(caption_json)[args.capjson]
        except KeyError:
          exit(f"Error: Not found {args.capjson} in caption.json file, please check caption.json and ensure that everything is in correct format.")

      try:
        caption = _caption["text"]
        parse_mode = _caption["mode"]
      except KeyError as error_code:
        exit(f"Error: An error occured while reading json.\n{error_code}")
      
      if parse_mode.lower() == "html":
        parse_mode = enums.ParseMode.HTML
      elif parse_mode.lower() == "markdown":
        parse_mode = enums.ParseMode.MARKDOWN
      elif parse_mode.lower() == "disabled":
        parse_mode = enums.ParseMode.DISABLED
    elif args.caption:
      caption = args.caption
      if args.parse_mode:
        if args.parse_mode.lower() == "html":
          parse_mode = enums.ParseMode.HTML
        elif args.parse_mode.lower() == "markdown":
          parse_mode = enums.ParseMode.MARKDOWN
        elif args.parse_mode.lower() == "disabled":
          parse_mode = enums.ParseMode.DISABLED
    else:
      caption = ""

    if args.as_photo:
      if Path(args.path).is_file():
        try:
          filename = PurePath(args.path).name
          file_size, file_sha256, file_md5, creation_time, modification_time = file_info(args.path, caption)
          start_time = time()
          client.send_photo(chat_id, args.path, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, path = PurePath(args.path)), progress=upload_progress, disable_notification=args.silent, has_spoiler=args.spoiler)
          Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
        except Exception as error_code:
          print(f"\nAn error occured!\n{error_code}")
      elif Path(args.path).is_dir():
        print("discovering paths...")
        for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
          filename = PurePath(_path).name
          if Path(_path).is_file():
            try:
              file_size, file_sha256, file_md5, creation_time, modification_time = file_info(_path, caption)
              start_time = time()
              client.send_photo(chat_id, _path, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, path = PurePath(_path)), progress=upload_progress, disable_notification=args.silent, has_spoiler=args.spoiler)
              Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
            except Exception as error_code:
              print(f"\nAn error occured!\n{error_code}")
          else:
            print(f"[Dir] -> {PurePath(_path).name}")
      else:
        print("Error: Given path is invalid.")
    elif args.as_video:
      if Path(args.path).is_file():
        try:
          filename = args.filename or PurePath(args.path).name
          if args.prefix:
            filename = args.prefix + filename
          if args.replace:
            filename = filename.replace(args.replace[0], args.replace[1])
          file_size, file_sha256, file_md5, creation_time, modification_time = file_info(args.path, caption)
          with VideoFileClip(args.path) as video:
            Path("thumb").mkdir(exist_ok=True)
            if args.thumb == 'auto':
              args.thumb = f"thumb/THUMB_{PurePath(args.path).stem}.jpg"
              video.save_frame(args.thumb, t=floor(video.duration / 2))
            elif args.thumb != None and args.thumb.isdigit():
              video.save_frame(f"thumb/THUMB_{PurePath(args.path).stem}.jpg", t=int(args.thumb))
              args.thumb = f"thumb/THUMB_{PurePath(args.path).stem}.jpg"
            if not args.height:
              args.height = video.h
            if not args.width:
              args.width = video.w
            if args.duration == -1:
              args.duration = floor(video.duration)
          start_time = time()
          client.send_video(chat_id, args.path, progress=upload_progress, duration=args.duration, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, width=args.width, height=args.height, duration=args.duration, path = PurePath(args.path)), has_spoiler=args.spoiler, width=args.width, height=args.height, thumb=args.thumb, file_name=filename, supports_streaming=args.disable_stream, disable_notification=args.silent)
          Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
        except Exception as error_code:
          print(f"\nAn error occured!\n{error_code}")
      elif Path(args.path).is_dir():
        print("discovering paths...")
        for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
          if Path(_path).is_file():
            try:
              filename = PurePath(_path).name
              if args.prefix:
                filename = args.prefix + filename
              if args.replace:
                filename = filename.replace(args.replace[0], args.replace[1])
              file_size, file_sha256, file_md5, creation_time, modification_time = file_info(_path, caption)
              with VideoFileClip(_path) as video:
                Path("thumb").mkdir(exist_ok=True)
                if args.thumb == 'auto':
                  args.thumb = f"thumb/THUMB_{PurePath(_path).stem}.jpg"
                  video.save_frame(args.thumb, t=floor(video.duration / 2))
                elif args.thumb != None and args.thumb.isdigit():
                  video.save_frame(f"thumb/THUMB_{PurePath(_path).stem}.jpg", t=int(args.thumb))
                  args.thumb = f"thumb/THUMB_{PurePath(_path).stem}.jpg"
                if not args.height:
                  args.height = video.h
                if not args.width:
                  args.width = video.w
                if args.duration == -1:
                  args.duration = floor(video.duration)
              start_time = time()
              client.send_video(chat_id, _path, progress=upload_progress, duration=args.duration, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, width=args.width, height=args.height, duration=args.duration, path = PurePath(_path)), has_spoiler=args.spoiler, width=int(args.width), height=int(args.height), thumb=args.thumb, file_name=filename, supports_streaming=args.disable_stream, disable_notification=args.silent)
              Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
            except Exception as error_code:
              print(f"\nAn error occured!\n{error_code}")
          else:
            print(f"[Dir] -> {PurePath(_path).name}")
      else:
        print("Error: Given path is invalid.")

    elif args.as_audio:
      if Path(args.path).is_file():
        try:
          filename= args.filename or PurePath(args.path).name
          if args.prefix:
            filename = args.prefix + filename
          if args.replace:
            filename = filename.replace(args.replace[0], args.replace[1])
          if args.duration == -1:
            with AudioFileClip(args.path) as audio:
              args.duration = floor(audio.duration)
          file_size, file_sha256, file_md5, creation_time, modification_time = file_info(args.path, caption)
          start_time = time()
          client.send_audio(chat_id, args.path, progress=upload_progress, duration=args.duration, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, duration=args.duration, path = PurePath(args.path)), performer=args.artist, title=args.title, thumb=args.thumb, file_name=filename, disable_notification=args.silent)
          Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
        except Exception as error_code:
          print(f"\nAn error occured!\n{error_code}")
      elif Path(args.path).is_dir():
        print("discovering paths...")
        for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
          if Path(_path).is_file():
            try:
              filename = PurePath(_path).name
              if args.prefix:
                filename = args.prefix + filename
              if args.replace:
                filename = filename.replace(args.replace[0], args.replace[1])
              if args.duration == -1:
                with AudioFileClip(_path) as audio:
                  args.duration = floor(audio.duration)
              file_size, file_sha256, file_md5, creation_time, modification_time = file_info(_path, caption)
              start_time = time()
              client.send_video(chat_id, _path, progress=upload_progress, duration=args.duration, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, duration=args.duration, path = PurePath(_path)), performer=args.artist, thumb=args.thumb, file_name=filename, disable_notification=args.silent)
              Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
            except Exception as error_code:
              print(f"\nAn error occured!\n{error_code}")
          else:
            print(f"[Dir] -> {PurePath(_path).name}")
      else:
        print("Error: Given path is invalid.")

    elif args.as_voice:
      if Path(args.path).is_file():
        try:
          filename = args.filename or PurePath(args.path).name
          if args.prefix:
            filename = args.prefix + filename
          if args.replace:
            filename = filename.replace(args.replace[0], args.replace[1])
          if args.duration == -1:
            with AudioFileClip(args.path) as audio:
              args.duration = floor(audio.duration)
          file_size, file_sha256, file_md5, creation_time, modification_time = file_info(args.path, caption)
          start_time = time()
          client.send_voice(chat_id. args.path, progress=upload_progress, duration=args.duration, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, duration=args.duration, path = PurePath(args.path)), disable_notification=args.silent)
          Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
        except Exception as error_code:
          print(f"\nAn error occured!\n{error_code}")
      elif Path(args.path).is_dir():
        print("discovering paths...")
        for _path in Path(args.path).glob('**/*') if args.recursive else Path(args.path).glob("*"):
          if Path(_path).is_file():
            try:
              filename = PurePath(_path).name
              if args.prefix:
                filename = args.prefix + filename
              if args.replace:
                filename = filename.replace(args.replace[0], args.replace[1])
              if args.duration == -1:
                with AudioFileClip(_path) as audio:
                  args.duration = floor(audio.duration)
              file_size, file_sha256, file_md5, creation_time, modification_time = file_info(_path, caption)
              start_time = time()
              client.send_video(chat_id, _path, progress=upload_progress, duration=args.duration, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, duration=args.duration, path = PurePath(_path)), disable_notification=args.silent)
              Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
            except Exception as error_code:
              print(f"\nAn error occured!\n{error_code}")
          else:
            print(f"[Dir] -> {PurePath(_path).name}")
      else:
        print("Error: Given path is invalid.")

    elif args.as_video_note:
      if Path(args.path).is_file():
        try:
          filename = args.filename or PurePath(args.path).name
          if args.prefix:
            filename = args.prefix + filename
          if args.replace:
            filename = filename.replace(args.replace[0], args.replace[1])
          with VideoFileClip(args.path) as video:
            Path("thumb").mkdir(exist_ok=True)
            if args.thumb == 'auto':
              args.thumb = f"thumb/THUMB_{PurePath(args.path).stem}.jpg"
              video.save_frame(args.thumb, t=floor(video.duration / 2))
            elif args.thumb != None and args.thumb.isdigit():
              video.save_frame(f"thumb/THUMB_{PurePath(args.path).stem}.jpg", t=int(args.thumb))
              args.thumb = f"thumb/THUMB_{PurePath(args.path).stem}.jpg"
            if not args.height:
              args.height = video.h
            if not args.width:
              args.width = video.w
            if args.duration == -1:
              args.duration = floor(video.duration)
          start_time = time()
          client.send_video_note(chat_id, args.path, progress=upload_progress, duration=args.duration, thumb=args.thumb, disable_notification=args.silent)
          Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
        except Exception as error_code:
          print(f"\nAn error occured!\n{error_code}")
      elif Path(args.path).is_dir():
        print("discovering paths...")
        for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
          if Path(_path).is_file():
            try:
              filename = PurePath(_path).name
              if args.prefix:
                filename = args.prefix + filename
              if args.replace:
                filename = filename.replace(args.replace[0], args.replace[1])
              with VideoFileClip(_path) as video:
                Path("thumb").mkdir(exist_ok=True)
                if args.thumb == 'auto':
                  args.thumb = f"thumb/THUMB_{PurePath(_path).stem}.jpg"
                  video.save_frame(args.thumb, t=floor(video.duration / 2))
                elif args.thumb != None and args.thumb.isdigit():
                  video.save_frame(f"thumb/THUMB_{PurePath(_path).stem}.jpg", t=int(args.thumb))
                  args.thumb = f"thumb/THUMB_{PurePath(_path).stem}.jpg"
                if not args.height:
                  args.height = video.h
                if not args.width:
                  args.width = video.w
                if args.duration == -1:
                  args.duration = floor(video.duration)
              start_time = time()
              client.send_video_note(chat_id, _path, progress=upload_progress, thumb=args.thumb, disable_notification=args.silent)
              Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
            except Exception as error_code:
              print(f"\nAn error occured!\n{error_code}")
          else:
            print(f"[Dir] -> {PurePath(_path).name}")
      else:
        print("Error: Given path is invalid.")

    else:
      if Path(args.path).is_file():
        try:
          filename = args.filename or PurePath(args.path).name
          if args.prefix:
            filename = args.prefix + filename
          if args.replace:
            filename = filename.replace(args.replace[0], args.replace[1])
          if args.split and Path(args.path).stat().st_size > args.split and args.split != 0:
            for _splitted_file, filename in split_file(args.path, args.split, filename):
              file_size, file_sha256, file_md5, creation_time, modification_time = file_info(_splitted_file, caption)
              start_time = time()
              client.send_document(chat_id, _splitted_file, progress=upload_progress, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, path = PurePath(_splitted_file)), force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
              Path(_splitted_file).unlink(missing_ok=True) if args.delete_on_done else None
          else:
            file_size, file_sha256, file_md5, creation_time, modification_time = file_info(args.path, caption)
            start_time = time()
            client.send_document(chat_id, args.path, progress=upload_progress, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, path = PurePath(args.path)), force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
          Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
        except Exception as error_code:
          print(f"\nAn error occured!\n{error_code}")
      elif Path(args.path).is_dir():
        print("discovering paths...")
        for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
          if Path(_path).is_file():
            try:
              filename = PurePath(_path).name
              if args.prefix:
                filename = args.prefix + filename
              if args.replace:
                filename = filename.replace(args.replace[0], args.replace[1])
              if args.split and Path(_path).stat().st_size > args.split and args.split != 0:
                for _splitted_file, filename in split_file(_path, args.split, filename):
                  file_size, file_sha256, file_md5, creation_time, modification_time = file_info(_splitted_file, caption)
                  start_time = time()
                  client.send_document(chat_id, _splitted_file, progress=upload_progress, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, path = PurePath(_splitted_file)), force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
                  Path(_splitted_file).unlink(missing_ok=True) if args.delete_on_done else None
              else:
                file_size, file_sha256, file_md5, creation_time, modification_time = file_info(_path, caption)
                start_time = time()
                client.send_document(chat_id, _path, progress=upload_progress, parse_mode=parse_mode, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / (1024 * 1024 * 1024), file_sha256 = file_sha256, file_md5 = file_md5, creation_time = creation_time, modification_time = modification_time, path = PurePath(_path)), force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
                Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
            except Exception as error_code:
              print(f"\nAn error occured!\n{error_code}")
          else:
            print(f"[Dir] -> {PurePath(_path).name}")
      else:
        print("Error: Given path is invalid.")
