How to use (all files should be in this directory).:
- Extract:
  - Make sure `item.json`, `menu.json`, and `shopnames.json` are present.
  - Prepare `shop` subfile named `shop.bin`.
  - Run `Extract.py`.
  - Result will be on `result.json`.
- Patch:
  - Prepare the first 0x208 bytes of `shop` subfile (with all of its possible edits) named `shop_header.bin` (the first 0x208 bytes of `shop` subfile) (inventory count/offset are adjusted automatically)
  - Do all the edits needed on `result.json`. Make sure to observe proper formatting. Any name-based stuff doesn't actually matter.
  - Run `Patch.py`.
  - Result will be on `shop.bin`.
