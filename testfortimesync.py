import subprocess

def is_time_synchronized():
    try:
        result = subprocess.run(
            ["timedatectl", "show", "-p", "NTPSynchronized"],
            capture_output=True, text=True, check=True
        )
        output = result.stdout.strip()
        synced = output.split("=")[-1].lower() == "yes"
        return synced
    except FileNotFoundError:
        print("timedatectl not found. Try using chronyc method below.")
        return None
    except subprocess.CalledProcessError as e:
        print("Error checking time sync:", e)
        return None

if __name__ == "__main__":
    synced = is_time_synchronized()
    if synced is True:
        print("✅ System clock is synchronized with NTP server.")
    elif synced is False:
        print("❌ System clock is NOT synchronized with NTP server.")
    else:
        print("⚠️ Unable to determine synchronization status.")
