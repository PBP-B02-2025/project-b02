# 🧪 Menjalankan Unit Tests dengan Coverage

## Cara Menggunakan

### 1. Jalankan Tests dengan Coverage Report Otomatis

```powershell
# Masuk ke folder voucher
cd voucher

# Jalankan script test
python run_voucher_tests.py
```

### 2. Output yang Ditampilkan

Script akan otomatis menampilkan:

1. **Test Results** - Hasil dari semua 33 test cases (semua passed ✅)
2. **Coverage Report di Terminal** - Persentase coverage langsung di console:
   ```
   ======================================================================
   📊 COVERAGE REPORT FOR VOUCHER MODULE
   ======================================================================
   
   Name        Stmts   Miss   Cover   Missing
   ------------------------------------------
   forms.py        8      0 100.00%
   models.py      15     13  13.33%   1-35, 39-41
   views.py       74      1  98.65%   98
   ------------------------------------------
   TOTAL          97     14  85.57%
   ```

3. **HTML Report** - Path ke laporan HTML detail

### 3. Lihat HTML Coverage Report

```powershell
# Buka dengan browser default
start htmlcov/index.html
```

## File Coverage

| File | Purpose | Coverage | Status |
|------|---------|----------|--------|
| `forms.py` | Form validation | ✅ **100%** | Perfect! |
| `views.py` | Business logic | ✅ **98.65%** | Excellent! |
| `models.py` | Data models | ℹ️ **13.33%** | (mostly imports) |
| **TOTAL** | **All files** | ✅ **85.57%** | **Above 80%!** |

**Note:** Coverage hanya menampilkan `forms.py`, `views.py`, dan `models.py` (file utama yang ditest).

## Test Summary

### 📊 Total: 33 Test Cases (All Passed ✅)

#### Model Tests (10 tests)
- ✅ Voucher creation
- ✅ String representation (active/inactive)
- ✅ Unique kode constraint
- ✅ Decimal places handling
- ✅ Blank deskripsi
- ✅ Meta verbose names
- ✅ Min value validator (0.01)
- ✅ Max value validator (100.00)

#### Form Tests (4 tests)
- ✅ Valid form data
- ✅ Missing required fields
- ✅ Invalid persentase range
- ✅ Blank deskripsi allowed

#### View Tests (17 tests)
- ✅ Login required checks
- ✅ Admin permission checks
- ✅ Create voucher (success & errors)
- ✅ Update voucher (success & errors)
- ✅ Delete voucher (success & errors)
- ✅ Get vouchers JSON
- ✅ Exception handling (create/update/delete)
- ✅ Duplicate kode validation
- ✅ Missing fields validation

#### Integration Tests (2 tests)
- ✅ Complete lifecycle (create → update → delete)
- ✅ Multiple vouchers ordering

## Struktur File Testing

```
voucher/
├── .coveragerc              # Konfigurasi coverage
├── run_voucher_tests.py     # Script runner dengan auto coverage
├── tests.py                 # 33 unit test cases
├── README_TESTS.md          # Dokumentasi testing detail
├── README_COVERAGE.md       # Dokumentasi coverage (file ini)
└── htmlcov/                 # HTML coverage reports
    └── index.html
```

## Tips

- **Quick Test**: `python run_voucher_tests.py`
- **View Missing Lines**: Lihat kolom "Missing" di coverage report
- **Interactive Report**: Buka `htmlcov/index.html` untuk line-by-line visualization
- **Test Specific**: Edit `tests.py` untuk fokus pada test tertentu

## Coverage Goals

- ✅ Forms: **100%** coverage (ACHIEVED!)
- ✅ Views: **98.65%** coverage (ACHIEVED! Target was 95%+)
- ℹ️ Models: **13.33%** (sebagian besar import statements)
- ✅ **TOTAL: 85.57%** (ACHIEVED! Above 80% target!)

### Missing Coverage Details

**views.py** - Only 1 line missing (98):
- Line 98: Validation error message path (edge case)

**models.py** - 13 lines missing (1-35, 39-41):
- Lines 1-35: Import statements and field definitions
- Lines 39-41: Class Meta definition

## Achievements 🎉

- ✅ **33/33 tests passing** (100% pass rate)
- ✅ **85.57% total coverage** (above 80% requirement)
- ✅ **100% forms.py coverage** (perfect!)
- ✅ **98.65% views.py coverage** (near-perfect!)
- ✅ **Comprehensive test suite** covering all major functionality
- ✅ **Exception handling tested** for all CRUD operations
- ✅ **Authorization & authentication** fully tested
