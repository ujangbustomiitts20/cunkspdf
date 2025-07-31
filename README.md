#  PDF to Chunked JSON Converter

Skrip ini digunakan untuk **mengekstrak teks dari file PDF** dan memecahnya menjadi potongan-potongan (chunk) yang terstruktur menggunakan `Langchain RecursiveCharacterTextSplitter`. Hasilnya akan disimpan dalam format `.json` untuk digunakan dalam pipeline NLP atau sistem RAG (Retrieval-Augmented Generation).

##  Fitur

-  Membaca semua file `.pdf` dari folder tertentu
-  Memecah teks menjadi chunk dengan panjang yang disesuaikan
-  Menggunakan `RecursiveCharacterTextSplitter` dari `Langchain`
-  Menyimpan hasil dalam format `.json` siap pakai
-  Deteksi otomatis file yang membutuhkan waktu proses terlalu lama

##  Struktur Folder

```
project_root/
├── pdf_chunker.py          # Skrip utama
├── pdf_dokumen/            # Folder input, berisi file-file PDF
├── chunk_json/             # Folder output hasil dalam format JSON
```

##  Konfigurasi

Di dalam skrip, Anda dapat menyesuaikan beberapa parameter berikut:

```python
PDF_FOLDER = "./pdf_dokumen"             # Folder tempat file PDF disimpan
CHUNK_OUTPUT_FOLDER = "./chunk_json"     # Folder hasil output
MAX_ALLOWED_TIME_PER_FILE = 60           # Timeout per file (dalam detik)
```

##  Cara Menjalankan

1. **Clone repository ini atau salin skripnya**
2. **Install dependensi Python**

```bash
pip install pdfplumber langchain tqdm
```

3. **Masukkan file PDF ke dalam folder `pdf_dokumen/`**
4. **Jalankan skrip**

```bash
python pdf_chunker.py
```

5. **Lihat hasil di folder `chunk_json/`**

Setiap file `.pdf` akan menghasilkan satu file `.json` yang berisi list chunk seperti berikut:

```json
[
  {
    "filename": "dokumen1.pdf",
    "chunk_id": "dokumen1.pdf_chunk_0",
    "text": "Isi teks chunk pertama..."
  },
  ...
]
```

##  Catatan

- Halaman kosong atau tidak dapat diekstrak akan dilewati secara otomatis.
- Hasil cocok digunakan untuk preprocessing sistem QA berbasis dokumen, training LLM, RAG, dsb.

---

 Dibuat dengan  menggunakan `Langchain`, `pdfplumber`, dan `tqdm`.  
Silakan fork dan modifikasi sesuai kebutuhanmu.
