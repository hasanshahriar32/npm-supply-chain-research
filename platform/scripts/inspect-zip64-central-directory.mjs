import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const [tailPath, rangeStartText] = process.argv.slice(2);
if (!tailPath || !rangeStartText) throw new Error("Usage: node inspect-zip64-central-directory.mjs <tail-path> <range-start-byte>");
const rangeStart = BigInt(rangeStartText);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const buffer = await readFile(tailPath);

function findLastSignature(signature) {
  for (let index = buffer.length - 4; index >= 0; index -= 1) if (buffer.readUInt32LE(index) === signature) return index;
  return -1;
}

function uint64(offset) { return buffer.readBigUInt64LE(offset); }

function parseZip64Extra(extra, needs) {
  let offset = 0;
  const values = {};
  while (offset + 4 <= extra.length) {
    const id = extra.readUInt16LE(offset);
    const size = extra.readUInt16LE(offset + 2);
    const body = extra.subarray(offset + 4, offset + 4 + size);
    if (id === 0x0001) {
      let position = 0;
      if (needs.uncompressed && position + 8 <= body.length) { values.uncompressedSize = body.readBigUInt64LE(position); position += 8; }
      if (needs.compressed && position + 8 <= body.length) { values.compressedSize = body.readBigUInt64LE(position); position += 8; }
      if (needs.offset && position + 8 <= body.length) values.localHeaderOffset = body.readBigUInt64LE(position);
    }
    offset += 4 + size;
  }
  return values;
}

const eocd = findLastSignature(0x06054b50);
if (eocd < 0) throw new Error("ZIP end-of-central-directory record not found in supplied tail.");
const locator = eocd >= 20 && buffer.readUInt32LE(eocd - 20) === 0x07064b50 ? eocd - 20 : -1;
if (locator < 0) throw new Error("ZIP64 locator not found; this inspector expects a ZIP64 archive.");
const zip64EocdOffset = uint64(locator + 8);
const zip64Relative = Number(zip64EocdOffset - rangeStart);
if (zip64Relative < 0 || zip64Relative + 56 > buffer.length || buffer.readUInt32LE(zip64Relative) !== 0x06064b50) throw new Error("ZIP64 end record is outside the supplied tail.");
const totalEntries = uint64(zip64Relative + 32);
const centralDirectorySize = uint64(zip64Relative + 40);
const centralDirectoryOffset = uint64(zip64Relative + 48);
const centralRelative = Number(centralDirectoryOffset - rangeStart);
const centralEnd = centralRelative + Number(centralDirectorySize);
if (centralRelative < 0 || centralEnd > buffer.length) throw new Error("Complete central directory is outside the supplied tail.");

const entries = [];
let cursor = centralRelative;
while (cursor < centralEnd) {
  if (buffer.readUInt32LE(cursor) !== 0x02014b50) throw new Error(`Invalid central-directory signature at relative byte ${cursor}.`);
  const compressed32 = buffer.readUInt32LE(cursor + 20);
  const uncompressed32 = buffer.readUInt32LE(cursor + 24);
  const fileNameLength = buffer.readUInt16LE(cursor + 28);
  const extraLength = buffer.readUInt16LE(cursor + 30);
  const commentLength = buffer.readUInt16LE(cursor + 32);
  const localOffset32 = buffer.readUInt32LE(cursor + 42);
  const fileNameStart = cursor + 46;
  const fileName = buffer.subarray(fileNameStart, fileNameStart + fileNameLength).toString("utf8");
  const extra = buffer.subarray(fileNameStart + fileNameLength, fileNameStart + fileNameLength + extraLength);
  const zip64 = parseZip64Extra(extra, { uncompressed: uncompressed32 === 0xffffffff, compressed: compressed32 === 0xffffffff, offset: localOffset32 === 0xffffffff });
  entries.push({
    name: fileName,
    compressionMethod: buffer.readUInt16LE(cursor + 10),
    compressedSize: String(zip64.compressedSize ?? BigInt(compressed32)),
    uncompressedSize: String(zip64.uncompressedSize ?? BigInt(uncompressed32)),
    localHeaderOffset: String(zip64.localHeaderOffset ?? BigInt(localOffset32)),
  });
  cursor = fileNameStart + fileNameLength + extraLength + commentLength;
}

const report = {
  study: "chrono-resolution-selective-archive-inspection",
  archive: "https://zenodo.org/records/17576373/files/chrono-resolution.zip?download=1",
  retrievedAtUtc: new Date().toISOString(),
  rangedTailStartByte: String(rangeStart),
  rangedTailBytes: buffer.length,
  zip64: { totalEntries: String(totalEntries), centralDirectoryOffset: String(centralDirectoryOffset), centralDirectorySize: String(centralDirectorySize) },
  entries,
  conclusion: "Central-directory metadata only. No archive member payload was downloaded or executed.",
};
await writeFile(path.join(researchDir, "72_chrono_resolution_archive_inventory.json"), JSON.stringify(report, null, 2) + "\n");
console.log(JSON.stringify(report, null, 2));
