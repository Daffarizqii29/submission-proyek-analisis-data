# Proyek Analisis Data - E-Commerce Public Dataset

Proyek ini dibuat untuk memenuhi submission **Belajar Fundamental Analisis Data**.

## Struktur Folder
```
submission_proyek_analisis_data/
├── dashboard/
│   ├── dashboard.py
│   ├── main_data.csv
│   └── rfm_segment.csv
├── data/
│   ├── customers_dataset.csv
│   ├── order_items_dataset.csv
│   ├── order_payments_dataset.csv
│   ├── order_reviews_dataset.csv
│   ├── orders_dataset.csv
│   ├── product_category_name_translation.csv
│   └── products_dataset.csv
├── Proyek_Analisis_Data.ipynb
├── README.md
└── requirements.txt
```

## Ringkasan Pertanyaan Bisnis
1. Kategori produk apa yang menghasilkan revenue tertinggi, dan bagaimana tren revenue bulanannya selama 2017-2018?
2. Sejauh mana keterlambatan pengiriman memengaruhi review pelanggan, dan state mana yang memiliki late delivery rate tertinggi?

## Analisis Lanjutan
Proyek ini juga menerapkan **RFM Analysis** untuk segmentasi pelanggan.

## Cara Menjalankan Notebook
Buka file `Proyek_Analisis_Data.ipynb` melalui Jupyter Notebook / JupyterLab, lalu jalankan seluruh cell.

## Cara Menjalankan Dashboard
1. Masuk ke folder proyek.
2. Install dependency:
   ```bash
   pip install -r requirements.txt
   ```
3. Jalankan streamlit:
   ```bash
   streamlit run dashboard/dashboard.py
   ```

## Catatan
Dashboard disiapkan untuk berjalan di local sesuai kriteria utama submission.
