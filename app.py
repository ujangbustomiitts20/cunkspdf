import os
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
import json
from tqdm import tqdm
import time

# === KONFIGURASI ===
PDF_FOLDER = "./pdf_dokumen"
CHUNK_OUTPUT_FOLDER = "./chunk_json"
MAX_ALLOWED_TIME_PER_FILE = 60  # deteksi file lambat jika > 60 detik

# === CEK FOLDER ===
if not os.path.exists(PDF_FOLDER):
    print(f" Folder '{PDF_FOLDER}' tidak ditemukan.")
    exit(1)

os.makedirs(CHUNK_OUTPUT_FOLDER, exist_ok=True)

pdf_files = [f for f in os.listdir(PDF_FOLDER) if f.lower().endswith(".pdf")]
if not pdf_files:
    print(f"  Tidak ada file PDF di folder '{PDF_FOLDER}'.")
    exit(1)

# === INISIALISASI TEXT SPLITTER ===
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

# === PROSES PDF ===
print(f" Memulai proses ekstraksi & chunking untuk {len(pdf_files)} file PDF...\n")

for i, filename in enumerate(tqdm(pdf_files, desc="📚 Memproses PDF", unit="file")):
    file_path = os.path.join(PDF_FOLDER, filename)
    start_time = time.time()
    tqdm.write(f"\n [{i+1}/{len(pdf_files)}] Membuka: {filename}")

    try:
        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)
            tqdm.write(f"📄 {filename} terdiri dari {total_pages} halaman.")

            full_text = ""
            for i, page in enumerate(pdf.pages):
                page_text = page.extract_text()
                if page_text:
                    full_text += f"\n[Halaman {i+1}]\n{page_text}"
                else:
                    tqdm.write(f"    Halaman kosong: {filename}, halaman {i+1}")

            if not full_text.strip():
                tqdm.write(f"    Tidak ada teks yang bisa diekstrak dari: {filename}")
                continue

            # Chunking
            chunks = text_splitter.split_text(full_text)
            chunk_list = []
            for idx, chunk in enumerate(chunks):
                chunk_list.append({
                    "filename": filename,
                    "chunk_id": f"{filename}_chunk_{idx}",
                    "text": chunk
                })

            # Simpan ke file JSON
            output_filename = filename.replace(".pdf", ".json").replace(".PDF", ".json")
            output_path = os.path.join(CHUNK_OUTPUT_FOLDER, output_filename)

            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(chunk_list, f, ensure_ascii=False, indent=2)

            end_time = time.time()
            elapsed = end_time - start_time
            tqdm.write(f" {filename} → {len(chunks)} chunk → {output_filename} (⏱ {elapsed:.2f} detik)")

            if elapsed > MAX_ALLOWED_TIME_PER_FILE:
                tqdm.write(f"  {filename} butuh waktu cukup lama: {elapsed:.2f} detik")

    except Exception as e:
        tqdm.write(f" Gagal proses {filename}: {e}")

print(f"\n Semua file selesai diproses! Hasil disimpan di folder '{CHUNK_OUTPUT_FOLDER}'")
