import requests, sys, zipfile, easygui, os, shutil, time, subprocess
import tkPBar as tkPB
import regioninfoGenerator as rig
from threading import Thread

def checkVersion():
	try:
		versionURL = "https://raw.githubusercontent.com/Nidhogg-Wyrmborn/ImposterServerCustom/main/Current.version"
		versionRESPONSE = requests.get(versionURL, verify=False)
		version = versionRESPONSE.text
		#print(repr(version))
		return version
	except Exception as e:
		easygui.msgbox("unable to check version, please try again later\n\n"+str(e))

def unzip(filepath, version, path):
	with zipfile.ZipFile(filepath, 'r') as zipObject:
		contents = zipObject.namelist()
		pbar = tkPB.tkProgressbar(len(contents), Title=f"unzip {filepath}", Determinate=True)
		for filename in contents:
			zipObject.extract(filename, f"{path}/ImposterServer_{version}")
			pbar.update(1)
			pbar.description(Desc=f"{filename} extracted")
	try:
		pbar.root.destroy()
	except:
		# already destroyed
		pass
	#return pbar


def download(url, path, filename, pbar=None):
	print("-"*20+"downloading"+"-"*20)
	#print(url)
	heads = requests.get(url, stream=True, verify=False).headers
	#print(repr(heads))
	filesize = requests.get(url, stream=True, verify=False).headers['Content-Length']
	#print(filesize)
	if not pbar:
		pbar = tkPB.tkProgressbar(int(filesize), Title=f"downloading {filename} from {url}", Determinate=True)
	if pbar:
		pbar.total = int(filesize)
		pbar.title = f"downloading {filename} from {url}"
	with requests.get(url, stream=True, verify=False) as r:
		r.raise_for_status()
		prev = 0
		with open(f"{path}/{filename}", 'wb') as f:
			num = 0
			for chunk in r.iter_content(chunk_size=8192):
				f.write(chunk)
				num += 1
				pbar.update(len(chunk))
				current = prev + (len(chunk)/int(filesize))*100
				prev = current
				pbar.description(Desc=f"%{round(current, 1)}")
	try:
		pbar.root.destroy()
	except:
		# already destroyed
		pass
	#return pbar

def runcommand(command):
	subprocess.call(command)

def performUpdate(version):
	try:
		path = easygui.diropenbox("save to")
		os.mkdir("./tmp")
		print(version)
		url = f"https://github.com/Nidhogg-Wyrmborn/ImposterServerCustom/raw/main/{version}.zip"
		download(url, path="./tmp", filename=f"{version}.zip")
		shutil.move(f"./tmp/{version}.zip", f"./{version}.zip")
		unzip(filepath=f"./{version}.zip", version=version, path=path)
		download("https://download.visualstudio.microsoft.com/download/pr/9f4d3331-ff2a-4415-ab5d-eafc9c4f09ee/1922162c9ed35d6c10160f46c26127d6/dotnet-sdk-6.0.402-win-x64.exe", path="./tmp", filename="dotnet-sdk-6.0.402-win-x64.exe")
		shutil.move("./tmp/dotnet-sdk-6.0.402-win-x64.exe", "./dotnet-sdk-6.0.402-win-x64.exe")
		subprocess.call("dotnet-sdk-6.0.402-win-x64.exe")
		os.remove("dotnet-sdk-6.0.402-win-x64.exe")
		if "win" in sys.platform:
			download("https://github.com/playit-cloud/playit-agent/releases/download/v0.9.3/playit-0.9.3-signed.exe", path="./tmp", filename="playit-0.9.3-signed.exe")
			shutil.move("./tmp/playit-0.9.3-signed.exe", f"{path}/playit-0.9.3-signed.exe")
			setup = easygui.buttonbox("setup playit.gg?", choices=["not now", "yes"])
			if setup == "yes":
				easygui.msgbox("connect your playit.gg account and then your set to go, if you need help setting up the configurations for your server (tunneling) send me a ping or discord\nJörmungandr#3230")
				playgg = Thread(target=lambda: runcommand(f"start {path}/playit-0.9.3-signed.exe"), daemon=True)
				playgg.start()
				print("started join")
				playgg.join()
				print("join finished")
			os.remove(f"./{version}.zip")
		if "linux" in sys.platform:
			easygui.msgbox("[!] Please enter your root password when prompted, the commands run will be,\ncurl -SsL https://playit-cloud.github.io/ppa/key.gpg | sudo apt-key add -\nsudo curl -SsL -o /etc/apt/sources.list.d/playit-cloud.list https://playit-cloud.github.io/ppa/playit-cloud.l\nsudo apt update\nsudo apt install playit")
			os.system("curl -SsL https://playit-cloud.github.io/ppa/key.gpg | sudo apt-key add -")
			os.system("sudo curl -SsL -o /etc/apt/sources.list.d/playit-cloud.list https://playit-cloud.github.io/ppa/playit-cloud.l")
			os.system("sudo apt update")
			os.system("sudo apt install playit")
			easygui.msgbox("installed playit.gg")
			os.remove(f"./{version}.zip")
		#if "darwin" in sys.platform:
		#	download("https://github.com/playit-cloud/playit-agent/releases/download/v0.9.3/playit-0.9.3.dmg", path="./tmp", filename="playit-0.9.3.dmg")
		#	shutil.move("./tmp/playit-0.9.3.dmg", f"{path}/playit-0.9.3.dmg")
		#	setup = easygui.buttonbox("setup playit.gg?", choices=["not now", "yes"])
		#	if setup == "yes":
		#		easygui.msgbox("connect your playit.gg account and then your set to go, if you need help setting up the configurations for your server (tunneling) send me a ping or discord\nJörmungandr#3230")
		#		playgg = Thread(target=lambda: runcommand(f"open {path}/playit-0.9.3.dmg"), daemon=True)
		#		playgg.start()
		#		print("started join")
		#		playgg.join()
		#		print("join finished")
		#	os.remove(f"./{version}.zip")
		if (("win" not in sys.platform) and ("linux" not in sys.platform)):# and ("darwin" not in sys.platform)):
			easygui.msgbox("unsupported operating system detected, unable to continue\n\nif you believe this is in error, please report on github\n"+githublink)
			return
		shutil.rmtree("tmp")
		easygui.msgbox("setup complete")
	except Exception as d:
		print(d)
		try:
			shutil.rmtree("tmp")
		except Exception as e:
			print(e)
		try:
			pbar.root.destroy()
		except Exception as e:
			print(e)
		easygui.msgbox("Install failed, please take note of this code\n\n"+str(d))


if __name__ == '__main__':
	setupType = easygui.buttonbox("setup server or client?", choices=["server", "client"])
	if setupType == "server":
		version = checkVersion()
		performUpdate(version)
	if setupType == "client":
		outfile = rig.createfile()
		os.replace(outfile, f"C:/users/{os.getlogin()}/appdata/locallow/innersloth/among us/regionInfo.json")
		#shutil.move(outfile, f"C:/users/{os.getlogin()}/appdata/locallow/innersloth/among us/")
		easygui.msgbox("client setup complete")