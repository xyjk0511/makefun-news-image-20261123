import { createHash } from 'node:crypto';
import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1048576; // 1 MiB
const MAX_DIMENSION = 1024;
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
const PNG_IEND = Buffer.from([0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4e, 0x44, 0xae, 0x42, 0x60, 0x82]);

interface ImageMeta {
  readonly format: 'png' | 'jpeg';
  readonly width: number;
  readonly height: number;
  readonly bytes: number;
}

function parsePngMeta(buf: Buffer): ImageMeta {
  if (buf.length < 33 || !buf.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error('Invalid PNG signature');
  }
  const chunkType = buf.subarray(12, 16).toString('ascii');
  if (chunkType !== 'IHDR') {
    throw new Error(`Expected IHDR chunk, found ${chunkType}`);
  }
  const width = buf.readUInt32BE(16);
  const height = buf.readUInt32BE(20);
  if (!buf.subarray(buf.length - 12).equals(PNG_IEND)) {
    throw new Error('PNG missing complete IEND trailer');
  }
  return { format: 'png', width, height, bytes: buf.length };
}

function parseJpegMeta(buf: Buffer): ImageMeta {
  if (buf.length < 4 || buf[0] !== 0xff || buf[1] !== 0xd8) {
    throw new Error('Invalid JPEG SOI header');
  }
  if (buf[buf.length - 2] !== 0xff || buf[buf.length - 1] !== 0xd9) {
    throw new Error('JPEG missing EOI trailer');
  }
  let offset = 2;
  while (offset + 9 < buf.length) {
    if (buf[offset] !== 0xff) {
      throw new Error(`Malformed JPEG marker at offset ${offset}`);
    }
    const marker = buf[offset + 1];
    if (marker === 0xd9 || marker === 0xda) break;
    const segLen = buf.readUInt16BE(offset + 2);
    if (marker >= 0xc0 && marker <= 0xc3 && marker !== 0xc4) {
      const height = buf.readUInt16BE(offset + 5);
      const width = buf.readUInt16BE(offset + 7);
      return { format: 'jpeg', width, height, bytes: buf.length };
    }
    offset += 2 + segLen;
  }
  throw new Error('Could not locate JPEG SOF dimensions');
}

function validateImageBuffer(buf: Buffer): ImageMeta {
  if (buf.length === 0 || buf.length > MAX_BYTES) {
    throw new Error(`Image size ${buf.length} bytes exceeds limit (${MAX_BYTES})`);
  }
  const isPng = buf.length >= 8 && buf.subarray(0, 8).equals(PNG_SIGNATURE);
  const isJpeg = buf.length >= 2 && buf[0] === 0xff && buf[1] === 0xd8;
  if (!isPng && !isJpeg) {
    throw new Error('Unsupported image format: expected PNG or JPEG');
  }
  const meta = isPng ? parsePngMeta(buf) : parseJpegMeta(buf);
  if (meta.width < 1 || meta.height < 1 || meta.width > MAX_DIMENSION || meta.height > MAX_DIMENSION) {
    throw new Error(`Dimensions ${meta.width}x${meta.height} exceed ${MAX_DIMENSION}x${MAX_DIMENSION}`);
  }
  return meta;
}

function main(): void {
  const repoDir = dirname(fileURLToPath(import.meta.url));
  const sourcePath = join(repoDir, 'entry.png');
  const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const targetPath = join(outputDir, 'entry.png');

  const payload = readFileSync(sourcePath);
  const meta = validateImageBuffer(payload);

  mkdirSync(outputDir, { recursive: true });
  writeFileSync(targetPath, payload);

  if (process.argv.includes('--verify')) {
    const sha256 = createHash('sha256').update(payload).digest('hex');
    console.log(JSON.stringify({ ok: true, targetPath, sha256, ...meta }));
  }
}

main();
