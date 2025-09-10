#!/usr/bin/env python3
"""
convert_txt_to_ts.py
TXT -> TS 转换脚本
"""

import argparse
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

def parse_line(line):
    line = line.strip()
    if not line or line.startswith('#'):
        return None, None
    if '=' in line:
        src, tgt = line.split('=', 1)
        return src.strip(), tgt.strip()
    if '\t' in line:
        src, tgt = line.split('\t', 1)
        return src.strip(), tgt.strip()
    if '|||' in line:
        src, tgt = line.split('|||', 1)
        return src.strip(), tgt.strip()
    return line, ''

def prettify(elem):
    rough = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough)
    return reparsed.toprettyxml(indent="  ", encoding='utf-8')

def build_ts(messages, language):
    TS = ET.Element('TS', version="2.1", language=language)
    context = ET.SubElement(TS, 'context')
    name = ET.SubElement(context, 'name')
    name.text = 'SignalRGB'
    for src, tgt in messages:
        message = ET.SubElement(context, 'message')
        source = ET.SubElement(message, 'source')
        source.text = src
        translation = ET.SubElement(message, 'translation')
        translation.text = tgt
    return TS

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('input', help='input TXT file')
    parser.add_argument('output', help='output TS file')
    parser.add_argument('--lang', default='zh_CN', help='language code')
    args = parser.parse_args()

    lines = Path(args.input).read_text(encoding='utf-8').splitlines()
    messages = []
    for ln in lines:
        src, tgt = parse_line(ln)
        if src is None: 
            continue
        messages.append((src, tgt))

    ts = build_ts(messages, args.lang)
    Path(args.output).write_bytes(prettify(ts))
    print(f"Wrote {args.output} with {len(messages)} messages. Compile with lrelease to get .qm.")

if __name__ == '__main__':
    main()
