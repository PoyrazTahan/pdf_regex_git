# Field Patterns Guide

## 🎯 Purpose
Reference guide for field extraction patterns, common variations, and quality validation. Use this to understand what successful extraction should look like and troubleshoot pattern issues.

## 📋 Field Categories & Patterns

### **Identity & Tax Fields**

#### **TC Kimlik No (Identity Number)**
**Field Variations**: `TC Kimlik`, `TCKN`, `TCK`, `Kimlik No`, `TC / VERGİ KİMLİK NO`, `TCK/VERGİ DR. NO`

**Expected Patterns**:
- Masked: `****8901`, `******78901`, `19*******68`
- Full: `12345678901` (11 digits)
- Zero placeholder: `0`

**Quality Indicators**:
- ✅ **Good**: Consistent masking pattern, 11-digit sequences
- ⚠️ **Check**: Mixed formats, inconsistent masking levels
- ❌ **Bad**: Non-numeric, wrong length, empty when should exist

#### **Vergi No (Tax Number)**
**Field Variations**: `Vergi No`, `VERGİ NO`, `Vergi Kimlik`, `VKN`

**Expected Patterns**:
- Masked: `*******890`, `***456***`
- Full: `1234567890` (10 digits)
- Zero: `0` (individual customers)

### **Policy Information**

#### **Police No (Policy Number)**
**Field Variations**: `Poliçe No`, `POLİÇE NO`, `Policy No`, `Pol No`

**Expected Patterns**:
- Standard: `123456789/001`, `987654321/1`
- With prefixes: `K-123456789/1`, `POL-123456789`
- Sequence: `422000093852269`

**Quality Indicators**:
- ✅ **Good**: Consistent format across company PDFs
- ⚠️ **Check**: Mixed separators (/ vs -), inconsistent prefixes
- ❌ **Bad**: Non-numeric sequences, missing separators

#### **Previous Policy Number**
**Field Variations**: `Önceki Pol`, `ÖNCEKI POLİÇE NO`, `Eski Poliçe`, `Previous Policy`

**Expected Patterns**:
- Same format as current policy
- May be empty/null for new policies
- Sometimes shows "YOK" or "-"

### **Customer Information**

#### **Customer Name**
**Field Variations**: `Sigortalı Adı`, `SİGORTALI AD SOYAD`, `Müşteri Adı`, `Customer Name`

**Expected Patterns**:
- Turkish names: `AHMET MEHMET KOÇ`, `FATİMA YILMAZ`
- Company names: `ABC LTD. ŞTİ.`, `XYZ A.Ş.`
- Spacing issues: `AHMET  KOÇ` (double spaces)

**Quality Indicators**:
- ✅ **Good**: All caps, proper Turkish characters, realistic names
- ⚠️ **Check**: Mixed case, extra spaces, unusual characters
- ❌ **Bad**: Numbers in names, special symbols, very short

#### **Customer Phone/GSM**
**Field Variations**: `GSM`, `TEL`, `Telefon`, `GSM / TEL`, `Cep Telefonu`

**Expected Patterns**:
- Mobile: `05551234567`, `+90 555 123 45 67`
- Landline: `02121234567`, `(212) 123 45 67`
- Formatted: `555 123 45 67`, `0555-123-45-67`

#### **Customer Email**
**Field Variations**: `E-posta`, `Email`, `Eposta`, `E-mail`

**Expected Patterns**:
- Standard: `ahmet@gmail.com`, `customer@company.com.tr`
- Corporate: `info@firma.com.tr`
- May be empty/null (not all customers provide)

### **Vehicle Information**

#### **License Plate**
**Field Variations**: `Plaka`, `Plaka No`, `License Plate`

**Expected Patterns**:
- New format: `34 ABC 123`, `06 XYZ 789`
- Old format: `34 AB 1234`
- Numbers only: `34 1234 AB` (older vehicles)

