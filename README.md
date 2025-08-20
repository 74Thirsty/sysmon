# SysMon - Terminal System, WiFi & RunFaster Utility

![GADGET SAAVY banner](https://raw.githubusercontent.com/74Thirsty/74Thirsty/main/assets/banner.svg)

## 🔧 Technologies & Tools

[![Cyfrin](https://img.shields.io/badge/Cyfrin-Audit%20Ready-005030?logo=shield&labelColor=F47321)](https://www.cyfrin.io/)  
[![FlashBots](https://img.shields.io/pypi/v/finta?label=Finta&logo=python&logoColor=2774AE&labelColor=FFD100)](https://www.flashbots.net/)  
[![Python](https://img.shields.io/badge/Python-3.11-003057?logo=python&labelColor=B3A369)](https://www.python.org/)  
[![Solidity](https://img.shields.io/badge/Solidity-0.8.20-7BAFD4?logo=ethereum&labelColor=4B9CD3)](https://docs.soliditylang.org)  
[![pYcHARM](https://img.shields.io/badge/Built%20with-PyCharm-782F40?logo=pycharm&logoColor=CEB888)](https://www.jetbrains.com/pycharm/)  
[![Issues](https://img.shields.io/github/issues/74Thirsty/sysmon.svg?color=hotpink&labelColor=brightgreen)](https://github.com/74Thirsty/sysmon/issues)  
[![Lead Dev](https://img.shields.io/badge/C.Hirschauer-Lead%20Developer-041E42?logo=parrotsecurity&labelColor=C5B783)](https://christopherhirschauer.bio)  
[![Security](https://img.shields.io/badge/encryption-AES--256-orange.svg?color=13B5EA&labelColor=9EA2A2)]()  

> <p><strong>Christopher Hirschauer</strong><br>
> Builder @ the bleeding edge of MEV, automation, and high-speed arbitrage.<br>
<em>June 13, 2025</em></p>

**SysMon** is a lightweight terminal-based dashboard built with Python's `curses` that monitors system resources and WiFi connection details in real time.  
It also lets you tweak WiFi settings and run the **RunFaster Utility** — an integrated cleanup & optimization tool that clears caches, resets services, and refreshes network connections.

---

## 📌 Features
- 📊 **Real-time monitoring** of:
  - CPU usage
  - RAM usage
  - Disk usage
  - Network TX/RX speeds
  - WiFi signal strength & frequency
- ⚙ **WiFi controls**:
  - Change TX power (dBm)
  - Change WiFi frequency (MHz)
  - Restart WiFi interface
  - Switch between adapters instantly
- 🚀 **RunFaster Utility**:
  - Install missing dependencies (NetworkManager, Bluetooth)
  - Clear APT cache
  - Remove temporary files (`/tmp`)
  - Clean user cache (excluding browser data)
  - Remove unused packages
  - Refresh WiFi / restart NetworkManager
  - Reset Bluetooth service
- 📡 Quick launch of `wavemon` for detailed WiFi stats
- ⌨ Easy-to-use **keyboard shortcuts**

---

## ⌨ Controls

| Key | Action |
|-----|--------|
| `t` | Change TX Power (dBm) |
| `f` | Change WiFi Frequency (MHz) |
| `r` | Restart WiFi Interface |
| `a` | Change WiFi Adapter |
| `w` | Launch Wavemon |
| `x` | Open RunFaster Utility Menu |
| `h` | Show Help Menu |
| `q` | Quit SysMon |

---

---

## ⚡ RunFaster Utility

The **RunFaster Utility** is fully integrated into SysMon.  
It’s an interactive menu (press `x`) that lets you perform system cleanup and maintenance tasks without leaving the dashboard.

### 📋 RunFaster Menu

```
RunFaster Menu
--------------
[1] Install Dependencies
[2] Clear APT Cache
[3] Remove Temp Files
[4] Remove User Cache (skip browsers)
[5] Remove Unused Packages
[6] Refresh WiFi
[7] Reset Bluetooth
[8] Run All
[q] Back
```

### 🛠 Features
- 🔍 **Dependency Checker**  
  Automatically ensures `network-manager` and `bluetooth` services are installed.

- 🧹 **Cache & Temp Cleanup**  
  - Clear APT cache (`apt clean`, `apt autoclean`)  
  - Remove system temp files (`/tmp/*`)  
  - Clean user cache (`~/.cache`) while **preserving browser data** (cookies, history, sessions).

- 📦 **Package Maintenance**  
  - Remove unused packages with `apt autoremove`.

- 📶 **Network & Connectivity Refresh**  
  - Restart **NetworkManager** to reset WiFi and internet connectivity.  
  - Restart **Bluetooth service** to fix device pairing or connectivity issues.

- 🚀 **One-Click Optimize**  
  Run all the above steps in one go with option `[8] Run All`.


## 🚀 Installation & Usage

# Clone repository
```
git clone https://github.com/74Thirsty/sysmon.git
cd sysmon
```

# Install dependencies
```
pip install -r requirements.txt
```

# Run SysMon
```
python3 sysmon.py
```
