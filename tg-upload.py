from pyrogram import Client
from pathlib import Path, PurePath
from sys import version_info as py_ver
from pkg_resources import get_distribution as get_dist
from time import time
from json import load as json_load

import argparse
import hashlib

parser = argparse.ArgumentParser(
  prog="tg-upload.py",
  usage="To perform any task listed below, you will need to create or use a new/existing session.\nEach new/existing session can be accessed by its name provided using the --profile flag.\n\nYou don't need to provide API_ID, API_HASH, phone number or bot token etc to perform any task again & again!\nOnce you successfully login & created a session then you just need to provide its name using --profile flag and you will be logged in without any authentication flow (until you terminate the session using Telegram).",
  description="An open-source Python program to upload files/folder to Telegram effortlessly.",
  epilog="An open-source program developed by Dr.Caduceus (GitHub.com/TheCaduceus)"
  )

# CONNECTIVITY FLAGS
parser.add_argument("--ipv6", action="store_true", help="Connect Telegram using device's IPv6. By default IPv4")
parser.add_argument("--proxy", help="Proxy name (in proxy.json) to use for connecting Telegram.")

# LOGIN FLAGS
parser.add_argument("-p","--profile", required=True, help="Name of your new/existing session.")
parser.add_argument("--api_id", type=int, help="Telegram API ID required to create new session.")
parser.add_argument("--api_hash", help="Telegram API HASH required to create new session.")
parser.add_argument("--phone", help="Phone number (international format) required to login as user.")
parser.add_argument("--hide_pswd", action="store_true", help="Hide 2FA password using getpass.")
parser.add_argument("--bot", help="Telegram bot token required to login as bot.")
parser.add_argument("--login_string", help="Session string to login without auth & creating a session file.")
parser.add_argument("--export_string", action="store_true", help="Generate & display session string using existing session file.")
parser.add_argument("--tmp_session", action="store_true", help="Don't create session file for this login.")
parser.add_argument("--login_only", action="store_true", help="Exit immediately after authorization process.")

# FILE FLAGS
parser.add_argument("-l","--path", help="Path to the file or folder to upload.")
parser.add_argument("-n","--filename", help="To upload data with custom name.")
parser.add_argument("-i","--thumb", help="Path of thumbnail image (JPEG format) to be attached with given file.")
parser.add_argument("-z","--caption", default="", help="Caption text to be attached with file(s), markdown & HTML formatting allowed.")
parser.add_argument("--duration", default=0, type=int, help="Duration of sent media in seconds.")
parser.add_argument("--capjson", help="Caption name (in caption.json) to attach with given file(s).")

# BEHAVIOUR FLAGS
parser.add_argument("-c","--chat_id", help="Identity of chat to send the file to? can be username, phone number (international format) or ID number. By default to Saved Messages.")
parser.add_argument("--as_photo", action="store_true", help="Send given file as picture.")
parser.add_argument("--as_video", action="store_true", help="Send given file as video.")
parser.add_argument("--as_audio", action="store_true", help="Send given file as audio.")
parser.add_argument("--as_voice", action="store_true", help="Send given file as voice.")
parser.add_argument("--as_video_note", action="store_true", help="Send given file as video note.")
parser.add_argument("--split", type=int, help="Split files in given bytes and upload.")
parser.add_argument("--replace", nargs=2, type=str, help="Replace given character or keyword in filename. Requires two arguments including 'text to replace' 'text to replace from'.")
parser.add_argument("--disable_stream", action="store_false", help="Disable streaming for given video.")
parser.add_argument("-b","--spoiler", action="store_true", help="Send media with spoiler animation.")
parser.add_argument("-d","--delete_on_done", action="store_true",help="Delete the given file after task completion.")
parser.add_argument("-w","--width", type=int, default=1280, help="Set custom width for video.")
parser.add_argument("-e","--height", type=int, default=552, help="Set custom height for video.")
parser.add_argument("-a","--artist", help="Set artist name of given audio file.")
parser.add_argument("-t","--title", help="Set title of given audio file")
parser.add_argument("-s","--silent", action="store_true", help="Send files silently to given chat.")
parser.add_argument("-r","--recursive", action="store_true", help="Upload files recursively if path is a folder.")
parser.add_argument("--prefix", help="Add given prefix text to each filename (prefix + filename) before upload.")
parser.add_argument("--no_warn", action="store_true", help="Don't show warning messages.")

# MISC FLAGS
parser.add_argument("--device_model", help="Overwrite device model before starting client, by default 'tg-upload', can be anything like your name.")
parser.add_argument("--system_version", help="Overwrite system version before starting client, by default installed python version, can be anything like 'Windows 11'.")
parser.add_argument("-v","--version", action="version", help="Display current tg-upload version.", version=f"tg-upload: 1.0.3\nPython: {py_ver[0]}.{py_ver[1]}.{py_ver[2]}\nPyrogram: {get_dist('pyrogram').version}\nTgCrypto: {get_dist('tgcrypto').version}")
args = parser.parse_args()

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

