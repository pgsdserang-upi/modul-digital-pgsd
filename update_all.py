#!/usr/bin/env python3
import os
import re
from pathlib import Path

# Template untuk detail pertemuan
MEETING_DETAIL = """
                <div class="meeting-details">
                    <p><strong>Deskripsi:</strong> {desc}</p>
                    <p><strong>Tujuan Pembelajaran:</strong> {tujuan}</p>
                    <p><strong>Pokok Materi:</strong> {materi}</p>
                    <p><strong>Aktivitas Pembelajaran:</strong> {aktivitas}</p>
                    <p><strong>Tugas/Latihan:</strong> {tugas}</p>
                </div>"""

def create_meeting_html(week, judul, desc, tujuan, materi, aktivitas, tugas):
    detail = MEETING_DETAIL.format(desc=desc, tujuan=tujuan, materi=materi, aktivitas=aktivitas, tugas=tugas)
    return f"""
            <div class="timeline-item">
                <span class="week-badge">Pertemuan {week}</span>
                <h3>{judul}</h3>{detail}
            </div>"""

def process_file(filepath, meetings_data, references):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Build timeline HTML
    timeline_html = ""
    for week in range(1, 17):
        if week in meetings_data:
            m = meetings_data[week]
            if week == 8 or week == 16:
                # UTS/UAS - simplified
                title = "UTS" if week == 8 else "UAS"
                timeline_html += f"""
            <div class="timeline-item">
                <span class="week-badge">Pertemuan {week}</span>
                <h3>{title}</h3>
                <div class="meeting-details">
                    <p><strong>Deskripsi:</strong> {m.get('desc', 'Evaluasi semester')}</p>
                    <p><strong>Tujuan Pembelajaran:</strong> {m.get('tujuan', 'Mengukur capaian pembelajaran')}</p>
                    <p><strong>Pokok Materi:</strong> Review materi</p>
                    <p><strong>Aktivitas Pembelajaran:</strong> Ujian tertulis</p>
                    <p><strong>Tugas/Latihan:</strong> Persiapan ujian</p>
                </div>
            </div>"""
            else:
                timeline_html += create_meeting_html(week, m['judul'], m['desc'], m['tujuan'], m['materi'], m['aktivitas'], m['tugas'])
    
    # Build references HTML
    refs_html = ""
    for ref in references:
        refs_html += f"\n                <li>{ref}</li>"
    
    # Replace timeline section
    pattern_timeline = r'(<div class="timeline">).*(</div>\s*</div>\s*<div class="section-card">\s*<h2>📚 Sumber Belajar)'
    replacement_timeline = f'\\1{timeline_html}\\2'
    content = re.sub(pattern_timeline, replacement_timeline, content, flags=re.DOTALL)
    
    # Replace references section  
    pattern_refs = r'(<ul class="ref-list">).*(</ul>\s*</div>\s*</main>)'
    replacement_refs = f'\\1{refs_html}\\2'
    content = re.sub(pattern_refs, replacement_refs, content, flags=re.DOTALL)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Updated: {filepath}")

# Data untuk setiap modul (akan dilengkapi secara bertahap)
MODUL_DATA = {}

