# 🎨 Voucher Card Color Palette

Daftar variasi warna gradien untuk voucher cards yang sudah diterapkan dalam sistem.

## Variasi Warna Aktif (6 Variasi)

### 1. **Purple Bliss** 💜 (Original)
- **Gradient:** `#667eea` → `#764ba2`
- **Deskripsi:** Ungu elegan yang profesional dan modern
- **Cocok untuk:** Voucher premium, diskon eksklusif
- **Pattern:** Card ke-1, 7, 13, 19... (6n+1)

### 2. **Sunset Orange** 🌅
- **Gradient:** `#f093fb` → `#f5576c`
- **Deskripsi:** Pink-orange hangat seperti senja
- **Cocok untuk:** Flash sale, limited time offers
- **Pattern:** Card ke-2, 8, 14, 20... (6n+2)

### 3. **Ocean Blue** 🌊
- **Gradient:** `#4facfe` → `#00f2fe`
- **Deskripsi:** Biru segar seperti samudra
- **Cocok untuk:** Voucher regular, cashback
- **Pattern:** Card ke-3, 9, 15, 21... (6n+3)

### 4. **Fresh Green** 🌿
- **Gradient:** `#43e97b` → `#38f9d7`
- **Deskripsi:** Hijau mint yang menyegarkan
- **Cocok untuk:** Voucher eco-friendly, new customer
- **Pattern:** Card ke-4, 10, 16, 22... (6n+4)

### 5. **Golden Hour** ✨
- **Gradient:** `#fa709a` → `#fee140`
- **Deskripsi:** Pink-kuning cerah yang energik
- **Cocok untuk:** Special events, seasonal offers
- **Pattern:** Card ke-5, 11, 17, 23... (6n+5)

### 6. **Royal Purple** 👑
- **Gradient:** `#a18cd1` → `#fbc2eb`
- **Deskripsi:** Ungu pastel yang lembut dan mewah
- **Cocok untuk:** Loyalty rewards, VIP vouchers
- **Pattern:** Card ke-6, 12, 18, 24... (6n+6)

---

## Warna Inactive

### **Silver Gray** ⚪
- **Gradient:** `#bdc3c7` → `#95a5a6`
- **Deskripsi:** Abu-abu netral untuk voucher tidak aktif
- **Opacity:** 0.7
- **Digunakan untuk:** Voucher expired atau non-aktif

---

## Cara Kerja Sistem Warna

Sistem menggunakan CSS `nth-child` selector untuk secara otomatis memberikan warna berbeda pada setiap voucher card:

```css
/* Contoh pattern */
.voucher-card:nth-child(6n+1) { /* Purple Bliss */ }
.voucher-card:nth-child(6n+2) { /* Sunset Orange */ }
.voucher-card:nth-child(6n+3) { /* Ocean Blue */ }
/* dst... */
```

Setiap 6 voucher akan mengulang pattern warna yang sama, sehingga tampilan tetap konsisten dan variatif.

---

## Tips Tambahan

### Menambah Variasi Warna Baru
Untuk menambah warna gradien baru, tambahkan pattern `nth-child` dengan angka yang berbeda:

```css
/* 7. Nama Warna Baru */
.voucher-card:nth-child(7n+7) {
    background: linear-gradient(135deg, #color1 0%, #color2 100%);
}
```

### Rekomendasi Gradien Tambahan

Jika ingin menambah variasi lebih banyak:

1. **Crimson Fire** 🔥
   - `#eb3349` → `#f45c43`
   - Merah energik untuk super sale

2. **Violet Dream** 🌌
   - `#360033` → `#0b8793`
   - Gelap mistis untuk midnight deals

3. **Peachy Cream** 🍑
   - `#ffecd2` → `#fcb69f`
   - Pastel hangat untuk bundle offers

4. **Electric Blue** ⚡
   - `#00c6ff` → `#0072ff`
   - Biru terang untuk tech vouchers

5. **Cherry Blossom** 🌸
   - `#fbc2eb` → `#a6c1ee`
   - Pink-biru lembut untuk beauty products

---

## Preview Visual

Saat voucher ditampilkan, akan terlihat seperti ini:

```
Card 1: Purple Bliss
Card 2: Sunset Orange  
Card 3: Ocean Blue
Card 4: Fresh Green
Card 5: Golden Hour
Card 6: Royal Purple
Card 7: Purple Bliss (repeat)
Card 8: Sunset Orange (repeat)
...dan seterusnya
```

---

## Technical Notes

- Semua gradien menggunakan `linear-gradient` dengan sudut `135deg`
- Efek hover: `translateY(-5px)` + shadow lebih gelap
- Inactive state: override dengan `!important` untuk abu-abu
- Responsive: Otomatis adjust di mobile (1 kolom)
- Animation: Smooth transition 0.3s ease

---

**Last Updated:** October 24, 2025  
**File Location:** `voucher/templates/voucher.html`