#### **Brand/Model**
**Field Variations**: `Marka`, `Marka/Tip`, `Brand/Model`, `Vehicle Type`

**Expected Patterns**:
- Turkish brands: `RENAULT CLIO`, `VOLKSWAGEN GOLF`
- Model years: May include year `2020 TOYOTA COROLLA`
- Formatting: Usually ALL CAPS

### **Coverage Information**

#### **Glass Coverage (Cam Klozu)**
**Field Variations**: `OTO CAM KLOZU`, `CAM KIRILMASI`, `Glass Coverage`, `Cam Teminatı`

**Expected Patterns**:
- Included: `Dahil`, `DAHİL`, `Maruz kalınacak cam hasarlarında muafiyet uygulanmayacaktır`
- Amount: `2,500.00 TL`, `5000 TL`
- Detailed terms: Full clause text with conditions

**Section Boundary Issues**:
- ⚠️ **Problem**: Pattern may bleed into next section (IKAME ARAÇ, ÇEKME KURTARMA)
- ✅ **Solution**: Use lookahead to stop at next all-caps heading
- 🔧 **Pattern**: `(HEADING\s*\n[^\n]+)(?=\s*\n[A-ZÇĞIJKLMNOPRSŞTUÜVYZ]{3,})`

#### **Replacement Vehicle (İkame Araç)**
**Field Variations**: `İKAME ARAÇ`, `IKAME ARAC`, `Replacement Vehicle`, `Yedek Araç`

**Expected Patterns**:
- Duration: `2X14`, `2X7`, `30 gün`
- Conditions: `ikame araç sağlanır`, `replacement vehicle provided`

#### **Spare Parts Coverage**
**Field Variations**: `YEDEK PARÇA`, `Spare Parts`, `Parts Coverage`

**Expected Patterns**:
- Original: `orjinal yedek parça`, `orijinal parça`
- Equivalent: `eşdeğer parça`, `muadil parça`
- Mixed: `orjinal yedek parça veya eşdeğer`

#### **No-Claims Discount Level (Hasar Kademesi)**
**Field Variations**: `Hasar Kademesi`, `Hasarsızlık Kademesi`, `İNDİRİM/ ARTTIRIM`, `HASARSIZLIK İNDİRİMİ`

**Target Format**: Level number `0`, `1`, `2`, `3`, `4`, `5` (discount step level)

**Current Extraction Issues** (20 companies analyzed):
- **✅ Correct Format** (6 companies): Level numbers `0-5`
  - turkiye_E, anadolu_E, orient_E: `2`, `4`, `0`, `1`
  - gulf_E: `5`, mg_E: `0.KADEME`, unico_E: `0.BASAMAK`
- **❌ Wrong Format - Percentages** (4 companies): 
  - allianz_E: `%65`, `%60`, axa_E: `%60`, `%30`, turkiyekatilim_E: `%60`, `%40`
- **❌ Wrong Format - Raw Numbers** (3 companies):
  - ankara_E: `60`, `50`, ray_E: `40`, `60`, zurich_E: `60`, `70`
- **❌ Wrong Format - Descriptions** (5 companies):
  - ak_E: `3.yıl (% 50) hasarsızlık indirimi`, doga_E: `Basamak 3 (%50)`
  - hdi_E: `İNDİRİMSİZ`, quick_E: `4.YIL VE ÜZERİ İNDİRİMİ`, sompo_E: `1. KADEME`
- **❌ Failed Extraction** (2 companies): mapfre_E, turknippon_E (0% success)

**Standardization Priority**: **CRITICAL** - 14/20 companies extracting wrong data type

#### **Glass Coverage (Oto Cam Klozu)**
**Field Variations**: `OTO CAM KLOZU`, `CAM KIRILMASI`, `Cam Kırılması`, `Cam Hasarları`

