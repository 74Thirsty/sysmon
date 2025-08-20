#!/usr/bin/env python3
import curses
import subprocess
import os
import time
import psutil
import shutil
import logging

# === Logging Setup ===
LOG_FILE = os.path.expanduser("~/sysmon_tool.log")   # safer than /var/log
logging.basicConfig(filename=LOG_FILE, level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

# ------------------------
# Utility Functions
# ------------------------
def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, shell=True, text=True).strip()
    except Exception as e:
        logging.error(f"Command failed: {cmd} ({e})")
        return ""

def get_default_interface():
    iface = run_cmd("ip route | grep default | awk '{print $5}'")
    return iface if iface else "wlan0"

def get_wifi_signal(iface):
    try:
        iw = run_cmd(f"iw dev {iface} link")
        for line in iw.splitlines():
            if "signal:" in line:
                return line.split(":")[1].strip()
    except:
        return "N/A"
    return "N/A"

def get_wifi_freq(iface):
    try:
        iw = run_cmd(f"iw dev {iface} info")
        for line in iw.splitlines():
            if "channel" in line.lower():
                return line.strip()
    except:
        return "N/A"
    return "N/A"

def change_tx_power(iface, power):
    run_cmd(f"sudo iw dev {iface} set txpower fixed {power*100}")
    logging.info(f"TX power for {iface} set to {power} dBm")

def change_frequency(iface, freq):
    run_cmd(f"sudo iw dev {iface} set freq {freq}")
    logging.info(f"Frequency for {iface} set to {freq} MHz")

def restart_wifi(iface):
    run_cmd(f"sudo ip link set {iface} down && sudo ip link set {iface} up")
    logging.info(f"Restarted interface {iface}")

# ------------------------
# RunFaster Integrated Functions
# ------------------------
def rf_install_dependencies():
    run_cmd("dpkg -l | grep -q network-manager || (sudo apt update && sudo apt install -y network-manager)")
    run_cmd("dpkg -l | grep -q bluetooth || (sudo apt update && sudo apt install -y bluetooth bluez)")
    logging.info("Dependencies checked/installed")

def rf_clear_apt_cache():
    run_cmd("sudo apt clean && sudo apt autoclean")
    logging.info("APT cache cleared")

def rf_remove_temp_files():
    run_cmd("sudo rm -rf /tmp/*")
    logging.info("Temporary files removed")

def rf_remove_user_cache():
    cache_dir = os.path.expanduser("~/.cache")
    if not os.path.exists(cache_dir):
        return
    for entry in os.listdir(cache_dir):
        if any(browser in entry for browser in ["mozilla", "chromium", "google-chrome"]):
            continue
        run_cmd(f"rm -rf {os.path.join(cache_dir, entry)}")
    logging.info("User cache cleared (browser data intact)")

def rf_remove_unused_packages():
    run_cmd("sudo apt autoremove -y")
    logging.info("Unused packages removed")

def rf_refresh_wifi():
    run_cmd("sudo systemctl restart NetworkManager")
    logging.info("WiFi refreshed")

def rf_reset_bluetooth():
    run_cmd("sudo systemctl restart bluetooth")
    logging.info("Bluetooth reset")

