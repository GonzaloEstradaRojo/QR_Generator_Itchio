# QR_Generator_Itchio# 🎯 QR Generator for Itch.io

Aplicación de escritorio en Python (Tkinter + Selenium) que:

- Descarga las entradas de una jam de [Itch.io](https://itch.io)
- Genera códigos QR para cada juego
- Crea automáticamente un PDF con todos ellos

Ideal para organizar o imprimir los juegos de una jam.

---

## 📘 Cómo usar la aplicación

Consulta la guía completa aquí 👉 [USAGE.md](USAGE.md)

---

## 🧰 Requisitos

- Python 3.10 o superior
- Google Chrome, Mozilla Firefox o Microsoft Edge instalados
- Sistema operativo: Windows (probado), compatible con Linux/Mac

---

## ⚙️ Instalación (modo desarrollador)

1. Clona este repositorio:

   ```bash
   git clone https://github.com/tuusuario/QR_Generator_Itchio.git
   cd QR_Generator_Itchio
    ```

2. Instala las dependencias:

   ```bash
    pip install -r requirements.txt
    ```

3. Ejecuta la aplicación:

   ```bash
    python App.py
    ```

---

## 🧩 Tecnologías utilizadas

Tkinter — Interfaz gráfica

Selenium + webdriver-manager — Navegación y scraping de Itch.io

qrcode + Pillow (PIL) — Generación de códigos QR

ReportLab — Creación del PDF final