def file_hash(file_path, caption_text):
  file_size = Path(file_path).stat().st_size

  if '{file_sha256}' in caption_text and '{file_md5}' in caption_text:
    with open(file_path, "rb") as f:
      bytes_read = 0
      file_sha256 = hashlib.sha256()
      file_md5 = hashlib.md5()
      while True:
        chunk = f.read(4096)
        if not chunk:
          break
        file_sha256.update(chunk)
        file_md5.update(chunk)
        bytes_read += len(chunk)
        progress = bytes_read / file_size * 100
        print(f"\rCalculating SHA256 & MD5 - {progress:.2f}%", end="")
    file_sha256=file_sha256.hexdigest()
    file_md5 = file_md5.hexdigest()
  elif '{file_sha256}' in caption_text:
    with open(file_path, "rb") as f:
      bytes_read = 0
      file_sha256 = hashlib.sha256()
      while True:
        chunk = f.read(4096)
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
        chunk = f.read(4096)
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

  return file_size, file_sha256, file_md5

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

def upload_progress(current,total):
  elapsed_time = time() - start_time
  upload_speed = current / elapsed_time / 1024 / 1024
  print(f"\rUP: [{filename}] - {current/total*100:.2f}% | {upload_speed:.2f}MB/s", end="")

def get_chatid(raw_id):
  raw_id = raw_id.lstrip()
  if raw_id[0] == '-' and raw_id[1:].isdigit():
    return int(raw_id)
  elif raw_id.isdigit():
    return int(raw_id)
  else:
    return raw_id

if args.api_id and args.api_hash:
  if args.phone and args.bot:
    exit("Error: Both phone number and bot token cannot be passed at the same time.")
  elif not args.phone and not args.bot:
    if not Path(f"{args.profile}.session").exists():
      raise ValueError ("Given profile is not yet initialized! provide phone number or bot token to initialize.")
elif not args.api_id or not args.api_hash:
  if not Path(f'{args.profile}.session').exists() and not args.login_string:
    raise ValueError("Given profile is not yet initialized! provide API_ID and API_HASH to initialize.")

