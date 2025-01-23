# Summary of data loading features¶

This topic provides a quick-reference of the supported features for using the
[COPY INTO <table>](../sql-reference/sql/copy-into-table) command to load data
from files into Snowflake tables.

## Data file details¶

The following table describes the general details for the files used to load
data:

Feature | Supported | Notes  
---|---|---  
Location of files | Local environment | Files are first copied (“staged”) to an internal (Snowflake) stage, then loaded into a table.  
| Amazon S3 | Files can be loaded directly from any user-supplied bucket.  
| Google Cloud Storage | Files can be loaded directly from any user-supplied bucket.  
| Microsoft Azure cloud storage

  * Blob storage
  * Data Lake Storage Gen2
  * General-purpose v1
  * General-purpose v2

| Files can be loaded directly from any user-supplied container.  
File formats | Delimited files (CSV, TSV, etc.) | Any valid delimiter is supported; default is comma (i.e. CSV).  
| [Semi-structured formats](semistructured-intro)

  * JSON
  * Avro
  * ORC
  * Parquet
  * XML (supported as a [preview feature](../release-notes/preview-features))

|  
| [Unstructured formats](unstructured-intro) |   
File encoding | File format-specific | For delimited files (CSV, TSV, etc.), the default character set is UTF-8. To use any other characters sets, you must explicitly specify the encoding to use for loading. For the list of supported character sets, see Supported Character Sets for Delimited Files (in this topic).  
|  | For semi-structured file formats (JSON, Avro, etc.), the only supported character set is UTF-8.  
|  | Snowflake doesn’t support loading data from tar (tape archive) files.  
  
### Supported character sets for delimited files¶

The following table lists the encoding character sets supported for loading
data from delimited files (CSV, TSV, etc.):

Character Set | `ENCODING` Value | Supported Languages | Notes  
---|---|---|---  
Big5 | `BIG5` | Traditional Chinese |   
EUC-JP | `EUCJP` | Japanese |   
EUC-KR | `EUCKR` | Korean |   
GB18030 | `GB18030` | Chinese |   
IBM420 | `IBM420` | Arabic |   
IBM424 | `IBM424` | Hebrew |   
IBM949 | `IBM949` | Korean |   
ISO-2022-CN | `ISO2022CN` | Simplified Chinese |   
ISO-2022-JP | `ISO2022JP` | Japanese |   
ISO-2022-KR | `ISO2022KR` | Korean |   
ISO-8859-1 | `ISO88591` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |   
ISO-8859-2 | `ISO88592` | Czech, Hungarian, Polish, Romanian |   
ISO-8859-5 | `ISO88595` | Russian |   
ISO-8859-6 | `ISO88596` | Arabic |   
ISO-8859-7 | `ISO88597` | Greek |   
ISO-8859-8 | `ISO88598` | Hebrew |   
ISO-8859-9 | `ISO88599` | Turkish |   
ISO-8859-15 | `ISO885915` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish | Identical to ISO-8859-1 except for 8 characters, including the Euro currency symbol.  
KOI8-R | `KOI8R` | Russian |   
Shift_JIS | `SHIFTJIS` | Japanese |   
UTF-8 | `UTF8` | All languages | For loading data from delimited files (CSV, TSV, etc.), UTF-8 is the default. . . For loading data from all other supported file formats (JSON, Avro, etc.), as well as unloading data, UTF-8 is the only supported character set.  
UTF-16 | `UTF16` | All languages |   
UTF-16BE | `UTF16BE` | All languages |   
UTF-16LE | `UTF16LE` | All languages |   
UTF-32 | `UTF32` | All languages |   
UTF-32BE | `UTF32BE` | All languages |   
UTF-32LE | `UTF32LE` | All languages |   
windows-874 | `WINDOWS874` | Thai |   
windows-949 | `WINDOWS949` | Korean |   
windows-1250 | `WINDOWS1250` | Czech, Hungarian, Polish, Romanian |   
windows-1251 | `WINDOWS1251` | Russian |   
windows-1252 | `WINDOWS1252` | Danish, Dutch, English, French, German, Italian, Norwegian, Portuguese, Swedish |   
windows-1253 | `WINDOWS1253` | Greek |   
windows-1254 | `WINDOWS1254` | Turkish |   
windows-1255 | `WINDOWS1255` | Hebrew |   
windows-1256 | `WINDOWS1256` | Arabic |   
  
## Compression of staged files¶

The following table describes how Snowflake handles compression of data files
for loading. The options are different depending on whether the files are
staged, uncompressed, or already-compressed:

Feature | Supported | Notes  
---|---|---  
Uncompressed files | gzip | When staging uncompressed files in a Snowflake stage, the files are automatically compressed using gzip, unless compression is explicitly disabled.  
Already-compressed files | 

  * gzip
  * bzip2
  * deflate
  * raw_deflate
  * Brotli
  * Zstandard

| Snowflake can automatically detect any of these compression methods, or you
can explicitly specify the method that was used to compress the files. Auto-
detection isn’t supported for Brotli-compressed files; when staging or loading
Brotli-compressed files, you must explicitly specify the compression method
that was used. Snowflake doesn’t support uploading compressed tar (tape
archive) files.  
  
## Encryption of staged files¶

The following table describes how Snowflake handles encryption of data files
for loading. The options are different depending on whether the files are
staged unencrypted or already-encrypted:

Feature | Supported | Notes  
---|---|---  
**Unencrypted files** | 128-bit or 256-bit keys | All files stored on internal stages for data loading and unloading operations are automatically encrypted using AES-256 strong encryption on the server side. By default, Snowflake provides additional client-side encryption with a 128-bit key (with the option to configure a 256-bit key).  
**Already-encrypted files** | User-supplied key | Files that are already encrypted can be loaded into Snowflake from external cloud storage; the key used to encrypt the files must be provided to Snowflake.