**Expected Patterns**: Coverage description or status
- Simple status: `Dahil`, `DAHİL`, `Dâhil`
- Coverage clause: `Maruz kalınacak cam hasarlarında muafiyet uygulanmayacaktır`
- Service info: `CASU-ANLAŞMALI CAM SERVİSLERİ`, `TÜM SERVİSLER`

**Performance**: **GOOD** - 16/20 companies ≥88% success rate
**Issues**: 4 companies with 33-50% success (doga_E, gulf_E, hdi_E, zurich_E)

#### **Replacement Vehicle (İkame Araç)**
**Field Variations**: `İKAME ARAÇ`, `IKAME ARAC`, `İkame araç`, `Replacement Vehicle`

**Expected Patterns**: Duration and conditions
- Duration format: `2X7`, `2X14`, `2*7`, `2*15`
- Service description: `ikame araç sağlanır`, `İkame araç hizmeti`
- Exclusion: `İkame Hariç`, `İkamesiz`, `teminatı bulunmamaktadır`
- Detailed: `C Segment 7 gün olmak üzere yılda 2 kez`

**Performance**: **GOOD** - 14/20 companies ≥88% success rate
**Issues**: 6 companies with 33-77% success need pattern improvement

## 🔍 Pattern Development Guidelines

### **Heading + Content Extraction**
When extracting sections with headings:
```regex
(HEADING_TEXT\s*\n[^\n]+)(?=\s*\n[A-ZÇĞIJKLMNOPRSŞTUÜVYZ]{3,})
```
This pattern:
- Captures heading and first content line
- Stops at next all-caps Turkish heading
- Prevents bleeding into subsequent sections

### **Multi-line Content Extraction**
For longer sections:
```regex
HEADING_TEXT\s*\n(.*?)(?=\n[A-Z]{3,}|$)
```
- Captures everything after heading until next major section
- Uses non-greedy matching to prevent over-extraction

### **Value After Label Pattern**
Standard field extraction:
```regex
FIELD_LABEL\s*:?\s*\n?\s*([^\n]+)
```
- Handles optional colons and newlines
- Captures value on same or next line

## 🚨 Common Quality Issues

### **Extraction Bleeding**
**Problem**: Pattern captures content from next section
**Indicators**: Values contain unrelated text, section headings
**Solution**: Add lookahead boundaries, use section-aware patterns

### **Missing Values vs. Null Fields**
**Good Null Cases**: 
- Previous policy number for new customers
- Email addresses (not all customers provide)
- Optional coverage fields

**Bad Null Cases**:
- Policy numbers (should always exist)
- Customer names (required field)
- License plates (mandatory for vehicle insurance)

### **Format Inconsistencies**
**Name Formatting**: `AHMET KOÇ` vs `Ahmet Koç` vs `AHMET  KOÇ`
**Date Formatting**: `15/01/2024` vs `15.01.2024` vs `2024-01-15`
**Phone Formatting**: `05551234567` vs `0555 123 45 67` vs `+90 555 123 45 67`

## 📊 Success Rate Expectations

### **High Success Fields (90%+)**
- Policy numbers, customer names, license plates
- Basic coverage information, dates

### **Medium Success Fields (70-90%)**
- Customer contact information (phone/email)
- Vehicle technical details, coverage amounts

### **Variable Success Fields (50-70%)**
- Optional coverage details, previous policy info
- Customer profession, detailed terms and conditions

### **Company-Specific Variations**
- Each company has different document layouts
- Field names vary significantly between companies
- Success patterns from one company rarely work directly on others
- Always test patterns across multiple company PDFs

## 🎯 When to Use This Guide

**During Pattern Development**:
- Check expected patterns for field type
- Validate extraction quality against examples
- Identify potential boundary issues

**During Quality Review**:
- Compare extracted values against expected patterns
- Identify format inconsistencies or extraction errors
- Validate success rates against field expectations

**During Troubleshooting**:
- Reference common variations when fields not found
- Check for section bleeding issues
- Validate field naming patterns across companies