# KU100 - Pendidikan Agama Islam
MODUL_DATA['KU100'] = {
    'meetings': {
        1: {'judul': 'Pengantar PAI dan Metodologi Memahami Islam', 'desc': 'Perkenalan ruang lingkup PAI dan pendekatan memahami Islam', 'tujuan': 'Memahami konsep dasar PAI', 'materi': 'Konsep pendidikan Islam, sumber ajaran', 'aktivitas': 'Diskusi kelompok', 'tugas': 'Ringkasan PAI era modern'},
        2: {'judul': 'Manusia dan Agama', 'desc': 'Hakikat manusia dan fitrah beragama', 'tujuan': 'Menganalisis kebutuhan spiritual', 'materi': 'Fitrah, tujuan penciptaan', 'aktivitas': 'Studi kasus', 'tugas': 'Esai spiritual'},
        3: {'judul': 'Sumber Ajaran: Al-Quran dan Hadis', 'desc': 'Mengenal sumber utama Islam', 'tujuan': 'Mengidentifikasi sumber ajaran', 'materi': 'Kodifikasi Quran, ilmu hadis', 'aktivitas': 'Praktik mencari ayat', 'tugas': '5 ayat-hadis akhlak'},
        4: {'judul': 'Keimanan (Rukun Iman)', 'desc': 'Enam rukun iman', 'tujuan': 'Menginternalisasi nilai keimanan', 'materi': 'Iman kepada Allah, malaikat, kitab, rasul, hari akhir, qadar', 'aktivitas': 'Presentasi kelompok', 'tugas': 'Peta konsep rukun iman'},
        5: {'judul': 'Ibadah dan Ketakwaan', 'desc': 'Lima rukun Islam', 'tujuan': 'Melaksanakan ibadah mahdhah', 'materi': 'Syahadat, shalat, zakat, puasa, haji', 'aktivitas': 'Demonstrasi ibadah', 'tugas': 'Jurnal ibadah mingguan'},
        6: {'judul': 'Pernikahan dan Hukum Keluarga', 'desc': 'Hukum pernikahan Islam', 'tujuan': 'Memahami ketentuan syariat nikah', 'materi': 'Hukum nikah, mahar, wali, nafkah', 'aktivitas': 'Simulasi akad', 'tugas': 'Analisis kasus keluarga'},
        7: {'judul': 'Ekonomi Islam', 'desc': 'Prinsip pengelolaan harta syariah', 'tujuan': 'Menerapkan ekonomi Islam', 'materi': 'Halal-haram, zakat, bank syariah', 'aktivitas': 'Kalkulasi zakat', 'tugas': 'Hitung zakat penghasilan'},
        8: {'desc': 'Evaluasi tengah semester', 'tujuan': 'Mengukur capaian'},
        9: {'judul': 'Mazhab dan Aliran Islam', 'desc': 'Keragaman mazhab fikih', 'tujuan': 'Bersikap toleran', 'materi': '4 mazhab Sunni, aliran kalam', 'aktivitas': 'Presentasi perbandingan', 'tugas': 'Makalah moderasi'},
        10: {'judul': 'Akhlak Mulia', 'desc': 'Implementasi akhlak sehari-hari', 'tujuan': 'Mengamalkan akhlak terpuji', 'materi': 'Akhlak kepada Allah, sesama, lingkungan', 'aktivitas': 'Role play', 'tugas': 'Observasi akhlak kampus'},
        11: {'judul': 'Dakwah Amar Maruf Nahi Munkar', 'desc': 'Konsep dakwah Islam', 'tujuan': 'Merancang strategi dakwah', 'materi': 'Metode dakwah, etika', 'aktivitas': 'Simulasi ceramah', 'tugas': 'Konten dakwah digital'},
        12: {'judul': 'Jihad dan Perdamaian', 'desc': 'Makna jihad sebenarnya', 'tujuan': 'Meluruskan pemahaman jihad', 'materi': 'Jihad besar-kecil, toleransi', 'aktivitas': 'Debat radikalisme vs moderasi', 'tugas': 'Resensi artikel'},
        13: {'judul': 'Kepemimpinan Islam', 'desc': 'Prinsip kepemimpinan', 'tujuan': 'Visi kepemimpinan Islami', 'materi': 'Khalifah, musyawarah, keadilan', 'aktivitas': 'Studi kasus Rasulullah', 'tugas': 'Analisis pemimpin muslim'},
        14: {'judul': 'Islam Nusantara', 'desc': 'Islam ramah budaya lokal', 'tujuan': 'Menghargai akulturasi', 'materi': 'Wali Songo, tradisi Nusantara', 'aktivitas': 'Presentasi tradisi daerah', 'tugas': 'Dokumentasi tradisi'},
        15: {'judul': 'Moderasi Beragama', 'desc': 'Islam wasathiyah', 'tujuan': 'Agen moderasi', 'materi': 'Indikator wasathiyah, bahaya radikalisme', 'aktivitas': 'Workshop komitmen', 'tugas': 'Rencana aksi guru moderat'},
        16: {'desc': 'Evaluasi akhir', 'tujuan': 'Capaian akhir'}
    },
    'refs': [
        "Departemen Agama RI. (2019). Al-Qur'an dan Terjemahnya. Jakarta.",
        "Shihab, M.Q. (2020). Wawasan Al-Qur'an. Bandung: Mizan.",
        "Yatim, B. (2018). Sejarah Peradaban Islam. Jakarta: Rajawali.",
        "Nata, A. (2019). Ilmu Pendidikan Islam. Jakarta: Kencana.",
        "Kemenag RI. (2021). Moderasi Beragama. Jakarta.",
        "Azra, A. (2019). Islam Nusantara. Bandung: Mizan."
    ]
}

print("Starting update...")
for kode, data in MODUL_DATA.items():
    filepath = Path(f"/workspace/{kode}/index.html")
    if filepath.exists():
        process_file(filepath, data['meetings'], data['refs'])

print("Done!")
