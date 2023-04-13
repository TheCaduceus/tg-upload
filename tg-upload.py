from pyrogram import Client
from pathlib import Path, PurePath
from sys import version_info as py_ver
from pkg_resources import get_distribution as get_dist
from time import time
import argparse

parser = argparse.ArgumentParser(
  prog="tg-upload.py",
  usage="To perform any task listed below, you will need to create or use a new/existing session.\nEach new/existing session can be accessed by its name provided using the --profile flag.\n\nYou don't need to provide API_ID, API_HASH, phone number or bot token etc to perform any task again & again!\nOnce you successfully login & created a session then you just need to provide its name using --profile flag and you will be logged in without any authentication flow (until you terminate the session using Telegram).",
  description="A program to upload files/folder to Telegram.",
  epilog="An open-source program developed by Dr.Caduceus (GitHub.com/TheCaduceus)"
  )

# LOGIN FLAGS
parser.add_argument("--profile", required=True, help="Name of your new/existing session.")
parser.add_argument("--api_id", type=int, help="Telegram API ID required to create new session.")
parser.add_argument("--api_hash", help="Telegram API HASH required to create new session.")
parser.add_argument("--phone", help="Phone number (international format) required to login as user.")
parser.add_argument("--hide_pswd", action="store_true", help="Hide 2FA password using getpass.")
parser.add_argument("--bot", help="Telegram bot token required to login as bot.")
parser.add_argument("--login_string", help="Session string to login without auth & creating a session file.")
parser.add_argument("--export_string", action="store_true", help="Generate & display session string using existing session file.")
parser.add_argument("--login_only", action="store_true", help="Exit immediately after authorization process.")

# FILE FLAGS
parser.add_argument("--path", help="Path to the file or folder to upload.")
parser.add_argument("--filename", help="To upload data with custom name.")
parser.add_argument("--thumb", help="Path of thumbnail image (JPEG format) to be attached with given file.")
parser.add_argument("--caption", help="Caption text to be attached with file(s), markdown & HTML formatting allowed.")

# BEHAVIOUR FLAGS
parser.add_argument("--chat_id", help="Identity of chat to send the file to? can be username, phone number (international format) or ID number. By default to Saved Messages.")
parser.add_argument("--as_photo", action="store_true", help="Send given file as picture.")
parser.add_argument("--as_video", action="store_true", help="Send given file as video.")
parser.add_argument("--as_audio", action="store_true", help="Send given file as audio.")
parser.add_argument("--as_voice", action="store_true", help="Send given file as voice.")
parser.add_argument("--as_video_note", action="store_true", help="Send given file as video note.")
parser.add_argument("--disable_stream", action="store_false", help="Disable streaming for given video.")
parser.add_argument("--spoiler", action="store_true", help="Send media with spoiler animation.")
parser.add_argument("--delete_on_done", action="store_true",help="Delete the given file after task completion.")
parser.add_argument("--width", help="Set custom width for video.")
parser.add_argument("--height", help="Set custom height for video.")
parser.add_argument("--artist", help="Set artist name of given audio file.")
parser.add_argument("--title", help="Set title of given audio file")
parser.add_argument("--silent", action="store_true", help="Send files silently to given chat.")
parser.add_argument("--recursive", action="store_true", help="Upload files recursively if path is a folder.")
parser.add_argument("--prefix", help="Add given prefix text to each filename (prefix + filename) before upload.")
parser.add_argument("--no_warn", action="store_true", help="Don't show warning messages.")

# MISC FLAGS
parser.add_argument("--device_model", help="Overwrite device model before starting client, by default 'tg-upload', can be anything like your name.")
parser.add_argument("--system_version", help="Overwrite system version before starting client, by default installed python version, can be anything like 'Windows 11'.")
parser.add_argument("--version", action="version", help="Display current tg-upload version.", version=f"tg-upload: 1.0.1\nPython: {py_ver[0]}.{py_ver[1]}.{py_ver[2]}\nPyrogram: {get_dist('pyrogram').version}\nTgCrypto: {get_dist('tgcrypto').version}")
args = parser.parse_args()


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
elif not Path(f'{args.profile}.session').exists() and not args.login_string:
  raise ValueError("Given profile is not yet initialized! provide API_ID and API_HASH to initialize.")

if args.phone:
  client = Client(
    args.profile,
    api_id=args.api_id,
    api_hash=args.api_hash,
    phone_number=args.phone,
    hide_password=args.hide_pswd,
    app_version="1.0.1",
    device_model=args.device_model or "tg-upload",
    system_version=args.system_version or f"{py_ver[0]}.{py_ver[1]}.{py_ver[2]}"
  )
