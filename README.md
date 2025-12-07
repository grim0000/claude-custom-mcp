# ⚡ Claude Custom MCP Suite

> **"Give your Agent Hands, Eyes, and Ears."**

![Banner](https://img.shields.io/badge/MCP-Enabled-blue?style=for-the-badge&logo=anthropic)
![Language](https://img.shields.io/badge/Python-3.10%2B-yellow?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

Welcome to the **Claude Custom MCP Suite**. This project transforms Claude from a chatbot into a **System-Integrated Agent** capable of interacting with your local environment, auditing networks, and managing your knowledge base.

It comes with a **Universal One-Click Installer** so you can deploy it anywhere instantly.

---

##  Features:

This suite is composed of three powerful specialized servers:

### 1. 🛡️ Network Security & Recon (`wifi-nmap-mcp`)
*   **One-Click Security Report**: Generates a full markdown report including Ping, DNS, Whois, and SSL analysis for any target.
*   **WiFi Control**: Scan available networks, check signal strength, and inspect interfaces.
*   **Packet Analysis**: Capture and analyze packets using `tshark` integration.
*   **Web Recon**: Analyze SSL certificates and Security Headers.
*   **DNS & Whois**: Deep dive into domain ownership and infrastructure.

### 2. 💻 System Control & Forensics (`system-mcp`)
*   **Desktop Automation**: Move mouse, type text, click elements, and drag-and-drop.
*   **Vision & Accessibility**: "See" the screen using UI tree inspection and image matching statistics.
*   **Forensics**:
    *   **Magic Byte Analysis**: Detect malicious files disguising their extension (e.g., `invoice.pdf.exe`).
    *   **String Extraction**: Pull readable data from binary files.
    *   **Registry & Ports**: Read Windows Registry keys and list open ports/processes.
*   **Steganography**: Hide and reveal secret messages inside images.
*   **Voice**: Text-to-Speech capabilities for audible feedback.

### 3. 🧠 Knowledge Management (`obsidian-mcp`)
*   **Vault Integration**: Read, write, and append to your local Obsidian vault.
*   **Smart Search**: Search notes, list tags, and find backlinks to connect ideas.
*   **Frontmatter Management**: Read and update note metadata programmatically.

---

##  Universal Installer:

We provide a **Universal Installer (`mcp_setup.exe`)** in the Releases section. 

**What it does:**
1.  **Checks Environment**: Ensures Python is installed (offers to auto-install via Winget if missing).
2.  **Portable Deployment**: Self-extracts all server code to `~/.mcp_servers`, ensuring it works regardless of where you run the EXE.
3.  **Auto Actions**: Installs all required Python libraries (`pip install`).
4.  **Smart Config**: Automatically creates/updates your `claude_desktop_config.json` to point to the installed servers.
5.  **Obsidian Integration**: Optional setup for your Local REST API key.

###  [Download v1 Release here](#):

---

## 🛠️ Manual Installation (For Developers)

If you prefer to run from source:

1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/your-username/claude-custom-mcp.git
    cd claude-custom-mcp
    ```

2.  **Install Requirements**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure Claude**:
    Add the following to your `claude_desktop_config.json`:
    ```json
    {
      "mcpServers": {
        "wifi-nmap": {
          "command": "python",
          "args": ["/abs/path/to/wifi-nmap-mcp/wifi_nmap_server.py"]
        },
        "system": {
          "command": "python",
          "args": ["/abs/path/to/system-mcp/system_server.py"]
        }
      }
    }
    ```

---

## ⚠️ Disclaimer

This tool includes cybersecurity capabilities (Nmap, Packet Capture, WiFi Scanning). **Use responsibly.**
*   Only scan networks/systems you own or have explicit permission to test.
*   The authors are not responsible for misuse of these tools.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <sub>Built for the future of Agentic AI.</sub>
</div>