if args.phone:
  client = Client(
    args.profile,
    api_id=args.api_id,
    api_hash=args.api_hash,
    phone_number=args.phone,
    hide_password=args.hide_pswd,
    app_version="1.0.3",
    device_model=args.device_model or "tg-upload",
    system_version=args.system_version or f"{py_ver[0]}.{py_ver[1]}.{py_ver[2]}",
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
  elif not args.path:
    exit("Error: Path is not provided.")

  chat_id = get_chatid(args.chat_id) if args.chat_id else "me"

  if args.capjson:
    if not Path("caption.json").exists():
      raise FileNotFoundError("Not found: caption.json [file].")
    with open("caption.json", "r") as caption_json:
      try:
        caption = json_load(caption_json)[args.capjson]["text"]
      except KeyError:
        exit(f"Error: Not found {args.capjson} in caption.json file, please check caption.json and ensure that everything is in correct format.")
  elif args.caption:
    caption = args.caption
  else:
    caption = ""

  if args.as_photo:
    if Path(args.path).is_file():
      try:
        filename = PurePath(args.path).name
        file_size, file_sha256, file_md5 = file_hash(args.path, caption)
        start_time = time()
        client.send_photo(chat_id, args.path, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), progress=upload_progress, disable_notification=args.silent, has_spoiler=args.spoiler)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
    elif Path(args.path).is_dir():
      print("discovering paths...")
      for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
        filename = PurePath(_path).name
        if Path(_path).is_file():
          try:
            file_size, file_sha256, file_md5 = file_hash(_path, caption)
            start_time = time()
            client.send_photo(chat_id, _path, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), progress=upload_progress, disable_notification=args.silent, has_spoiler=args.spoiler)
            Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
          except Exception as error_code:
            print(f"An error occured!\n{error_code}")
        else:
          print(f"[Dir] -> {filename}")
  elif args.as_video:
    if Path(args.path).is_file():
      try:
        filename = args.filename or PurePath(args.path).name
        if args.prefix:
          filename = args.prefix + filename
        if args.replace:
          filename = filename.replace(args.replace[0], args.replace[1])
        file_size, file_sha256, file_md5 = file_hash(args.path, caption)
        start_time = time()
        client.send_video(chat_id, args.path, progress=upload_progress, duration=args.duration, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), has_spoiler=args.spoiler, width=int(args.width), height=int(args.height), thumb=args.thumb, file_name=filename, supports_streaming=args.disable_stream, disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
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
            file_size, file_sha256, file_md5 = file_hash(_path, caption)
            start_time = time()
            client.send_video(chat_id, _path, progress=upload_progress, duration=args.duration, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), has_spoiler=args.spoiler, width=int(args.width), height=int(args.height), thumb=args.thumb, file_name=filename, supports_streaming=args.disable_stream, disable_notification=args.silent)
            Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
          except Exception as error_code:
            print(f"An error occured!\n{error_code}")
        else:
          print(f"[Dir] -> {filename}")
  elif args.as_audio:
    if Path(args.path).is_file():
      try:
        filename= args.filename or PurePath(args.path).name
        if args.prefix:
          filename = args.prefix + filename
        if args.replace:
          filename = filename.replace(args.replace[0], args.replace[1])
        file_size, file_sha256, file_md5 = file_hash(args.path, caption)
        start_time = time()
        client.send_audio(chat_id, args.path, progress=upload_progress, duration=args.duration, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), performer=args.artist, title=args.title, thumb=args.thumb, file_name=filename, disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
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
            file_size, file_sha256, file_md5 = file_hash(_path, caption)
            start_time = time()
            client.send_video(chat_id, _path, progress=upload_progress, duration=args.duration, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), performer=args.artist, thumb=args.thumb, file_name=filename, disable_notification=args.silent)
            Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
          except Exception as error_code:
            print(f"An error occured!\n{error_code}")
        else:
          print(f"[Dir] -> {filename}")
  elif args.as_voice:
    if Path(args.path).is_file():
      try:
        filename = args.filename or PurePath(args.path).name
        if args.prefix:
          filename = args.prefix + filename
        if args.replace:
          filename = filename.replace(args.replace[0], args.replace[1])
        file_size, file_sha256, file_md5 = file_hash(args.path, caption)
        start_time = time()
        client.send_voice(chat_id. args.path, progress=upload_progress, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
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
            file_size, file_sha256, file_md5 = file_hash(_path, caption)
            start_time = time()
            client.send_video(chat_id, _path, progress=upload_progress, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), disable_notification=args.silent)
            Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
          except Exception as error_code:
            print(f"An error occured!\n{error_code}")
        else:
          print(f"[Dir] -> {filename}")
  elif args.as_video_note:
    if Path(args.path).is_file():
      try:
        filename = args.filename or PurePath(args.path).name
        if args.prefix:
          filename = args.prefix + filename
        if args.replace:
          filename = filename.replace(args.replace[0], args.replace[1])
        file_size, file_sha256, file_md5 = file_hash(args.path, caption)
        start_time = time()
        client.send_video_note(chat_id, args.path, progress=upload_progress, thumb=args.thumb, disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
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
            file_size, file_sha256, file_md5 = file_hash(_path, caption)
            start_time = time()
            client.send_video_note(chat_id, _path, progress=upload_progress, thumb=args.thumb, disable_notification=args.silent)
            Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
          except Exception as error_code:
            print(f"An error occured!\n{error_code}")
        else:
          print(f"[Dir] -> {filename}")
  else:
    if Path(args.path).is_file():
      try:
        filename = args.filename or PurePath(args.path).name
        if args.prefix:
          filename = args.prefix + filename
        if args.replace:
          filename = filename.replace(args.replace[0], args.replace[1])
        if args.split and Path(args.path).stat().st_size > args.split:
          for _splitted_file, filename in split_file(args.path, args.split, filename):
            file_size, file_sha256, file_md5 = file_hash(_splitted_file, caption)
            start_time = time()
            client.send_document(chat_id, _splitted_file, progress=upload_progress, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
            Path(_splitted_file).unlink(missing_ok=True) if args.delete_on_done else None
        else:
          file_size, file_sha256, file_md5 = file_hash(args.path, caption)
          start_time = time()
          client.send_document(chat_id, args.path, progress=upload_progress, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
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
            if args.split and Path(_path).stat().st_size > args.split:
              for _splitted_file, filename in split_file(_path, args.split, filename):
                file_size, file_sha256, file_md5 = file_hash(_splitted_file, caption)
                start_time = time()
                client.send_document(chat_id, _splitted_file, progress=upload_progress, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
                Path(_splitted_file).unlink(missing_ok=True) if args.delete_on_done else None
            else:
              file_size, file_sha256, file_md5 = file_hash(_path, caption)
              start_time = time()
              client.send_document(chat_id, _path, progress=upload_progress, caption=caption.format(file_name = PurePath(filename).stem, file_format = PurePath(filename).suffix, file_size_b = file_size, file_size_kb = file_size / 1024, file_size_mb = file_size / (1024 * 1024), file_size_gb = file_size / 1024 * 1024 * 1024, file_sha256 = file_sha256, file_md5 = file_md5), force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
              Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
          except Exception as error_code:
            print(f"An error occured!\n{error_code}")
        else:
          print(f"[Dir] -> {filename}")