elif args.bot:
  client = Client(
    args.profile,
    api_id=args.api_id,
    api_hash=args.api_hash,
    bot_token=args.bot
  )
elif args.login_string:
  client = Client(
    args.profile,
    session_string=args.login_string
  )
else:
  client = Client(args.profile)

with client:
  if args.login_only:
    exit("Authorization completed!")
  elif args.export_string:
    exit(f"Your session string:\n{client.export_session_string()}")
  elif not args.path:
    exit("Error: Path is not provided.")

  chat_id = get_chatid(args.chat_id) if args.chat_id else "me"
  start_time = time()

  if args.as_photo:
    if Path(args.path).is_file():
      try:
        filename = PurePath(args.path).name
        client.send_photo(chat_id, args.path, caption=args.caption, progress=upload_progress, disable_notification=args.silent, has_spoiler=args.spoiler)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
    elif Path(args.path).is_dir():
      for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
        filename = PurePath(_path).name
        if Path(_path).is_file():
          try:
            client.send_photo(chat_id, _path, caption=args.caption, progress=upload_progress, disable_notification=args.silent, has_spoiler=args.spoiler)
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
        client.send_video(chat_id, args.path, progress=upload_progress, caption=args.caption, has_spoiler=args.spoiler, width=args.width, height=args.height, thumb=args.thumb, file_name=filename, supports_streaming=args.disable_stream, disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
    elif Path(args.path).is_dir():
      for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
        if Path(_path).is_file():
          try:
            filename = PurePath(_path).name
            if args.prefix:
              filename = args.prefix + filename
            client.send_video(chat_id, _path, progress=upload_progress, caption=args.caption, has_spoiler=args.spoiler, width=args.width, height=args.height, thumb=args.thumb, file_name=filename, supports_streaming=args.disable_stream, disable_notification=args.silent)
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
        client.send_audio(chat_id, args.path, progress=upload_progress, caption=args.caption, performer=args.artist, title=args.title, thumb=args.thumb, file_name=filename, disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
    elif Path(args.path).is_dir():
      for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
        if Path(_path).is_file():
          try:
            filename = PurePath(_path).name
            if args.prefix:
              filename = args.prefix + filename
            client.send_video(chat_id, _path, progress=upload_progress, caption=args.caption, performer=args.artist, thumb=args.thumb, file_name=filename, disable_notification=args.silent)
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
        client.send_voice(chat_id. args.path, progress=upload_progress, caption=args.caption, disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
    elif Path(args.path).is_dir():
      for _path in Path(args.path).glob('**/*') if args.recursive else Path(args.path).glob("*"):
        if Path(_path).is_file():
          try:
            filename = PurePath(_path).name
            if args.prefix:
              filename = args.prefix + filename
            client.send_video(chat_id, _path, progress=upload_progress, caption=args.caption, disable_notification=args.silent)
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
        client.send_video_note(chat_id, args.path, progress=upload_progress, caption=args.caption, disable_notification=args.silent)
        Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
      except Exception as error_code:
        print(f"An error occured!\n{error_code}")
    elif Path(args.path).is_dir():
      for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
        if Path(_path).is_file():
          try:
            filename = PurePath(_path).name
            if args.prefix:
              filename = args.prefix + filename
            client.send_video_note(chat_id, _path, progress=upload_progress, caption=args.caption, disable_notification=args.silent)
            Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
          except Exception as error_code:
            print(f"An error occured!\n{error_code}")
        else:
          print(f"[Dir] -> {filename}")
  elif Path(args.path).is_file():
    try:
      filename = args.filename or PurePath(args.path).name
      if args.prefix:
        filename = args.prefix + filename
      client.send_document(chat_id, args.path, progress=upload_progress, caption=args.caption, force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
      Path(args.path).unlink(missing_ok=True) if args.delete_on_done else None
    except Exception as error_code:
        print(f"An error occured!\n{error_code}")
  elif Path(args.path).is_dir():
    for _path in Path(args.path).glob("**/*") if args.recursive else Path(args.path).glob("*"):
      if Path(_path).is_file():
        try:
          filename = PurePath(_path).name
          if args.prefix:
            filename = args.prefix + filename
          client.send_document(chat_id, _path, progress=upload_progress, caption=args.caption, force_document=True, file_name=filename, thumb=args.thumb, disable_notification=args.silent)
          Path(_path).unlink(missing_ok=True) if args.delete_on_done else None
        except Exception as error_code:
          print(f"An error occured!\n{error_code}")
      else:
        print(f"[Dir] -> {filename}")