def runfaster_menu(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(False)  # <— block for key input instead of constant loop

    while True:
        stdscr.clear()
        menu_items = [
            "RunFaster Menu",
            "--------------",
            "[1] Install Dependencies",
            "[2] Clear APT Cache",
            "[3] Remove Temp Files",
            "[4] Remove User Cache (skip browsers)",
            "[5] Remove Unused Packages",
            "[6] Refresh WiFi",
            "[7] Reset Bluetooth",
            "[8] Run All",
            "[q] Back"
        ]
        for i, line in enumerate(menu_items):
            stdscr.addstr(i+1, 2, line)
        stdscr.refresh()

        key = stdscr.getch()  # waits here until a key is pressed
        if key == ord('1'): rf_install_dependencies()
        elif key == ord('2'): rf_clear_apt_cache()
        elif key == ord('3'): rf_remove_temp_files()
        elif key == ord('4'): rf_remove_user_cache()
        elif key == ord('5'): rf_remove_unused_packages()
        elif key == ord('6'): rf_refresh_wifi()
        elif key == ord('7'): rf_reset_bluetooth()
        elif key == ord('8'):
            rf_install_dependencies()
            rf_clear_apt_cache()
            rf_remove_temp_files()
            rf_remove_user_cache()
            rf_remove_unused_packages()
            rf_refresh_wifi()
            rf_reset_bluetooth()
            logging.info("All RunFaster tasks completed")
        elif key == ord('q'):
            break  # exit back to dashboard

    stdscr.nodelay(True)  # restore non-blocking mode for dashboard

# ------------------------
# UI Helpers
# ------------------------
def draw_bar(stdscr, y, x, width, percent, color_pair):
    fill_width = int(width * percent / 100)
    stdscr.addstr(y, x, "[" + "#" * fill_width + "-" * (width - fill_width) + "]", curses.color_pair(color_pair))

def show_help(stdscr):
    stdscr.clear()
    help_lines = [
        "SysMon Help Menu",
        "----------------",
        "[t] Change TX Power (dBm)",
        "[f] Change WiFi Frequency (MHz)",
        "[r] Restart WiFi Interface",
        "[a] Change WiFi Adapter",
        "[w] Launch Wavemon",
        "[x] RunFaster Utility",
        "[h] Show Help Menu",
        "[q] Quit",
        "",
        "Press any key to return..."
    ]
    for i, line in enumerate(help_lines):
        stdscr.addstr(i+1, 2, line)
    stdscr.refresh()
    stdscr.getch()

# ------------------------
# Main UI Loop
# ------------------------
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    h, w = stdscr.getmaxyx()
    iface = get_default_interface()
    prev_net = psutil.net_io_counters(pernic=True).get(iface)

    while True:
        stdscr.erase()

        # Title
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(0, 2, f" SysMon Dashboard - Interface: {iface} (Press h for help, q to quit) ")
        stdscr.attroff(curses.color_pair(2))

        # CPU
        cpu = psutil.cpu_percent(interval=None)
        stdscr.addstr(2, 2, f"CPU Usage: {cpu:.1f}%")
        draw_bar(stdscr, 3, 2, 30, cpu, 3)

        # Memory
        mem = psutil.virtual_memory()
        stdscr.addstr(5, 2, f"Memory Usage: {mem.percent:.1f}% ({mem.used // (1024**2)}MB/{mem.total // (1024**2)}MB)")
        draw_bar(stdscr, 6, 2, 30, mem.percent, 4)

        # Disk
        disk = psutil.disk_usage('/')
        stdscr.addstr(8, 2, f"Disk Usage: {disk.percent:.1f}% ({disk.used // (1024**3)}GB/{disk.total // (1024**3)}GB)")
        draw_bar(stdscr, 9, 2, 30, disk.percent, 5)

        # Network
        net_now = psutil.net_io_counters(pernic=True).get(iface)
        if net_now and prev_net:
            tx_speed = (net_now.bytes_sent - prev_net.bytes_sent) / 1024
            rx_speed = (net_now.bytes_recv - prev_net.bytes_recv) / 1024
        else:
            tx_speed, rx_speed = 0, 0
        prev_net = net_now
        stdscr.addstr(11, 2, f"Network TX: {tx_speed:.1f} KB/s   RX: {rx_speed:.1f} KB/s")

        # WiFi Info
        stdscr.addstr(13, 2, f"WiFi Signal: {get_wifi_signal(iface)}")
        stdscr.addstr(14, 2, f"WiFi Frequency: {get_wifi_freq(iface)}")

        # Footer Controls
        stdscr.attron(curses.color_pair(2))
        stdscr.addstr(h-2, 2, "[t] TX Power  [f] Frequency  [r] Restart WiFi  [a] Adapter  [w] WiFi Stats  [x] RunFaster  [h] Help  [q] Quit")
        stdscr.attroff(curses.color_pair(2))

        # Handle Keys
        try:
            key = stdscr.getch()
            if key == ord('q'):
                break
            elif key == ord('h'):
                show_help(stdscr)
            elif key == ord('t'):
                curses.echo()
                stdscr.nodelay(False)
                stdscr.addstr(h-1, 2, "Enter TX Power (dBm): ")
                stdscr.clrtoeol()
                power = int(stdscr.getstr().decode())
                curses.noecho()
                stdscr.nodelay(True)
                change_tx_power(iface, power)
            elif key == ord('f'):
                curses.echo()
                stdscr.nodelay(False)
                stdscr.addstr(h-1, 2, "Enter Frequency (MHz): ")
                stdscr.clrtoeol()
                freq = int(stdscr.getstr().decode())
                curses.noecho()
                stdscr.nodelay(True)
                change_frequency(iface, freq)
            elif key == ord('r'):
                restart_wifi(iface)
            elif key == ord('a'):
                curses.echo()
                stdscr.nodelay(False)
                stdscr.addstr(h-1, 2, "Enter new adapter name: ")
                stdscr.clrtoeol()
                iface = stdscr.getstr().decode().strip()
                curses.noecho()
                stdscr.nodelay(True)
            elif key == ord('w'):
                curses.endwin()
                subprocess.run("wavemon", shell=True)
            elif key == ord('x'):
                runfaster_menu(stdscr)
        except Exception:
            pass

        stdscr.refresh()
        time.sleep(1)

# ------------------------
# Color Setup
# ------------------------
def init_colors():
    curses.start_color()
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_CYAN)   # Header/Footer
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)  # CPU Bar
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK) # RAM Bar
    curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)# Disk Bar

# ------------------------
# Entry Point
# ------------------------
if __name__ == "__main__":
    if not shutil.which("dstat") or not shutil.which("wavemon"):
        print("Error: Install 'dstat' and 'wavemon' first.")
        exit(1)
    curses.wrapper(lambda stdscr: (init_colors(), main(stdscr)))
